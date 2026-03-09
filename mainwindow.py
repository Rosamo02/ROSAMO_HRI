# mainwindow.py
# This Python file uses the following encoding: utf-8
import os

import sys
import threading
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QKeyEvent, QPixmap
from PySide6.QtCore import Qt, QTimer, QTime
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings

from ui_form import Ui_MainWindow
from gst_video_widget import GstVideoWidget

from geometry_msgs.msg import Twist

# SDL2 for controller input
import sdl2
import sdl2.ext

from image_viewer import ImageViewer

from login_manager import LoginManager

from px4_msgs.msg import BatteryStatus

class BatteryNode(Node):
    def __init__(self, ui):
        super().__init__('battery_node')
        self.ui = ui

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.battery_sub = self.create_subscription(
            BatteryStatus,
            '/fmu/out/battery_status_v1',
            self.battery_callback,
            qos
        )


    def battery_callback(self, msg):
        percent = int(msg.remaining * 100)

        # Update the Qt label safely using Qt's thread
        self.ui.labelBattery.setText(f"Battery: {percent}%")

        # Optional color coding
        if percent > 50:
            self.ui.labelBattery.setStyleSheet("color: green;")
        elif percent > 20:
            self.ui.labelBattery.setStyleSheet("color: orange;")
        else:
            self.ui.labelBattery.setStyleSheet("color: red; font-weight: bold;")

class TeleopNode(Node):
    def __init__(self):
        super().__init__('qt_teleop')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def send_cmd(self, linear, angular):
        print(f"[CMD] Publishing: linear={linear:.2f}, angular={angular:.2f}")
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.pub.publish(msg)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        rclpy.init()

        #Statusbar
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status_bar)
        self.timer.start(1000)

        # Create login manager
        self.login = LoginManager()

        # Connect login button
        self.ui.Login_Button.clicked.connect(self.handle_login)

        #Hide the sidebar on startup
        self.ui.sidebarWidget.setVisible(False)

        #sidebar button mapping

        self.nav_map = {
            self.ui.Home_Button: self.ui.Home_pg,
            self.ui.Main_Button: self.ui.Main_pg,
            self.ui.Alarm_Button: self.ui.Alarm_pg,
            self.ui.Map_Button: self.ui.Map_pg,
            self.ui.Settings_Button: self.ui.Settings_pg
        }

        #Connect Sidebar buttons

        for button, page in self.nav_map.items():
            button.clicked.connect(lambda _, p=page, b=button: self.navigate(p, b))

        self.switch_page(self.ui.Login_pg)

        # Setup for video stream from depth camera
        self.ui.videoLabel.setText("Waiting for RealSense...")
        self.ui.videoLabel.setScaledContents(True)

        # Track keyboard state
        self.keys_down = {"space": False, "w": False, "a": False, "s": False, "d": False}

        # Teleop node
        self.teleop_node = TeleopNode()

        # Image viewer node (compressed RealSense)
        self.image_node = ImageViewer(
            topic="/apriltag/overlay/compressed"
        )
        self.image_node.new_frame.connect(self.update_image)

        #create battery node
        self.battery_node = BatteryNode(self.ui)
        # Start ROS executor thread with both nodes
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(self.teleop_node)
        self.executor.add_node(self.image_node)
        self.executor.add_node(self.battery_node)


        self.ros_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.ros_thread.start()

        # Teleop state
        self.linear = 0.0
        self.angular = 0.0

        # Video pipeline (GStreamer)
        pipeline = (
            'udpsrc port=5000 caps="application/x-rtp, media=video, encoding-name=H264, payload=96" ! '
            'rtph264depay ! h264parse ! avdec_h264 ! '
            'videoconvert ! video/x-raw,format=BGR ! '
            'appsink name=appsink emit-signals=true max-buffers=1 drop=true'
        )

        self.video = GstVideoWidget(pipeline)
        self.ui.videoLayout.addWidget(self.video)

        # Ensure window receives keyboard focus
        self.setFocusPolicy(Qt.StrongFocus)

        # Input mode
        self.current_mode = "keyboard"
        self.ui.toggleInputButton.clicked.connect(self.on_toggleInputButton_clicked)

        # SDL2 CONTROLLER SETUP
        print("\n[SDL2] Initializing controller system...")
        sdl2.SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)

        num_joy = sdl2.SDL_NumJoysticks()
        print(f"[SDL2] Joysticks detected: {num_joy}")

        self.controller = None
        for i in range(num_joy):
            if sdl2.SDL_IsGameController(i):
                self.controller = sdl2.SDL_GameControllerOpen(i)
                print("[SDL2] Controller connected:", sdl2.SDL_GameControllerName(self.controller))
                break

        if self.controller is None:
            print("No controller detected")

        self.rb_down = False

        # Start SDL2 polling thread
        print("Starting controller polling thread...")
        self.sdl_thread = threading.Thread(target=self.poll_controller, daemon=True)
        self.sdl_thread.start()

        #Initializing the map
        html_path = "/home/rodrigomoreira/Rosamo_3/map_assets/map.html"
        print("Loading:", html_path)

        settings = self.ui.mapView.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.ui.mapView.load(QUrl.fromLocalFile(html_path))

        #more debugging ( important to delete)

        def test_js():
            print("Running JS test...")
            self.ui.mapView.page().runJavaScript("centerOnRobot();")
            self.ui.mapView.page().runJavaScript("updateRobot(41.1580, -8.6295);")

        QTimer.singleShot(3000, test_js)

        #Debugging(delete later)
        print([name for name in dir(self.ui) if "Battery" in name])
        print(type(self.ui.mapView))
        print("Loading:", html_path)
        print("HTML path:", html_path)








    # MODE SWITCHING

    def on_toggleInputButton_clicked(self):
        if self.current_mode == "keyboard":
            self.current_mode = "controller"
            self.ui.toggleInputButton.setText("Use Keyboard")
            print("Switched to CONTROLLER mode")
        else:
            self.current_mode = "keyboard"
            self.ui.toggleInputButton.setText("Use Controller")
            print("Switched to KEYBOARD mode")

        # Reset motion when switching modes
        self.linear = 0.0
        self.angular = 0.0
        self.keys_down = {k: False for k in self.keys_down}
        self.update_cmd()

    # KEYBOARD TELEOP

    def update_cmd(self):
        self.teleop_node.send_cmd(self.linear, self.angular)

    def update_motion(self):
        if not self.keys_down["space"]:
            self.linear = 0.0
            self.angular = 0.0
        else:
            if self.keys_down["w"]:
                self.linear = 1.0
            elif self.keys_down["s"]:
                self.linear = -1.0
            else:
                self.linear = 0.0

            if self.keys_down["a"]:
                self.angular = 1.0
            elif self.keys_down["d"]:
                self.angular = -1.0
            else:
                self.angular = 0.0

        print(f"[KEYBOARD] linear={self.linear}, angular={self.angular}")
        self.update_cmd()

    def keyPressEvent(self, event: QKeyEvent):
        if self.current_mode != "keyboard":
            return

        key = event.text().lower()

        if event.key() == Qt.Key_Space:
            self.keys_down["space"] = True

        if key in self.keys_down:
            self.keys_down[key] = True

        self.update_motion()

    def keyReleaseEvent(self, event: QKeyEvent):
        if self.current_mode != "keyboard":
            return

        key = event.text().lower()

        if event.key() == Qt.Key_Space:
            self.keys_down["space"] = False

        if key in self.keys_down:
            self.keys_down[key] = False

        self.update_motion()

    # CONTROLLER TELEOP

    def poll_controller(self):
        event = sdl2.SDL_Event()

        while True:
            while sdl2.SDL_PollEvent(event):
                if event.type == sdl2.SDL_CONTROLLERAXISMOTION:
                    print("[SDL2] AXIS EVENT:", event.caxis.axis, event.caxis.value)
                    self.handle_axis(event.caxis)

                elif event.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
                    print("[SDL2] BUTTON DOWN:", event.cbutton.button)
                    self.handle_button(event.cbutton, True)

                elif event.type == sdl2.SDL_CONTROLLERBUTTONUP:
                    print("[SDL2] BUTTON UP:", event.cbutton.button)
                    self.handle_button(event.cbutton, False)

            sdl2.SDL_Delay(5)

    def handle_axis(self, axis_event):
        if self.current_mode != "controller":
            return

        value = axis_event.value / 32767.0

        # Dead-man switch not pressed -> stop immediately
        if not self.rb_down:
            self.linear = 0.0
            self.angular = 0.0
            self.update_cmd()
            return

        # Update motion based on axis
        if axis_event.axis == sdl2.SDL_CONTROLLER_AXIS_LEFTX:
            self.angular = -value
        elif axis_event.axis == sdl2.SDL_CONTROLLER_AXIS_LEFTY:
            self.linear = -value

        print(f"[CONTROLLER] linear={self.linear:.2f}, angular={self.angular:.2f}")

        # auto-repeat
        for _ in range(20):
            self.update_cmd()
            sdl2.SDL_Delay(1)

    def handle_button(self, button_event, pressed):
        if self.current_mode != "controller":
            return

        # RB dead-man switch
        if button_event.button == sdl2.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER:
            print("[RB] pressed:", pressed)
            self.rb_down = pressed

            if not pressed:
                self.linear = 0.0
                self.angular = 0.0
                self.update_cmd()

    # IMAGE HANDLING

    def update_image(self, qimg):
        self.ui.videoLabel.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        self.executor.shutdown()
        rclpy.shutdown()
        super().closeEvent(event)

    def switch_page(self, page):
        self.ui.stackedWidget.setCurrentWidget(page)

    def navigate(self, page, button):
        # Switch page
        self.ui.stackedWidget.setCurrentWidget(page)

        # Reset all button styles
        for btn in self.nav_map.keys():
            btn.setStyleSheet("""
                QPushButton {
                    background-color: none;
                    color: white;
                    border: none;
                    text-align: left;
                    padding: 8px;
                }
            """)

        # Highlight active button
        button.setStyleSheet("""
            QPushButton {
                background-color: #2d89ef;
                color: white;
                font-weight: bold;
                border: none;
                text-align: middle;
                padding: 8px;
            }
        """)


    def handle_login(self):
        username = self.ui.usernameField.text()
        password = self.ui.passwordField.text()

        if self.login.validate(username, password):
            self.ui.sidebarWidget.setVisible(True)
            print("Successful login")
        else:
            print("Failed login")

    def update_status_bar(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.ui.labelTime.setText(f"Time: {current_time}")

if __name__ == "__main__":
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--allow-file-access-from-files"
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
