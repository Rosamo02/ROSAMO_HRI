from rclpy.node import Node
from geometry_msgs.msg import Twist


class TeleopNode(Node):
    def __init__(self):
        super().__init__('qt_teleop')

        self.pub = self.create_publisher(Twist, '/cmd_vel', 20)

        # Drive speed scale: linear.x and angular.z
        self.speed_scale = 0.0

        # Tool speed scale: linear.z
        self.tool_scale = 0.0

    def set_speed_scale(self, scale):
        self.speed_scale = scale
        print(f"Drive scale is set to {scale}")

    def set_tool_scale(self, scale):
        self.tool_scale = scale
        print(f"Tool scale is set to {scale}")

    def send_cmd(self, linear, angular, tool):
        msg = Twist()

        msg.linear.x = linear * self.speed_scale
        msg.angular.z = angular * self.speed_scale

        # Tool uses its own slider
        msg.linear.z = tool * self.tool_scale

        self.pub.publish(msg)
