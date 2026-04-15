import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel


class GstVideoWidget(QLabel):
    frame_ready = Signal(QImage)

    def __init__(self, pipeline_str, parent=None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        self.setText("Waiting for video...")

        Gst.init(None)

        self.pipeline = Gst.parse_launch(pipeline_str)
        self.appsink = self.pipeline.get_by_name("appsink")

        if self.appsink is None:
            raise RuntimeError("appsink element named 'appsink' was not found in the pipeline")

        self.appsink.connect("new-sample", self.on_new_sample)
        self.frame_ready.connect(self.update_frame)

        self.pipeline.set_state(Gst.State.PLAYING)

    def on_new_sample(self, sink):
        sample = sink.emit("pull-sample")
        if sample is None:
            return Gst.FlowReturn.ERROR

        buf = sample.get_buffer()
        caps = sample.get_caps()
        structure = caps.get_structure(0)

        width = structure.get_value("width")
        height = structure.get_value("height")

        success, map_info = buf.map(Gst.MapFlags.READ)
        if not success:
            return Gst.FlowReturn.ERROR

        try:
            image = QImage(
                map_info.data,
                width,
                height,
                width * 3,
                QImage.Format_RGB888
            ).copy()   # copy before unmapping
        finally:
            buf.unmap(map_info)

        self.frame_ready.emit(image)
        return Gst.FlowReturn.OK

    def update_frame(self, image):
        self.setPixmap(QPixmap.fromImage(image))

    def close(self):
        if self.pipeline is not None:
            self.pipeline.set_state(Gst.State.NULL)
        super().close()
