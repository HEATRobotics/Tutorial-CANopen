"""Provided bounded differential mix: FL, BL, FR, BR; positive turn is left."""
import math


def mix(forward, turn):
    if not all(math.isfinite(v) and abs(v) <= 1 for v in (forward, turn)):
        raise ValueError('comms requires finite normalized inputs')
    left, right = forward - turn, forward + turn
    scale = max(1.0, abs(left), abs(right))
    return [left / scale, left / scale, right / scale, right / scale]
