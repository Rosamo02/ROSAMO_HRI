import sys
from PySide6.QtWidgets import QApplication
import rclpy
from rclpy.node import Node

def test_node(label):
    print(f"before rclpy.init: {label}")
    rclpy.init()
    print(f"after rclpy.init: {label}")
    n = Node("test_node")
    print(f"after Node: {label}")
    n.destroy_node()
    rclpy.shutdown()
    print(f"done: {label}")

print("before QApplication")
app = QApplication(sys.argv)
print("after QApplication")

test_node("baseline")

print("import alarm_manager")
import alarm_manager
test_node("after alarm_manager")

print("import alarm")
import alarm
test_node("after alarm")

print("import teleop_controller")
import teleop_controller
test_node("after teleop_controller")

print("import hmi_order_sender")
import hmi_order_sender
test_node("after hmi_order_sender")

print("import slammap_node")
import slammap_node
test_node("after slammap_node")

print("import ping_monitor")
import ping_monitor
test_node("after ping_monitor")

print("import local_process_manager")
import local_process_manager
test_node("after local_process_manager")

print("import ui_form")
import ui_form
test_node("after ui_form")

print("import teleop_node")
import teleop_node
test_node("after teleop_node")

print("import data_reader_node")
import data_reader_node
test_node("after data_reader_node")

print("import image_viewer")
import image_viewer
test_node("after image_viewer")

print("import sdl_controller")
import sdl_controller
test_node("after sdl_controller")

print("import gst_video_widget")
import gst_video_widget
test_node("after gst_video_widget")

print("import login_manager")
import login_manager
test_node("after login_manager")

print("import map_view")
import map_view
test_node("after map_view")
