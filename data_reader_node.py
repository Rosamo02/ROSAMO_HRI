from time import monotonic
import subprocess
import math

from rclpy.node import Node
from px4_msgs.msg import VehicleStatus, VehicleOdometry
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
    connection_updated = Signal(str)
    odom_updated = Signal(str)


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
            depth=10,
        )

        self.current_percent = None
        self.current_current = None
        self.current_charge = None

        self.last_status_rx_time = None
        self.last_status_timestamp = 0

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

        self.odom_sub = self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odom_callback,
            px4_status_qos
        )

        self.time_left_timer = self.create_timer(2.0, self.update_time_left)
        self.status_watchdog_timer = self.create_timer(0.5, self.check_status_timeout)

        # Check Husarnet connection every 3 seconds
        self.connection_timer = self.create_timer(3.0, self.update_connection_status)

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
        self.last_status_rx_time = monotonic()

        if msg.timestamp <= self.last_status_timestamp:
            return
        self.last_status_timestamp = msg.timestamp

        armed = (msg.arming_state == VehicleStatus.ARMING_STATE_ARMED)
        offboard_active = (
            msg.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD
        )
        offboard_requested = (
            msg.nav_state_user_intention == VehicleStatus.NAVIGATION_STATE_OFFBOARD
        )

        print(
            f"STATUS RX ts={msg.timestamp} "
            f"arming_state={msg.arming_state} armed={armed} "
            f"nav_state={msg.nav_state} offboard_active={offboard_active} "
            f"user_intention={msg.nav_state_user_intention} "
            f"offboard_requested={offboard_requested}",
            flush=True,
        )

        self.signals.arming_updated.emit("Armed" if armed else "Disarmed")

        if offboard_active:
            offboard_text = "Offboard: On"
        elif offboard_requested:
            offboard_text = "Offboard: Requested"
        else:
            offboard_text = "Offboard: Off"

        self.signals.offboard_updated.emit(offboard_text)

    def check_status_timeout(self):
        if self.last_status_rx_time is None:
            self.signals.arming_updated.emit("Arming: No Data")
            self.signals.offboard_updated.emit("Offboard: No Data")
            return

        if monotonic() - self.last_status_rx_time > 1.5:
            self.signals.arming_updated.emit("Arming: Stale")
            self.signals.offboard_updated.emit("Offboard: Stale")

    def update_connection_status(self):
        status = self.get_connection_status("Robot")
        self.signals.connection_updated.emit(status)

    def get_connection_status(self, peer_name: str) -> str:
        try:
            result = subprocess.run(
                ["husarnet", "status"],
                capture_output=True,
                text=True,
                timeout=2.0,
            )

            if result.returncode != 0:
                return "Connection: None"

            lines = (result.stdout or "").splitlines()
            peer_name_lower = peer_name.lower()

            for i, line in enumerate(lines):
                if peer_name_lower in line.lower():
                    nearby = " ".join(lines[i:i + 4]).lower()

                    if "direct" in nearby:
                        return "Connection: P2P"
                    if "tunelled" in nearby or "tunneled" in nearby:
                        return "Connection: Tunneled"

                    return "Connection: None"

            return "Connection: None"

        except Exception as e:
            print(f"Failed to get Husarnet status: {e}")
            return "Connection: None"

    def odom_callback(self, msg: VehicleOdometry):
        vx = float(msg.velocity[0])
        vy = float(msg.velocity[1])
        vz = float(msg.velocity[2])
        az = float(msg.angular_velocity[2])
        speed = math.sqrt(vx * vx + vy * vy + vz * vz)
        angular = az * 180/math.pi
        self.signals.odom_updated.emit(f"Speed: {speed:.2f} m/s AngularSpeed: {angular:.2f} º/s ")
