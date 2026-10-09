# ROSAMO HRI — Script and Component Guide

This document describes the purpose of the main files in the [ROSAMO_HRI](https://github.com/Rosamo02/ROSAMO_HRI) repository. The project is a Python/PySide6 human–robot interface (HRI) for monitoring and teleoperating a ROS 2/PX4 mobile robot. It combines manual control, robot status displays, camera streams, maps, and commands for enabling supporting robot processes.

> **Scope:** Descriptions are based on the public `main` branch as viewed on 9 October 2026 and the additional script versions discussed during documentation. Some scripts are supporting utilities, placeholders, or build assets rather than components executed on every run. See individual files for current parameter values and detailed implementations.

## 1. Application and interface

| File | Purpose |
| --- | --- |
| [`main.py`](main.py) | Application entry point. Starts the Qt application and main interface. |
| [`mainwindow.py`](mainwindow.py) | Central HMI controller. Connects Qt buttons, displays and navigation with robot commands, ROS 2 data, video widgets, and the other application components. |
| [`login_manager.py`](login_manager.py) | Handles login-related interface logic and access to HMI functionality. |
| [`alarm.py`](alarm.py) | Defines the data representation used for alarms. |
| [`alarm_manager.py`](alarm_manager.py) | Manages the alarms maintained and displayed by the HMI. |
| [`alarm_page.py`](alarm_page.py) | Provides the interface logic for viewing alarms. |
| [`compass_widget.py`](compass_widget.py) | Custom Qt widget for drawing and updating the heading/compass display. |
| [`form.ui`](form.ui) | Qt Designer layout describing the interface's widgets and pages. |
| [`ui_form.py`](ui_form.py) | Python representation of the Qt Designer interface, used to construct the widgets in the application. |

## 2. Teleoperation and controller input

| File | Purpose |
| --- | --- |
| [`teleop_controller.py`](teleop_controller.py) | Maintains the operator's requested movement and tool values and provides the interface for sending teleoperation commands. |
| [`teleop_node.py`](teleop_node.py) | ROS 2 teleoperation communication component responsible for publishing control commands, including velocity commands, to the robot. |
| [`sdl_controller.py`](sdl_controller.py) | Reads SDL2 gamepad axes and buttons in a polling thread. Maps left-stick motion to linear/steering commands and shoulder/trigger inputs to tool control; publishes commands at **20 Hz** while in controller mode. The right shoulder button is used as a deadman switch. |

### Gamepad controls

| Input | Action |
| --- | --- |
| Left stick, vertical | Forward/reverse movement |
| Left stick, horizontal | Steering |
| Right shoulder (RB) | Deadman switch: releasing it resets and sends zero movement/tool commands |
| Left shoulder (LB), with RB held | Forward tool command |
| Left trigger (LT), with RB held | Reverse tool command |

> **Safety note:** In the currently discussed SDL controller implementation, mode changes and physical controller disconnections are not fully handled as automatic stop events. Robot-side command timeouts and independent safety interlocks remain essential.

## 3. ROS 2 commands and robot status

| File | Purpose |
| --- | --- |
| [`hmi_order_sender.py`](hmi_order_sender.py) | Implements `HMICommandClient`, which publishes start/stop requests for camera streams, LiDAR, mapping, RTK, arm/offboard control and other robot subsystems. Also provides safety stop/reset topic publishers. |
| [`hmi_command_receiver.py`](hmi_command_receiver.py) | Listens for string commands on `/hmi/command` and launches or stops associated local processes (for example mapping, debug utilities and the ROS 2 router). |
| [`local_process_manager.py`](local_process_manager.py) | Helper for managing processes started on the HMI computer. |
| [`data_reader_node.py`](data_reader_node.py) | Robot-status ROS 2 node (named `BatteryNode` in code). Reads LiTime battery data, PX4 arming/offboard state, odometry and pole distance, estimates remaining battery time, monitors stale status and queries Husarnet connection information. Forwards data to Qt through signals. |
| [`heading_node.py`](heading_node.py) | Subscribes to PX4 local-position heading information, validates it and emits heading updates to the GUI. |
| [`gps_position_node.py`](gps_position_node.py) | Reads PX4 GPS position and fix quality. Validates coordinates, reports GPS/RTK fix status and emits latitude/longitude updates through Qt signals. |
| [`rosout_node.py`](rosout_node.py) | Subscribes to `/rosout`, formats ROS 2 log severity/source/message text and emits the result for presentation in the GUI. |
| [`ping_monitor.py`](ping_monitor.py) | Uses a Qt timer and a nonblocking `QProcess` running Linux `ping` to measure ICMP round-trip time to a configured host. Emits success or failure signals to the interface. |

### Selected ROS 2 topics

This table gives examples of the interfaces used by the HMI; it is **not** an exhaustive topic inventory.

| Topic | Role |
| --- | --- |
| `/cmd_vel` | Velocity command output for teleoperation |
| `/litime_bms/state` | Battery monitoring |
| `/fmu/out/vehicle_status_v1` | PX4 arm/offboard status |
| `/fmu/out/vehicle_odometry` | Robot speed/odometry data |
| `/fmu/out/vehicle_gps_position` | GPS coordinates and fix quality |
| `/fmu/out/vehicle_local_position_v1` | Heading information |
| `/pole_distance` | Detected pole/tree distance |
| `/rosout` | ROS 2 log messages |
| `/hmi/command` | Local process-control strings |
| `/start_offboard`, `/stop_offboard` | Requests to change offboard control |
| `/start_arming`, `/stop_arming` | Requests to arm/disarm |
| `/safety/stop`, `/safety/reset` | Safety stop/reset requests |

## 4. Video and camera display

| File | Purpose |
| --- | --- |
| [`gstream_setup.py`](gstream_setup.py) | Creates and attaches GStreamer-based camera views to the main window. Defines the receiving pipelines for primary/secondary, standard/low-quality H.264-over-RTP UDP streams and configures toolpath overlays. |
| [`gst_video_widget.py`](gst_video_widget.py) | Qt widget that receives GStreamer frames through an `appsink`, converts them to Qt images and draws them in the HMI, with optional toolpath graphics. |
| [`image_viewer.py`](image_viewer.py) | ROS 2 image-display helper for camera/image topic data. |

The current GStreamer setup uses UDP ports **5000** (primary), **5002** (primary low quality), **5001** (secondary), and **5003** (secondary low quality). These are receiver-side settings and must match the sender configuration.

## 5. Maps, navigation and localization

| File | Purpose |
| --- | --- |
| [`map_view.py`](map_view.py) | Configures a Qt WebEngine map view: enables JavaScript and local/remote resource access, handles geolocation permissions and loads the HTML map from `map_assets/map.html`. |
| [`slammap_node.py`](slammap_node.py) | ROS 2 mapping-related component that supports displaying map data in the interface. |
| [`pathfinder.py`](pathfinder.py) | Geographic route-planning utility. Calculates Haversine distances and bearings between GPS coordinates and finds the shortest visit order by evaluating permutations of target positions. Suitable for small target sets because exhaustive permutation search grows factorially. |
| [`map_assets/`](map_assets/) | HTML, JavaScript and other static assets used by the interactive web-based map. |

**Portability:** Map HTML paths should be resolved relative to `map_view.py`, rather than referring to a specific Linux home directory. This lets another developer clone the repository into a different location.

## 6. Development, packaging and auxiliary files

| File | Purpose |
| --- | --- |
| [`node_launcher.py`](node_launcher.py) | Placeholder/experimental ROS node-launching code; not a complete standalone application component in the inspected version. |
| [`battery_monitor.py`](battery_monitor.py) | Empty/placeholder script in the inspected repository version; battery functionality is implemented in `data_reader_node.py`. |
| [`teleop_qt.py`](teleop_qt.py) | Empty/placeholder script in the inspected repository version. |
| [`test_imports_ros.py`](test_imports_ros.py) | Development script for checking whether the required ROS/Python modules can be imported. |
| [`test_module_isolation.py`](test_module_isolation.py) | Development diagnostic script for checking module loading/isolation. |
| [`run_qtcreator.sh`](run_qtcreator.sh) | Shell utility for launching the project/development tooling with the intended environment. |
| [`requirements.txt`](requirements.txt) | Python dependency declarations. |
| [`pyproject.toml`](pyproject.toml) | Python project/build configuration. |
| [`main.spec`](main.spec) | PyInstaller build specification used to package the GUI. |
| [`dist/`](dist/) | Build/distribution outputs, not application source code. |
| [`icons/`](icons/) | Graphical resources used by the interface. |
| [`INSTALL.md`](INSTALL.md) | Installation and setup instructions. |
| [`.gitignore`](.gitignore) | Files and directories excluded from Git version control. |

## 7. How the components fit together

```text
Operator
   |
   +--> PySide6 interface (main.py, mainwindow.py, form.ui/ui_form.py)
   |        |
   |        +--> Keyboard/gamepad input (teleop_controller.py, sdl_controller.py)
   |        |         +--> teleop_node.py --> ROS 2 commands --> robot
   |        |
   |        +--> Buttons --> hmi_order_sender.py --> ROS 2 start/stop topics
   |        |                                      +--> hmi_command_receiver.py
   |        |
   |        +--> Robot telemetry (data_reader_node.py, gps_position_node.py,
   |        |                     heading_node.py, rosout_node.py, ping_monitor.py)
   |        |
   |        +--> Camera feeds (gstream_setup.py, gst_video_widget.py,
   |        |                  image_viewer.py)
   |        |
   |        +--> Maps (map_view.py, slammap_node.py, pathfinder.py)
   |        |
   |        +--> Alarms/login/display helpers
   |
   +--> Visual feedback and status display
```

Most ROS 2 monitoring components pass information to Qt widgets using **Qt signals**, keeping the ROS message-handling logic separate from the GUI update logic. The interface coordinates these components and allows operators to command and supervise the robot.

## 8. Where to start reading

For someone new to the project, a useful reading order is:

1. `main.py` — how the application starts.
2. `mainwindow.py` — how the GUI connects the subsystems.
3. `teleop_controller.py`, `teleop_node.py`, `sdl_controller.py` — operator input and command publishing.
4. `hmi_order_sender.py` and `hmi_command_receiver.py` — enabling/disabling supporting systems.
5. `data_reader_node.py`, `gps_position_node.py`, `heading_node.py`, `rosout_node.py` — feedback from the robot.
6. `gstream_setup.py`, `gst_video_widget.py`, `map_view.py` — video and map visualization.

For installation instructions and prerequisites, refer to [`INSTALL.md`](INSTALL.md).
