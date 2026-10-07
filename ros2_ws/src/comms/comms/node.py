"""15-minute exercise: subscribe, convert normalized levels to rpm, send.

CANopen protocol, mixing, watchdog, arm/stop and cleanup are already supplied.
"""
import rclpy
from interfaces.msg import DriveCommand
from .mixing import mix
from .support.runtime import CommsRuntime


class Comms(CommsRuntime):
    def connect_input(self):
        # C01: the helper output topic name, as a string.
        return self.create_subscription(
            DriveCommand, '/drive/normalized', self.on_command, 1)

    def mix_inputs(self, forward, turn):
        # Provided: bound the differential wheel mix in FL, BL, FR, BR order.
        return mix(forward, turn)

    def target_rpm(self, level, direction):
        # C02: multiply level * self.speed * direction.
        return level * self.speed * direction

    def send_target(self, control, rpm):
        # C03: return control.command(rpm), which performs the CANopen transfer.
        return control.command(rpm)


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = Comms()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
