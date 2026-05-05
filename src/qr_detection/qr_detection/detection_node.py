import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge


class DetectionNode(Node):
    def __init__(self):
        super().__init__('detection_node')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10)
        self.publisher_ = self.create_publisher(String, 'qr/data', 10)

    def image_callback(self, msg):
        pass


def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
