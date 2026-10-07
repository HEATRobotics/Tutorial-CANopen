"""Provided ESCON2 SDO integer encoding."""
def encode_sdo(value, size, signed=False):
    return int(value).to_bytes(size, 'little', signed=signed)
