"""15-minute exercise: clamp each finite axis and publish a fresh message."""
import math
import rclpy
from rclpy.node import Node
from interfaces.msg import DriveCommand
from .blanks import TODO


class Helper(Node):
    def __init__(self):
        super().__init__('helper')
        self.publisher = self.create_publisher(DriveCommand, '/drive/normalized', 1)
        self.subscription = self.create_subscription(
            DriveCommand, '/drive/raw', self.on_command, 1)

    def on_command(self, msg):
        output = DriveCommand()
        if not (math.isfinite(msg.forward) and math.isfinite(msg.turn)):
            output.forward = output.turn = 0.0
        else:
            # H01: clamp msg.forward with max(-1.0, min(1.0, VALUE)).
            output.forward = TODO('H01')
            # H02: clamp msg.turn using the same pattern.
            output.turn = TODO('H02')
        # H03: publish output with self.publisher. No timer/repeated stale messages.
        TODO('H03')


def main(args=None):
    rclpy.init(args=args)
    node = Helper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
