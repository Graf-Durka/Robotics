import math

from geometry_msgs.msg import Twist
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from turtlesim.msg import Pose


def validate_parameter_value(name: str, val):
    if val is None or not isinstance(val, (int, float)) or math.isnan(val) or math.isinf(val):
        return False, f'{name} must be a valid finite number'
    if name == 'linear_speed':
        if not (0.0 <= val <= 1.0):
            return False, 'linear_speed must be between 0.0 and 1.0'
    elif name == 'turn_rate':
        if not (-1.0 <= val <= 1.0):
            return False, 'turn_rate must be between -1.0 and 1.0'
    elif name == 'publish_hz':
        if not (1.0 <= val <= 30.0):
            return False, 'publish_hz must be between 1.0 and 30.0'
    return True, ''


def compute_cmd_vel(pose, linear_speed=0.5, turn_rate=0.3):
    msg = Twist()
    if pose is None:
        return msg
    msg.linear.x = float(linear_speed)
    msg.angular.z = float(turn_rate)
    return msg


class PatrolNode(Node):

    def __init__(self):
        super().__init__('patrol')
        self.latest_pose = None

        self.declare_parameter('linear_speed', 0.5)
        self.declare_parameter('turn_rate', 0.3)
        self.declare_parameter('publish_hz', 10.0)

        self.linear_speed = self.get_parameter('linear_speed').value
        self.turn_rate = self.get_parameter('turn_rate').value
        self.publish_hz = self.get_parameter('publish_hz').value

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        self.publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )
        self.timer = self.create_timer(1.0 / self.publish_hz, self.timer_callback)
        self.add_on_set_parameters_callback(self.parameters_callback)

    def pose_callback(self, msg: Pose):
        self.latest_pose = msg

    def timer_callback(self):
        msg = compute_cmd_vel(self.latest_pose, self.linear_speed, self.turn_rate)
        self.publisher.publish(msg)

    def parameters_callback(self, params):
        # Validate proposed parameters first
        for param in params:
            if param.name in ('linear_speed', 'turn_rate', 'publish_hz'):
                if param.type_ not in (Parameter.Type.DOUBLE, Parameter.Type.INTEGER):
                    return SetParametersResult(
                        successful=False,
                        reason=f'{param.name} must be a number'
                    )
                valid, reason = validate_parameter_value(param.name, param.value)
                if not valid:
                    return SetParametersResult(successful=False, reason=reason)

        # Apply changes only after all proposed parameters are validated
        new_hz = None
        for param in params:
            if param.name == 'linear_speed':
                self.linear_speed = float(param.value)
            elif param.name == 'turn_rate':
                self.turn_rate = float(param.value)
            elif param.name == 'publish_hz':
                new_hz = float(param.value)

        if new_hz is not None and new_hz != self.publish_hz:
            self.publish_hz = new_hz
            self.timer.cancel()
            self.timer.destroy()
            self.timer = self.create_timer(1.0 / self.publish_hz, self.timer_callback)

        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
