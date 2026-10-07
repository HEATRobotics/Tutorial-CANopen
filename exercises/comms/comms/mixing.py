"""Lesson 05: positive turn is left; outputs are FL, BL, FR, BR."""
import math
from .blanks import TODO


def mix(forward, turn):
    if not all(math.isfinite(v) and abs(v) <= 1 for v in (forward, turn)):
        raise ValueError('comms requires finite normalized inputs')
    # C01/C02: differential mix: left=forward-turn, right=forward+turn.
    left = TODO('C01')
    right = TODO('C02')
    # C03: one common divisor >= 1, bounding BOTH wheel levels.
    scale = TODO('C03')
    return [left / scale, left / scale, right / scale, right / scale]
