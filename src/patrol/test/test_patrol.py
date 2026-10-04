from geometry_msgs.msg import Twist
from patrol.patrol_node import compute_cmd_vel, validate_parameter_value
from turtlesim.msg import Pose


def test_compute_cmd_vel_before_first_pose():
    msg = compute_cmd_vel(None)
    assert isinstance(msg, Twist)
    assert msg.linear.x == 0.0
    assert msg.linear.y == 0.0
    assert msg.linear.z == 0.0
    assert msg.angular.x == 0.0
    assert msg.angular.y == 0.0
    assert msg.angular.z == 0.0


def test_compute_cmd_vel_after_pose_default():
    pose = Pose(x=5.5, y=5.5, theta=0.0, linear_velocity=0.0, angular_velocity=0.0)
    msg = compute_cmd_vel(pose)
    assert isinstance(msg, Twist)
    assert msg.linear.x == 0.5
    assert msg.linear.y == 0.0
    assert msg.linear.z == 0.0
    assert msg.angular.x == 0.0
    assert msg.angular.y == 0.0
    assert msg.angular.z == 0.3


def test_compute_cmd_vel_with_custom_params():
    pose = Pose(x=5.5, y=5.5, theta=0.0, linear_velocity=0.0, angular_velocity=0.0)
    msg = compute_cmd_vel(pose, linear_speed=0.8, turn_rate=-0.5)
    assert msg.linear.x == 0.8
    assert msg.angular.z == -0.5


def test_validate_parameter_publish_hz():
    # Valid frequencies
    valid, _ = validate_parameter_value('publish_hz', 10.0)
    assert valid
    valid, _ = validate_parameter_value('publish_hz', 5.0)
    assert valid
    valid, _ = validate_parameter_value('publish_hz', 1.0)
    assert valid
    valid, _ = validate_parameter_value('publish_hz', 30.0)
    assert valid

    # Invalid: zero
    valid, reason = validate_parameter_value('publish_hz', 0.0)
    assert not valid
    assert '1.0 and 30.0' in reason

    # Invalid: negative
    valid, reason = validate_parameter_value('publish_hz', -5.0)
    assert not valid
    assert '1.0 and 30.0' in reason

    # Invalid: greater than 30
    valid, reason = validate_parameter_value('publish_hz', 50.0)
    assert not valid
    assert '1.0 and 30.0' in reason

    # Invalid: NaN and Inf
    valid, _ = validate_parameter_value('publish_hz', float('nan'))
    assert not valid
    valid, _ = validate_parameter_value('publish_hz', float('inf'))
    assert not valid


def test_validate_parameter_linear_speed():
    valid, _ = validate_parameter_value('linear_speed', 0.5)
    assert valid
    valid, _ = validate_parameter_value('linear_speed', 0.0)
    assert valid
    valid, _ = validate_parameter_value('linear_speed', 1.0)
    assert valid

    valid, _ = validate_parameter_value('linear_speed', -0.1)
    assert not valid
    valid, _ = validate_parameter_value('linear_speed', 1.5)
    assert not valid


def test_validate_parameter_turn_rate():
    valid, _ = validate_parameter_value('turn_rate', 0.3)
    assert valid
    valid, _ = validate_parameter_value('turn_rate', -1.0)
    assert valid
    valid, _ = validate_parameter_value('turn_rate', 1.0)
    assert valid

    valid, _ = validate_parameter_value('turn_rate', -1.5)
    assert not valid
    valid, _ = validate_parameter_value('turn_rate', 1.5)
    assert not valid
