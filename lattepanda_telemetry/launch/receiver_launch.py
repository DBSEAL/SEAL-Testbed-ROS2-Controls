from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable

def generate_launch_description():
    return LaunchDescription([
        # Lock in the matching network ID (Channel 42)
        SetEnvironmentVariable('ROS_DOMAIN_ID', '42'),
        
        # Launch the database injection node
        Node(
            package='lattepanda_telemetry',
            executable='lattepanda_metrics_sub',
            name='lattepanda_metrics_sub',
            output='screen',
            emulate_tty=True
        )
    ])
