"""Single-drive control policy, independent of ROS for contract testing."""
import math
import time


def positive(value, name):
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f'{name} must be finite and positive')
    return value


class Controller:
    def __init__(self, drive, max_rpm, timeout=0.5, clock=time.monotonic):
        self.max_rpm = positive(max_rpm, 'max_speed_rpm')
        self.timeout = positive(timeout, 'command_timeout')
        if self.max_rpm > 6000:
            raise ValueError('Reference motor limit is 6000 rpm; verify your motor/mechanism')
        self.drive, self.clock = drive, clock
        self.armed = False
        self.fault = None
        self.last_command = None

    def prepare(self):
        self.drive.write(0x6040, 0, 2)
        self.drive.wait_state(0x40)
        self.drive.write(0x60FF, 0, 4, signed=True)
        if self.drive.read(0x60A9) != 0x00B44700:
            raise ValueError('Commission velocity units 0x60A9 as rpm (0x00B44700)')
        if self.max_rpm > min(self.drive.read(0x6080), self.drive.read(0x607F)):
            raise ValueError('Requested speed limit exceeds commissioned drive limits')
        self.drive.write(0x6060, 3, 1, signed=True)
        if self.drive.read(0x6061) != 3:
            raise RuntimeError('Profile velocity mode was not accepted')
        self.drive.operational()

    def stop(self):
        """Best effort quick stop, zero target, disable voltage, even after errors."""
        self.armed = False
        self.last_command = None
        errors = []
        for index, value, size in ((0x6040, 11, 2), (0x60FF, 0, 4), (0x6040, 0, 2)):
            try:
                self.drive.write(index, value, size)
            except Exception as exc:
                errors.append(str(exc))
        if errors:
            self.fault = 'Stop unconfirmed: ' + '; '.join(errors)
        return errors

    def fail(self, reason):
        errors = self.stop()
        self.fault = str(reason) + ('; stop unconfirmed: ' + '; '.join(errors) if errors else '')

    def arm(self):
        if self.fault:
            raise RuntimeError(self.fault + '; restart required')
        if self.armed:
            raise RuntimeError('Already armed')
        try:
            self.drive.write(0x60FF, 0, 4, signed=True)
            for word, state in ((6, 0x21), (7, 0x23), (15, 0x27)):
                self.drive.write(0x6040, word, 2)
                self.drive.wait_state(state)
            self.armed = True
            self.last_command = self.clock()
        except Exception as exc:
            self.fail(exc)
            raise

    def command(self, rpm):
        if self.fault or not self.armed:
            return False
        received = self.clock()
        try:
            # A queued command must not revive a timed-out drive.
            if received - self.last_command >= self.timeout:
                raise TimeoutError('Command timeout; restart required')
            if not math.isfinite(rpm) or abs(rpm) > self.max_rpm:
                raise ValueError('Target must be finite and within max_speed_rpm')
            self.drive.check()
            if self.drive.read(0x6041) & 0x6F != 0x27:
                raise RuntimeError('Drive is not operation enabled')
            # Preserve a fractional configured limit after integer rpm conversion.
            target = int(rpm)
            self.drive.write(0x60FF, target, 4, signed=True)
            if self.clock() - received >= self.timeout:
                raise TimeoutError('Command expired during SDO transfer')
            # ESCON2 PVM applies the target on the subsequent controlword write.
            self.drive.write(0x6040, 15, 2)
            self.last_command = received
            return True
        except Exception as exc:
            self.fail(exc)
            return False

    def poll(self):
        if self.fault:
            return None
        try:
            if self.armed and self.clock() - self.last_command >= self.timeout:
                raise TimeoutError('Command timeout; restart required')
            self.drive.check()
            status = self.drive.read(0x6041)
            if status & 8 or (self.armed and status & 0x6F != 0x27):
                raise RuntimeError(f'Drive fault/disabled: 0x{status:04x}')
            return float(self.drive.read(0x606C, signed=True))
        except Exception as exc:
            self.fail(exc)
            return None
