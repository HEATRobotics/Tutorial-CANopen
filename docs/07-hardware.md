# Lesson 07: Raspberry Pi + ESCON2

Complete the simulation/tests first. This is an educational scaffold, not a bench-validated motor controller. Review your completed CAN encoding/transport and command path with a supervisor before connecting real hardware.

Reference equipment: Autobot's Maxon EC-i 52 **667065** with ESCON2 Compact 60/30. The exact Pi, CAN adapter, motor/load, firmware, and wiring must be recorded for your setup. Do not guess connector pinouts, HAT overlays, or current limits. Use the [manufacturer hardware reference](https://www.maxongroup.com/medias/sys_master/root/9523021381662/ESCON2-Compact-60-30-Hardware-Reference-En.pdf) for the actual revision.

## Commission before enabling motion

Secure and guard the unloaded motor; provide independent means to stop/remove motor power. Commission the exact motor/feedback, current limits, speed limits, acceleration/deceleration and quick-stop behavior in Motion Studio. Export its configuration. Verify:

- Node ID and bitrate match your Pi interface and ROS parameters.
- Velocity units `0x60A9` are rpm (`0x00B44700`).
- Motor/profile speed limits (`0x6080`, `0x607F`) match the mechanism and allow the chosen software limit.
- Drive-side communication-loss stopping and physical stop circuit work independently of the Pi.
- Mounting direction is correct for each enabled motor.

The supplied code does not commission ramps/current, save to flash, reset faults automatically, or configure/generate a CANopen heartbeat. Do not assume a heartbeat consumer can supervise this node without implementing a producer. Have a qualified integrator establish and demonstrate an independent communication-loss response supported by the drive/system before bench motion. Blocking SDO transfers can extend the ROS timeout response; it is not hard real time.

## Prepare the Pi host

Use a 64-bit OS supported by your Pi model, Docker Engine/Compose v2, and a SocketCAN-compatible adapter with its host driver installed. The Pi GPIO header alone is not a CAN transceiver. Clone your completed learner branch on the Pi; do not copy desktop build/install directories. Power off for wiring. Follow the drive/adapter manuals for CAN_H, CAN_L, reference ground, and termination at both ends.

On the Pi host:

```bash
sudo apt-get update
sudo apt-get install -y can-utils iproute2
ip -brief link
bash scripts/setup_can.sh can0 1000000
candump -e can0
```

This example assumes commissioned 1 Mbit/s and `can0`; use your actual settings. If errors/BUS-OFF occur, correct wiring/bitrate/termination before manually restarting. Ctrl+C exits candump.

Start the Linux hardware networking overlay:

```bash
docker compose -f compose.yaml -f compose.pi.yaml build
docker compose -f compose.yaml -f compose.pi.yaml up -d
docker compose exec tutorial bash
```

Inside, create/copy the four packages if not already on your learner branch, then build/source them as in lesson 06. The overlay exposes host SocketCAN with NET_RAW; it does not need privileged mode or configure the host adapter.

## Start one motor only

Start maxon_controller at zero input and helper in separate shells. Start comms with **only node 1 selected**, after verifying it is your wired motor:

```bash
ros2 run comms node --ros-args \
  -p simulate:=false -p hardware_ready:=true \
  -p channel:=can0 -p bitrate:=1000000 \
  -p 'enabled_motor_ids:=[1]' -p max_speed_rpm:=100.0
```

**100 rpm is illustrative**, not an approved operating limit. Replace it with a verified positive limit. The shipped default is zero and refuses startup. The reference motor software ceiling is 6000 rpm; this is not a recommended operating speed. The `hardware_ready` flag is an operator acknowledgement, not automatic validation.

Default `motor_ids` are `[1, 3, 2, 4]` in FL, BL, FR, BR order. Only selected drives are connected, initialized, commanded, and stopped. Selecting node 1 uses the FL slot; input forward with zero turn commands that motor. Excluding a drive does not stop one already running. For a remapped bench ID, change the corresponding `motor_ids` entry and select it. Run one controller per drive, stopping Autobot or other handlers first.

Inspect `/drive/status`: it must show `simulated: false`, your selected IDs, and disabled startup. Establish the stop procedure first, then call `/drive/arm` while the zero publisher is running. Under supervision, change the forward parameter to a verified small level. With a 100 rpm limit, 0.1 forward and zero turn produces a 10 rpm target. Observe physical response and measured feedback; then call `/drive/stop`.

Stop attempts quick stop, zero target, and voltage disable. Acknowledgement does not confirm standstill; disabling removes holding torque. If CAN/Pi power is lost, software cannot ensure stopping. Verify independent stopping before touching hardware. Normal shutdown also attempts this sequence; process crashes may prevent it.

## Windows/macOS access

Use local Docker for simulation. To run physical commands, open SSH sessions to the Pi from PowerShell or a Mac terminal:

```text
ssh YOUR-USER@YOUR-PI
cd Tutorial-CANopen
docker compose exec tutorial bash
```

All ROS command publishers remain on the Pi; DDS is localhost-only. No direct Windows/macOS USB-CAN passthrough is supplied.

Completion: record Pi/OS/adapter/driver, motor/load/gearbox, firmware/Motion Studio version, exported settings, IDs/bitrate, chosen limits, and supervised results for normal stop, publisher loss, CAN loss, and Pi power loss. Hardware validation is separate from simulation success.

[Return to index](../README.md).
