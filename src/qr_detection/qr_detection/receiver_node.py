import rclpy
from geometry_msgs.msg import Point
from rclpy.node import Node


class ReceiverNode(Node):
    """Receives QR coordinates (e.g. from a ground-side link) and re-publishes into ROS2."""

    def __init__(self):
        super().__init__('receiver_node')
        # TODO: Replace this subscription with your actual transport
        # (e.g. serial, UDP, MAVLink) and call _publish() with the received Point.
        self.subscription = self.create_subscription(
            Point, 'qr/coordinates', self._on_received, 10)
        self.publisher_ = self.create_publisher(Point, 'qr/received_coordinates', 10)

    def _on_received(self, msg):
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Received and relayed coordinate: x={msg.x:.3f}, y={msg.y:.3f}, z={msg.z:.3f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = ReceiverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
