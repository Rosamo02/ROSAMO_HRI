import os
import signal
import subprocess
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HMICommandReceiver(Node):
    def __init__(self):
        super().__init__("hmi_command_receiver")

        self.sub = self.create_subscription(
            String,
            "/hmi/command",
            self.callback,
            10
        )

        self.processes = {}
        self.log_dir = os.path.expanduser("~/hmi_logs")
        os.makedirs(self.log_dir, exist_ok=True)

        self.get_logger().info("Receiver ready. Listening on /hmi/command")

    def callback(self, msg):
        command = msg.data.strip()
        self.get_logger().info(f"Received command: {command}")

        if command == "start_debug":
            self.start_process(
                "debug",
                "ros2 run teleop_twist_joy teleop_node"
            )

        elif command == "stop_debug":
            self.stop_process("debug")

        elif command == "start_listener":
            self.start_process(
                "listener",
                "ros2 run demo_nodes_cpp listener"
            )

        elif command == "stop_listener":
            self.stop_process("listener")

        elif command == "start_ros2router":
            self.start_ros2router()

        elif command == "stop_ros2router":
            self.stop_ros2router()

        elif command == "start_mapping":
            self.start_mapping()

        elif command == "stop_mapping":
            self.stop_mapping()

        elif command == "start_image_mapping":
            self.start_process(
                "ImageMapping",
                "ros2 run map_marker_pkg map_to_image"
            )   

        elif command == "stop_image_mapping":
            self.stop_process("ImageMapping")                         

        else:
            self.get_logger().warn(f"Unknown command: {command}")

    def start_ros2router(self):
        compose_dir = os.path.expanduser("~/ros2router")

        if not os.path.isdir(compose_dir):
            self.get_logger().error(f"Compose directory not found: {compose_dir}")
            return

        try:
            self.get_logger().info("Running: docker compose down")
            subprocess.run(
                ["docker", "compose", "down"],
                cwd=compose_dir,
                check=True
            )

            self.get_logger().info("Running: docker compose up -d --force-recreate")
            subprocess.run(
                ["docker", "compose", "up", "-d", "--force-recreate"],
                cwd=compose_dir,
                check=True
            )

            self.get_logger().info("ROS 2 Router docker stack restarted successfully")

        except subprocess.CalledProcessError as e:
            self.get_logger().error(f"docker compose failed: {e}")
        except Exception as e:
            self.get_logger().error(f"Failed to start ros2router stack: {e}")

    def stop_ros2router(self):
        compose_dir = os.path.expanduser("~/ros2router")

        if not os.path.isdir(compose_dir):
            self.get_logger().error(f"Compose directory not found: {compose_dir}")
            return

        try:
            self.get_logger().info("Running: docker compose down")
            subprocess.run(
                ["docker", "compose", "down"],
                cwd=compose_dir,
                check=True
            )

            self.get_logger().info("ROS 2 Router docker stack stopped successfully")

        except subprocess.CalledProcessError as e:
            self.get_logger().error(f"docker compose down failed: {e}")
        except Exception as e:
            self.get_logger().error(f"Failed to stop ros2router stack: {e}")

    def start_mapping(self):
        self.get_logger().info("Starting local mapping stack...")

        self.start_process(
            "mapping_odom_to_tf",
            "python3 ~/Desktop/odom_to_tf_broadcaster.py"
        )

        self.start_process(
            "mapping_static_tf",
            "ros2 run tf2_ros static_transform_publisher "
            "--x 0 --y 0 --z 0 --yaw 0 --pitch 0 --roll 0 "
            "--frame-id base_link_ekf --child-frame-id livox_frame"
        )

        time.sleep(2)

        self.start_process(
            "mapping_slam_toolbox",
            "ros2 run slam_toolbox async_slam_toolbox_node --ros-args "
            "-p odom_frame:=odom_filtered "
            "-p map_frame:=map "
            "-p base_frame:=base_link_ekf "
            "-p scan_topic:=/scan "
            "-p use_sim_time:=false "
            "-p mode:=mapping "
            "-p resolution:=0.15 "
            "-p max_laser_range:=20.0 "
            "-p map_update_interval:=0.05 "
            "-p transform_publish_period:=0.05 "
            "-p transform_timeout:=0.1 "
            "-p minimum_time_interval:=0.0 "
            "-p minimum_travel_distance:=0.0 "
            "-p minimum_travel_heading:=0.0 "
            "-p do_loop_closing:=true "
            "-p stack_size_to_use:=40000000"
        )

        time.sleep(3)

        if (
            "mapping_slam_toolbox" in self.processes and
            self.processes["mapping_slam_toolbox"]["proc"].poll() is None
        ):
            self.activate_slam_toolbox()
        else:
            self.get_logger().error(
                "slam_toolbox is not running, skipping lifecycle activation"
            )

        self.get_logger().info("Local mapping stack start command issued")

    def stop_mapping(self):
        self.get_logger().info("Stopping local mapping stack...")

        self.stop_process("mapping_slam_toolbox")
        self.stop_process("mapping_static_tf")
        self.stop_process("mapping_odom_to_tf")

        self.get_logger().info("Local mapping stack stopped")

    def activate_slam_toolbox(self):
        self.get_logger().info("Activating slam_toolbox lifecycle node...")

        configure_cmd = (
            "source /opt/ros/jazzy/setup.bash && "
            "source ~/ros2_ws/install/setup.bash && "
            "ros2 service call /slam_toolbox/change_state "
            "lifecycle_msgs/srv/ChangeState "
            '"{transition: {id: 1}}"'
        )

        activate_cmd = (
            "source /opt/ros/jazzy/setup.bash && "
            "source ~/ros2_ws/install/setup.bash && "
            "ros2 service call /slam_toolbox/change_state "
            "lifecycle_msgs/srv/ChangeState "
            '"{transition: {id: 3}}"'
        )

        try:
            subprocess.run(["bash", "-lc", configure_cmd], check=True)
            self.get_logger().info("slam_toolbox configured")

            time.sleep(1)

            subprocess.run(["bash", "-lc", activate_cmd], check=True)
            self.get_logger().info("slam_toolbox activated")

        except subprocess.CalledProcessError as e:
            self.get_logger().error(f"Failed to activate slam_toolbox: {e}")
        except Exception as e:
            self.get_logger().error(
                f"Unexpected error while activating slam_toolbox: {e}"
            )

    def start_process(self, name, cmd_string):
        if name in self.processes:
            proc = self.processes[name]["proc"]
            if proc.poll() is None:
                self.get_logger().warn(f"Process '{name}' is already running")
                return
            else:
                self._cleanup_process_entry(name)

        full_cmd = (
            "source /opt/ros/jazzy/setup.bash && "
            "source ~/ros2_ws/install/setup.bash && "
            f"{cmd_string}"
        )

        stdout_path = os.path.join(self.log_dir, f"{name}.out.log")
        stderr_path = os.path.join(self.log_dir, f"{name}.err.log")

        try:
            stdout_file = open(stdout_path, "a")
            stderr_file = open(stderr_path, "a")

            proc = subprocess.Popen(
                ["bash", "-lc", full_cmd],
                start_new_session=True,
                stdout=stdout_file,
                stderr=stderr_file
            )

            self.processes[name] = {
                "proc": proc,
                "stdout_file": stdout_file,
                "stderr_file": stderr_file,
            }

            self.get_logger().info(
                f"Started '{name}' with PID {proc.pid}: {cmd_string}"
            )

            time.sleep(1.0)
            if proc.poll() is not None:
                self.get_logger().error(
                    f"Process '{name}' exited immediately with code {proc.returncode}. "
                    f"Check logs: {stdout_path}, {stderr_path}"
                )
                self._cleanup_process_entry(name)

        except Exception as e:
            self.get_logger().error(f"Failed to start '{name}': {e}")

    def stop_process(self, name):
        if name not in self.processes:
            self.get_logger().warn(f"Process '{name}' is not running")
            return

        proc = self.processes[name]["proc"]

        if proc.poll() is not None:
            self.get_logger().warn(f"Process '{name}' already exited")
            self._cleanup_process_entry(name)
            return

        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGINT)
            proc.wait(timeout=5)
            self.get_logger().info(f"Stopped '{name}' cleanly")
        except subprocess.TimeoutExpired:
            self.get_logger().warn(
                f"'{name}' did not stop after SIGINT, killing it"
            )
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception as e:
            self.get_logger().error(f"Failed to stop '{name}': {e}")
        finally:
            self._cleanup_process_entry(name)

    def _cleanup_process_entry(self, name):
        if name not in self.processes:
            return

        entry = self.processes[name]

        try:
            entry["stdout_file"].close()
        except Exception:
            pass

        try:
            entry["stderr_file"].close()
        except Exception:
            pass

        del self.processes[name]

    def destroy_node(self):
        for name in list(self.processes.keys()):
            self.stop_process(name)
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = HMICommandReceiver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()