#!/usr/bin/env bash
# Native Ubuntu 22.04 / ROS 2 Humble dependencies, like Autobot's native setup.
set -eo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source /etc/os-release
if [[ "$ID" != ubuntu || "$VERSION_ID" != 22.04 ]]; then
    echo 'This script expects your Ubuntu 22.04 Pi.' >&2
    exit 1
fi
if [[ ! -f /opt/ros/humble/setup.bash ]]; then
    echo 'ROS 2 Humble is missing; install it before running this script.' >&2
    exit 1
fi
sudo apt-get update
sudo apt-get install -y python3-colcon-common-extensions python3-pip python3-pytest \
    ros-humble-rosidl-default-generators ros-humble-rosidl-default-runtime \
    ros-humble-std-msgs ros-humble-std-srvs can-utils iproute2
python3 -m pip install --user -r "$repo_root/requirements.txt"
echo 'Dependencies ready. Build ros2_ws, source install/setup.bash, then run your nodes.'
