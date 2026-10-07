# Lesson 06: Run your completed pipeline

Finish all blanks first. In a container shell, build all four packages and run the learner tests:

```bash
cd /work/tutorial/ros2_ws
colcon build --symlink-install --base-paths src
source install/setup.bash
python3 -m pytest -q src/helper/test/test_normalization.py src/comms/test/test_commands.py src/comms/test/test_sdo_transport.py src/comms/test/test_node_blanks.py
```

Expected: **19 tests** pass. The virtual SDO test checks the supplied CAN transport with an emulated CANopen device, without physical CAN or motor power. It does not validate a real controller. If testing fails, use the named blank/expected result rather than removing the assertion.

## Run nodes manually

Open three container bash shells. Source the workspace in any shell opened before the build.

Terminal A:

```bash
ros2 run maxon_controller node --ros-args -p forward:=0.5 -p turn:=0.25
```

Terminal B:

```bash
ros2 run helper node
```

Terminal C:

```bash
ros2 run comms node --ros-args -p simulate:=true -p max_speed_rpm:=100.0
```

Comms starts disabled. In terminal D inspect the graph, then arm:

```bash
ros2 node list
ros2 topic list -t
ros2 service call /drive/arm std_srvs/srv/Trigger '{}'
ros2 topic echo /drive/status
```

Expected: three nodes, the two `interfaces/msg/DriveCommand` topics, `simulated: true`, and rpm values `[25, 25, 75, 75]` ordered FL, BL, FR, BR. Ctrl+C stops the echo. To stop the drives:

```bash
ros2 service call /drive/stop std_srvs/srv/Trigger '{}'
```

Expected: disarmed, zero simulated speed; raw messages may continue. Zero target alone leaves a drive enabled; stop also attempts voltage disable. A normal stop allows rearming. Set parameters on `/maxon_controller` to explore forward, reverse, turn, and clamping. Run only one raw command publisher.

## Test upstream loss

Arm with maxon_controller publishing, then Ctrl+C maxon_controller. Helper must also stop publishing. After roughly 0.5 s plus polling/transport time, comms should latch a timeout and disarm. `/drive/arm` should now fail. Restart comms after correcting the cause; it never automatically resets drive faults.

Stop all three nodes before running the automated simulation check, which launches and cleans up its own nodes:

```bash
cd /work/tutorial
python3 scripts/smoke_pipeline.py
```

Expected: `PASS: custom message, clamp, four-motor rpm mix, stop, upstream-loss watchdog`. This exercises all three completed Python nodes and generated message bindings. It forces simulation and checks for existing tutorial nodes. Do not run alongside hardware control.

If messages are missing, check topic spelling, generated message type, and sourced workspace. If zero rpm persists after arming, check C02/C03 and `/drive/normalized`. If the watchdog never fires after maxon_controller stops, check that helper only publishes in its callback.

Completion: all 19 tests and the full simulation check pass. [Next: hardware](07-hardware.md).
