import os
from ament_index_python.packages import get_package_share_path
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.actions import RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart, OnProcessExit
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    urdf_path = os.path.join(get_package_share_path('ros2_robotic_arm'),'urdf','main.xacro')
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_node =Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d',os.path.join(get_package_share_path('ros2_robotic_arm'),'rviz','config.rviz')]
    )

    gazebo_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("gazebo_ros"), "/launch", "/gazebo.launch.py"]
        ),
    )


    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'robotic_arm'],
                    output='screen')
    

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager"       
        ]
    )

    base_mid_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=[
            "base_to_mid_joint_position_controller",
            "--controller-manager",
            "/controller_manager"       
        ]
    )

    mid_top_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        output="screen",
        arguments=[
            "mid_to_top_joint_position_controller",
            "--controller-manager",
            "/controller_manager"       
        ]
    )


    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node,
        gazebo_node,
        spawn_entity,
        joint_state_broadcaster_spawner,
        base_mid_controller_spawner,
        mid_top_controller_spawner
        ])
