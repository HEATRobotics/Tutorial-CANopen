# Lesson 02: Define DriveCommand

Edit `ros2_ws/src/interfaces/msg/DriveCommand.msg`.

| Blank | Task | Hint |
| --- | --- | --- |
| I01 | Replace the type before `forward` | ROS primitive for a 32-bit floating-point number |
| I02 | Replace the type before `turn` | Same primitive type as forward |

The fields represent dimensionless forward and turn inputs. Raw values may exceed [-1, 1]; helper will clamp them. Positive turn means left in this tutorial. Do not add wheel-specific fields: comms handles wheel mixing.

The supplied `CMakeLists.txt` registers the `.msg` with `rosidl_generate_interfaces`; `package.xml` declares the generator, runtime, and interface-package group. Inspect both files to understand why this package differs from the Python nodes.

Build only the interface, then inspect its generated type:

```bash
cd /work/tutorial/ros2_ws
colcon build --symlink-install --base-paths src --packages-select interfaces
source install/setup.bash
ros2 interface show interfaces/msg/DriveCommand
python3 -c 'from interfaces.msg import DriveCommand; print(DriveCommand(forward=0.5, turn=-0.25))'
```

Expected: two floating-point fields with exactly the names `forward` and `turn`, and a message populated with the given values. If generation reports an invalid type, a placeholder is still present. If Python cannot import it, source the install setup in that same shell.

Completion: the message builds and can be imported before either node package exists at runtime.

References: [custom ROS interfaces](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html), [message primitive types](https://docs.ros.org/en/humble/Concepts/Basic/About-Interfaces.html).

[Next: maxon_controller](03-maxon-controller.md).
