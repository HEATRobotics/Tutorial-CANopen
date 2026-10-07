"""10-minute exercise: fill M01–M03, then publish raw forward/turn inputs."""
import rclpy
from rclpy.node import Node
from interfaces.msg import DriveCommand


class MaxonController(Node):
    def __init__(self):
        super().__init__('maxon_controller')
        self.declare_parameter('forward', 0.0)
        self.declare_parameter('turn', 0.0)
        self.publisher = self.create_publisher(DriveCommand, '/drive/raw', 1)
        self.timer = self.create_timer(0.05, self.publish_command)

    def publish_command(self):
        msg = DriveCommand()
        # M01: read self.get_parameter('forward').value as a float.
        msg.forward = float(self.get_parameter('forward').value)
        # M02: do the same for the 'turn' parameter.
        msg.turn = float(self.get_parameter('turn').value)
        # M03: publish msg with self.publisher.
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MaxonController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
