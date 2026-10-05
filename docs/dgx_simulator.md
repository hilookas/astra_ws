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

# Start the navigation test world, map server, Nav2, and RViz.
./scripts/aharobot-sim nav2
```

Only one GUI mode is intended to run at a time. Starting either command stops
the previous RViz or Gazebo process in the dedicated container.

## Nav2 navigation test

The navigation launch uses a lightweight differential-drive AhaRobot base with
a 2D LiDAR. The upstream hardware URDF is not changed. The test world has a
matching occupancy map and uses Gazebo odometry as ground-truth localization,
which keeps planner and controller tests deterministic while AMCL tuning is
kept as a separate task.

After `./scripts/aharobot-sim nav2`, set a goal using RViz's **Nav2 Goal** tool,
or send one from SSH:

```bash
# Default goal: x=2.0, y=0.0 in the map frame.
./scripts/aharobot-sim nav-goal

# Custom map-frame goal.
./scripts/aharobot-sim nav-goal 1.5 -0.5
```

The robot starts at `(0, 0)`. Keep goals inside the inner walls at
approximately `-3.5 < x,y < 3.5`.

## Diagnostics and shutdown

```bash
./scripts/aharobot-sim status
./scripts/aharobot-sim logs
./scripts/aharobot-sim stop
```

## Current scope

- RViz loads the complete upstream AhaRobot URDF and provides joint sliders.
- Gazebo Fortress spawns the robot and ground plane with physics enabled.
- The Nav2 mode bridges `/clock`, `/cmd_vel`, `/odom`, `/tf`, and `/scan`, and
  starts the map server, planner, DWB controller, behavior tree navigator,
  recovery behaviors, velocity smoother, and RViz.
- The simulation copy removes two zero-size end-effector collision placeholders
  that make the DART physics engine abort. The upstream hardware URDF is not
  modified.
- Arm joint controllers and simulated cameras are not connected yet. Navigation
  uses the dedicated base model; integrating the full arm collision model and
  AMCL localization are separate follow-up stages.
