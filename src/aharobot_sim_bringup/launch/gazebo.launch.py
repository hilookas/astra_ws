from pathlib import Path
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    description_share = Path(get_package_share_directory("astra_description"))
    gazebo_share = Path(get_package_share_directory("ros_gz_sim"))
    urdf_path = description_share / "urdf" / "astra_description.urdf"
    urdf_root = ET.fromstring(urdf_path.read_text())

    # The upstream URDF uses zero-size cylinders as placeholders on the two
    # end-effector links. DART rejects those collision shapes, so omit only
    # those invalid placeholders in the simulation copy of the description.
    for link in urdf_root.findall("link"):
        for collision in list(link.findall("collision")):
            cylinder = collision.find("./geometry/cylinder")
            if cylinder is None:
                continue
            radius = float(cylinder.get("radius", "0"))
            length = float(cylinder.get("length", "0"))
            if radius <= 0 or length <= 0:
                link.remove(collision)

    robot_description = ET.tostring(urdf_root, encoding="unicode")
    robot_description = robot_description.replace(
        "package://astra_description/", f"file://{description_share}/"
    )

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(str(gazebo_share / "launch" / "gz_sim.launch.py")),
                launch_arguments={"gz_args": "-r empty.sdf"}.items(),
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[{"robot_description": robot_description}],
                output="screen",
            ),
            Node(
                package="ros_gz_sim",
                executable="create",
                arguments=["-name", "aharobot", "-topic", "robot_description", "-z", "0.05"],
                output="screen",
            ),
        ]
    )
