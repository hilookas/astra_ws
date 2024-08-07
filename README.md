# ROS2 Workspace for Astra

## Single Arm Teleop

```bash
ros2 launch astra_description display_publish_model_only.launch
cd src/astra_controller/astra_controller
python teleop_node.py
python ik_node.py
python dry_run_node.py
```