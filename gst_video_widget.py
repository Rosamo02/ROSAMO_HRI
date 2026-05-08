import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import QLabel


class GstVideoWidget(QLabel):
    frame_ready = Signal(QImage)

    def __init__(self, pipeline_str, parent=None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        self.setText("Waiting for video...")
        self.setScaledContents(False)

        # Toolpath in CAMERA IMAGE pixel coordinates.
        # Replace these example points with your real toolpath.
        self.toolpath_points = []

        self.show_toolpath = True

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
            ).copy()
        finally:
            buf.unmap(map_info)

        self.frame_ready.emit(image)
        return Gst.FlowReturn.OK

    def draw_toolpath(self, image):
        if not self.show_toolpath:
            return image

        if len(self.toolpath_points) < 2:
            return image

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        line_width = 4
        point_size = line_width
        # Draw path line

        path_pen = QPen(QColor(0, 0, 255))
        path_pen.setWidth(line_width)
        painter.setPen(path_pen)

        for i in range(len(self.toolpath_points) - 1):
            x1, y1 = self.toolpath_points[i]
            x2, y2 = self.toolpath_points[i + 1]
            painter.drawLine(x1, y1, x2, y2)

        # Draw points on the path
        painter.setPen(QPen(QColor(0, 0, 255), line_width))
        painter.setBrush(QBrush(QColor(0, 0, 255)))

        radius = point_size//2

        #for x, y in self.toolpath_points:
        #    painter.drawEllipse(x - radius, y - radius, point_size, point_size)

        painter.end()
        return image

    def update_frame(self, image):

        #FLip the image (horizontally, vertically)
        image = image.mirrored(True,True)

        # Draw the fixed toolpath on the frame        
        image = self.draw_toolpath(image)

        pixmap = QPixmap.fromImage(image)

        # Scale to fit the QLabel while preserving aspect ratio
        pixmap = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.setPixmap(pixmap)

    def set_toolpath_pixels(self, points):
        self.toolpath_points = points

    def toggle_toolpath(self, enabled):
        self.show_toolpath = enabled

    def close(self):
        if self.pipeline is not None:
            self.pipeline.set_state(Gst.State.NULL)
        super().close()
