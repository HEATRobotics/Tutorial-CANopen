"""Maintainer checks validate the scaffold; they do not solve learner blanks."""
import ast
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def test_python_starters_parse():
    for path in (ROOT / 'exercises').rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))


def test_exactly_four_package_manifests():
    manifests = list((ROOT / 'exercises').glob('*/package.xml'))
    assert {ET.parse(p).getroot().findtext('name') for p in manifests} == {
        'interfaces', 'maxon_controller', 'helper', 'comms'}


def test_numbered_blanks_and_lesson_references():
    blanks = set()
    for path in (ROOT / 'exercises').rglob('*.py'):
        blanks.update(re.findall(r"TODO\('([MHC]\d+)['\)]", path.read_text()))
    expected = {f'M{i:02}' for i in range(1, 6)} | {f'H{i:02}' for i in range(1, 8)} | {
        f'C{i:02}' for i in range(1, 8)}
    assert blanks == expected
    docs = '\n'.join(p.read_text() for p in (ROOT / 'docs').glob('*.md'))
    assert all(blank in docs for blank in expected | {'I01', 'I02'})


def test_workspace_location_exists():
    # This check remains valid after learners create their own packages.
    assert (ROOT / 'ros2_ws/src/.gitkeep').is_file()
