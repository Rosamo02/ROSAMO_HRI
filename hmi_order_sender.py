from std_msgs.msg import String

#This class is responsible for sending commands from the HMI to the robot

class HMICommandClient:
    def __init__(self, node):
        self.pub = node.create_publisher(String, "/hmi/command", 5)
        self.i_debug = False;
        self.i_Lmap = False;

    def send(self, command: str):
        msg = String()
        msg.data = command
        self.pub.publish(msg)
        print(f"[HMI] Sent command: {command}")


    def start_stop_debug_msg(self):
        if self.i_debug == False:
            self.send("start_debug")
            self.i_debug = True
        else:
            self.send("stop_debug")
            self.i_debug = False

    def start_stop_Lidar_Map_msg(self):
        if self.i_Lmap == False:
            self.send("start_mapping")
            self.i_Lmap = True
        else:
            self.send("stop_mapping")
            self.i_Lmap = False
