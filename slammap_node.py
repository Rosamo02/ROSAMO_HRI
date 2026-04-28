import rclpy
from rclpy.node import Node

from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import Image

from PySide6.QtGui import QImage, QColor
from PySide6.QtCore import Signal, QObject

from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

class MapBridge(QObject):
    map_updated = Signal(QImage)
    map_image_updated = Signal(QImage)

class MapNode(Node):
    def __init__(self):
        super().__init__("map_node")

        self.bridge = MapBridge()

        map_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.map_subscription = self.create_subscription(
            OccupancyGrid,
            "/map",
            self.map_callback,
            map_qos
        )

        self.map_image_subscription = self.create_subscription(
            Image,
            "/map_image",
            self.map_image_callback,
            map_qos
        )

    def map_callback(self, msg):
        w = msg.info.width
        h = msg.info.height
        data = msg.data

        img = QImage(w, h, QImage.Format_RGB888)

        for y in range(h):
            for x in range(w):
                cell = data[y * w + x]

                if cell == -1:
                    color = QColor(127, 127, 127)
                elif cell == 0:
                    color = QColor(255, 255, 255)
                else:
                    color = QColor(0, 0, 0)

                img.setPixelColor(x, h - y - 1, color)

        self.bridge.map_updated.emit(img)

    def map_image_callback(self, msg):
        if msg.encoding.lower() != "bgr8":
            self.get_logger().warn(
                f"Unsupported /map_image encoding: {msg.encoding}"
            )
            return

        qimg = QImage(
            bytes(msg.data),
            msg.width,
            msg.height,
            msg.step,
            QImage.Format_BGR888
        ).copy()

        self.bridge.map_image_updated.emit(qimg)
