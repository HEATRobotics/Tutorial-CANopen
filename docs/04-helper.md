# Clamp and republish — 15 minutes

Edit `ros2_ws/src/helper/helper/node.py`. The subscriber, publisher, output message, and NaN/infinity checks are already supplied.

| Blank | Fill with |
| --- | --- |
| H01 | `max(-1.0, min(1.0, msg.forward))` |
| H02 | The same clamp for `msg.turn` |
| H03 | Publish `output` using `self.publisher` |

“Normalized” here means each finite axis is clamped to [-1, 1]. Preserve values already in range. If either input is nonfinite, the supplied guard outputs zeros. Republish only in the callback: a timer repeating the last input would hide upstream failure.

Check your callback:

```bash
cd /work/tutorial/ros2_ws
python3 -m pytest -q src/helper/test/test_normalization.py
```

Expected: six tests pass. These tests call your actual node callback. On the native Pi, replace `/work/tutorial` with your checkout path.

Run `ros2 run helper node` alongside maxon_controller and echo `/drive/normalized`. With raw forward=2.0 and turn=-0.25, expect 1.0 and -0.25. Stopping maxon_controller must stop the normalized stream too.

References: [Python subscriber callbacks](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html), [min/max](https://docs.python.org/3.10/library/functions.html#max).

[Next: comms](05-comms.md).
