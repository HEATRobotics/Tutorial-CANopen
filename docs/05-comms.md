# Lesson 05: Map inputs to Maxon CANopen commands

Edit the four student files under `ros2_ws/src/comms/comms/`: `mixing.py`, `encoding.py`, `can_sender.py`, and `node.py`. Leave `support/` unchanged.

| Blank | Task |
| --- | --- |
| C01 | Left level = forward minus turn |
| C02 | Right level = forward plus turn |
| C03 | Common divisor: maximum of 1.0 and both absolute wheel levels |
| C04 | Encode the integer using `int.to_bytes`, little-endian, respecting the supplied signed flag and size |
| C05 | Call `self.motor.sdo.download` with the provided index, subindex 0, and encoded bytes |
| C06 | Subscribe to `/drive/normalized`, `DriveCommand`, `self.on_command`, depth 1 |
| C07 | Convert the level at `slot` to rpm using `self.speed` and `self.directions[slot]` |

The mixer returns **FL, BL, FR, BR**. Positive turn is left: the left side slows/reverses and the right side speeds up. Scale both sides by one common divisor so mixing two valid axes cannot exceed the wheel range and their ratio is preserved. For forward=1 and turn=1, expect `[0, 0, 1, 1]`.

The signed rpm target is motor-shaft speed, not gearbox output speed. The supplied controller truncates fractional rpm toward zero and enforces the positive configured limit. Default simulation IDs are `[1, 3, 2, 4]`; the same order is used by Autobot. Mounting directions are configurable signs; verify them on your actual mechanism.

## CANopen path

The supplied controller validates rpm units and commissioned speed limits, selects profile velocity mode, then keeps the drive disabled until `/drive/arm` is called. It sends the target followed by a controlword write. Your C04/C05 functions implement the typed SDO transport for those writes, rather than guessing arbitrary CAN frame IDs.

| Object | Purpose | Encoding |
| --- | --- | --- |
| `0x6040:00` | Controlword | 2 bytes unsigned |
| `0x6041:00` | Statusword | Read, state/fault checks |
| `0x6060:00` | Select profile velocity mode (3) | 1 byte signed |
| `0x60FF:00` | Target velocity in commissioned rpm units | 4 bytes signed |
| `0x606C:00` | Actual velocity | Read signed |

The sequence is implemented in the supplied [controller](../exercises/comms/comms/support/controller.py). It uses SDOs sequentially, without synchronized PDOs. Successful communication does not establish motor motion or standstill.

## Check your answers without CAN hardware

```bash
cd /work/tutorial/ros2_ws
colcon build --symlink-install --base-paths src --packages-up-to comms
source install/setup.bash
python3 -m pytest -q src/comms/test/test_commands.py
```

Expected: nine tests pass, covering mixes, rejected invalid inputs, signed byte encoding, and overflow. C05 is checked separately by the virtual SDO test in [the next lesson](06-run-pipeline.md); simulation deliberately bypasses physical transport. An out-of-range/nonfinite normalized message is rejected by comms even if helper was bypassed.

Completion: pure-function tests pass and you can explain how a dimensionless wheel level becomes an INTEGER32 target.

References: [Autobot ESCON2 setup](https://github.com/HEATRobotics/EMBR-AutoBot/blob/main/documentation/escon2_canopen.md), [canopen-python SDO uploads/downloads](https://canopen.readthedocs.io/en/stable/sdo.html), [Python integer byte conversion](https://docs.python.org/3.10/library/stdtypes.html#int.to_bytes), [maxon PVM application notes, section 2.3](https://www.maxongroup.com/medias/sys_master/root/9523021905950/ESCON2-Application-Notes-En.pdf).

[Next: run the pipeline](06-run-pipeline.md).
