# References by task

- Package creation: [ROS 2 Humble packages](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html).
- I01/I02: [custom interfaces](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html) and [primitive message types](https://docs.ros.org/en/humble/Concepts/Basic/About-Interfaces.html).
- M01–M05, H04–H07, C06: [Python publisher/subscriber](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html), [rclpy Node API](https://docs.ros.org/en/humble/p/rclpy/api/node.html).
- Parameter inputs: [Python parameter tutorial](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html).
- H01–H03: [math.isfinite](https://docs.python.org/3.10/library/math.html#math.isfinite) and [min/max](https://docs.python.org/3.10/library/functions.html#max).
- C01–C03/C07: [Autobot's drivetrain approach](https://github.com/HEATRobotics/EMBR-AutoBot/blob/main/documentation/escon2_canopen.md). This exercise defines positive turn as left and uses common-divisor wheel normalization.
- C04/C05: [int.to_bytes](https://docs.python.org/3.10/library/stdtypes.html#int.to_bytes), [canopen-python SDO API](https://canopen.readthedocs.io/en/stable/sdo.html).
- ESCON2 PVM state/target sequence: [maxon Application Notes](https://www.maxongroup.com/medias/sys_master/root/9523021905950/ESCON2-Application-Notes-En.pdf), section 2.3.
- Drive object dictionary: [maxon firmware specification](https://www.maxongroup.com/medias/sys_master/root/9523021185054/ESCON2-Firmware-Specification-En.pdf), use the revision matching your firmware.
- Wiring/commissioning: [ESCON2 Compact 60/30 hardware reference](https://www.maxongroup.com/medias/sys_master/root/9523021381662/ESCON2-Compact-60-30-Hardware-Reference-En.pdf).
- Linux CAN setup: [python-can SocketCAN](https://python-can.readthedocs.io/en/stable/interfaces/socketcan.html).
- Windows: [Docker Desktop installation](https://docs.docker.com/desktop/setup/install/windows-install/) and [WSL 2 integration](https://docs.docker.com/desktop/features/wsl/).

The Autobot documentation and local drivetrain implementation informed the supplied ESCON2 state/stop policy and motor order. The tutorial uses its own `interfaces/msg/DriveCommand` rather than Autobot's custom message packages. ROS documentation may require browser access if its automated-access protection blocks a direct fetch.
