import traceback

print("importing rclpy")
import rclpy
from rclpy.node import Node
print("rclpy ok")

def test_node(label):
    print(f"test node start: {label}")
    rclpy.init()
    n = Node("test_node")
    print(f"test node ok: {label}")
    n.destroy_node()
    rclpy.shutdown()

test_node("baseline")

print("importing PySide6.QtWidgets")
from PySide6.QtWidgets import QApplication
print("PySide6 ok")
test_node("after PySide6")

print("importing gi/Gst")
import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst
print("Gst ok")
test_node("after Gst")

print("importing sdl2")
import sdl2
print("sdl2 ok")
test_node("after sdl2")

print("importing cv2")
import cv2
print("cv2 ok")
test_node("after cv2")

print("importing cv_bridge")
import cv_bridge
print("cv_bridge ok")
test_node("after cv_bridge")
