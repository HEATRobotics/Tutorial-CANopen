# ROS 2 + Maxon: a one-hour node exercise

Four packages are **already created** and included in the Humble container. Fill **nine blanks in three node files** to connect this pipeline:

```text
maxon_controller -> /drive/raw -> helper -> /drive/normalized -> comms -> Maxons
```

The custom message is already defined: `interfaces/msg/DriveCommand` has `float32 forward` and `float32 turn`. Package metadata, publishers/subscribers where repetitive, motor mixing, CANopen transport, watchdog, and stop handling are supplied. Unfinished nodes intentionally raise errors rather than move motors.

## Start on Windows, macOS, or Linux desktop

Install Docker Desktop (Windows: WSL 2 with Linux containers), or Docker Engine on Linux. In the cloned repository:

```text
docker compose up -d --build
docker compose exec tutorial bash
```

Inside that bash shell, build the editable workspace once:

```bash
bash scripts/build_workspace.sh
source ros2_ws/install/setup.bash
```

Edit the three files below in your normal editor. Your checkout is mounted into the container. Because this is a symlink install, restart nodes after edits; Python-only edits do not require another build. New container bash shells automatically load your workspace.

## The 60-minute plan

| Time | Task | File |
| --- | --- | --- |
| 0–5 min | Inspect the ready-made message and packages | [Package map](docs/01-package-map.md) |
| 5–15 min | Read forward/turn parameters and publish: M01–M03 | [maxon_controller/node.py](ros2_ws/src/maxon_controller/maxon_controller/node.py) |
| 15–30 min | Clamp inputs and republish: H01–H03 | [helper/node.py](ros2_ws/src/helper/helper/node.py) |
| 30–45 min | Subscribe, calculate rpm, send: C01–C03 | [comms/node.py](ros2_ws/src/comms/comms/node.py) |
| 45–60 min | Run tests and the full simulated pipeline | [Run guide](docs/06-run-pipeline.md) |

This is a one-hour coding exercise once the environment is ready. Docker downloads and physical commissioning are separate. Each lesson supplies exact hints and reference links. Replace each `TODO('ID')` call with the requested expression or statement. No package creation, CMake work, custom message generation work, or CAN frame construction is required.

For example, replace:

```python
msg.forward = TODO('M01')
```

with:

```python
msg.forward = float(self.get_parameter('forward').value)
```

Keep the assignment and indentation; replace the entire `TODO('M01')` call.

Follow [publisher](docs/03-maxon-controller.md), [helper](docs/04-helper.md), and [comms](docs/05-comms.md) in order. Start in simulation.

## Raspberry Pi: native ROS, like Autobot

The Pi runs the same packages natively, using your existing Ubuntu 22.04, MCP2515 `can0`, and 1 Mbit/s setup. Docker is only for desktop development/simulation. See [native Pi deployment](docs/07-hardware.md); it reuses Autobot's CAN startup script.

All three nodes can run on the Pi. The motor controller starts disabled and requires explicit arming. Hardware defaults refuse to start without a positive verified rpm limit and commissioning acknowledgement. The reference drive/motor is ESCON2 Compact 60/30 with Autobot's EC-i 52; default motor order is FL, BL, FR, BR, IDs 1, 3, 2, 4.

See [platform setup](docs/00-environment.md), [references](docs/references.md), [validation](docs/validation.md), and [contributing](CONTRIBUTING.md). Licensed under [Apache 2.0](LICENSE).
