import os
import signal
import subprocess


class LocalProcessManager:
    def __init__(self):
        self.hmi_receiver_proc = None

    def start_hmi_receiver(self):
        if self.hmi_receiver_proc is not None and self.hmi_receiver_proc.poll() is None:
            print("hmi_command_receiver.py is already running")
            return False

        cmd = (
            "source /opt/ros/jazzy/setup.bash && "
            "source ~/ros2_ws/install/setup.bash && "
            "python3 ~/Desktop/hmi_command_receiver.py"
        )

        self.hmi_receiver_proc = subprocess.Popen(
            ["bash", "-lc", cmd],
            start_new_session=True
        )

        print("Started hmi_command_receiver.py")
        return True

    def stop_hmi_receiver(self):
        if self.hmi_receiver_proc is None or self.hmi_receiver_proc.poll() is not None:
            print("hmi_command_receiver.py is not running")
            self.hmi_receiver_proc = None
            return False

        try:
            os.killpg(os.getpgid(self.hmi_receiver_proc.pid), signal.SIGINT)
            self.hmi_receiver_proc.wait(timeout=5)
            print("Stopped hmi_command_receiver.py")
        except Exception as e:
            print(f"Failed to stop hmi_command_receiver.py: {e}")
            return False
        finally:
            self.hmi_receiver_proc = None

        return True

    def toggle_hmi_receiver(self):
        if self.hmi_receiver_proc is None or self.hmi_receiver_proc.poll() is not None:
            started = self.start_hmi_receiver()
            return "started" if started else "failed"
        else:
            stopped = self.stop_hmi_receiver()
            return "stopped" if stopped else "failed"

    def is_hmi_receiver_running(self):
        return (
            self.hmi_receiver_proc is not None and
            self.hmi_receiver_proc.poll() is None
        )
