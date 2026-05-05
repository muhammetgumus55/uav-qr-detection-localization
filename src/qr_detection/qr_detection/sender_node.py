import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point


class SenderNode(Node):
    def __init__(self):
        super().__init__('sender_node')
        self.subscription = self.create_subscription(
            Point, 'qr/coordinates', self.coordinate_callback, 10)

    def coordinate_callback(self, msg):
        pass


def main(args=None):
    rclpy.init(args=args)
    node = SenderNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
