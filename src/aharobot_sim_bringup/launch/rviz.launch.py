from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    description_share = Path(get_package_share_directory("astra_description"))
    bringup_share = Path(get_package_share_directory("aharobot_sim_bringup"))
    robot_description = (description_share / "urdf" / "astra_description.urdf").read_text()

    return LaunchDescription(
        [
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[{"robot_description": robot_description}],
                output="screen",
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                output="screen",
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=["-d", str(bringup_share / "rviz" / "aharobot.rviz")],
                output="screen",
            ),
        ]
    )
