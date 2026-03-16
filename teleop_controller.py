# teleop_controller.py
from PySide6.QtCore import QObject
from geometry_msgs.msg import Twist

class TeleopController(QObject):
    def __init__(self, teleop_node):
        super().__init__()
        self.node = teleop_node

        # Track key states
        self.keys_down = {"space": False, "w": False, "a": False, "s": False, "d": False}
        self.linear = 0.0
        self.angular = 0.0

    def handle_key_press(self, key):
        if key == " ":
            self.keys_down["space"] = True
        elif key in self.keys_down:
            self.keys_down[key] = True

        self.update_motion()

    def handle_key_release(self, key):
        if key == " ":
            self.keys_down["space"] = False
        elif key in self.keys_down:
            self.keys_down[key] = False

        self.update_motion()

    def update_motion(self):
        if not self.keys_down["space"]:
            self.linear = 0.0
            self.angular = 0.0
        else:
            self.linear = 1.0 if self.keys_down["w"] else -1.0 if self.keys_down["s"] else 0.0
            self.angular = 1.0 if self.keys_down["a"] else -1.0 if self.keys_down["d"] else 0.0

        self.send_cmd()

    def send_cmd(self):
        msg = Twist()
        msg.linear.x = self.linear
        msg.angular.z = self.angular
        self.node.pub.publish(msg)
