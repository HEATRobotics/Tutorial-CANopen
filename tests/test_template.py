"""Maintainer checks validate the scaffold; they do not solve learner blanks."""
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


def test_numbered_blanks_and_lesson_references():
    blanks = set()
    for path in (ROOT / 'ros2_ws/src').rglob('*.py'):
        blanks.update(re.findall(r"TODO\('([MHC]\d+)['\)]", path.read_text()))
    expected = {f'M{i:02}' for i in range(1, 4)} | {f'H{i:02}' for i in range(1, 4)} | {
        f'C{i:02}' for i in range(1, 4)}
    assert blanks == expected
    docs = '\n'.join(p.read_text() for p in (ROOT / 'docs').glob('*.md'))
    assert all(blank in docs for blank in expected)


def test_blanks_only_live_in_three_node_files():
    paths = [p for p in (ROOT / 'ros2_ws/src').rglob('*.py')
             if re.search(r"TODO\('[MHC]\d+", p.read_text())]
    assert len(paths) == 3 and all(p.name == 'node.py' for p in paths)
