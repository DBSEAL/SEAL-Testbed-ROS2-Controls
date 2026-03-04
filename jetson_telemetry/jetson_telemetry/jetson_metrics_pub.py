import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
from jtop import jtop

class JetsonMetricsPublisher(Node):
    def __init__(self):
        # Name this specific node
        super().__init__('jetson_metrics_pub')
        
        # Create a "Topic" named 'jetson_telemetry' to broadcast the data
        self.publisher_ = self.create_publisher(String, 'jetson_telemetry', 10)
        
        # Run the timer_callback function every 10 seconds
        self.timer = self.create_timer(10.0, self.timer_callback)
        
        # Start the jtop hardware reader
        self.jetson = jtop()
        self.jetson.start()

    def format_3_sig_figs(self, num):
        try:
            if num == 0: return 0.0
            return float(f"{float(num):.3g}")
        except:
            return 0.0

    def timer_callback(self):
        if self.jetson.ok():
            # Gather the data
            metrics = {
                "cpu_utilization": self.format_3_sig_figs(self.jetson.stats.get('CPU1', 0)),
                "gpu_utilization": self.format_3_sig_figs(self.jetson.stats.get('GPU', 0)),
                "ram_used": self.format_3_sig_figs(self.jetson.stats.get('RAM', 0))
            }
            
            # Convert dictionary to a string and publish it to the ROS network
            msg = String()
            msg.data = json.dumps(metrics)
            self.publisher_.publish(msg)
            
            # Print to the terminal so we can see it working
            self.get_logger().info(f'Publishing: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = JetsonMetricsPublisher()
    try:
        rclpy.spin(node) # Keeps the script looping forever
    except KeyboardInterrupt:
        pass
    node.jetson.close()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
