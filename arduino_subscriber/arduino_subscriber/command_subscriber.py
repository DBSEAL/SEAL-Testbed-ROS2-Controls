import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class CommandSubscriber(Node):
    def __init__(self):
        super().__init__('command_subscriber')

        # ROS subscription
        self.subscription = self.create_subscription(
            String,
            'motor_commands',
            self.listener_callback,
            10
        )

        # Serial connection to Arduino
        self.serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.get_logger().info('Subscriber ready and serial open.')

    def listener_callback(self, msg):
        command = msg.data
        self.get_logger().info(f'Received command: {command}')

        # Send to Arduino
        self.serial_port.write((command + '\n').encode())

def main(args=None):
    rclpy.init(args=args)
    node = CommandSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
