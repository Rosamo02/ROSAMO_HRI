from PySide6.QtCore import QObject, Signal
from rclpy.node import Node
from rcl_interfaces.msg import Log


class RosoutSignals(QObject):
    log_received = Signal(str)


#ROS 2 node responsible for receiving log messages published on the /rosout topic and forwarding them to the HMI.

#The received messages are formatted to include their severity level, the name of the publishing node, and the log message.
class RosoutNode(Node):
    def __init__(self):
        #Initializes the ROS 2 log listener and creates a subscription to the /rosout topic.
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
        #Processes incoming ROS 2 log messages.

        #Converts the numeric severity level into a readable string, formats the message, and emits it through a Qt sign also it can be displayed in the HMI.
        
        level_name = self.level_to_name(msg.level)

        text = (
            f"[{level_name}] "
            f"{msg.name}: "
            f"{msg.msg}"
        )

        self.signals.log_received.emit(text)

    def level_to_name(self, level):

        #Converts ROS 2 numeric log severity levels into their corresponding readable names.
        
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
