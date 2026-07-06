from std_msgs.msg import String, Empty
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

class HMICommandClient:
    def __init__(self, node,screen_button=None,lq_screen_button=None,secondary_camera_button=None,lq_secondary_camera_button=None,apriltag_button=None):

        #Local publisher
        self.pub = node.create_publisher(String, "/hmi/command", 5)

        qos_best_effort = QoSProfile(
                    reliability=ReliabilityPolicy.BEST_EFFORT,
                    durability=DurabilityPolicy.VOLATILE,
                    history=HistoryPolicy.KEEP_LAST,
                    depth=5,
                )

        #Publisher into the robot
        self.pubstartoff = node.create_publisher(Empty, "/start_offboard", 5)
        self.pubstopoff = node.create_publisher(Empty, "/stop_offboard", 5)

        self.pubstartarm = node.create_publisher(Empty, "/start_arming", 5)
        self.pubstoparm = node.create_publisher(Empty, "/stop_arming", 5)

        self.pubstartcamera = node.create_publisher(Empty, "/start_camera_stream", qos_best_effort)
        self.pubstopcamera = node.create_publisher(Empty, "/stop_camera_stream", qos_best_effort)

        self.publqstartcamera = node.create_publisher(Empty, "/start_lq_camera_stream", qos_best_effort)
        self.publqstopcamera = node.create_publisher(Empty, "/stop_lq_camera_stream", qos_best_effort)

        self.pubsecondstartcamera = node.create_publisher(Empty, "/start_secondary_camera_stream", qos_best_effort)
        self.pubsecondstopcamera = node.create_publisher(Empty, "/stop_secondary_camera_stream", qos_best_effort)

        self.publqsecondstartcamera = node.create_publisher(Empty, "/start_lq_secondary_camera_stream", qos_best_effort)
        self.publqsecondstopcamera = node.create_publisher(Empty, "/stop_lq_secondary_camera_stream", qos_best_effort)

        self.pubstartcamera_front = node.create_publisher(Empty, "/start_station_detection_APRILTAG", qos_best_effort)
        self.pubstopcamera_front = node.create_publisher(Empty, "/stop_station_detection_APRILTAG", qos_best_effort)

        self.pubstartlivox = node.create_publisher(Empty, "/start_livox_driver", qos_best_effort)
        self.pubstoplivox = node.create_publisher(Empty, "/stop_livox_driver", qos_best_effort)

        self.pubstartpclscan = node.create_publisher(Empty, "/start_pointcloud_to_laserscan", qos_best_effort)
        self.pubstoppclscan = node.create_publisher(Empty, "/stop_pointcloud_to_laserscan", qos_best_effort)

        self.pubstartvicon = node.create_publisher(Empty, "/start_vicon_bridge", qos_best_effort)
        self.pubstopvicon = node.create_publisher(Empty, "/stop_vicon_bridge", qos_best_effort)

        self.pubstartekf = node.create_publisher(Empty, "/start_ekf", qos_best_effort)
        self.pubstopekf = node.create_publisher(Empty, "/stop_ekf", qos_best_effort)

        self.pubstartstatictf = node.create_publisher(Empty, "/start_static_tf_livox", qos_best_effort)
        self.pubstopstatictf = node.create_publisher(Empty, "/stop_static_tf_livox", qos_best_effort)

        self.pubstartbridge = node.create_publisher(Empty, "/start_px4_odom_bridge", qos_best_effort)
        self.pubstopbridge = node.create_publisher(Empty, "/stop_px4_odom_bridge", qos_best_effort)

        self.pubstartslamtoolbox = node.create_publisher(Empty, "/start_slam_toolbox", qos_best_effort)
        self.pubstopslamtoolbox = node.create_publisher(Empty, "/stop_slam_toolbox", qos_best_effort)

        self.pubstartrtk = node.create_publisher(Empty, "/start_rtk_ntrip", qos_best_effort)
        self.pubstoprtk = node.create_publisher(Empty, "/stop_rtk_ntrip", qos_best_effort)

        #store the buttons in the class
        self.screen_button = screen_button
        self.lq_screen_button = lq_screen_button
        self.apriltag_button = apriltag_button
        self.secondary_camera_button = secondary_camera_button
        self.lq_secondary_camera_button = lq_secondary_camera_button

        #Starting booleans(Assumes that all features are turn off previously to the interface being used)
        self.i_debug = False
        self.i_Lmap = False
        self.i_router = False
        self.i_off = False
        self.i_arm = False
        self.i_camera = False
        self.i_second_camera = False
        self.i_front_camera = False
        self.i_rtk = False

        #if self.screen_button is not None:
        #    self.screen_button.setText("Turn On Back Camera")

        #if self.apriltag_button is not None:
        #    self.apriltag_button.setText("Turn On Back Camera")

    def send(self, command: str):
        msg = String()
        msg.data = command
        self.pub.publish(msg)
        print(f"[HMI] Sent command: {command}")

    def send_empty(self, publisher, label: str):
        msg = Empty()
        publisher.publish(msg)
        print(f"[HMI] Sent empty command: {label}")

    def start_stop_debug_msg(self):
        if not self.i_debug:
            self.send("start_debug")
            self.i_debug = True
        else:
            self.send("stop_debug")
            self.i_debug = False

    def start_stop_Lidar_Map_msg(self):
        if not self.i_Lmap:
            self.send("start_mapping")
            self.send("start_image_mapping")

            self.send_empty(self.pubstartlivox, "/start_livox_driver")
            self.send_empty(self.pubstartpclscan, "/start_pointcloud_to_laserscan")
            self.send_empty(self.pubstartbridge, "/start_px4_odom_bridge")
            self.send_empty(self.pubstartvicon, "/start_vicon_bridge")
            self.send_empty(self.pubstartekf, "/start_ekf")
            self.send_empty(self.pubstartstatictf, "/start_static_tf_livox")
            self.send_empty(self.pubstartslamtoolbox, "/start_slam_toolbox")

            self.i_Lmap = True
        else:
            self.send("stop_mapping")
            self.send("stop_image_mapping")

            self.send_empty(self.pubstopekf, "/stop_ekf")
            self.send_empty(self.pubstopvicon, "/stop_vicon_bridge")
            self.send_empty(self.pubstoppclscan, "/stop_pointcloud_to_laserscan")
            self.send_empty(self.pubstopbridge, "/stop_px4_odom_bridge")
            self.send_empty(self.pubstoplivox, "/stop_livox_driver")
            self.send_empty(self.pubstopstatictf, "/stop_static_tf_livox")
            self.send_empty(self.pubstopslamtoolbox, "/stop_slam_toolbox")

            self.i_Lmap = False

    def start_stop_offboard(self):
        if not self.i_off:
            self.send_empty(self.pubstartoff, "/start_offboard")
            self.i_off = True
        else:
            self.send_empty(self.pubstopoff, "/stop_offboard")
            self.i_off = False

    def start_stop_arming(self):
        if not self.i_arm:
            self.send_empty(self.pubstartarm, "/start_arming")
            self.i_arm = True
        else:
            self.send_empty(self.pubstoparm, "/stop_arming")
            self.i_arm = False


    def start_stop_rtk(self):
        if not self.i_rtk:
            self.send_empty(self.pubstartrtk, "/start_rtk_ntrip")
            self.i_rtk = True
        else:
            self.send_empty(self.pubstoprtk, "/stop_rtk_ntrip")
            self.i_rtk = False


    def start_stop_ros2router_msg(self):
        if not self.i_router:
            self.send("start_ros2router")
            self.i_router = True
        else:
            self.send("stop_ros2router")
            self.i_router = False

    def start_stop_front_camera(self):
        if not self.i_camera:
            self.send_empty(self.pubstartcamera, "/start_camera_stream")
            self.i_camera = True
            if self.screen_button is not None:
                self.lq_screen_button.setText("Turn Off CSI Camera")
                self.screen_button.setText("Turn Off CSI Camera")
        else:
            self.send_empty(self.pubstopcamera, "/stop_camera_stream")
            self.send_empty(self.publqstopcamera, "/stop_lq_camera_stream")
            self.i_camera = False
            if self.screen_button is not None:
                self.lq_screen_button.setText("Turn On CSI Camera")
                self.screen_button.setText("Turn On CSI Camera")


    def start_stop_lq_front_camera(self):
        if not self.i_camera:
            self.send_empty(self.publqstartcamera, "/start_lq_camera_stream")
            self.i_camera = True
            if self.lq_screen_button is not None:
                self.lq_screen_button.setText("Turn Off CSI Camera")
                self.screen_button.setText("Turn Off CSI Camera")
        else:
            self.send_empty(self.publqstopcamera, "/stop_lq_camera_stream")
            self.send_empty(self.pubstopcamera, "/stop_camera_stream")
            self.i_camera = False
            if self.lq_screen_button is not None:
                self.lq_screen_button.setText("Turn On CSI Camera")
                self.screen_button.setText("Turn On CSI Camera")

    def start_stop_second_camera(self):
        if not self.i_second_camera:
            self.send_empty(self.pubsecondstartcamera, "/start_secondary_camera_stream")
            self.i_second_camera = True
            if self.secondary_camera_button is not None:
                self.secondary_camera_button.setText("Turn Off Back CSI Camera")
        else:
            self.send_empty(self.pubsecondstopcamera, "/stop_secondary_camera_stream")
            self.send_empty(self.publqsecondstopcamera, "/stop_lq_secondary_camera_stream")
            self.i_second_camera = False
            if self.secondary_camera_button is not None:
                self.secondary_camera_button.setText("Turn On Back CSI Camera")

    def start_stop_lq_second_camera(self):
        if not self.i_second_camera:
            self.send_empty(self.publqsecondstartcamera, "/start_lq_secondary_camera_stream")
            self.i_second_camera = True
            if self.lq_secondary_camera_button is not None:
                self.lq_secondary_camera_button.setText("Turn Off Back CSI Camera")
                self.secondary_camera_button.setText("Turn Off Back CSI Camera")
        else:
            self.send_empty(self.publqsecondstopcamera, "/stop_lq_secondary_camera_stream")
            self.send_empty(self.pubsecondstopcamera, "/stop_secondary_camera_stream")
            self.i_second_camera = False
            if self.lq_secondary_camera_button is not None:
                self.lq_secondary_camera_button.setText("Turn On Back CSI Camera")
                self.secondary_camera_button.setText("Turn On Back CSI Camera")

    def start_stop_back_camera(self):
        if not self.i_front_camera:
            self.send_empty(self.pubstartcamera_front, "/start_station_detection_APRILTAG")
            self.i_front_camera = True
            if self.apriltag_button is not None:
                self.apriltag_button.setText("Turn Off RealSense Camera")
        else:
            self.send_empty(self.pubstopcamera_front, "/stop_station_detection_APRILTAG")
            self.i_front_camera = False
            if self.apriltag_button is not None:
                self.apriltag_button.setText("Turn On RealSense Camera")
