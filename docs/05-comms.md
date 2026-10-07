# Connect normalized commands to CANopen — 15 minutes

Edit only `ros2_ws/src/comms/comms/node.py`. The larger ROS/CAN state machine lives in the supplied `support/runtime.py`; you do not need to edit it.

| Blank | Fill with |
| --- | --- |
| C01 | Helper's output topic name as a string: `/drive/normalized` |
| C02 | `level * self.speed * direction` |
| C03 | Return the result of calling `control.command(rpm)` |

Read the supplied subscription call: its message is `DriveCommand` and its callback is `self.on_command`. That callback mixes forward/turn into bounded left/right wheel levels, calls your rpm conversion, and passes the result through your send hook. The controller then performs the CANopen transfer. Simulation uses the same path with an in-memory drive.

Motor order is FL, BL, FR, BR. Positive turn means left. The supplied mixer uses left=forward-turn, right=forward+turn, then scales both sides if necessary. At 100 rpm, forward=0.5 and turn=0.25 produce `[25, 25, 75, 75]` rpm. Mounting direction can reverse an individual target.

Check the hooks and supplied transport:

```bash
cd /work/tutorial/ros2_ws
python3 -m pytest -q src/comms/test
```

Expected: 13 tests pass. Three directly check your node blanks; the others check mixing and CANopen byte encoding, including a virtual CAN exchange. No physical hardware is needed.

You do not need to construct CAN frames. The supplied driver selects ESCON2 profile velocity mode, sends target velocity through `0x60FF`, applies it with a `0x6040` controlword write, and handles timeout/stop. It starts disabled until explicitly armed.

References: [Python subscriptions](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html), [Autobot CANopen workflow](https://github.com/HEATRobotics/EMBR-AutoBot/blob/main/documentation/escon2_canopen.md), [SDO API](https://canopen.readthedocs.io/en/stable/sdo.html), [ESCON2 PVM notes](https://www.maxongroup.com/medias/sys_master/root/9523021905950/ESCON2-Application-Notes-En.pdf).

[Next: run the pipeline](06-run-pipeline.md).
