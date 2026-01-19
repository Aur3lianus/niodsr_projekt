#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')

        self.subscription = self.create_subscription(
            Image,
            'image_raw',
            self.listener_callback,
            10
        )

        self.publisher = self.create_publisher(Point, '/point', 10)

        self.bridge = CvBridge()
        self.window_name = "camera"

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )
        self.aruco_params = cv2.aruco.DetectorParameters_create()

    def listener_callback(self, image_data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(
                image_data, desired_encoding='bgr8'
            )
        except Exception as e:
            self.get_logger().error(f'Błąd konwersji obrazu: {e}')
            return

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = cv2.aruco.detectMarkers(
            gray, self.aruco_dict, parameters=self.aruco_params
        )

        if ids is not None:
            c = corners[0][0]
            cx = int(np.mean(c[:, 0]))
            cy = int(np.mean(c[:, 1]))

            cv2.aruco.drawDetectedMarkers(cv_image, corners, ids)
            cv2.circle(cv_image, (cx, cy), 5, (0, 0, 255), -1)

            point_msg = Point()
            point_msg.x = float(cx)
            point_msg.y = float(cy)
            point_msg.z = 0.0

            self.publisher.publish(point_msg)

        cv2.imshow(self.window_name, cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
