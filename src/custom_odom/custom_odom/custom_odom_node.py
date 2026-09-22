import math

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class CustomOdometry(Node):

    def __init__(self):

        super().__init__('custom_odometry')

        # Publisher for Odometry message
        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        # TF broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Robot pose
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Custom movement
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0

        # Timer
        self.last_time = self.get_clock().now()

        self.timer = self.create_timer(
            0.05,
            self.update_odometry
        )

    def update_odometry(self):

        current_time = self.get_clock().now()

        dt = (
            current_time - self.last_time
        ).nanoseconds / 1e9

        self.last_time = current_time

        # Update position
        self.x += (
            self.linear_velocity
            * math.cos(self.theta)
            * dt
        )

        self.y += (
            self.linear_velocity
            * math.sin(self.theta)
            * dt
        )

        self.theta += (
            self.angular_velocity
            * dt
        )

        # Quaternion
        q = Quaternion()

        q.x = 0.0
        q.y = 0.0

        q.z = math.sin(
            self.theta / 2.0
        )

        q.w = math.cos(
            self.theta / 2.0
        )

        # -----------------------------
        # Publish Odometry
        # -----------------------------

        odom = Odometry()

        odom.header.stamp = current_time.to_msg()

        odom.header.frame_id = 'odom'

        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        odom.pose.pose.orientation = q

        odom.twist.twist.linear.x = (
            self.linear_velocity
        )

        odom.twist.twist.angular.z = (
            self.angular_velocity
        )

        self.odom_pub.publish(odom)

        # -----------------------------
        # Publish TF
        # -----------------------------

        transform = TransformStamped()

        transform.header.stamp = current_time.to_msg()

        transform.header.frame_id = 'odom'

        transform.child_frame_id = 'base_link'

        transform.transform.translation.x = self.x

        transform.transform.translation.y = self.y

        transform.transform.translation.z = 0.0

        transform.transform.rotation = q

        self.tf_broadcaster.sendTransform(
            transform
        )


def main(args=None):
    rclpy.init(args=args)

    node = CustomOdometry()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
