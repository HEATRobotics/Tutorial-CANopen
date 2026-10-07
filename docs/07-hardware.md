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

## Native Pi workflow, like Autobot

Your existing setup is Ubuntu 22.04.5, an MCP2515 SPI adapter on `can0`, and `CAN_BIT_RATE=1000000`. Keep the working boot overlay (`oscillator=12000000`, `interrupt=25`, `spimaxfrequency=2000000`) and driver. The Pi runs ROS 2 Humble directly; it does not need Docker.

Clone your completed learner branch on the Pi. Transfer source only; build/install directories must be built on the Pi. From the checkout root:

```bash
bash scripts/setup_pi.sh
source /opt/ros/humble/setup.bash
bash scripts/build_workspace.sh
source ros2_ws/install/setup.bash
```

The packages are already created. If completing the node blanks on the Pi, edit them directly under `ros2_ws/src`; replace `/work/tutorial` in desktop instructions with your checkout path. The dependency script uses your existing Humble installation, just like Autobot's native workflow.

Bring up CAN using your existing Autobot script:

```bash
export CAN_BIT_RATE=1000000
bash ~/EMBR-AutoBot/Tools/start_can_network.sh
ip -details link show can0
```

Alternatively, from this checkout: `bash scripts/setup_can.sh can0 1000000`. Run one setup method. Expected: `can0` UP at 1000000 bit/s. Stop Autobot's motor-control nodes before running tutorial comms.

Open native Pi terminals (or SSH sessions). In each, run:

```bash
cd ~/Tutorial-CANopen
source /opt/ros/humble/setup.bash
source ros2_ws/install/setup.bash
```

Terminal A: `ros2 run maxon_controller node` (zero inputs by default).

Terminal B: `ros2 run helper node`.

Terminal C: run comms using the hardware command below. The flow is `maxon_controller -> /drive/raw -> helper -> /drive/normalized -> comms -> can0 -> ESCON2`. All three nodes can run on the Pi, matching Autobot's native workflow.

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
source /opt/ros/humble/setup.bash
source ros2_ws/install/setup.bash
```

Run the ROS nodes in those native SSH shells. Desktop Docker is only for development/simulation. Keeping all three nodes on the Pi avoids additional cross-machine DDS networking setup.

Completion: record Pi/OS/adapter/driver, motor/load/gearbox, firmware/Motion Studio version, exported settings, IDs/bitrate, chosen limits, and supervised results for normal stop, publisher loss, CAN loss, and Pi power loss. Hardware validation is separate from simulation success.

[Return to index](../README.md).
