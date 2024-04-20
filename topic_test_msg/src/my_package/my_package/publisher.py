import rclpy
from rclpy.node import Node
from example_msgs.msg import Point2D

class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')
        self.publisher_ = self.create_publisher(Point2D, 'point_topic', 10)
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        msg = Point2D()
        msg.x = 1.0
        msg.y = 2.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: x=%f, y=%f' % (msg.x, msg.y))


def main(args=None):
    rclpy.init(args=args)
    publisher_node = PublisherNode()
    rclpy.spin(publisher_node)
    publisher_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()