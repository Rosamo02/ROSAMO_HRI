from PySide6.QtCore import QObject, Signal
from rclpy.node import Node
from rcl_interfaces.msg import Log


class RosoutSignals(QObject):
    log_received = Signal(str)


class RosoutNode(Node):
    def __init__(self):
        super().__init__("hmi_rosout_listener")

        self.signals = RosoutSignals()

        self.sub = self.create_subscription(
            Log,
            "/rosout",
            self.rosout_callback,
            100
        )

        self.get_logger().info("Rosout listener started")

    def rosout_callback(self, msg):
        level_name = self.level_to_name(msg.level)

        text = (
            f"[{level_name}] "
            f"{msg.name}: "
            f"{msg.msg}"
        )

        self.signals.log_received.emit(text)

    def level_to_name(self, level):
        if level == Log.DEBUG:
            return "DEBUG"
        elif level == Log.INFO:
            return "INFO"
        elif level == Log.WARN:
            return "WARN"
        elif level == Log.ERROR:
            return "ERROR"
        elif level == Log.FATAL:
            return "FATAL"
        else:
            return str(level)
