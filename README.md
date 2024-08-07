# ROS2 Workspace for Astra

## Single Arm Teleop

```bash
ros2 launch astra_description display_publish_model_only.launch
source non_ros_src/venv/bin/activate
cd src/astra_controller/astra_controller
python main_teleop.py
python main.py
```