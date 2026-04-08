from rclpy.node import Node
from px4_msgs.msg import BatteryStatus, VehicleStatus
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from PySide6.QtCore import QObject, Signal

class BatterySignalBridge(QObject):
    battery_updated = Signal(int)
    arming_updated = Signal(str)
    offboard_updated = Signal(str)

class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        self.signals = BatterySignalBridge()

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Battery Subscription
        self.battery_sub = self.create_subscription(
            BatteryStatus,
            '/fmu/out/battery_status_v1',
            self.battery_callback,
            qos
        )

        # Vehicle Status Subscription
        self.status_sub = self.create_subscription(
            VehicleStatus,
            '/fmu/out/vehicle_status_v1',
            self.status_callback,
            qos
        )

    def battery_callback(self, msg):
        percent = int(msg.remaining * 100)
        self.signals.battery_updated.emit(percent)

    def status_callback(self, msg):
        # 1. Handle Arming Status
        is_armed = "Armed" if msg.arming_state == 2 else "Disarmed"
        self.signals.arming_updated.emit(is_armed)

        # 2. Handle Offboard Status
        is_offboard = "Offboard:Off" if msg.nav_state == 14 else "Offboard:On"
        self.signals.offboard_updated.emit(is_offboard)
