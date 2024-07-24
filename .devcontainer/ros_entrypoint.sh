#!/bin/bash
# shellcheck disable=SC1090,SC1091
set -e

# setup ros2 environment
source /opt/ros/"$ROS_DISTRO"/setup.bash --
source ~/ros2_ws/install/setup.bash --
export PATH="$HOME/.local/bin:$PATH"
# export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages:/opt/ros/humble/lib/python3.10/site-packages/

exec "$@"
