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
        if not msg.heading_good_for_control:
            #print("Heading not good for control yet")
            return

        heading_rad = float(msg.heading)

        if not math.isfinite(heading_rad):
            print("Invalid heading: not finite")
            return

        heading_deg = math.degrees(heading_rad)

        # Normalize to 0-360 degrees
        heading_deg = heading_deg % 360.0

        self.signals.heading_updated.emit(heading_deg)
        self.signals.heading_label_message.emit(
            f"Heading: {heading_deg:.1f}°"
        )
