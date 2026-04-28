# mainwindow.py
import os
import sys
import threading

import rclpy
from rclpy.executors import SingleThreadedExecutor

from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtGui import QKeyEvent, QPixmap, QTransform
from PySide6.QtCore import Qt, QTimer, QTime

from alarm_manager import AlarmManager
from alarm import AlarmSeverity
from teleop_controller import TeleopController
from hmi_order_sender import HMICommandClient
from slammap_node import MapNode
from ping_monitor import PingMonitor
from local_process_manager import LocalProcessManager
from ui_form import Ui_MainWindow
from teleop_node import TeleopNode
from data_reader_node import BatteryNode
from image_viewer import ImageViewer
from sdl_controller import SDLController
from login_manager import LoginManager
from map_view import setup_map
from gps_position_node import GPSPositionNode

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # UI setup
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        print("checkpoint 1")
        self.ui.passwordField.setEchoMode(QLineEdit.EchoMode.Password)

        # ROS init first
        print("checkpoint 2")
        rclpy.init()
        print("checkpoint 3")

        # Basic UI / managers that should be safe
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status_bar)
        self.timer.start(1000)
        print("checkpoint 4")

        self.login = LoginManager()
        self.ui.Login_Button.clicked.connect(self.handle_login)
        print("checkpoint 5")

        self.local_process_manager = LocalProcessManager()
        self.ui.localprocessButton.clicked.connect(self.toggle_hmi_receiver)
        self.ui.localprocessLabel.setText("HMI Receiver OFF")
        print("checkpoint 6")

        self.ui.sidebarWidget.setVisible(False)
        print("checkpoint 7")

        self.nav_map = {
            self.ui.Home_Button: self.ui.Home_pg,
            self.ui.Main_Button: self.ui.Main_pg,
            self.ui.Alarm_Button: self.ui.Alarm_pg,
            self.ui.Map_Button: self.ui.Map_pg,
            self.ui.Settings_Button: self.ui.Settings_pg,
            self.ui.Main_2_Button: self.ui.Main_2_pg
        }
        print("checkpoint 8")

        for button, page in self.nav_map.items():
            button.clicked.connect(lambda _, p=page, b=button: self.navigate(p, b))
        print("checkpoint 9")

        self.switch_page(self.ui.Login_pg)
        print("checkpoint 10")

        self.ui.videoLabel.setText("Waiting for RealSense...")
        self.ui.videoLabel.setScaledContents(True)
        print("checkpoint 11")

        # ROS nodes - create ONCE
        print("before TeleopNode")
        self.teleop_node = TeleopNode()
        print("after TeleopNode")

        print("before BatteryNode")
        self.battery_node = BatteryNode()
        print("after BatteryNode")

        print("before TeleopController")
        self.teleop_controller = TeleopController(self.teleop_node)
        print("after TeleopController")

        print("before ImageViewer")
        self.image_node = ImageViewer("/apriltag/overlay/compressed")
        print("after ImageViewer")
        self.image_node.new_frame.connect(self.update_image)

        print("before HMICommandClient")
        self.command_client = HMICommandClient(
            self.teleop_node,
            self.ui.screenToggler,
            self.ui.maincameraToggler
        )
        print("after HMICommandClient")

        print("before MapNode")
        self.map_node = MapNode()
        print("after MapNode")
        self.map_node.bridge.map_updated.connect(self.update_map_view)
        self.map_node.bridge.map_image_updated.connect(self.update_map_image_view)

        print("before GPSPositionNode")
        self.gps_position_node = GPSPositionNode()
        print("after GPSPositionNode")
        self.gps_position_node.signals.gps_updated.connect(self.update_robot_gps_on_map)
        self.has_centered_on_robot = False
        print("checkpoint 12")

        # ROS executor
        self.executor = SingleThreadedExecutor()
        self.executor.add_node(self.teleop_node)
        self.executor.add_node(self.battery_node)
        self.executor.add_node(self.image_node)
        self.executor.add_node(self.map_node)
        self.executor.add_node(self.gps_position_node)
        print("checkpoint 13")

        self.ros_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.ros_thread.start()
        print("checkpoint 14")

        # Connect controls
        self.ui.offboardButton.clicked.connect(self.command_client.start_stop_offboard)
        self.ui.armButton.clicked.connect(self.command_client.start_stop_arming)
        print("checkpoint 15")

        self.ui.screenToggler.clicked.connect(self.command_client.start_stop_back_camera)
        self.ui.mapToggler.clicked.connect(self.command_client.start_stop_Lidar_Map_msg)
        self.ui.routerToggler.clicked.connect(self.command_client.start_stop_ros2router_msg)
        self.ui.maincameraToggler.clicked.connect(self.command_client.start_stop_front_camera)

        self.current_mode = "keyboard"
        self.ui.toggleInputButton.clicked.connect(self.on_toggleInputButton_clicked)
        self.ui.labelControlMode.setText(f"ControlMode: {self.current_mode}")
        print("checkpoint 16")

        self.ui.powerSlider.valueChanged.connect(self.update_slider_scale)
        print("checkpoint 17")

        self.sdl = SDLController(self)
        print("checkpoint 18")

        setup_map(self.ui.mapView)
        self.map_ready = False
        self.ui.mapView.loadFinished.connect(self.on_map_loaded)

        print("checkpoint 19")
        self.ui.treeInput.setPlaceholderText("Tree position: lat, lon")
        self.ui.addTreeButton.clicked.connect(self.add_tree_marker_from_input)
        self.ui.treeInput.returnPressed.connect(self.add_tree_marker_from_input)

        # Alarm setup
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["Time", "Severity", "Code", "Message"]
        )
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        print("checkpoint 20")

        self.alarm_manager = AlarmManager()
        self.alarm_manager.alarmRaised.connect(self.add_alarm_to_table)
        self.alarm_manager.alarmCleared.connect(self.remove_alarm_from_table)
        print("checkpoint 21")

        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.toggle_alarm_icon)
        self.blink_state = False
        print("checkpoint 22")

        self.ui.ackButton.clicked.connect(self.acknowledge_alarms)
        self.alarm_manager.unacknowledgedChanged.connect(self.handle_unacknowledged_change)
        print("checkpoint 23")

        self.alarm_manager.raise_alarm(
            "Initial Alarm",
            "This is the initial alarm that pops off when the HMI is started",
            AlarmSeverity.WARNING
        )
        print("checkpoint 24")

        # Battery node signals
        self.battery_node.signals.battery_updated.connect(self.update_battery_ui)
        self.battery_node.signals.time_left_updated.connect(self.update_time_left_ui)
        self.battery_node.signals.arming_updated.connect(self.update_arming_ui)
        self.battery_node.signals.offboard_updated.connect(self.update_offboard_ui)
        self.battery_node.signals.connection_updated.connect(self.update_connection_ui)
        self.battery_node.signals.odom_updated.connect(self.update_velocimeter_ui)
        self.gps_position_node.signals.gps_label_message.connect(self.update_gps_label)
        print("checkpoint 25")

        # Ping monitor
        self.ui.labelPing.setText("Ping: -- ms")
        self.ping_monitor = PingMonitor("Robot", 2000, self)
        self.ping_monitor.ping_updated.connect(self.update_ping_ui)
        self.ping_monitor.ping_failed.connect(self.handle_ping_failure)
        self.ping_monitor.start()
        print("checkpoint 26")

        # Delay GStreamer setup until Qt event loop starts
        QTimer.singleShot(0, self.setup_gstreamer)

        print("MainWindow initialized successfully.")



    def setup_gstreamer(self):

        import gi
        gi.require_version("Gst", "1.0")
        from gi.repository import Gst
        from gst_video_widget import GstVideoWidget

        print("before Gst.init")
        Gst.init(None)
        print("after Gst.init")

        pipeline = (
            'udpsrc address=:: port=5000 '
            'caps="application/x-rtp,media=video,encoding-name=H264,payload=96,clock-rate=90000" ! '
            'rtpjitterbuffer latency=50 drop-on-latency=true ! '
            'rtph264depay ! h264parse ! avdec_h264 ! '
            'videoconvert ! video/x-raw,format=RGB ! '
            'appsink name=appsink emit-signals=true max-buffers=1 drop=true sync=false'
        )

        print("before GstVideoWidget")
        self.video = GstVideoWidget(pipeline)
        self.ui.videoLayout.addWidget(self.video)
        print("after GstVideoWidget")

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
            self.navigate(self.ui.Home_pg, self.ui.Home_Button)#Changes from the login screen to the Home screen upon sucessfull login
            print("Successful login")
        else:
            print("Failed login")

    def update_battery_ui(self, percent, current):
        self.ui.labelBattery.setText(f"Battery: {percent}% Current: {current:.2f}A")
        # Color logic
        if percent > 50:
            style = "color: green;"
        elif percent > 20:
            style = "color: yellow;"
        else:
            style = "color: red;"
        self.ui.labelBattery.setStyleSheet(style)

    def update_time_left_ui(self, time_left):
        self.ui.labelTimeRemaingBattery.setText(f"Time left: {time_left}")

    def update_velocimeter_ui(self, odom_text):
        self.ui.linearspeedLabel.setText(odom_text)

    def update_arming_ui(self, status_text):
        self.ui.armLabel.setText(status_text)
        if status_text == "Armed":
            color = "green"
        elif "No Data" in status_text or "Stale" in status_text:
            color = "orange"
        else:
            color = "gray"
        self.ui.armLabel.setStyleSheet(f"color: {color}; font-weight: bold;")

    def update_offboard_ui(self, status_text):
        self.ui.offboardLabel.setText(status_text)
        if status_text == "Offboard: On":
            color = "#2d89ef"
        elif status_text == "Offboard: Requested":
            color = "orange"
        elif "No Data" in status_text or "Stale" in status_text:
            color = "orange"
        else:
            color = "gray"
        self.ui.offboardLabel.setStyleSheet(f"color: {color}; font-weight: bold;")

    def update_connection_ui(self, status_text):
        self.ui.routerLabel.setText(status_text)
        if status_text == "Connection: P2P":
            color = "green"
        elif status_text == "Connection: Tunneled":
            color = "orange"
        else:
            color = "red"
        self.ui.routerLabel.setStyleSheet(
            f"color: {color}; font-weight: bold;"
        )

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

    def update_map_image_view(self, qimg):
        pix = QPixmap.fromImage(qimg)

        pix = pix.scaled(
            self.ui.mapImageView.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.ui.mapImageView.setPixmap(pix)

        #This 2 are responsible for sending the offboard and arming commands through the terminal.
        #Maybe not ideal solution considering the screen "freezes" while its being processed
    #def offboard_command(self):
    #    print("Offboard command via terminal...")
    #    cmd = 'ros2 service call /px4/offboard std_srvs/srv/SetBool "{data: true}"'
    #    exit_code = os.system(cmd)
    #    if exit_code == 0:
    #        print("Command for offboard executed successfully in terminal.")
    #    else:
    #        print(f"Command for offboard failed with exit code: {exit_code}")

    #def arming_command(self):
    #    print("Arming command via terminal...")
    #    cmd = 'ros2 service call /px4/arm std_srvs/srv/SetBool "{data: true}"'
    #    exit_code = os.system(cmd)
    #    if exit_code == 0:
    #            print("Command for arming executed successfully in terminal.")
    #    else:
    #            print(f"Command for arming failed with exit code: {exit_code}")

    # Close Event

    def update_ping_ui(self, ping_ms):
        self.ui.labelPing.setText(f"Ping: {ping_ms:.1f} ms")

        if ping_ms < 80:
            color = "green"
        elif ping_ms < 150:
            color = "orange"
        else:
            color = "red"

        self.ui.labelPing.setStyleSheet(f"color: {color}; font-weight: bold;")


    def handle_ping_failure(self, reason):
        self.ui.labelPing.setText("Ping: timeout")
        self.ui.labelPing.setStyleSheet("color: red; font-weight: bold;")
        print(f"Ping failed: {reason}")

    def toggle_hmi_receiver(self):
        result = self.local_process_manager.toggle_hmi_receiver()

        if result == "started":
            self.ui.localprocessButton.setText("Stop HMI \nReceiver")
            self.ui.localprocessLabel.setText("HMI Receiver ON")
        elif result == "stopped":
            self.ui.localprocessButton.setText("Start HMI \nReceiver")
            self.ui.localprocessLabel.setText("HMI Receiver OFF")
        else:
            print("Failed to toggle hmi_command_receiver.py")

    def add_tree_marker_from_input(self):
        text = self.ui.treeInput.text().strip()

        try:
            lat_str, lon_str = text.split(",")
            lat = float(lat_str.strip())
            lon = float(lon_str.strip())
        except ValueError:
            print("Invalid tree position. Use format: latitude, longitude")
            return

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            print("Invalid GPS coordinates.")
            return

        js = f"addTreeMarker({lat}, {lon});"
        self.ui.mapView.page().runJavaScript(js)

        self.ui.treeInput.clear()
        print(f"Added tree marker at lat={lat}, lon={lon}")

    def on_map_loaded(self, ok):
        self.map_ready = ok
        print(f"Map loaded: {ok}")

    def update_robot_gps_on_map(self, lat, lon):
        print(f"Updating robot marker on map: lat={lat}, lon={lon}")

        self.ui.mapView.page().runJavaScript(
            f"updateRobot({lat}, {lon});"
        )

        if not self.has_centered_on_robot:
            self.ui.mapView.page().runJavaScript(
                f"map.setView([{lat}, {lon}], 18);"
            )
            self.has_centered_on_robot = True

    def update_gps_label(self, text):
        self.ui.gpsLabel.setText(text)


    def closeEvent(self, event):
        if hasattr(self, "video") and self.video is not None:
            try:
                from gi.repository import Gst
                self.video.pipeline.set_state(Gst.State.NULL)
            except Exception as e:
                print(f"Error stopping GStreamer pipeline: {e}")

        if hasattr(self, "local_process_manager"):
            self.local_process_manager.stop_hmi_receiver()

        if hasattr(self, "executor"):
            self.executor.shutdown()

        rclpy.shutdown()
        super().closeEvent(event)
