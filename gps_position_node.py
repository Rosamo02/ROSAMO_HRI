import math

from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from PySide6.QtCore import QObject, Signal

from px4_msgs.msg import SensorGps


class GPSPositionSignals(QObject):
    gps_updated = Signal(float, float)
    gps_label_message = Signal(str)
    gps_rtk_message = Signal(str)


class GPSPositionNode(Node):
    def __init__(self):
        super().__init__("gps_position_node")

        self.signals = GPSPositionSignals()

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.subscription = self.create_subscription(
            SensorGps,
            "/fmu/out/vehicle_gps_position",
            self.vehicle_gps_position_callback,
            qos_profile
        )

        print("GPSPositionNode subscribed to /fmu/out/vehicle_gps_position")

    def fix_type_to_text(self, fix_type):
        fix_types = {
                0: "No fix",
                1: "No fix",
                2: "2D fix",
                3: "3D fix",
                4: "DGPS / RTCM differential",
                5: "RTK float",
                6: "RTK fixed",
                8: "Extrapolated",
        }

        return fix_types.get(fix_type, f"Unknown fix type {fix_type}")

    def vehicle_gps_position_callback(self, msg):
        print("GPS callback received")

        fix_text = self.fix_type_to_text(msg.fix_type)

        self.signals.gps_rtk_message.emit(
            f"GPS Fix: {fix_text} ({msg.fix_type})"
        )

        if msg.fix_type < 3:
            print(f"GPS fix not good enough: fix_type={msg.fix_type}")
            return

        lat = float(msg.latitude_deg)
        lon = float(msg.longitude_deg)

        if not math.isfinite(lat) or not math.isfinite(lon):
            print("Invalid GPS: not finite")
            return

        if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
            print(f"Invalid GPS coordinates: lat={lat}, lon={lon}")
            return

        print(f"GPS position: lat={lat}, lon={lon}")
        self.signals.gps_updated.emit(lat, lon)
        self.signals.gps_label_message.emit(f"GPS Position: lat={lat:.7f},lon={lon:.7f}")
