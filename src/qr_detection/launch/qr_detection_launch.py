from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='qr_detection',
            executable='camera_node',
            name='camera_node',
            output='screen',
        ),
        Node(
            package='qr_detection',
            executable='detection_node',
            name='detection_node',
            output='screen',
        ),
    ])
