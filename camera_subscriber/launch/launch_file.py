from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    linear_speed = LaunchConfiguration('linear_speed', default='0.1')

    turtlebot_model = SetEnvironmentVariable(
        name='TURTLEBOT3_MODEL',
        value='burger'
    )

    turtlebot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('turtlebot3_gazebo'),
                'launch',
                'empty_world.launch.py'
            )
        )
    )

    usb_cam_node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='usb_cam',
        output='screen'
    )

    camera_node = Node(
        package='camera_subscriber',
        executable='camera_node',
        name='camera_node',
        output='screen'
    )

    robot_mover_node = Node(
        package='camera_subscriber',
        executable='robot_mover',
        name='robot_mover',
        output='screen',
        parameters=[{
            'linear_speed': linear_speed
        }]
    )

    return LaunchDescription([
        turtlebot_model,
        turtlebot_launch,
        usb_cam_node,
        camera_node,
        robot_mover_node,
    ])

