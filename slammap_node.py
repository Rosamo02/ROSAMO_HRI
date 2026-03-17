import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid

from PySide6.QtGui import QImage, QColor
from PySide6.QtCore import Signal, QObject


class MapBridge(QObject):
    map_updated = Signal(QImage)


class MapNode(Node):
    def __init__(self):
        super().__init__("map_node")

        self.bridge = MapBridge()

        self.subscription = self.create_subscription(
            OccupancyGrid,
            "/map",
            self.map_callback,
            10
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
