# Environment: Windows, macOS, Linux, Raspberry Pi

The shared [Dockerfile](../docker/Dockerfile) provides Ubuntu 22.04, ROS 2 Humble, colcon, custom-interface generators, pytest, canopen-python, and CAN tools. Compose starts a development shell environment; it builds and installs the ready-made packages but does not automatically start unfinished nodes or motors.

| Host | Local exercises | Physical motors |
| --- | --- | --- |
| Windows + Docker Desktop, WSL 2 Linux containers | All simulation/development lessons | SSH to Pi |
| macOS + Docker Desktop | All simulation/development lessons | SSH to Pi |
| 64-bit Linux + Docker Engine | All simulation/development lessons | Local SocketCAN or SSH to Pi |
| Your Ubuntu 22.04 Raspberry Pi + native ROS 2 Humble | All lessons natively | Existing MCP2515 / can0 at 1 Mbit/s |

## Windows

Follow [Docker's Windows installation guide](https://docs.docker.com/desktop/setup/install/windows-install/) and [WSL 2 setup](https://docs.docker.com/desktop/features/wsl/). Start Docker Desktop with the WSL 2 backend and **Linux containers**. Use a Windows/WSL version supported by your installed Docker Desktop release.

In PowerShell, from your clone:

```powershell
docker info --format '{{.OSType}}'
docker compose version
docker compose build
docker compose up -d
docker compose exec tutorial bash
```

The OS type should be `linux`. All subsequent lesson commands are **inside that bash shell**; do not paste bash line continuations or `source` into PowerShell. Open another PowerShell terminal and run `docker compose exec tutorial bash` for each ROS terminal. For a WSL checkout, enable Docker Desktop integration with that WSL distribution and keep the checkout in its Linux filesystem. The repository's `.gitattributes` keeps shell scripts LF-terminated on Windows.

## macOS and Linux

Install [Docker Desktop on macOS](https://docs.docker.com/desktop/setup/install/mac-install/) or [Docker Engine](https://docs.docker.com/engine/install/). Use the same `docker compose build`, `up -d`, and `exec tutorial bash` commands. The ROS image supports amd64 and arm64; the Compose file does not force emulation. No GUI/XQuartz is needed.

## Raspberry Pi: native ROS 2, like Autobot

Your Pi already runs Ubuntu 22.04.5 with an MCP2515 adapter exposed as `can0`; Autobot uses `CAN_BIT_RATE=1000000`. Keep the existing boot overlay and host driver. No Docker is needed on the Pi.

From your checkout on the Pi:

```bash
bash scripts/setup_pi.sh
source /opt/ros/humble/setup.bash
```

For lessons 01–06, use a native Pi terminal in place of a container bash shell. Replace `/work/tutorial` with your checkout path (for example `~/Tutorial-CANopen`). After completing the node blanks, build with `bash scripts/build_workspace.sh` and source `ros2_ws/install/setup.bash`. See [the native hardware workflow](07-hardware.md).

## Workspace and shells

Your checkout is mounted at `/work/tutorial`. Learner packages go in `/work/tutorial/ros2_ws/src`. Build/install/log directories remain in that workspace and are Git-ignored. Do not share those generated directories across different OS/CPU environments; clone/build separately on the Pi.

Interactive shells source ROS and the installed workspace if present. After each build, run `source /work/tutorial/ros2_ws/install/setup.bash` in existing shells; new shells load it automatically. For noninteractive commands use `docker compose exec tutorial rosenv COMMAND`.

If Docker is unavailable, start Desktop/the daemon and check `docker info`. If scripts show `bash\r` errors, restore LF line endings. If bind mounts fail, check Docker Desktop's file access settings or use a WSL Linux checkout. Stop the environment from the host with `docker compose down`.

[Next: inspect the packages](01-package-map.md).
