import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point


class ReceiverNode(Node):
    def __init__(self):
        super().__init__('receiver_node')
        self.publisher_ = self.create_publisher(Point, 'qr/received_coordinates', 10)

    def run(self):
        pass


def main(args=None):
    rclpy.init(args=args)
    node = ReceiverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
