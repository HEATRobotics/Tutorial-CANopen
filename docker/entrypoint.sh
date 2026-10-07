#!/usr/bin/env bash
set -e
source /opt/ros/humble/setup.bash
if [ -f /work/tutorial/ros2_ws/install/setup.bash ]; then
    source /work/tutorial/ros2_ws/install/setup.bash
fi
exec "$@"
