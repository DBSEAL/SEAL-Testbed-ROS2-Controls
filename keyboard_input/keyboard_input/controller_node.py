import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys
import termios
import tty

def getch():
    """Get a single keypress without waiting for Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class KeyboardPublisher(Node):
    def __init__(self):
        super().__init__('keyboard_publisher')
        self.publisher_ = self.create_publisher(String, 'motor_commands', 10)
        self.get_logger().info('Keyboard control started: W/A/S/D/X to move, Q to quit.')

        self.run()

    def run(self):
        while rclpy.ok():
            key = getch()
            msg = String()

            if key.lower() == 'w':
                msg.data = 'forward'
            elif key.lower() == 's':
                msg.data = 'backward'
            elif key.lower() == 'a':
                msg.data = 'left'
            elif key.lower() == 'd':
                msg.data = 'right'
            elif key.lower() == 'x':
                msg.data = 'stop'
            elif key.lower() == 'q':
                self.get_logger().info('Exiting keyboard control...')
                rclpy.shutdown()
                return
            else:
                continue  # ignore other keys

            self.publisher_.publish(msg)
            self.get_logger().info(f"Sent command: '{msg.data}'")

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardPublisher()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
