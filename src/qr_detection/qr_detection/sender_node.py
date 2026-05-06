import rclpy
from geometry_msgs.msg import Point
from rclpy.node import Node


class SenderNode(Node):
    def __init__(self):
        super().__init__('sender_node')
        self.subscription = self.create_subscription(
            Point, 'qr/coordinates', self.coordinate_callback, 10)

    def coordinate_callback(self, msg):
        self.get_logger().info(
            f'Sending QR coordinate: x={msg.x:.3f}, y={msg.y:.3f}, z={msg.z:.3f}'
        )
        # TODO: Implement actual transmission (e.g. MAVLink, MAVROS setpoint, serial)


def main(args=None):
    rclpy.init(args=args)
    node = SenderNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
