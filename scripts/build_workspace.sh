#!/usr/bin/env bash
set -e
cd /work/tutorial/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install --base-paths src
