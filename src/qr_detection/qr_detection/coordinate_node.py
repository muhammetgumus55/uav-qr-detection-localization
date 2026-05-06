import json

import cv2
import numpy as np
import rclpy
from geometry_msgs.msg import Point
from rclpy.node import Node
from std_msgs.msg import String


class CoordinateNode(Node):
    def __init__(self):
        super().__init__('coordinate_node')
        self.declare_parameter('fx', 800.0)
        self.declare_parameter('fy', 800.0)
        self.declare_parameter('cx', 320.0)
        self.declare_parameter('cy', 240.0)
        self.declare_parameter('qr_size_m', 0.15)

        self.subscription = self.create_subscription(
            String, 'qr/data', self.qr_callback, 10)
        self.publisher_ = self.create_publisher(Point, 'qr/coordinates', 10)

    def qr_callback(self, msg):
        try:
            payload = json.loads(msg.data)
            corners = np.array(payload['corners'], dtype=np.float32)
        except (json.JSONDecodeError, KeyError):
            self.get_logger().warning('Malformed message on qr/data — expected JSON with "corners" key')
            return

        fx = self.get_parameter('fx').value
        fy = self.get_parameter('fy').value
        cx = self.get_parameter('cx').value
        cy = self.get_parameter('cy').value
        qr_size = self.get_parameter('qr_size_m').value

        camera_matrix = np.array([[fx, 0.0, cx], [0.0, fy, cy], [0.0, 0.0, 1.0]], dtype=np.float32)
        dist_coeffs = np.zeros((5, 1), dtype=np.float32)

        half = qr_size / 2.0
        object_points = np.array([
            [-half, -half, 0.0],
            [ half, -half, 0.0],
            [ half,  half, 0.0],
            [-half,  half, 0.0],
        ], dtype=np.float32)

        success, rvec, tvec = cv2.solvePnP(object_points, corners, camera_matrix, dist_coeffs)
        if not success:
            self.get_logger().warning('solvePnP failed — check camera intrinsics and corner order')
            return

        point = Point(x=float(tvec[0]), y=float(tvec[1]), z=float(tvec[2]))
        self.publisher_.publish(point)
        self.get_logger().info(
            f'QR position: x={point.x:.3f} m, y={point.y:.3f} m, z={point.z:.3f} m'
        )


def main(args=None):
    rclpy.init(args=args)
    node = CoordinateNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
