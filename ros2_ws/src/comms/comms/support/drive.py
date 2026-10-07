"""Typed SDO adapter and hardware-free backend. No commissioning writes."""
import time


class CanopenDrive:
    def __init__(self, channel, node_id, bitrate, sdo_timeout=0.1, state_timeout=2.0):
        import canopen
        self.network = canopen.Network()
        self.state_timeout = state_timeout
        try:
            self.network.connect(interface='socketcan', channel=channel, bitrate=bitrate)
            self.motor = self.network.add_node(node_id, None)
            self.motor.sdo.RESPONSE_TIMEOUT = sdo_timeout
            self.motor.sdo.MAX_RETRIES = 1
        except BaseException:
            self.network.disconnect()
            raise

    def read(self, index, signed=False):
        return int.from_bytes(self.motor.sdo.upload(index, 0), 'little', signed=signed)

    def write(self, index, value, size, signed=False):
        self.motor.sdo.download(index, 0, int(value).to_bytes(size, 'little', signed=signed))

    def wait_state(self, expected):
        deadline = time.monotonic() + self.state_timeout
        while time.monotonic() < deadline:
            status = self.read(0x6041)
            if status & 0x08:
                raise RuntimeError(f'Drive fault: statusword=0x{status:04x}; no automatic reset')
            if status & 0x6F == expected:
                return
            time.sleep(0.01)
        raise TimeoutError(f'Drive did not reach state 0x{expected:02x}')

    def operational(self):
        self.motor.nmt.state = 'OPERATIONAL'

    def check(self):
        self.network.check()
        if self.motor.emcy.active:
            raise RuntimeError('Drive emergency active')

    def close(self):
        self.network.disconnect()


class SimulatedDrive:
    """Instantaneous velocity model, not an electrical/mechanical simulation."""
    def __init__(self):
        self.values = {0x6041: 0x40, 0x60A9: 0x00B44700, 0x6080: 6000,
                       0x607F: 6000, 0x6061: 0, 0x606C: 0, 0x60FF: 0}
        self.writes = []

    def read(self, index, signed=False):
        return self.values[index]

    def write(self, index, value, size, signed=False):
        int(value).to_bytes(size, 'little', signed=signed)
        self.writes.append((index, value, size, signed))
        self.values[index] = value
        if index == 0x6060:
            self.values[0x6061] = value
        if index == 0x6040:
            self.values[0x6041] = {0: 0x40, 6: 0x21, 7: 0x23,
                                   15: 0x27, 11: 0x07}[value]
            self.values[0x606C] = self.values[0x60FF] if value == 15 else 0

    def wait_state(self, expected):
        if self.read(0x6041) & 0x6F != expected:
            raise RuntimeError('Unexpected simulated drive state')

    def operational(self):
        pass

    def check(self):
        pass

    def close(self):
        pass
