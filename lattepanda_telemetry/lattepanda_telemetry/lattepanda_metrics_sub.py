import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
from influxdb import InfluxDBClient

class MetricsSubscriber(Node):
    def __init__(self):
        super().__init__('lattepanda_metrics_sub')
        
        # 1. Listen to the exact same topic the Jetson is broadcasting on
        self.subscription = self.create_subscription(
            String,
            'jetson_telemetry',
            self.listener_callback,
            10)
        
        # 2. Connect to the local InfluxDB container on the LattePanda
        self.client = InfluxDBClient(host='localhost', port=8086, database='telegraf')
        self.get_logger().info('Connected to InfluxDB. Waiting for Jetson data...')

    def listener_callback(self, msg):
        # 3. Unpack the JSON string sent by the Jetson
        data = json.loads(msg.data)
        
        # 4. Format the payload specifically for InfluxDB
        json_body = [
            {
                "measurement": "jetson_stats",
                "tags": {
                    "host": "BabySEAL_Remote"
                },
                "fields": {
                    "cpu_utilization": float(data["cpu_utilization"]),
                    "gpu_utilization": float(data["gpu_utilization"]),
                    "ram_used": float(data["ram_used"])
                }
            }
        ]
        
        # 5. Save it to the database
        self.client.write_points(json_body)
        self.get_logger().info(f'Saved to InfluxDB: {data}')

def main(args=None):
    rclpy.init(args=args)
    node = MetricsSubscriber()
    try:
        rclpy.spin(node) # Keeps the script listening forever
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
