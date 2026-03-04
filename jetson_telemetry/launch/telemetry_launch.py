from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable

def generate_launch_description():
    return LaunchDescription([
        # 1. Lock in the network ID automatically
        SetEnvironmentVariable('ROS_DOMAIN_ID', '42'),
        
        # 2. Launch your telemetry node
        Node(
            package='jetson_telemetry',
            executable='jetson_metrics_pub',
            name='jetson_metrics_pub',
            output='screen',
            emulate_tty=True
        )
    ])
