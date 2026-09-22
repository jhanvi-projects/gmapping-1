from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    serial_port = LaunchConfiguration(
        'serial_port'
    )

    serial_baudrate = LaunchConfiguration(
        'serial_baudrate'
    )

    # ----------------------------------
    # RPLIDAR
    # ----------------------------------

    rplidar = Node(

        package='rplidar_ros',

        executable='rplidar_node',

        name='rplidar_node',

        output='screen',

        parameters=[

            {
                'serial_port':
                    serial_port,

                'serial_baudrate':
                    serial_baudrate,

                'frame_id':
                    'laser',

                'inverted':
                    False,

                'angle_compensate':
                    True,
            }

        ]
    )

    # ----------------------------------
    # Custom Odometry
    # ----------------------------------

    custom_odom = Node(

        package='custom_odom',

        executable='custom_odom_node',

        name='custom_odometry',

        output='screen'
    )

    # ----------------------------------
    # base_link -> laser
    # ----------------------------------

    static_tf = Node(

        package='tf2_ros',

        executable='static_transform_publisher',

        name='base_to_laser',

        arguments=[

            '0',
            '0',
            '0',

            '0',
            '0',
            '0',

            'base_link',
            'laser'

        ],

        output='screen'
    )

    # ----------------------------------
    # GMapping
    # ----------------------------------

    gmapping = Node(

        package='slam_gmapping',

        executable='slam_gmapping',

        name='slam_gmapping',

        output='screen',

        parameters=[

            '/home/jhanvi/'
            'gmapping_ws/src/'
            'gmapping_demo/config/'
            'gmapping.yaml'

        ]
    )

    # ----------------------------------
    # RViz
    # ----------------------------------

    rviz = Node(

        package='rviz2',

        executable='rviz2',

        name='rviz2',

        output='screen',

        arguments=[

            '-d',

            '/home/jhanvi/'
            'gmapping_ws/src/'
            'gmapping_demo/rviz/'
            'gmapping.rviz'

        ]
    )

    return LaunchDescription([

        DeclareLaunchArgument(

            'serial_port',

            default_value='/dev/ttyUSB0'

        ),

        DeclareLaunchArgument(

            'serial_baudrate',

            default_value='115200'

        ),

        rplidar,

        custom_odom,

        static_tf,

        gmapping,

        rviz,

    ])
