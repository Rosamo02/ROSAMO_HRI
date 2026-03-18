from rclpy.node import Node
from px4_msgs.msg import BatteryStatus
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class BatteryNode(Node):
    def __init__(self, ui):
        super().__init__('battery_node')
        self.ui = ui

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.sub = self.create_subscription(
            BatteryStatus,
            '/fmu/out/battery_status_v1',
            self.callback,
            qos
        )

    def callback(self, msg):
        percent = int(msg.remaining * 100)        
        self.ui.labelBattery.setText(f"Battery: {percent}%")
        if percent > 50:
            self.ui.labelBattery.setStyleSheet("color: green;")
        elif percent > 20:
            self.ui.labelBattery.setStyleSheet("color: yellow;")
        else:
            self.ui.labelBattery.setStyleSheet("color: red;")
