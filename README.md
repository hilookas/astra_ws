# ROS2 Workspace for AhaRobot

<div align="center">
  <img src="assets/logo.png" alt="AhaRobot Logo" width="200"/>
</div>

<div align="center">
  <a href="https://aha-robot.github.io/" target="_blank">Project Website</a> • 
  <a href="https://arxiv.org/abs/2503.10070" target="_blank">Paper</a> • 
  <a href="https://www.notion.so/1b433900bc8780c4a503e3490ce3e718?pvs=21" target="_blank">Documentation</a> • 
  <a href="https://github.com/hilookas/astra_ws" target="_blank">ROS Code</a> •
  <a href="https://github.com/hilookas/AstraFirmwares" target="_blank">Firmware Code</a> •
  <a href="https://github.com/hilookas/Astra_Hardwares" target="_blank">Hardware Code</a> •
  <a href="https://huggingface.co/lookas" target="_blank">Dataset</a>
</div>

## Repository Contents

This repository is the ROS2 workspace for AhaRobot, organized into the following structure:

### ROS2 Packages (`src/`)
- **astra_description**: Robot URDF models and visualization configurations
- **astra_controller**: Implementation of robot control algorithms and nodes
- **astra_controller_interfaces**: ROS2 interfaces for the Astra robot control
- **astra_moveit_config**: MoveIt configuration for motion planning
- **usb_cam**: USB camera driver and utilities

### Non-ROS Components (`non_ros_src/`)
- **astra_teleop**: RoboPilot teleoperation client software
- **astra_teleop_web**: RoboPilot web-based teleoperation interface
- **urchin**: Custom libraries for robot control
- **ModernRobotics**: Robotics algorithms and utilities
- **lerobot**: Supplementary learning libraries
- **odrive-can**: ODrive motor controller interface
- **pyribbit**: Python utilities for the robot
- **mr_urdf_loader**: Modern Robotics URDF loading utilities

## How-to-use

For detailed documentation, please refer to the following resources:

- [Install ROS 2 Workspace](docs/tutorials.md)
  - Starting Your Docker
  - Installing Dependence
  - Visualizing Your Robot


## License

This project is licensed under the [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.en.html) with additional restrictions.

This means:
- ✅ You are free to use, modify and distribute the source code
- ✅ You must make your modifications available under the same license
- ✅ You must state changes made to the code
- ✅ You must include the original copyright notice
- ❌ You may not use the material for commercial purposes
- ❌ Modifications must also prohibit commercial use

IMPORTANT: This project explicitly prohibits ANY commercial use, including but not limited to selling products based on this project.

See the [LICENSE](LICENSE) file for the full license text.