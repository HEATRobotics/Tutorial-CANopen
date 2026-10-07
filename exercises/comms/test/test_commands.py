import math
import pytest
from comms.mixing import mix
from comms.encoding import encode_sdo


@pytest.mark.parametrize('forward,turn,expected', [
    (0.0, 0.0, [0.0]*4), (0.5, 0.0, [0.5]*4),
    (0.0, 0.5, [-0.5, -0.5, 0.5, 0.5]),
    (1.0, 1.0, [0.0, 0.0, 1.0, 1.0]),
    (-1.0, -1.0, [0.0, 0.0, -1.0, -1.0]),
])
def test_mix(forward, turn, expected):
    assert mix(forward, turn) == expected


@pytest.mark.parametrize('forward,turn', [(1.1, 0), (math.nan, 0), (0, math.inf)])
def test_comms_rejects_invalid_input(forward, turn):
    with pytest.raises(ValueError):
        mix(forward, turn)


def test_signed_sdo_encoding():
    assert encode_sdo(-10, 4, True) == b'\xf6\xff\xff\xff'
    assert encode_sdo(15, 2) == b'\x0f\x00'
    with pytest.raises(OverflowError):
        encode_sdo(256, 1)
