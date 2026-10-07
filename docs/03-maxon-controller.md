# Publish raw commands — 10 minutes

Edit `ros2_ws/src/maxon_controller/maxon_controller/node.py`. Publisher and 20 Hz timer are ready.

| Blank | Fill with |
| --- | --- |
| M01 | `float(self.get_parameter('forward').value)` |
| M02 | The same expression for the `turn` parameter |
| M03 | A call to `self.publisher.publish` with `msg` |

Example for M01:

```python
# Before
msg.forward = TODO('M01')

# After
msg.forward = float(self.get_parameter('forward').value)
```

Replace the whole TODO call, preserving indentation. Use this pattern for the remaining blanks.

Do not normalize here: this node represents the user's raw input. Restart it after editing:

```bash
ros2 run maxon_controller node --ros-args -p forward:=2.0 -p turn:=-0.25
```

In another container bash shell:

```bash
ros2 topic echo /drive/raw
```

Expect forward 2.0 and turn -0.25. Ctrl+C the echo, then try:

```bash
ros2 param set /maxon_controller forward 0.5
```

Echo again: forward should change without restarting the publisher. Stop the publisher before isolated tests later.

References: [Python publisher](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html), [reading parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html).

[Next: helper](04-helper.md).
