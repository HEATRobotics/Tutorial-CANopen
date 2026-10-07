"""Student SDO adapter over the supplied ESCON2 state/stop policy."""
from .encoding import encode_sdo
from .support.drive import CanopenDrive
from .blanks import TODO


class TutorialDrive(CanopenDrive):
    def write(self, index, value, size, signed=False):
        data = encode_sdo(value, size, signed)
        # C05: download data to the supplied object index, subindex 0.
        TODO('C05')
