#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist

class TurtleBotController(Node):
    def __init__(self):
        super().__init__('robot_mover')

        self.subscription = self.create_subscription(
            Point,
            '/point',
            self.listener_callback,
            10
        )

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.center_y = 256

        self.declare_parameter('linear_speed', 0.1)
        self.linear_speed = self.get_parameter('linear_speed').value

        self.timer = self.create_timer(0.1, self.publish_velocity)

        self.last_point = None

    def listener_callback(self, point: Point):
        self.last_point = point

    def publish_velocity(self):
        if self.last_point is None:
            return

        twist_msg = Twist()

        if self.last_point.y < self.center_y:
            twist_msg.linear.x = self.linear_speed
        else:
            twist_msg.linear.x = -self.linear_speed

        self.publisher.publish(twist_msg)

        self.get_logger().info(
            f"linear.x = {twist_msg.linear.x}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = TurtleBotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
