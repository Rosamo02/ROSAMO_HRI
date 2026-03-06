import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel


class GstVideoWidget(QLabel):
    def __init__(self, pipeline_str, parent=None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        self.setText("Waiting for video...")

        # Initialize GStreamer
        Gst.init(None)

        # Build pipeline
        self.pipeline = Gst.parse_launch(pipeline_str)

        # Get appsink element
        self.appsink = self.pipeline.get_by_name("appsink")
        self.appsink.connect("new-sample", self.on_new_sample)

        # Start pipeline
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_new_sample(self, sink):
        sample = sink.emit("pull-sample")
        buf = sample.get_buffer()
        caps = sample.get_caps()
        structure = caps.get_structure(0)

        width = structure.get_value("width")
        height = structure.get_value("height")

        success, map_info = buf.map(Gst.MapFlags.READ)
        if not success:
            return Gst.FlowReturn.ERROR

        # Convert raw frame to QImage
        frame = QImage(
            map_info.data,
            width,
            height,
            QImage.Format_RGB888
        ).rgbSwapped()

        self.setPixmap(QPixmap.fromImage(frame))

        buf.unmap(map_info)
        return Gst.FlowReturn.OK
