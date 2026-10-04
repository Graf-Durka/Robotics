from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


def compute_cmd_vel(pose):
    msg = Twist()
    if pose is None:
        return msg
    msg.linear.x = 0.5
    msg.angular.z = 0.3
    return msg


class PatrolNode(Node):

    def __init__(self):
        super().__init__('patrol')
        self.latest_pose = None
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
        self.timer = self.create_timer(0.1, self.timer_callback)

    def pose_callback(self, msg: Pose):
        self.latest_pose = msg

    def timer_callback(self):
        msg = compute_cmd_vel(self.latest_pose)
        self.publisher.publish(msg)


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
