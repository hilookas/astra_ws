from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    share = Path(get_package_share_directory("aharobot_sim_bringup"))
    nav2_share = Path(get_package_share_directory("nav2_bringup"))
    ros_gz_share = Path(get_package_share_directory("ros_gz_sim"))
    world = share / "worlds" / "nav_test.sdf"
    model_path = share / "models"
    map_file = share / "maps" / "nav_test.yaml"
    params = nav2_share / "params" / "nav2_params.yaml"
    rviz_config = nav2_share / "rviz" / "nav2_default_view.rviz"

    start_rviz = LaunchConfiguration("start_rviz")
    localization = LaunchConfiguration("localization")
    ground_truth = IfCondition(PythonExpression(["'", localization, "' == 'ground_truth'"]))
    amcl = IfCondition(PythonExpression(["'", localization, "' == 'amcl'"]))
    tuned_params = RewrittenYaml(
        source_file=str(params),
        param_rewrites={
            # The stock checker expects 0.5 m every 10 s, which falsely marks
            # this small base as stuck while DWB slows down near the goal.
            "required_movement_radius": "0.05",
            "movement_time_allowance": "20.0",
            "xy_goal_tolerance": "0.15",
            # Simulation odometry is already close to the Gazebo pose. Keep
            # particles tight enough to correct slip without jumping between
            # similar-looking walls in the small test room.
            "alpha1": "0.05",
            "alpha2": "0.05",
            "alpha3": "0.05",
            "alpha4": "0.05",
            "alpha5": "0.05",
            # Keep map -> odom fresh even while the simulated robot is idle.
            # Otherwise a goal sent after a long pause sees an expired AMCL TF.
            "update_min_d": "0.0",
            "update_min_a": "0.0",
            "min_particles": "300",
            "max_particles": "1200",
            "set_initial_pose": "true",
        },
        convert_types=True,
    )
    robot_description = """<?xml version='1.0'?>
<robot name='aharobot_nav'>
  <link name='base_footprint'/><link name='base_link'/><link name='laser_frame'/>
  <joint name='base_joint' type='fixed'><parent link='base_footprint'/><child link='base_link'/><origin xyz='0 0 0.18'/></joint>
  <joint name='laser_joint' type='fixed'><parent link='base_footprint'/><child link='laser_frame'/><origin xyz='0.20 0 0.43'/></joint>
</robot>"""
    return LaunchDescription([
        DeclareLaunchArgument("start_rviz", default_value="true"),
        DeclareLaunchArgument(
            "localization", default_value="ground_truth",
            description="ground_truth for deterministic tests, or amcl for LiDAR localization",
        ),
        SetEnvironmentVariable("IGN_GAZEBO_RESOURCE_PATH", str(model_path)),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(ros_gz_share / "launch" / "gz_sim.launch.py")),
            launch_arguments={"gz_args": f"-r {world}", "on_exit_shutdown": "true"}.items(),
        ),
        Node(package="robot_state_publisher", executable="robot_state_publisher", parameters=[{"robot_description": robot_description, "use_sim_time": True}]),
        Node(
            package="ros_gz_bridge", executable="parameter_bridge", output="screen",
            arguments=[
                "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
                "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
                "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
            ],
        ),
        # Ground-truth localization for deterministic navigation testing. Gazebo's
        # diff-drive odometry starts at the map origin, so map -> odom is identity.
        # AMCL can be added later without changing the planner/controller setup.
        Node(
            package="tf2_ros", executable="static_transform_publisher",
            arguments=["0", "0", "0", "0", "0", "0", "map", "odom"],
            parameters=[{"use_sim_time": True}],
            condition=ground_truth,
        ),
        Node(
            package="nav2_map_server", executable="map_server", name="map_server",
            parameters=[{"yaml_filename": str(map_file), "use_sim_time": True}], output="screen",
        ),
        Node(
            package="nav2_lifecycle_manager", executable="lifecycle_manager",
            name="lifecycle_manager_localization", output="screen",
            parameters=[{"use_sim_time": True, "autostart": True, "node_names": ["map_server"]}],
            condition=ground_truth,
        ),
        Node(
            package="nav2_amcl", executable="amcl", name="amcl", output="screen",
            parameters=[
                tuned_params,
                {
                    "use_sim_time": True,
                    "set_initial_pose": True,
                    "initial_pose.x": 0.0,
                    "initial_pose.y": 0.0,
                    "initial_pose.yaw": 0.0,
                },
            ],
            condition=amcl,
        ),
        Node(
            package="nav2_lifecycle_manager", executable="lifecycle_manager",
            name="lifecycle_manager_amcl", output="screen",
            parameters=[{
                "use_sim_time": True, "autostart": True,
                "node_names": ["map_server", "amcl"],
            }],
            condition=amcl,
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(nav2_share / "launch" / "navigation_launch.py")),
            launch_arguments={"params_file": tuned_params, "use_sim_time": "true", "autostart": "true", "use_composition": "False"}.items(),
        ),
        Node(package="rviz2", executable="rviz2", arguments=["-d", str(rviz_config)], parameters=[{"use_sim_time": True}], condition=IfCondition(start_rviz)),
    ])
