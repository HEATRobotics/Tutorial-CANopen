"""Lesson 04: clamp each axis; reject nonfinite pairs by outputting zero."""
import math
from .blanks import TODO


def normalize(forward, turn):
    # H01: true only when BOTH inputs are finite.
    if not (TODO('H01')):
        return 0.0, 0.0
    # H02/H03: clamp each finite input to [-1.0, 1.0].
    return TODO('H02'), TODO('H03')
