import rclpy
from rclpy.node import Node
from rclpy.qos import QoSHistoryPolicy, QoSProfile, QoSReliabilityPolicy
from turtlesim.msg import Pose


class PoseRelayNode(Node):

    def __init__(self):
        super().__init__('pose_relay')

        # Best effort publisher for sensor_pose
        sensor_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.publisher = self.create_publisher(
            Pose,
            'sensor_pose',
            sensor_qos
        )

        # Turtlesim publishes pose with reliable QoS by default
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

    def pose_callback(self, msg: Pose):
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PoseRelayNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
