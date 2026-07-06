from PySide6.QtCore import QObject


class TeleopController(QObject):
    def __init__(self, teleop_node):
        super().__init__()
        self.node = teleop_node

        self.keys_down = {
            "space": False,
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "c": False
        }

        self.linear = 0.0
        self.angular = 0.0
        self.tool = 0.0

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
            self.tool = 0.0
        else:
            self.linear = 1.0 if self.keys_down["w"] else -1.0 if self.keys_down["s"] else 0.0
            self.angular = 1.0 if self.keys_down["a"] else -1.0 if self.keys_down["d"] else 0.0
            self.tool = 1.0 if self.keys_down["c"] else 0.0

        self.send_cmd()

    def send_cmd(self):
        self.node.send_cmd(self.linear, self.angular, self.tool)
