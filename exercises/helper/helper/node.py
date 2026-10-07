"""Republish only on input callbacks: never refresh a stale upstream command."""
import rclpy
from rclpy.node import Node
from interfaces.msg import DriveCommand
from .normalization import normalize
from .blanks import TODO


class Helper(Node):
    def __init__(self):
        super().__init__('helper')
        # H04: publisher on /drive/normalized, DriveCommand, depth 1.
        self.publisher = TODO('H04')
        # H05: subscribe to /drive/raw with self.on_command, depth 1.
        self.subscription = TODO('H05')

    def on_command(self, msg):
        output = DriveCommand()
        # H06: call normalize with the two received fields.
        output.forward, output.turn = TODO('H06')
        # H07: publish output. Do not add a periodic republisher.
        TODO('H07')


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = Helper()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
