import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

class RectangleMover(Node):
    def __init__(self):
        super().__init__('rectangle_mover')

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.joint_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_callback, 10
        )
        self.timer = self.create_timer(0.05, self.control_loop)

        self.wheel_radius = 0.1
        self.wheel_separation = 0.45
        self.long_length = 4.0
        self.short_length = 2.0
        self.linear_speed = 0.3
        self.angular_speed = 0.3

        self.left_position = None
        self.right_position = None
        self.start_left = None
        self.start_right = None
        self.state = 0
        self.initialized = False

        self.get_logger().info('Rectangle Mover dimulai.')

    def joint_callback(self, msg):
        for i, name in enumerate(msg.name):
            if name == 'base_left_wheel_joint':
                self.left_position = msg.position[i]
            elif name == 'base_right_wheel_joint':
                self.right_position = msg.position[i]

        if (self.left_position is not None and
                self.right_position is not None and
                not self.initialized):
            self.start_left = self.left_position
            self.start_right = self.right_position
            self.initialized = True
            self.get_logger().info('Joint roda berhasil dibaca.')

    def reset_reference(self):
        self.start_left = self.left_position
        self.start_right = self.right_position

    def get_wheel_distances(self):
        dl = (self.left_position - self.start_left) * self.wheel_radius
        dr = (self.right_position - self.start_right) * self.wheel_radius
        return dl, dr

    def get_distance(self):
        dl, dr = self.get_wheel_distances()
        return (abs(dl) + abs(dr)) / 2.0

    def get_rotation_angle(self):
        dl, dr = self.get_wheel_distances()
        return abs((dr - dl) / self.wheel_separation)

    def control_loop(self):
        msg = Twist()

        if not self.initialized:
            self.cmd_pub.publish(msg)
            return

        if self.state == 0:
            if self.get_distance() < self.long_length:
                msg.linear.x = self.linear_speed
            else:
                self.get_logger().info('Sisi 1 selesai.')
                self.reset_reference()
                self.state = 1

        elif self.state == 1:
            if self.get_rotation_angle() < math.pi / 2:
                msg.angular.z = self.angular_speed
            else:
                self.get_logger().info('Belok 1 selesai.')
                self.reset_reference()
                self.state = 2

        elif self.state == 2:
            if self.get_distance() < self.short_length:
                msg.linear.x = self.linear_speed
            else:
                self.get_logger().info('Sisi 2 selesai.')
                self.reset_reference()
                self.state = 3

        elif self.state == 3:
            if self.get_rotation_angle() < math.pi / 2:
                msg.angular.z = self.angular_speed
            else:
                self.get_logger().info('Belok 2 selesai.')
                self.reset_reference()
                self.state = 4

        elif self.state == 4:
            if self.get_distance() < self.long_length:
                msg.linear.x = self.linear_speed
            else:
                self.get_logger().info('Sisi 3 selesai.')
                self.reset_reference()
                self.state = 5

        elif self.state == 5:
            if self.get_rotation_angle() < math.pi / 2:
                msg.angular.z = self.angular_speed
            else:
                self.get_logger().info('Belok 3 selesai.')
                self.reset_reference()
                self.state = 6

        elif self.state == 6:
            if self.get_distance() < self.short_length:
                msg.linear.x = self.linear_speed
            else:
                self.get_logger().info('Sisi 4 selesai.')
                self.reset_reference()
                self.state = 7

        elif self.state == 7:
            if self.get_rotation_angle() < math.pi / 2:
                msg.angular.z = self.angular_speed
            else:
                self.get_logger().info('Belok 4 selesai.')
                self.state = 8

        elif self.state == 8:
            self.cmd_pub.publish(Twist())
            self.get_logger().info('Persegi panjang selesai. Robot berhenti.')
            self.timer.cancel()
            return

        self.cmd_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RectangleMover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
