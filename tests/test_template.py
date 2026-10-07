"""Checks for the completed test branch."""
import ast
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def test_python_starters_parse():
    for path in (ROOT / 'ros2_ws/src').rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))


def test_exactly_four_package_manifests():
    manifests = list((ROOT / 'ros2_ws/src').glob('*/package.xml'))
    assert {ET.parse(p).getroot().findtext('name') for p in manifests} == {
        'interfaces', 'maxon_controller', 'helper', 'comms'}


def test_completed_nodes_have_no_blanks():
    for path in (ROOT / 'ros2_ws/src').rglob('*.py'):
        assert not re.search(r"TODO\('[MHC]\d+", path.read_text()), str(path)


def test_three_completed_node_files():
    for package in ('maxon_controller', 'helper', 'comms'):
        path = ROOT / 'ros2_ws/src' / package / package / 'node.py'
        assert path.is_file()
        assert 'def main(' in path.read_text()
