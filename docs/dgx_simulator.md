# AhaRobot simulator on DGX Spark

This setup keeps the ROS 2 Humble simulator separate from the host ROS 2 Jazzy
and LeKiwi environments. Rendering is sent to the active RDP X11 session. The
default display is `:11.0` and software OpenGL is used for reliable xrdp output.

## First-time setup

```bash
cd /home/shun.kodaira/aharobot_sim
./scripts/aharobot-sim build
./scripts/aharobot-sim up
./scripts/aharobot-sim bootstrap
./scripts/aharobot-sim check
```

## Launch

Open the DGX desktop through RDP, then run one of these commands over either the
RDP terminal or SSH:

```bash
cd /home/shun.kodaira/aharobot_sim

# Inspect the URDF and move joints with sliders.
./scripts/aharobot-sim rviz

# Spawn AhaRobot in Gazebo Fortress.
./scripts/aharobot-sim gazebo
```

Only one GUI mode is intended to run at a time. Starting either command stops
the previous RViz or Gazebo process in the dedicated container.

## Diagnostics and shutdown

```bash
./scripts/aharobot-sim status
./scripts/aharobot-sim logs
./scripts/aharobot-sim stop
```

## Current scope

- RViz loads the complete upstream AhaRobot URDF and provides joint sliders.
- Gazebo Fortress spawns the robot and ground plane with physics enabled.
- The simulation copy removes two zero-size end-effector collision placeholders
  that make the DART physics engine abort. The upstream hardware URDF is not
  modified.
- Joint controllers, mobile-base drive, simulated cameras, and ROS 2 navigation
  are not connected yet. Those are the next implementation stage.
