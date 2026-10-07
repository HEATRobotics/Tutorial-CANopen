#!/usr/bin/env python3
"""Launch completed student nodes in simulation and test the complete pipeline.

Run with no other tutorial nodes running. Never starts hardware.
"""
import json
import os
import signal
import subprocess
import tempfile
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger
from interfaces.msg import DriveCommand

rclpy.init()
node = Node('tutorial_pipeline_check')
status, raw, normalized = {}, {}, {}
node.create_subscription(String, '/drive/status',
                         lambda msg: status.update(json.loads(msg.data)), 1)
node.create_subscription(DriveCommand, '/drive/raw',
                         lambda msg: raw.update(forward=msg.forward, turn=msg.turn), 1)
node.create_subscription(DriveCommand, '/drive/normalized',
                         lambda msg: normalized.update(forward=msg.forward, turn=msg.turn), 1)
arm = node.create_client(Trigger, '/drive/arm')
stop = node.create_client(Trigger, '/drive/stop')
processes, logs = [], []


def wait_for(predicate, seconds=15):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        rclpy.spin_once(node, timeout_sec=0.02)
        if predicate():
            return
    raise AssertionError(f'Timed out: status={status}, raw={raw}, normalized={normalized}')


def service(client):
    assert client.wait_for_service(timeout_sec=10)
    future = client.call_async(Trigger.Request())
    wait_for(future.done)
    return future.result()


def start(package, parameters):
    log = tempfile.TemporaryFile(mode='w+t')
    logs.append(log)
    process = subprocess.Popen(['ros2', 'run', package, 'node', '--ros-args', *parameters],
                               stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    processes.append(process)
    return process


def terminate(process):
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGINT)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)


try:
    # Allow discovery before checking for another controller with the same names.
    end = time.monotonic() + 1.0
    while time.monotonic() < end:
        rclpy.spin_once(node, timeout_sec=0.05)
    assert not ({'maxon_controller', 'helper', 'comms'} & set(node.get_node_names())), \
        'Stop existing tutorial nodes before running this test'
    start('comms', ['-p', 'simulate:=true', '-p', 'max_speed_rpm:=100.0'])
    start('helper', [])
    publisher = start('maxon_controller', ['-p', 'forward:=2.0', '-p', 'turn:=0.5'])
    wait_for(lambda: status.get('simulated') and raw and normalized)
    assert not status['armed'] and status['actual_rpm'] == [0.0]*4
    assert raw == {'forward': 2.0, 'turn': 0.5}
    assert normalized == {'forward': 1.0, 'turn': 0.5}
    result = service(arm)
    assert result.success, result.message
    wait_for(lambda: status['actual_rpm'] == [33.0, 33.0, 100.0, 100.0])
    result = service(stop)
    assert result.success, result.message
    wait_for(lambda: not status['armed'] and status['actual_rpm'] == [0.0]*4)
    result = service(arm)
    assert result.success, result.message
    wait_for(lambda: status['armed'])
    terminate(publisher)
    wait_for(lambda: status.get('fault') and not status['armed'])
    assert 'timeout' in status['fault'].lower()
    result = service(arm)
    assert not result.success
    print('PASS: custom message, clamp, four-motor rpm mix, stop, upstream-loss watchdog')
except BaseException:
    for process in reversed(processes):
        terminate(process)
    for log in logs:
        log.seek(0)
        print(log.read())
    raise
finally:
    for process in reversed(processes):
        terminate(process)
    for log in logs:
        log.close()
    node.destroy_node()
    rclpy.shutdown()
