import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point


class CoordinateNode(Node):
    def __init__(self):
        super().__init__('coordinate_node')
        self.subscription = self.create_subscription(
            String, 'qr/data', self.qr_callback, 10)
        self.publisher_ = self.create_publisher(Point, 'qr/coordinates', 10)

    def qr_callback(self, msg):
        pass


def main(args=None):
    rclpy.init(args=args)
    node = CoordinateNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
