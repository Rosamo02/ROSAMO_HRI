# ROSAMO HRI Installation Protocol

## 1. Install ROS 2 Jazzy

Ensure that ROS 2 Jazzy is installed.

If ROS 2 Jazzy is not installed, run:

```bash
sudo apt update
sudo apt install -y ros-jazzy-desktop ros-dev-tools
```

Verify that the ROS 2 setup files exist:

```bash
ls -l /opt/ros/jazzy/setup.*
```

You should see files similar to:

```text
/opt/ros/jazzy/setup.bash
/opt/ros/jazzy/setup.sh
/opt/ros/jazzy/setup.zsh
```

---

## 2. Source ROS 2 Jazzy

### If using Zsh

Run:

```zsh
source /opt/ros/jazzy/setup.zsh
export ROS_DOMAIN_ID=0

which ros2
echo $ROS_DISTRO
ros2 topic list
```

You should see:

```text
/opt/ros/jazzy/bin/ros2
jazzy
```

`ros2 topic list` should also show the ROS 2 topics available on the network.

### If using Bash

Run:

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=0

which ros2
echo $ROS_DISTRO
ros2 topic list
```

You should see:

```text
/opt/ros/jazzy/bin/ros2
jazzy
```

---

## 3. Install Required Dependencies

Update the package list:

```bash
sudo apt update
```

Install the required system dependencies:

```bash
sudo apt install -y \
    git \
    python3.12-venv \
    python3-full \
    libsdl2-2.0-0 \
    libsdl2-dev \
    ros-jazzy-px4-msgs
```

These packages provide:

* Git for downloading the HMI repository.
* Python virtual environment support.
* Python development/runtime dependencies.
* SDL2 support for the controller.
* PX4 ROS 2 message definitions.

---

## 4. Clone the ROSAMO HRI Repository

Go to your home directory:

```bash
cd ~
```

Clone the HMI repository:

```bash
git clone https://github.com/Rosamo02/ROSAMO_HRI.git
```

Enter the repository:

```bash
cd ~/ROSAMO_HRI
```

---

## 5. Create the Python Virtual Environment

Create the virtual environment:

```bash
python3 -m venv ~/ros2_qt_env --system-site-packages
```

The `--system-site-packages` option is important because it allows the virtual environment to access ROS 2 Python packages such as `rclpy`.

Activate the environment:

```bash
source ~/ros2_qt_env/bin/activate
```

You should now see something similar to:

```text
ros2_qt_env
```

in your terminal prompt.

You can verify that the virtual environment is active with:

```bash
which python
which pip
```

The paths should look similar to:

```text
/home/<username>/ros2_qt_env/bin/python
/home/<username>/ros2_qt_env/bin/pip
```

---

## 6. Install Python Dependencies

Make sure you are inside the HMI repository:

```bash
cd ~/ROSAMO_HRI
```

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install the Python packages listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Install PySDL2:

```bash
python -m pip install PySDL2
```

---

## 7. Verify PX4 Messages

Verify that the PX4 ROS 2 messages are available:

```bash
source /opt/ros/jazzy/setup.zsh
ros2 pkg list | grep px4_msgs
```

If using Bash instead:

```bash
source /opt/ros/jazzy/setup.bash
ros2 pkg list | grep px4_msgs
```

You should see:

```text
px4_msgs
```

---

## 8. Run the Interface

Make sure the Python virtual environment is active:

```bash
source ~/ros2_qt_env/bin/activate
```

### Zsh

Source ROS 2:

```zsh
source /opt/ros/jazzy/setup.zsh
export ROS_DOMAIN_ID=0
```

Go to the HMI directory:

```zsh
cd ~/ROSAMO_HRI
```

Run the interface:

```zsh
python main.py
```

### Bash

Source ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=0
```

Go to the HMI directory:

```bash
cd ~/ROSAMO_HRI
```

Run the interface:

```bash
python main.py
```

---

## 9. Quick Start After Installation

After the installation has been completed once, you do not need to reinstall anything.

### Zsh

Open a terminal and run:

```zsh
source ~/ros2_qt_env/bin/activate
source /opt/ros/jazzy/setup.zsh
export ROS_DOMAIN_ID=0

cd ~/ROSAMO_HRI
python main.py
```

### Bash

Open a terminal and run:

```bash
source ~/ros2_qt_env/bin/activate
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=0

cd ~/ROSAMO_HRI
python main.py
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'sdl2'`

Install PySDL2 inside the virtual environment:

```bash
source ~/ros2_qt_env/bin/activate
python -m pip install PySDL2
```

Also make sure SDL2 is installed system-wide:

```bash
sudo apt install -y libsdl2-2.0-0 libsdl2-dev
```

### `ModuleNotFoundError: No module named 'px4_msgs'`

Install the PX4 ROS 2 messages:

```bash
sudo apt install -y ros-jazzy-px4-msgs
```

Then source ROS again:

```bash
source /opt/ros/jazzy/setup.zsh
```

or, when using Bash:

```bash
source /opt/ros/jazzy/setup.bash
```

### ROS 2 topics are not visible

Make sure ROS 2 is sourced and the domain is correct:

```bash
export ROS_DOMAIN_ID=0
ros2 topic list
```

If using Zsh:

```zsh
source /opt/ros/jazzy/setup.zsh
```

If using Bash:

```bash
source /opt/ros/jazzy/setup.bash
```

The computer must also be connected to the same ROS 2 network or configured remote network used by the robot.
