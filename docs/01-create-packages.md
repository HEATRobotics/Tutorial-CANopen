# Lesson 01: Create four ROS packages

Prerequisite: [container environment](00-environment.md). All commands below run inside `docker compose exec tutorial bash`.

```bash
cd /work/tutorial/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 interfaces
ros2 pkg create --build-type ament_python --license Apache-2.0 maxon_controller --dependencies rclpy interfaces
ros2 pkg create --build-type ament_python --license Apache-2.0 helper --dependencies rclpy interfaces
ros2 pkg create --build-type ament_python --license Apache-2.0 comms --dependencies rclpy interfaces std_srvs std_msgs
```

`interfaces` uses CMake because ROS generates message bindings there; the three nodes use Python. Names are intentionally generic for this isolated tutorial; don't combine this workspace with another package named `interfaces`.

Copy the starter overlays onto the generated packages (this replaces generated metadata with the supplied dependency/entry-point configuration):

```bash
cp -r /work/tutorial/exercises/interfaces/. interfaces/
cp -r /work/tutorial/exercises/maxon_controller/. maxon_controller/
cp -r /work/tutorial/exercises/helper/. helper/
cp -r /work/tutorial/exercises/comms/. comms/
cd /work/tutorial/ros2_ws
colcon list --base-paths src
```

Expected: four packages, including one `ament_cmake` and three `ament_python` packages. Do this copy **once**: repeating it later overwrites your answers. Edit files under `ros2_ws/src`, not the originals under `exercises`.

Do not build yet: the custom message's placeholder types intentionally prevent generation until lesson 02. TODO expressions in Python are syntactically valid but raise `NotImplementedError` when executed. Generated `test/` lint files may also need your maintainer metadata/docstrings; the supplied lesson tests can be run directly as shown in later lessons.

Completion: you can explain package vs node, identify each package's `package.xml`, and locate Python entry points in `setup.py`.

Reference: [ROS 2 Humble: creating your first package](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html).

[Next: interfaces](02-interfaces.md).
