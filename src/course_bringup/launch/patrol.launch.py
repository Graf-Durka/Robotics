from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='robot_a',
        description='Namespace for nodes and topics'
    )
    subscriber_reliability_arg = DeclareLaunchArgument(
        'subscriber_reliability',
        default_value='best_effort',
        description='Reliability QoS policy for patrol subscriber (reliable or best_effort)'
    )
    record_arg = DeclareLaunchArgument(
        'record',
        default_value='false',
        description='Whether to record topics to MCAP bag'
    )
    bag_dir_arg = DeclareLaunchArgument(
        'bag_dir',
        default_value='evidence/pr05/bag',
        description='Output directory for MCAP recording'
    )

    namespace = LaunchConfiguration('namespace')
    subscriber_reliability = LaunchConfiguration('subscriber_reliability')
    record = LaunchConfiguration('record')
    bag_dir = LaunchConfiguration('bag_dir')

    pose_relay_node = Node(
        package='course_bringup',
        executable='pose_relay',
        namespace=namespace,
        name='pose_relay',
        output='screen'
    )

    patrol_node = Node(
        package='patrol',
        executable='patrol',
        namespace=namespace,
        name='patrol',
        parameters=[{
            'subscriber_reliability': subscriber_reliability
        }],
        remappings=[
            ('cmd_vel', '/turtle1/cmd_vel')
        ],
        output='screen'
    )

    record_topic = PathJoinSubstitution(['/', namespace, 'sensor_pose'])

    bag_record_process = ExecuteProcess(
        condition=IfCondition(record),
        cmd=[
            'ros2', 'bag', 'record',
            '-s', 'mcap',
            '-o', bag_dir,
            '--topics', record_topic
        ],
        output='screen'
    )

    return LaunchDescription([
        namespace_arg,
        subscriber_reliability_arg,
        record_arg,
        bag_dir_arg,
        pose_relay_node,
        patrol_node,
        bag_record_process
    ])
