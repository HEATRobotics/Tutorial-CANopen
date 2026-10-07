# Inspect the ready-made packages — 5 minutes

No package creation or copying is needed. Everything is in `ros2_ws/src` and installed in the container image.

| Package | Provided | You edit |
| --- | --- | --- |
| interfaces | `msg/DriveCommand.msg`, complete CMake and manifest | Nothing |
| maxon_controller | Publisher, timer, parameters, entry point | Three blanks in `node.py` |
| helper | Subscriber, publisher, finite-input check | Three blanks in `node.py` |
| comms | ROS lifecycle, mixing, CANopen transport, watchdog, arm/stop | Three blanks in `node.py` |

Inside a container bash shell, inspect:

```bash
ros2 interface show interfaces/msg/DriveCommand
ros2 pkg executables maxon_controller
ros2 pkg executables helper
ros2 pkg executables comms
```

Expected: `float32 forward`, `float32 turn`, and a `node` executable for each Python package. The executables are installed but intentionally incomplete. Launching them before filling the blanks produces a named TODO error, either immediately or on their first callback.

Edit source files under `ros2_ws/src`, not files inside `/opt`. The desktop checkout is mounted at `/work/tutorial`. Run `bash scripts/build_workspace.sh` once and source `ros2_ws/install/setup.bash` before starting your edited nodes. On the Pi use the same command from your own checkout after installing native dependencies.

References, if curious: [ROS packages](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html), [custom interfaces](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html).

[Next: publisher](03-maxon-controller.md).
