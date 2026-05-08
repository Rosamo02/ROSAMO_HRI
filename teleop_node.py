from rclpy.node import Node
from geometry_msgs.msg import Twist

class TeleopNode(Node):
    def __init__(self):
        print("TeleopNode: before super")
        super().__init__('qt_teleop')
        print("TeleopNode: after super")
        print("TeleopNode: before create_publisher")
        self.pub = self.create_publisher(Twist, '/cmd_vel', 20)
        print("TeleopNode: after create_publisher")

    def send_cmd(self, linear, angular, tool):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        msg.linear.z = tool
        self.pub.publish(msg)
