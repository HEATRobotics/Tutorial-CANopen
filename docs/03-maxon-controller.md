# Lesson 03: Publish raw inputs

Edit `ros2_ws/src/maxon_controller/maxon_controller/node.py`. The custom message import and node lifecycle are supplied.

| Blank | Task |
| --- | --- |
| M01 | Create a `DriveCommand` publisher on `/drive/raw` with queue depth 1 |
| M02 | Create a 0.05-second timer calling `self.publish_command` |
| M03 | Read the current `forward` ROS parameter value |
| M04 | Read the current `turn` ROS parameter value |
| M05 | Publish `msg` using `self.publisher` |

Use a timer rather than a blocking while-loop. Reading parameters on every tick lets you change inputs without restarting. Leave normalization to helper; the publisher should preserve a raw input such as 2.0.

Build and run in terminal A:

```bash
cd /work/tutorial/ros2_ws
colcon build --symlink-install --base-paths src --packages-up-to maxon_controller
source install/setup.bash
ros2 run maxon_controller node --ros-args -p forward:=2.0 -p turn:=-0.25
```

Terminal B (new container bash shell):

```bash
ros2 topic echo /drive/raw
```

Expected: `forward: 2.0`, `turn: -0.25`. Ctrl+C the echo and run:

```bash
ros2 topic hz /drive/raw
```

Expected: roughly 20 Hz, allowing for scheduling. Use a third shell or stop the monitor to change a parameter:

```bash
ros2 param set /maxon_controller forward 0.5
```

The topic should change to 0.5 without restarting the publisher. If the node names a blank in an exception, complete that blank. If the topic is missing, check `ros2 node list` and source the workspace after rebuilding.

Completion: raw values are published at approximately 20 Hz and parameter updates are visible. Stop the publisher with Ctrl+C before subsequent isolated tests.

References: [Python publisher/subscriber tutorial](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html), [Python parameter tutorial](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html).

[Next: helper](04-helper.md).
