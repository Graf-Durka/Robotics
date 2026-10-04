from geometry_msgs.msg import Twist
from patrol.patrol_node import compute_cmd_vel
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


def test_compute_cmd_vel_after_pose():
    pose = Pose(x=5.5, y=5.5, theta=0.0, linear_velocity=0.0, angular_velocity=0.0)
    msg = compute_cmd_vel(pose)
    assert isinstance(msg, Twist)
    assert msg.linear.x == 0.5
    assert msg.linear.y == 0.0
    assert msg.linear.z == 0.0
    assert msg.angular.x == 0.0
    assert msg.angular.y == 0.0
    assert msg.angular.z == 0.3
