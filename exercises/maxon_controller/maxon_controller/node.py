"""Lesson 03: publish raw forward/turn inputs at 20 Hz."""
import rclpy
from rclpy.node import Node
from interfaces.msg import DriveCommand
from .blanks import TODO


class MaxonController(Node):
    def __init__(self):
        super().__init__('maxon_controller')
        self.declare_parameter('forward', 0.0)
        self.declare_parameter('turn', 0.0)
        # M01: create a DriveCommand publisher on /drive/raw, depth 1.
        self.publisher = TODO('M01')
        # M02: create a 0.05-second timer calling self.publish_command.
        self.timer = TODO('M02')

    def publish_command(self):
        msg = DriveCommand()
        # M03/M04: read the current parameter values, so ros2 param set works.
        msg.forward = TODO('M03')
        msg.turn = TODO('M04')
        # M05: publish the populated message (replace this statement).
        TODO('M05')


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = MaxonController()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
