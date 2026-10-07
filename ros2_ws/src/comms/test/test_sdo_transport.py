"""Verify the supplied transport over real canopen-python SDOs on a virtual CAN bus."""
from uuid import uuid4
import canopen
from canopen import objectdictionary as od
from comms.can_sender import TutorialDrive
from comms.support.controller import Controller


def test_student_sdo_transport(monkeypatch):
    channel = 'tutorial-' + uuid4().hex
    dictionary = od.ObjectDictionary()
    initial = {0x6040: (od.UNSIGNED16, 0), 0x6041: (od.UNSIGNED16, 0x40),
               0x60FF: (od.INTEGER32, 0), 0x606C: (od.INTEGER32, 0),
               0x6060: (od.INTEGER8, 0), 0x6061: (od.INTEGER8, 0),
               0x60A9: (od.UNSIGNED32, 0x00B44700),
               0x6080: (od.UNSIGNED32, 6000), 0x607F: (od.UNSIGNED32, 6000)}
    for index, (kind, value) in initial.items():
        var = od.Variable(f'object_{index:x}', index, 0)
        var.data_type, var.access_type, var.default = kind, 'rw', value
        dictionary.add_object(var)
    server_net = canopen.Network()
    server_net.connect(interface='virtual', channel=channel)
    server = server_net.add_node(canopen.LocalNode(1, dictionary))
    commands = []

    def on_write(index, subindex, data, **kwargs):
        value = int.from_bytes(data, 'little', signed=index in (0x60FF, 0x6060))
        if index in (0x6040, 0x60FF):
            commands.append((index, value))
        if index == 0x6060:
            server.set_data(0x6061, 0, data)
        if index == 0x6040:
            state = {0: 0x40, 6: 0x21, 7: 0x23, 15: 0x27, 11: 0x07}[value]
            server.set_data(0x6041, 0, state.to_bytes(2, 'little'))
            server.set_data(0x606C, 0, server.get_data(0x60FF, 0) if value == 15 else bytes(4))
    server.add_write_callback(on_write)
    connect = canopen.Network.connect
    monkeypatch.setattr(canopen.Network, 'connect',
                        lambda self, **kwargs: connect(self, interface='virtual', channel=channel))
    drive = None
    try:
        drive = TutorialDrive('unused', 1, 1000000, sdo_timeout=0.2)
        control = Controller(drive, 100.0, timeout=2.0)
        control.prepare()
        control.arm()
        assert control.command(-23)
        assert control.poll() == -23
        assert commands[-2:] == [(0x60FF, -23), (0x6040, 15)]
        assert not control.stop()
        assert control.poll() == 0
    finally:
        if drive is not None:
            drive.close()
        server_net.disconnect()
