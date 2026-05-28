# heading_node.py

import math

from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from PySide6.QtCore import QObject, Signal

from px4_msgs.msg import VehicleLocalPosition


class HeadingSignals(QObject):
    heading_updated = Signal(float)
    heading_label_message = Signal(str)


class HeadingNode(Node):
    def __init__(self):
        super().__init__("heading_node")

        self.signals = HeadingSignals()

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.subscription = self.create_subscription(
            VehicleLocalPosition,
            "/fmu/out/vehicle_local_position_v1",
            self.vehicle_local_position_callback,
            qos_profile
        )

        print("HeadingNode subscribed to /fmu/out/vehicle_local_position_v1")

    def vehicle_local_position_callback(self, msg):
        heading_rad = float(msg.heading)

        if not math.isfinite(heading_rad):
            print("Invalid heading: not finite")
            self.signals.heading_label_message.emit("Heading not good enough")
            return

        heading_deg = math.degrees(heading_rad) % 360.0

        # Always emit heading so the compass can still work for UI guidance
        self.signals.heading_updated.emit(heading_deg)

        if not msg.heading_good_for_control:
            self.signals.heading_label_message.emit("Heading not good enough")
            return

        self.signals.heading_label_message.emit(
            f"Heading: {heading_deg:.1f}°"
        )
