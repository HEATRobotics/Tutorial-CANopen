# Environment: Windows, macOS, Linux, Raspberry Pi

The shared [Dockerfile](../docker/Dockerfile) provides Ubuntu 22.04, ROS 2 Humble, colcon, custom-interface generators, pytest, canopen-python, and CAN tools. Compose starts a development shell environment; it does not build unfinished learner code or automatically start motors.

| Host | Local exercises | Physical motors |
| --- | --- | --- |
| Windows + Docker Desktop, WSL 2 Linux containers | All simulation/development lessons | SSH to Pi |
| macOS + Docker Desktop | All simulation/development lessons | SSH to Pi |
| 64-bit Linux + Docker Engine | All simulation/development lessons | Local SocketCAN or SSH to Pi |
| 64-bit Raspberry Pi + Docker Engine | All lessons | Host SocketCAN adapter required |

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

The Pi host should use a 64-bit OS supported by its board and CAN adapter; Humble's Jammy environment lives inside Docker. This tutorial does not specify a Pi HAT driver without knowing its model.

## Workspace and shells

Your checkout is mounted at `/work/tutorial`. Learner packages go in `/work/tutorial/ros2_ws/src`. Build/install/log directories remain in that workspace and are Git-ignored. Do not share those generated directories across different OS/CPU environments; clone/build separately on the Pi.

Interactive shells source ROS and the installed workspace if present. After each build, run `source /work/tutorial/ros2_ws/install/setup.bash` in existing shells; new shells load it automatically. For noninteractive commands use `docker compose exec tutorial rosenv COMMAND`.

If Docker is unavailable, start Desktop/the daemon and check `docker info`. If scripts show `bash\r` errors, restore LF line endings. If bind mounts fail, check Docker Desktop's file access settings or use a WSL Linux checkout. Stop the environment from the host with `docker compose down`.

[Next: create packages](01-create-packages.md).
