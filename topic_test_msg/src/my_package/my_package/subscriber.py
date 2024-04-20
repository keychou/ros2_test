import rclpy
from rclpy.node import Node
from example_msgs.msg import Point2D

class SubscriberNode(Node):

    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            Point2D,
            'point_topic',
            self.receive_message,
            10)

    def receive_message(self, msg):
        self.get_logger().info('Received: x=%f, y=%f' % (msg.x, msg.y))


def main(args=None):
    rclpy.init(args=args)
    subscriber_node = SubscriberNode()
    rclpy.spin(subscriber_node)
    subscriber_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()