from rclpy.node import Node
from px4_msgs.msg import VehicleStatus
from sensor_msgs.msg import BatteryState
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from PySide6.QtCore import QObject, Signal


class BatterySignalBridge(QObject):
    battery_updated = Signal(int)
    arming_updated = Signal(str)
    offboard_updated = Signal(str)
    time_left_updated = Signal(str)


class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        self.signals = BatterySignalBridge()

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.last_percent_for_estimate = None
        self.last_estimate_time = None

        self.current_percent = None
        self.current_current = None

        # Battery subscription
        self.battery_sub = self.create_subscription(
            BatteryState,
            '/litime_bms/state',
            self.battery_callback,
            qos
        )

        # Vehicle status subscription
        self.status_sub = self.create_subscription(
            VehicleStatus,
            '/fmu/out/vehicle_status_v1',
            self.status_callback,
            qos
        )

        # Recompute time remaining every 10 seconds
        self.time_left_timer = self.create_timer(2.0, self.update_time_left)

    def battery_callback(self, msg: BatteryState):
        percent = max(0.0, min(100.0, msg.percentage * 100.0))
        self.current_percent = percent
        self.current_current = msg.current

        self.signals.battery_updated.emit(int(percent))

    def update_time_left(self):
        print("update_time_left called")
        print(f"current_percent={self.current_percent}, current_current={self.current_current}")

        if self.current_percent is None or self.current_current is None:
            print("No battery data yet")
            self.signals.time_left_updated.emit("--")
            return

        now = self.get_clock().now().nanoseconds / 1e9
        percent = self.current_percent
        current = self.current_current

        time_left_str = "--"

        if current < 0.0:
            if self.last_percent_for_estimate is not None and self.last_estimate_time is not None:
                dp = self.last_percent_for_estimate - percent
                dt = now - self.last_estimate_time
                print(f"dp={dp}, dt={dt}")

                if dp > 0.0 and dt > 0.0:
                    seconds_per_percent = dt / dp
                    time_left_sec = percent * seconds_per_percent

                    hours = int(time_left_sec // 3600)
                    minutes = int((time_left_sec % 3600) // 60)
                    time_left_str = f"{hours}h {minutes}m"
        else:
            print("Battery not discharging")

        self.last_percent_for_estimate = percent
        self.last_estimate_time = now

        print(f"time_left_str={time_left_str}")
        self.signals.time_left_updated.emit(time_left_str)

    def status_callback(self, msg: VehicleStatus):
        is_armed = "Armed" if msg.arming_state == 2 else "Disarmed"
        self.signals.arming_updated.emit(is_armed)

        is_offboard = "Offboard:On" if msg.nav_state == 14 else "Offboard:Off"
        self.signals.offboard_updated.emit(is_offboard)
