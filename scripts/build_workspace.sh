#!/usr/bin/env bash
set -e
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/humble/setup.bash
cd "$repo_root/ros2_ws"
colcon build --symlink-install --base-paths src
