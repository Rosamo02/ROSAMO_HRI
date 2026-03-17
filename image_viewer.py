# image_viewer.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QImage
import cv2
import numpy as np


class ImageViewer(Node, QObject):
    new_frame = Signal(QImage)

    def __init__(self, topic="/apriltag/overlay/compressed"):
        Node.__init__(self, "qt_image_viewer")
        QObject.__init__(self)

        self.bridge = CvBridge()

        sensor_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.subscription = self.create_subscription(
            CompressedImage,
            topic,
            self.callback,
            qos_profile=sensor_qos
        )

    def callback(self, msg):
        try:
            # Decode JPEG from msg.data
            np_arr = np.frombuffer(msg.data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Optional: rotate 180° because the image comes in wrong(Maybe change if needed)
            frame = cv2.rotate(frame, cv2.ROTATE_180)

            # Ensure contiguous memory for Qt
            frame = frame.copy()

            h, w, ch = frame.shape
            bytes_per_line = ch * w

            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
            self.new_frame.emit(qimg.copy())
        except Exception as e:
            print("[ImageViewer ERROR]:", e)
