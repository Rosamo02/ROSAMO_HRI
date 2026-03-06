# image_viewer.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage
import cv2
import numpy as np


class ImageViewer(Node, QObject):
    new_frame = Signal(QImage)

    def __init__(self, topic="/camera/camera/color/image_raw/compressed"):
        Node.__init__(self, "qt_image_viewer")
        QObject.__init__(self)

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            CompressedImage,
            topic,
            self.callback,
            10
        )

    def callback(self, msg):
        try:
            # Decode JPEG from msg.data
            np_arr = np.frombuffer(msg.data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Optional: rotate 180°
            frame = cv2.rotate(frame, cv2.ROTATE_180)

            # Ensure contiguous memory for Qt
            frame = frame.copy()

            h, w, ch = frame.shape
            bytes_per_line = ch * w

            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
            self.new_frame.emit(qimg.copy())
        except Exception as e:
            print("[ImageViewer ERROR]:", e)
