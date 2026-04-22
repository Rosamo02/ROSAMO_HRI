from rclpy.node import Node
from px4_msgs.msg import VehicleStatus
from sensor_msgs.msg import BatteryState
from rclpy.qos import (
    QoSProfile,
    QoSReliabilityPolicy,
    QoSHistoryPolicy,
    QoSDurabilityPolicy,
)
from PySide6.QtCore import QObject, Signal


class BatterySignalBridge(QObject):
    battery_updated = Signal(int, float)
    arming_updated = Signal(str)
    offboard_updated = Signal(str)
    time_left_updated = Signal(str)


class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        self.signals = BatterySignalBridge()

        battery_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        px4_status_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            durability=QoSDurabilityPolicy.VOLATILE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.current_percent = None
        self.current_current = None
        self.current_charge = None

        self.battery_sub = self.create_subscription(
            BatteryState,
            '/litime_bms/state',
            self.battery_callback,
            battery_qos
        )

        self.status_sub = self.create_subscription(
            VehicleStatus,
            '/fmu/out/vehicle_status_v1',
            self.status_callback,
            px4_status_qos
        )

        self.time_left_timer = self.create_timer(2.0, self.update_time_left)

    def battery_callback(self, msg: BatteryState):
        self.current_percent = max(0.0, min(100.0, msg.percentage * 100.0))
        self.current_current = float(msg.current)
        self.current_charge = float(msg.charge)
        self.signals.battery_updated.emit(int(self.current_percent), self.current_current)

    def update_time_left(self):
        if (
            self.current_percent is None
            or self.current_current is None
            or self.current_charge is None
        ):
            self.signals.time_left_updated.emit("--")
            return

        time_left_str = "--"

        if self.current_current < -0.01:
            discharge_current = abs(self.current_current)
            remaining_ah = self.current_charge / 1000.0

            if remaining_ah > 0.0 and discharge_current > 0.0:
                hours_left = remaining_ah / discharge_current
                total_seconds = int(hours_left * 3600)
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                time_left_str = f"{hours}h {minutes}m"

        self.signals.time_left_updated.emit(time_left_str)

    def status_callback(self, msg: VehicleStatus):
        print("status_callback fired")
        self.get_logger().info(
            f"STATUS rx: arming_state={msg.arming_state}, "
            f"nav_state={msg.nav_state}, "
            f"user_intention={msg.nav_state_user_intention}"
        )

        is_armed = "Armed" if msg.arming_state == 2 else "Disarmed"
        self.signals.arming_updated.emit(is_armed)

        is_offboard = "Offboard:On" if msg.nav_state == 14 else "Offboard:Off"
        self.signals.offboard_updated.emit(is_offboard)
