"""Exercise the actual student callback without starting a ROS graph."""
import math
from types import SimpleNamespace
from unittest.mock import Mock
import pytest
from helper.node import Helper


@pytest.mark.parametrize('inputs,expected', [
    ((0.0, 0.0), (0.0, 0.0)), ((0.25, -0.5), (0.25, -0.5)),
    ((2.0, -3.0), (1.0, -1.0)), ((-2.0, 0.2), (-1.0, 0.2)),
    ((math.nan, 0.2), (0.0, 0.0)), ((0.2, math.inf), (0.0, 0.0)),
])
def test_callback(inputs, expected):
    node = object.__new__(Helper)
    node.publisher = Mock()
    node.on_command(SimpleNamespace(forward=inputs[0], turn=inputs[1]))
    output = node.publisher.publish.call_args.args[0]
    assert (output.forward, output.turn) == pytest.approx(expected)
