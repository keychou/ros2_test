import rclpy
from rclpy.node import Node
from example_msgs.srv import AddTwoInts


class AddTwoIntsClient(Node):

    def __init__(self):
        super().__init__('add_two_ints_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')

    def call_add_two_ints(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        self.future = self.client.call_async(request)
        #self.future.add_done_callback(self.handle_response)

    #def handle_response(self, future):
    #    self.get_logger().info('handle_response called')
    #    try:
    #        response = future.result()
    #        self.get_logger().info('Sum: %d' % response.sum)
    #    except Exception as e:
    #        self.get_logger().error('Service call failed: %r' % (e,))


def main(args=None):
    rclpy.init(args=args)
    add_two_ints_client = AddTwoIntsClient()
    add_two_ints_client.call_add_two_ints(3, 5)
    #rclpy.spin_once(add_two_ints_client)

    while rclpy.ok():
        rclpy.spin_once(add_two_ints_client) 
        if add_two_ints_client.future.done(): 
            try: 
                response = add_two_ints_client.future.result()
            except Exception as e: 
                add_two_ints_client.get_logger().info('Service call failed %r' % (e,))
            else: 
                add_two_ints_client.get_logger().info('Result of add_two_ints sum: %d' %(response.sum))
            break 

    add_two_ints_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()