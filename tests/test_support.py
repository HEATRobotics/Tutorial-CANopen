import math
import pytest
from comms.support.controller import Controller
from comms.support.drive import SimulatedDrive, CanopenDrive


@pytest.fixture
def rig():
    now = [10.0]
    drive = SimulatedDrive()
    control = Controller(drive, 100.0, clock=lambda: now[0])
    control.prepare()
    return control, drive, now


def test_startup_disabled_and_commands_require_arm(rig):
    c, d, _ = rig
    assert d.read(0x6041) == 0x40
    assert not c.command(20)
    assert d.read(0x606C) == 0
    c.arm()
    assert c.command(-12.8)
    assert d.writes[-2:] == [(0x60FF, -12, 4, True), (0x6040, 15, 2, False)]
    assert c.poll() == -12


@pytest.mark.parametrize('target', [101, -101, math.nan, math.inf, -math.inf])
def test_invalid_target_stops_and_latches(rig, target):
    c, d, _ = rig
    c.arm()
    assert not c.command(target)
    assert c.fault and not c.armed and d.read(0x6041) == 0x40
    assert not c.command(10)
    with pytest.raises(RuntimeError):
        c.arm()


def test_timeout_stops_and_cannot_be_revived_by_queued_command(rig):
    c, d, now = rig
    c.arm()
    c.command(20)
    now[0] += 0.5
    assert not c.command(20)
    assert 'timeout' in c.fault.lower()
    assert d.read(0x606C) == 0


def test_watchdog_and_user_stop(rig):
    c, d, now = rig
    c.arm()
    c.command(20)
    assert not c.stop()
    assert not c.fault and not c.armed
    c.arm()
    now[0] += 0.6
    assert c.poll() is None and c.fault
    assert d.read(0x6041) == 0x40


def test_late_sdo_does_not_apply_target(rig):
    c, d, now = rig
    c.arm()
    original = d.write
    def delayed(index, value, size, signed=False):
        original(index, value, size, signed)
        if index == 0x60FF:
            now[0] += 0.6
    d.write = delayed
    d.writes.clear()
    assert not c.command(10)
    assert not any(i == 0x6040 and v == 15 for i, v, _, _ in d.writes)
    assert c.fault and d.read(0x6041) == 0x40


def test_stop_attempts_disable_after_bus_error(rig):
    c, d, _ = rig
    c.arm()
    original = d.write
    def reject_quick_stop(index, value, size, signed=False):
        if index == 0x6040 and value == 11:
            raise TimeoutError('bus failure')
        original(index, value, size, signed)
    d.write = reject_quick_stop
    assert c.stop()
    assert c.fault and d.read(0x6041) == 0x40


@pytest.mark.parametrize('index,value', [(0x60A9, 0), (0x6080, 99), (0x607F, 99)])
def test_rejects_uncommissioned_units_or_limits(rig, index, value):
    c, d, _ = rig
    d.values[index] = value
    with pytest.raises(ValueError):
        c.prepare()
    assert not c.armed


def test_drive_fault_latches(rig):
    c, d, _ = rig
    c.arm()
    d.values[0x6041] = 8
    assert c.poll() is None
    assert c.fault and not c.armed


@pytest.mark.parametrize('speed', [0, -1, math.nan, math.inf, 6001])
def test_bad_configuration_rejected(speed):
    with pytest.raises(ValueError):
        Controller(SimulatedDrive(), speed)


def test_real_adapter_signed_bytes_and_state_fault():
    from unittest.mock import Mock
    d = object.__new__(CanopenDrive)
    d.motor = Mock()
    d.state_timeout = 0.1
    d.write(0x60FF, -10, 4, signed=True)
    d.motor.sdo.download.assert_called_once_with(0x60FF, 0, b'\xf6\xff\xff\xff')
    d.motor.sdo.upload.return_value = b'\xf6\xff\xff\xff'
    assert d.read(0x606C, signed=True) == -10
    d.motor.sdo.upload.return_value = b'\x08\x00'
    with pytest.raises(RuntimeError, match='Drive fault'):
        d.wait_state(0x27)
