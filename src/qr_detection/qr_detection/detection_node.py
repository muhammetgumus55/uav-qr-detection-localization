import json

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class DetectionNode(Node):
    def __init__(self):
        super().__init__('detection_node')
        self.bridge = CvBridge()
        self.qr_detector = cv2.QRCodeDetector()
        self.subscription = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10)
        self.publisher_ = self.create_publisher(String, 'qr/data', 10)

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        data, points, _ = self.qr_detector.detectAndDecode(frame)

        if not data or points is None:
            return

        # Encode QR content and pixel corner positions as JSON so that
        # coordinate_node can run solvePnP without needing a custom message type.
        corners = points[0].tolist()
        payload = json.dumps({'data': data, 'corners': corners})
        self.publisher_.publish(String(data=payload))
        self.get_logger().info(f'QR detected: "{data}"')


def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
