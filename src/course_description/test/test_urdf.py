"""Unit tests for course_ackermann URDF / xacro description."""

from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import pytest

# Ensure user site or local packages are accessible if run with python3 -s
_user_site = (
    Path.home()
    / '.local'
    / f'lib/python{sys.version_info.major}.{sys.version_info.minor}'
    / 'site-packages'
)
if _user_site.is_dir() and str(_user_site) not in sys.path:
    sys.path.insert(0, str(_user_site))

import xacro  # noqa: E402


def get_xacro_path() -> Path:
    """Return path to vehicle.urdf.xacro."""
    pkg_root = Path(__file__).resolve().parent.parent
    return pkg_root / 'urdf' / 'vehicle.urdf.xacro'


def parse_urdf_xml(xacro_path: Path) -> ET.Element:
    """Process xacro file and return XML root."""
    doc = xacro.process_file(str(xacro_path))
    xml_str = doc.toxml()
    return ET.fromstring(xml_str)


def test_urdf_parses_and_root_is_valid():
    """Verify xacro processing succeeds and generates valid robot element."""
    root = parse_urdf_xml(get_xacro_path())
    assert root.tag == 'robot'
    assert root.attrib.get('name') == 'course_ackermann'


def test_required_links_exist():
    """Verify that all required robot links are present."""
    root = parse_urdf_xml(get_xacro_path())
    link_names = {link.attrib['name'] for link in root.findall('link')}

    expected_links = {
        'base_link',
        'front_left_knuckle',
        'front_right_knuckle',
        'front_left_wheel',
        'front_right_wheel',
        'rear_left_wheel',
        'rear_right_wheel',
        'camera_link',
        'lidar_link',
        'imu_link',
    }
    missing = expected_links - link_names
    assert not missing, f'Missing required links: {missing}'


def test_sensor_parent_joints():
    """Verify that camera, lidar and imu have base_link as parent link."""
    root = parse_urdf_xml(get_xacro_path())

    joints = {
        j.attrib['name']: {
            'parent': j.find('parent').attrib['link'],
            'child': j.find('child').attrib['link'],
            'type': j.attrib.get('type'),
        }
        for j in root.findall('joint')
    }

    assert 'camera_joint' in joints
    assert joints['camera_joint']['parent'] == 'base_link'
    assert joints['camera_joint']['child'] == 'camera_link'
    assert joints['camera_joint']['type'] == 'fixed'

    # Defect test: lidar_joint must be attached to base_link, NOT camera_link
    assert 'lidar_joint' in joints
    assert joints['lidar_joint']['parent'] == 'base_link', (
        f"lidar_joint parent must be 'base_link', got '{joints['lidar_joint']['parent']}'"
    )
    assert joints['lidar_joint']['child'] == 'lidar_link'
    assert joints['lidar_joint']['type'] == 'fixed'

    assert 'imu_joint' in joints
    assert joints['imu_joint']['parent'] == 'base_link'
    assert joints['imu_joint']['child'] == 'imu_link'
    assert joints['imu_joint']['type'] == 'fixed'


def test_kinematic_dimensions():
    """Verify wheel base, wheel separation, and wheel radius dimensions."""
    root = parse_urdf_xml(get_xacro_path())

    joints = {j.attrib['name']: j for j in root.findall('joint')}

    fl_origin = [
        float(v) for v in joints['front_left_steering_joint'].find('origin').attrib['xyz'].split()
    ]
    rl_origin = [
        float(v) for v in joints['rear_left_wheel_joint'].find('origin').attrib['xyz'].split()
    ]

    wheel_base = fl_origin[0] - rl_origin[0]
    assert pytest.approx(0.8, rel=1e-3) == wheel_base, (
        f'Expected wheel_base 0.8, calculated {wheel_base}'
    )

    fr_origin = [
        float(v) for v in joints['front_right_steering_joint'].find('origin').attrib['xyz'].split()
    ]
    wheel_separation = fl_origin[1] - fr_origin[1]
    assert pytest.approx(0.62, rel=1e-3) == wheel_separation, (
        f'Expected wheel_separation 0.62, calculated {wheel_separation}'
    )

    # Check wheel radius in collision / visual
    wheel_link = next(
        link for link in root.findall('link') if link.attrib['name'] == 'front_left_wheel'
    )
    cylinder = wheel_link.find('.//cylinder')
    assert cylinder is not None
    assert pytest.approx(0.12, rel=1e-3) == float(cylinder.attrib['radius'])
    assert pytest.approx(0.07, rel=1e-3) == float(cylinder.attrib['length'])
