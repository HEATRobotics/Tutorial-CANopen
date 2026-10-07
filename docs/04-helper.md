# Lesson 04: Normalize and republish

Edit `ros2_ws/src/helper/helper/normalization.py` and `node.py`.

| Blank | Task |
| --- | --- |
| H01 | Check BOTH values with `math.isfinite` |
| H02 | Clamp forward into [-1.0, 1.0] |
| H03 | Clamp turn into [-1.0, 1.0] |
| H04 | Create a `DriveCommand` publisher on `/drive/normalized`, depth 1 |
| H05 | Subscribe to `/drive/raw` with `self.on_command`, depth 1 |
| H06 | Pass both received fields to `normalize` |
| H07 | Publish the new output message |

Here “normalize” means independently clamp each axis, preserving valid values. `2.0, -3.0` becomes `1.0, -1.0`. If either input is NaN or infinite, both outputs become zero. Do not divide a valid pair by its length: the wheel mix is a separate task.

Republish **only when a new raw message arrives**. A timer that repeats the last command would hide upstream failure from the comms watchdog.

Build and run the pure-function tests:

```bash
cd /work/tutorial/ros2_ws
colcon build --symlink-install --base-paths src --packages-up-to helper
source install/setup.bash
python3 -m pytest -q src/helper/test/test_normalization.py
```

Expected: six tests pass after completing H01–H03. TODO failures tell you which expression remains. Start helper in terminal A and the previous lesson's raw publisher in terminal B:

```bash
ros2 run helper node
```

Terminal C:

```bash
ros2 topic echo /drive/normalized
```

With raw inputs `forward:=2.0` and `turn:=-0.25`, expect 1.0 and -0.25. Stop maxon_controller; helper should stop publishing rather than keeping the last value alive. Stop the remaining nodes before moving on.

Completion: tests pass, topics are distinct, and no normalized messages are emitted when the raw stream stops.

References: [Python subscribers](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html), [math.isfinite](https://docs.python.org/3.10/library/math.html#math.isfinite), [min/max](https://docs.python.org/3.10/library/functions.html#max).

[Next: comms](05-comms.md).
