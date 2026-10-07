"""Provided typed CANopen transport; hardware protocol is not a learner blank."""
from .encoding import encode_sdo
from .support.drive import CanopenDrive


class TutorialDrive(CanopenDrive):
    def write(self, index, value, size, signed=False):
        self.motor.sdo.download(index, 0, encode_sdo(value, size, signed))
