import rclpy
from rclpy.action import ActionClient
from example_msgs.action import Fibonacci
from rclpy.node import Node


class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self.get_logger().info('add_done_callback goal_response_callback')
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        self.get_logger().info('goal_response_callback called')
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self.get_logger().info('add_done_callback get_result_callback')
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        self.get_logger().info('get_result_callback called')
        try:
            result = future.result().result.sequence
            self.get_logger().info('Result: {0}'.format(result))
        except Exception as e:
            self.get_logger().info('Service call failed %r' % (e,))


def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_client = FibonacciActionClient()
    fibonacci_action_client.send_goal(10)
    rclpy.spin_once(fibonacci_action_client)
    fibonacci_action_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()