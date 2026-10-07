import math
import pytest
from helper.normalization import normalize


@pytest.mark.parametrize('inputs,expected', [
    ((0.0, 0.0), (0.0, 0.0)), ((0.25, -0.5), (0.25, -0.5)),
    ((2.0, -3.0), (1.0, -1.0)), ((-2.0, 0.2), (-1.0, 0.2)),
    ((math.nan, 0.2), (0.0, 0.0)), ((0.2, math.inf), (0.0, 0.0)),
])
def test_normalize(inputs, expected):
    assert normalize(*inputs) == expected
