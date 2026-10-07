from unittest.mock import Mock
from comms.node import Comms


def test_subscribes_to_helper():
    node = object.__new__(Comms)
    node.create_subscription = Mock()
    node.connect_input()
    args = node.create_subscription.call_args.args
    assert args[1] == '/drive/normalized'
    assert args[2] == node.on_command and args[3] == 1


def test_level_to_signed_rpm():
    node = object.__new__(Comms)
    node.speed = 100.0
    assert node.target_rpm(0.25, -1) == -25.0


def test_calls_can_controller():
    node = object.__new__(Comms)
    control = Mock()
    control.command.return_value = True
    assert node.send_target(control, -25.0) is True
    control.command.assert_called_once_with(-25.0)
