# compass_widget.py

import math

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPolygonF
from PySide6.QtCore import Qt, QPointF


class CompassWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.relative_bearing = None
        self.distance_m = None
        self.tree_lat = None
        self.tree_lon = None
        self.heading_status_text = "Heading not available"

        self.setMinimumSize(180, 220)

        #make background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_target(self, relative_bearing, distance_m, tree_lat, tree_lon):

        #relative_bearing:0 degrees   = tree is straight ahead and 270 degrees = tree is to the left
        self.relative_bearing = relative_bearing
        self.distance_m = distance_m
        self.tree_lat = tree_lat
        self.tree_lon = tree_lon
        self.update()

    def clear_target(self):
        self.relative_bearing = None
        self.distance_m = None
        self.tree_lat = None
        self.tree_lon = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        center_x = width / 2
        center_y = 75
        radius = min(width * 0.35, 60)

        center = QPointF(center_x, center_y)

        # Compass circle
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.setPen(QPen(QColor("white"), 2))
        painter.drawEllipse(center, radius, radius)

        # Fixed robot forward arrow, always up
        self._draw_arrow(
            painter=painter,
            center=QPointF(center_x, center_y),
            angle_deg=0,
            length=44,
            color=QColor("red")
        )

        # Target tree arrow
        if self.relative_bearing is not None:
            self._draw_arrow(
                painter=painter,
                center=center,
                angle_deg=self.relative_bearing,
                length=44,
                color=QColor("lime")
            )

            info_font = QFont()
            info_font.setPointSize(8)
            painter.setFont(info_font)
            painter.setPen(QColor("white"))

            text = (
                f"Tree relative: {self.relative_bearing:.1f}°\n"
                f"Distance: {self.distance_m:.2f} m\n"
            )

            painter.drawText(
                12,
                int(center_y + radius + 20),
                width - 24,
                height - int(center_y + radius + 55),
                Qt.AlignCenter,
                text
            )

        else:
            painter.setPen(QColor("gray"))
            info_font = QFont()
            info_font.setPointSize(9)
            painter.setFont(info_font)

            painter.drawText(
                12,
                int(center_y + radius + 35),
                width - 24,
                40,
                Qt.AlignCenter,
                "No active tree target"
            )

        # Heading status text
        status_font = QFont()
        status_font.setPointSize(8)
        status_font.setBold(True)
        painter.setFont(status_font)

        if self.heading_status_text == "Heading not good enough":
            painter.setPen(QColor("orange"))
        else:
            painter.setPen(QColor("white"))

        painter.drawText(
            12,
            height - 28,
            width - 24,
            20,
            Qt.AlignCenter,
            self.heading_status_text
        )

    def _draw_arrow(self, painter, center, angle_deg, length, color):

        #Draws an arrow where: 0 degrees = up 270 degrees = left
        angle_rad = math.radians(angle_deg - 90)

        half_length = length / 2

        tip = QPointF(
            center.x() + math.cos(angle_rad) * half_length,
            center.y() + math.sin(angle_rad) * half_length
        )

        tail = QPointF(
            center.x() - math.cos(angle_rad) * half_length,
            center.y() - math.sin(angle_rad) * half_length
        )

        painter.setPen(QPen(color, 4, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(tail, tip)

        # Arrow head
        head_size = 14
        left_angle = angle_rad + math.radians(150)
        right_angle = angle_rad - math.radians(150)

        left = QPointF(
            tip.x() + math.cos(left_angle) * head_size,
            tip.y() + math.sin(left_angle) * head_size
        )

        right = QPointF(
            tip.x() + math.cos(right_angle) * head_size,
            tip.y() + math.sin(right_angle) * head_size
        )

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(color, 1))

        arrow_head = QPolygonF([tip, left, right])
        painter.drawPolygon(arrow_head)

    def set_heading_status(self, text):
        self.heading_status_text = text
        self.update()
