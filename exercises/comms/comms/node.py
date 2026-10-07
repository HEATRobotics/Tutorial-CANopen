"""Lesson 05: normalized commands -> rpm -> ESCON2 CANopen SDOs.

Supplied code handles startup checks, explicit arming, watchdog, and stop.
Fill C06/C07 to connect the ROS callback to that policy.
"""
import json
import rclpy
from rclpy.node import Node
from interfaces.msg import DriveCommand
from std_msgs.msg import String
from std_srvs.srv import Trigger
from .blanks import TODO
from .mixing import mix
from .can_sender import TutorialDrive
from .support.controller import Controller, positive
from .support.drive import SimulatedDrive


class Comms(Node):
    def __init__(self):
        super().__init__('comms')
        defaults = dict(simulate=True, hardware_ready=False, channel='can0',
                        bitrate=1000000, motor_ids=[1, 3, 2, 4],
                        enabled_motor_ids=[1, 3, 2, 4], directions=[1, 1, 1, 1],
                        max_speed_rpm=0.0, command_timeout=0.5)
        for name, value in defaults.items():
            self.declare_parameter(name, value)
        p = lambda name: self.get_parameter(name).value
        self.controls, self.drives, self.slots = [], [], []
        self.fault = None
        self.simulated = p('simulate')
        try:
            speed = positive(p('max_speed_rpm'), 'max_speed_rpm')
            timeout = positive(p('command_timeout'), 'command_timeout')
            if speed > 6000 or timeout <= 0.05:
                raise ValueError('Speed must be <= 6000; timeout must exceed 0.05 s polling')
            ids, selected = list(p('motor_ids')), list(p('enabled_motor_ids'))
            self.directions = list(p('directions'))
            if len(ids) != 4 or len(set(ids)) != 4 or any(not 1 <= i <= 127 for i in ids):
                raise ValueError('motor_ids: four unique IDs in FL, BL, FR, BR order')
            if not selected or len(set(selected)) != len(selected) or any(i not in ids for i in selected):
                raise ValueError('enabled_motor_ids: nonempty, unique subset of motor_ids')
            if len(self.directions) != 4 or any(d not in (-1, 1) for d in self.directions):
                raise ValueError('directions: four signs in FL, BL, FR, BR order')
            if not self.simulated and not p('hardware_ready'):
                raise ValueError('Commission hardware before setting hardware_ready:=true')
            if p('bitrate') <= 0:
                raise ValueError('bitrate must be positive')
            for slot, motor_id in enumerate(ids):
                if motor_id not in selected:
                    continue
                drive = SimulatedDrive() if self.simulated else TutorialDrive(
                    p('channel'), motor_id, p('bitrate'))
                self.drives.append(drive)
                control = Controller(drive, speed, timeout)
                self.controls.append(control)
                self.slots.append(slot)
                control.prepare()
            self.ids = [ids[slot] for slot in self.slots]
            self.speed = speed
            self.status = self.create_publisher(String, '/drive/status', 1)
            # C06: DriveCommand subscription on /drive/normalized, self.on_command, depth 1.
            self.subscription = TODO('C06')
            self.create_service(Trigger, '/drive/arm', self.arm)
            self.create_service(Trigger, '/drive/stop', self.stop)
            self.timer = self.create_timer(0.05, self.poll)
            self.get_logger().info('SIMULATION ready, disabled' if self.simulated else 'HARDWARE ready, disabled')
        except BaseException:
            self.cleanup()
            super().destroy_node()
            raise

    def fail(self, reason):
        self.fault = str(reason)
        for control in self.controls:
            control.fail(reason)
        self.get_logger().error(self.fault)

    def on_command(self, msg):
        if self.fault or not all(c.armed for c in self.controls):
            return
        try:
            levels = mix(msg.forward, msg.turn)
            for control, slot in zip(self.controls, self.slots):
                # C07: level at slot * configured rpm limit * mounting direction.
                rpm = TODO('C07')
                if not control.command(rpm):
                    raise RuntimeError(control.fault or 'Drive rejected command')
        except Exception as exc:
            self.fail(exc)

    def arm(self, request, response):
        try:
            if self.fault:
                raise RuntimeError(self.fault + '; restart required')
            if any(c.armed for c in self.controls):
                raise RuntimeError('Already armed; stop first')
            for control in self.controls:
                control.arm()
            response.success, response.message = True, 'Armed at zero; command watchdog active'
        except Exception as exc:
            self.fail(exc)
            response.success, response.message = False, str(exc)
        return response

    def stop(self, request, response):
        errors = [error for c in self.controls for error in c.stop()]
        if errors:
            self.fault = '; '.join(errors)
        response.success = not errors
        response.message = self.fault or 'Stop writes acknowledged; voltage disabled'
        return response

    def poll(self):
        rpms = [c.poll() for c in self.controls]
        faults = [c.fault for c in self.controls if c.fault]
        if faults and not self.fault:
            self.fail('; '.join(faults))
        self.status.publish(String(data=json.dumps(dict(
            simulated=self.simulated, armed=all(c.armed for c in self.controls),
            fault=self.fault, motor_ids=self.ids, actual_rpm=rpms))))

    def cleanup(self):
        for control in self.controls:
            errors = control.stop()
            if errors:
                self.get_logger().error('Stop unconfirmed: ' + '; '.join(errors))
        for drive in self.drives:
            try:
                drive.close()
            except Exception as exc:
                self.get_logger().error(str(exc))

    def destroy_node(self):
        self.timer.cancel()
        self.cleanup()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = Comms()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
