import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('qr_detection'),
        'config',
        'camera_params.yaml',
    )

    return LaunchDescription([
        Node(
            package='qr_detection',
            executable='camera_node',
            name='camera_node',
            output='screen',
            parameters=[config],
        ),
        Node(
            package='qr_detection',
            executable='detection_node',
            name='detection_node',
            output='screen',
        ),
        Node(
            package='qr_detection',
            executable='coordinate_node',
            name='coordinate_node',
            output='screen',
            parameters=[config],
        ),
        Node(
            package='qr_detection',
            executable='sender_node',
            name='sender_node',
            output='screen',
        ),
        Node(
            package='qr_detection',
            executable='receiver_node',
            name='receiver_node',
            output='screen',
        ),
    ])
