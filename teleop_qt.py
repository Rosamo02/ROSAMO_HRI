import sys
import threading
import rclpy
from rclpy.node import Node

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QKeyEvent
from geometry_msgs.msg import Twist


class TeleopNode(Node):
    def __init__(self):
        super().__init__('qt_teleop')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def send_cmd(self, linear, angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.pub.publish(msg)


class TeleopWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create ROS node
        self.node = TeleopNode()

        # Start ROS spinning in background
        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(self.node)

        self.ros_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.ros_thread.start()

        self.setWindowTitle("Qt ROS2 Teleop")

        # Current command state
        self.linear = 0.0
        self.angular = 0.0

    def update_cmd(self):
        self.node.send_cmd(self.linear, self.angular)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.text().lower()

        if key == 'w':
            self.linear = 1.0
        elif key == 's':
            self.linear = -1.0
        elif key == 'a':
            self.angular = 1.0
        elif key == 'd':
            self.angular = -1.0
        elif event.key() == 32:  # Space bar
            self.linear = 0.0
            self.angular = 0.0

        self.update_cmd()

    def keyReleaseEvent(self, event: QKeyEvent):
        key = event.text().lower()

        if key in ['w', 's']:
            self.linear = 0.0
        if key in ['a', 'd']:
            self.angular = 0.0

        self.update_cmd()

    def closeEvent(self, event):
        self.executor.shutdown()
        rclpy.shutdown()
        super().closeEvent(event)


if __name__ == "__main__":
    rclpy.init()
    app = QApplication(sys.argv)
    win = TeleopWindow()
    win.show()
    sys.exit(app.exec())
