from std_msgs.msg import String, Empty

class HMICommandClient:
    def __init__(self, node):
        self.pub = node.create_publisher(String, "/hmi/command", 5)

        self.pubstartoff = node.create_publisher(Empty, "/start_offboard", 5)
        self.pubstopoff = node.create_publisher(Empty, "/stop_offboard", 5)
        self.pubstartarm = node.create_publisher(Empty, "/start_arming", 5)
        self.pubstoparm = node.create_publisher(Empty, "/stop_arming", 5)

        self.i_debug = False
        self.i_Lmap = False
        self.i_router = False
        self.i_off = False
        self.i_arm = False

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
            self.i_Lmap = True
        else:
            self.send("stop_mapping")
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

    def start_stop_ros2router_msg(self):
        if not self.i_router:
            self.send("start_ros2router")
            self.i_router = True
        else:
            self.send("stop_ros2router")
            self.i_router = False
