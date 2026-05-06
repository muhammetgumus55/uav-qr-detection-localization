import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

PUBLISH_HZ = 30
LOG_EVERY_N_FRAMES = PUBLISH_HZ  # log success once per second


class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.bridge = CvBridge()
        self._frame_count = 0
        self._consecutive_failures = 0

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error(
                'Failed to open camera at index 0 — check that a camera device is available'
            )
        else:
            self.get_logger().info('Camera opened successfully (index 0)')

        self.timer = self.create_timer(1.0 / PUBLISH_HZ, self.timer_callback)
        self.get_logger().info(f'Camera node started, publishing at ~{PUBLISH_HZ} Hz on /camera/image_raw')

    def timer_callback(self):
        if not self.cap.isOpened():
            self.get_logger().warning('Camera device is not open — cannot capture frame')
            return

        ret, frame = self.cap.read()

        if not ret or frame is None:
            self._consecutive_failures += 1
            self.get_logger().warning(
                f'Frame capture failed (consecutive failures: {self._consecutive_failures})'
            )
            return

        # Reset failure counter on success
        if self._consecutive_failures > 0:
            self.get_logger().info(
                f'Frame capture resumed after {self._consecutive_failures} consecutive failure(s)'
            )
            self._consecutive_failures = 0

        self._frame_count += 1

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_frame'

        self.publisher_.publish(msg)

        if self._frame_count % LOG_EVERY_N_FRAMES == 0:
            self.get_logger().info(f'Published frame #{self._frame_count} to /camera/image_raw')

    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
            self.get_logger().info('Camera released')
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
