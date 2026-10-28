import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('antropi_turtlebot3_assignment')
    nav2_bringup_share = get_package_share_directory('nav2_bringup')
    nav2_sim_share = get_package_share_directory('nav2_minimal_tb3_sim')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    headless = LaunchConfiguration('headless')
    use_rviz = LaunchConfiguration('use_rviz')
    slam = LaunchConfiguration('slam')
    use_composition = LaunchConfiguration('use_composition')
    autostart = LaunchConfiguration('autostart')
    use_sim_time = LaunchConfiguration('use_sim_time')
    map_yaml_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    robot_name = LaunchConfiguration('robot_name')
    robot_sdf = LaunchConfiguration('robot_sdf')
    world = LaunchConfiguration('world')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    z_pose = LaunchConfiguration('z_pose')
    yaw = LaunchConfiguration('yaw')

    declare_headless = DeclareLaunchArgument(
        'headless',
        default_value='False',
        description='Whether to execute Gazebo in headless mode',
    )
    declare_use_rviz = DeclareLaunchArgument(
        'use_rviz',
        default_value='True',
        description='Whether to start RViz',
    )
    declare_slam = DeclareLaunchArgument(
        'slam',
        default_value='False',
        description='Whether to run SLAM instead of AMCL',
    )
    declare_use_composition = DeclareLaunchArgument(
        'use_composition',
        default_value='False',
        description='Whether to use composed bringup',
    )
    declare_autostart = DeclareLaunchArgument(
        'autostart',
        default_value='True',
        description='Automatically startup the nav2 stack',
    )
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation clock',
    )
    declare_map = DeclareLaunchArgument(
        'map',
        default_value=os.path.join(pkg_share, 'maps', 'tb3_sandbox.yaml'),
        description='Full path to map file',
    )
    declare_params = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(pkg_share, 'config', 'nav2_params.yaml'),
        description='Full path to Nav2 parameters file',
    )
    declare_rviz_config = DeclareLaunchArgument(
        'rviz_config_file',
        default_value=os.path.join(pkg_share, 'rviz', 'turtlebot3_nav2.rviz'),
        description='Full path to RViz config file',
    )
    declare_robot_name = DeclareLaunchArgument(
        'robot_name',
        default_value='turtlebot3_burger',
        description='Name of the robot',
    )
    declare_robot_sdf = DeclareLaunchArgument(
        'robot_sdf',
        default_value=os.path.join(
            pkg_share, 'models', 'turtlebot3_burger', 'model.sdf'
        ),
        description='Full path to robot sdf file to spawn in Gazebo',
    )
    declare_world = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(pkg_share, 'worlds', 'tb3_sandbox.sdf'),
        description='Full path to world model file to load',
    )
    declare_x = DeclareLaunchArgument(
        'x_pose', default_value='-2.00', description='Initial robot x coordinate'
    )
    declare_y = DeclareLaunchArgument(
        'y_pose', default_value='-0.50', description='Initial robot y coordinate'
    )
    declare_z = DeclareLaunchArgument(
        'z_pose', default_value='0.01', description='Initial robot z coordinate'
    )
    declare_yaw = DeclareLaunchArgument(
        'yaw', default_value='0.00', description='Initial robot yaw angle'
    )

    resource_paths = ':'.join([
        os.path.join(pkg_share, 'models'),
        os.path.join(nav2_sim_share, 'models'),
        '/opt/ros/jazzy/share',
    ])
    set_gz_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH', resource_paths
    )

    burger_urdf_path = os.path.join(pkg_share, 'urdf', 'turtlebot3_burger.urdf')
    with open(burger_urdf_path, 'r') as infp:
        robot_description = infp.read()

    start_robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time, 'robot_description': robot_description}
        ],
    )

    gazebo_server = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-s', world],
        output='screen',
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        condition=UnlessCondition(headless),
        launch_arguments={'gz_args': ['-v4 -g ']}.items(),
    )

    gz_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_sim_share, 'launch', 'spawn_tb3.launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'robot_name': robot_name,
            'robot_sdf': robot_sdf,
            'x_pose': x_pose,
            'y_pose': y_pose,
            'z_pose': z_pose,
            'yaw': yaw,
        }.items(),
    )

    bringup_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_share, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'slam': slam,
            'map': map_yaml_file,
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'autostart': autostart,
            'use_composition': use_composition,
        }.items(),
    )

    rviz_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_share, 'launch', 'rviz_launch.py')
        ),
        condition=IfCondition(use_rviz),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'rviz_config': rviz_config_file,
        }.items(),
    )

    return LaunchDescription([
        set_gz_resource_path,
        declare_headless,
        declare_use_rviz,
        declare_slam,
        declare_use_composition,
        declare_autostart,
        declare_use_sim_time,
        declare_map,
        declare_params,
        declare_rviz_config,
        declare_robot_name,
        declare_robot_sdf,
        declare_world,
        declare_x,
        declare_y,
        declare_z,
        declare_yaw,
        start_robot_state_publisher_cmd,
        gazebo_server,
        gazebo_client,
        gz_robot,
        bringup_cmd,
        rviz_cmd,
    ])
