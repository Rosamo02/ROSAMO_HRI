# mainwindow.py
import os
import sys
import threading
import rclpy
from rclpy.executors import SingleThreadedExecutor
from alarm_manager import AlarmManager
from alarm import AlarmSeverity
from teleop_controller import TeleopController
from hmi_order_sender import HMICommandClient
from slammap_node import MapNode


from PySide6.QtWidgets import QMainWindow,QTableWidgetItem

from PySide6.QtGui import QKeyEvent, QPixmap, QTransform
from PySide6.QtCore import Qt, QTimer, QTime

from ui_form import Ui_MainWindow
from teleop_node import TeleopNode
from data_reader_node import BatteryNode
from image_viewer import ImageViewer
from sdl_controller import SDLController
from gst_video_widget import GstVideoWidget
from login_manager import LoginManager
from map_view import setup_map


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # UI setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ROS init
        rclpy.init()

        # Status bar timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status_bar)
        self.timer.start(1000)

        # Login manager
        self.login = LoginManager()
        self.ui.Login_Button.clicked.connect(self.handle_login)

        # Hide sidebar initially
        self.ui.sidebarWidget.setVisible(False)

        # Sidebar navigation
        self.nav_map = {
            self.ui.Home_Button: self.ui.Home_pg,
            self.ui.Main_Button: self.ui.Main_pg,
            self.ui.Alarm_Button: self.ui.Alarm_pg,
            self.ui.Map_Button: self.ui.Map_pg,
            self.ui.Settings_Button: self.ui.Settings_pg
        }

        #Connect Sidebar buttons with their respective page
        for button, page in self.nav_map.items():
            button.clicked.connect(lambda _, p=page, b=button: self.navigate(p, b))

        #Set initial page as the login page
        self.switch_page(self.ui.Login_pg)

        # Video label
        self.ui.videoLabel.setText("Waiting for RealSense...")
        self.ui.videoLabel.setScaledContents(True)

        # ROS nodes
        self.teleop_node = TeleopNode()
        self.battery_node = BatteryNode()
        self.teleop_controller = TeleopController(self.teleop_node)
        self.image_node = ImageViewer("/apriltag/overlay/compressed")
        self.image_node.new_frame.connect(self.update_image)
        self.command_client = HMICommandClient(self.teleop_node)
        self.map_node = MapNode()
        self.map_node.bridge.map_updated.connect(self.update_map_view)

        # ROS executor
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(self.teleop_node)
        self.executor.add_node(self.battery_node)
        self.executor.add_node(self.image_node)
        self.executor.add_node(self.map_node)


        self.ros_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.ros_thread.start()

        # GStreamer video widget
        pipeline = (
            'udpsrc port=5000 caps="application/x-rtp, media=video, encoding-name=H264, payload=96" ! '
            'rtph264depay ! h264parse ! avdec_h264 ! '
            'videoconvert ! video/x-raw,format=BGR ! '
            'appsink name=appsink emit-signals=true max-buffers=1 drop=true'
        )
        self.video = GstVideoWidget(pipeline)
        self.ui.videoLayout.addWidget(self.video)

        #Connect Arming and Offboard

        self.ui.armButton.clicked.connect(self.arming_command)
        self.ui.offboardButton.clicked.connect(self.offboard_command)

        #Connect Togglers (Using debug msg right now)
        self.ui.screenToggler.clicked.connect(self.command_client.start_stop_debug_msg)
        self.ui.mapToggler.clicked.connect(self.command_client.start_stop_Lidar_Map_msg)

        # Input mode switching
        self.current_mode = "keyboard"
        self.ui.toggleInputButton.clicked.connect(self.on_toggleInputButton_clicked)

        #StatusBar ControlMode
        self.ui.labelControlMode.setText(f"ControlMode: {self.current_mode}")


        #SpeedSlider
        self.ui.powerSlider.valueChanged.connect(self.update_slider_scale)

        # SDL controller
        self.sdl = SDLController(self)

        # Map setup
        setup_map(self.ui.mapView)


        #Alarm Setup
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["Time", "Severity", "Code", "Message"]
        )
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)


        #Alarm manager
        self.alarm_manager = AlarmManager()

        # Connect signals
        self.alarm_manager.alarmRaised.connect(self.add_alarm_to_table)
        self.alarm_manager.alarmCleared.connect(self.remove_alarm_from_table)

        #BlinkerAlarm

        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.toggle_alarm_icon)
        self.blink_state = False

        #connect ack button

        self.ui.ackButton.clicked.connect(self.acknowledge_alarms)

        self.alarm_manager.unacknowledgedChanged.connect(self.handle_unacknowledged_change)

        #Debugging
        self.alarm_manager.raise_alarm(
            "TEST_1",
            "This is a test alarm",
            AlarmSeverity.WARNING
        )

        # Connect the signal to a local handler
        self.battery_node.signals.battery_updated.connect(self.update_battery_ui)
        self.battery_node.signals.arming_updated.connect(self.update_arming_ui)
        self.battery_node.signals.offboard_updated.connect(self.update_offboard_ui)

        print("MainWindow initialized successfully.")

    # UI Navigation
    def switch_page(self, page):
        self.ui.stackedWidget.setCurrentWidget(page)

    def navigate(self, page, button):
        self.ui.stackedWidget.setCurrentWidget(page)

        # Reset styles
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

    # Login
    def handle_login(self):
        username = self.ui.usernameField.text()
        password = self.ui.passwordField.text()

        if self.login.validate(username, password):
            self.ui.sidebarWidget.setVisible(True)
            print("Successful login")
        else:
            print("Failed login")

    def update_battery_ui(self, percent):
        self.ui.labelBattery.setText(f"Battery: {percent}%")
        # Color logic
        if percent > 50:
            style = "color: green;"
        elif percent > 20:
            style = "color: yellow;"
        else:
            style = "color: red;"
        self.ui.labelBattery.setStyleSheet(style)

    def update_arming_ui(self, status_text):
        self.ui.armLabel.setText(status_text)
        color = "red" if status_text == "Armed" else "gray"
        self.ui.armLabel.setStyleSheet(f"color: {color}; font-weight: bold;")

    def update_offboard_ui(self, status_text):
        self.ui.offboardLabel.setText(status_text)
        color = "#2d89ef" if "On" in status_text else "gray"
        self.ui.offboardLabel.setStyleSheet(f"color: {color};")

    # Status Bar
    def update_status_bar(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.ui.labelTime.setText(f"Time: {current_time}")

    def keyPressEvent(self, event: QKeyEvent):
        if self.current_mode != "keyboard":
            return

        key = event.text().lower()
        if event.key() == Qt.Key_Space:
            key = " "

        self.teleop_controller.handle_key_press(key)


    def keyReleaseEvent(self, event: QKeyEvent):
        if self.current_mode != "keyboard":
            return

        key = event.text().lower()
        if event.key() == Qt.Key_Space:
            key = " "

        self.teleop_controller.handle_key_release(key)

    def update_slider_scale(self, value):
        scale = value / 100.0
        self.teleop_controller.speed_scale = scale
        print(f"The scale is set to {scale}")

    # Controller Mode Switching
    def on_toggleInputButton_clicked(self):

        self.alarm_manager.raise_alarm(
            "TEST_2",
            "This is a test alarm_2",
            AlarmSeverity.WARNING
        )
        if self.current_mode == "keyboard":
            self.current_mode = "controller"
            self.ui.toggleInputButton.setText("Use Keyboard")
            print("Switched to CONTROLLER mode")
        else:
            self.current_mode = "keyboard"
            self.ui.toggleInputButton.setText("Use Controller")
            print("Switched to KEYBOARD mode")

        #Change Status Bar
        self.ui.labelControlMode.setText(f"ControlMode: {self.current_mode}")

        self.teleop_controller.keys_down = {k: False for k in self.teleop_controller.keys_down}
        self.teleop_controller.linear = 0.0
        self.teleop_controller.angular = 0.0
        self.teleop_controller.send_cmd()


    # Image Update
    def update_image(self, qimg):
        self.ui.videoLabel.setPixmap(QPixmap.fromImage(qimg))

    def add_alarm_to_table(self, alarm):
        table = self.ui.tableWidget
        row = table.rowCount()
        table.insertRow(row)

        table.setItem(row, 0, QTableWidgetItem(alarm.timestamp.strftime("%Y-%m-%d %H:%M:%S")))
        table.setItem(row, 1, QTableWidgetItem(alarm.severity.name))
        table.setItem(row, 2, QTableWidgetItem(alarm.code))
        table.setItem(row, 3, QTableWidgetItem(alarm.message))

    def remove_alarm_from_table(self, code):
        table = self.ui.tableWidget
        for row in range(table.rowCount()):
                if table.item(row, 2).text() == code:
                    table.removeRow(row)
                    break

    def handle_unacknowledged_change(self, has_unack):
        if has_unack:
            self.blink_timer.start(500)  # blink every 0.5 seconds
        else:
            self.blink_timer.stop()
            self.blink_state = False
            pix = QPixmap("icons/greyicon.png").scaled(
                32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.ui.alarmIcon.setPixmap(pix)

    def toggle_alarm_icon(self):
        self.blink_state = not self.blink_state
        icon = "icons/red_icon.png" if self.blink_state else "icons/greyicon.png"

        pix = QPixmap(icon).scaled(
            32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.ui.alarmIcon.setPixmap(pix)

    def acknowledge_alarms(self):
        self.alarm_manager.acknowledge()

    def update_map_view(self, qimg):

        # Rotate and flip to match ROS orientation
        rotated = qimg.transformed(QTransform().rotate(-90))
        final_img = rotated.mirrored(False, True)

        # Scale while keeping aspect ratio
        pix = QPixmap.fromImage(final_img)
        pix = pix.scaled(
            self.ui.slamMapView.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.ui.slamMapView.setPixmap(pix)

    def offboard_command(self):
        print("Offboard command via terminal...")
        # This is exactly what you type in the terminal
        cmd = 'ros2 service call /px4/offboard std_srvs/srv/SetBool "{data: true}"'

        exit_code = os.system(cmd)

        if exit_code == 0:
            print("Command for offboard executed successfully in terminal.")
        else:
            print(f"Command for offboard failed with exit code: {exit_code}")

    def arming_command(self):
        print("Arming command via terminal...")
        # This is exactly what you type in the terminal
        cmd = 'ros2 service call /px4/arm std_srvs/srv/SetBool "{data: true}"'

        exit_code = os.system(cmd)

        if exit_code == 0:
                print("Command for arming executed successfully in terminal.")
        else:
                print(f"Command for arming failed with exit code: {exit_code}")


    # Close Event
    def closeEvent(self, event):
        self.executor.shutdown()
        rclpy.shutdown()
        super().closeEvent(event)
