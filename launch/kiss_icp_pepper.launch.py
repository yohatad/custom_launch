import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")
    visualize    = LaunchConfiguration("visualize",    default="true")

    config_file = os.path.join(
        get_package_share_directory("kiss_icp"), "config", "pepper_l2.yaml"
    )

    # ── Unitree L2 driver ────────────────────────────────────────────────────
    lidar_node = Node(
        package="unitree_lidar_ros2",
        executable="unitree_lidar_ros2_node",
        name="unitree_lidar_ros2_node",
        output="screen",
        parameters=[
            {"initialize_type": 2},
            {"work_mode": 0},
            {"use_system_timestamp": True},
            {"range_min": 0.0},
            {"range_max": 100.0},
            {"cloud_scan_num": 18},
            {"lidar_port": 6101},
            {"lidar_ip": "192.168.1.62"},
            {"local_port": 6201},
            {"local_ip": "0.0.0.0"},
            {"cloud_frame": "unilidar_lidar"},
            {"cloud_topic": "unilidar/cloud"},
            {"imu_frame": "unilidar_imu"},
            {"imu_topic": "unilidar/imu"},
            # publish_tf: False — KISS-ICP owns odom -> base_footprint.
            # The static SonarFront_frame -> unilidar_lidar TF below is
            # sufficient for KISS-ICP to look up the sensor extrinsic.
            {"publish_tf": False},
        ],
    )

    # ── Static TF: SonarFront_frame -> unilidar_lidar ────────────────────────
    # Connects the L2 into Pepper's TF tree so KISS-ICP can resolve
    # base_footprint -> unilidar_lidar as the static sensor extrinsic.
    tf_sonar_to_lidar = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="tf_sonar_to_lidar",
        arguments=[
            "--x",     "0.075",
            "--y",     "0.0",
            "--z",     "0.03",
            "--yaw",   "3.1415",
            "--pitch", "-1.893",
            "--roll",  "0",
            "--frame-id",       "SonarFront_frame",
            "--child-frame-id", "unilidar_lidar",
        ],
    )

    # ── KISS-ICP odometry ────────────────────────────────────────────────────
    kiss_icp_node = Node(
        package="kiss_icp",
        executable="kiss_icp_node",
        name="kiss_icp_node",
        output="screen",
        remappings=[("pointcloud_topic", "unilidar/cloud")],
        parameters=[{"use_sim_time": use_sim_time}, config_file],
    )

    # ── RViz (optional) ──────────────────────────────────────────────────────
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=[
            "-d",
            PathJoinSubstitution(
                [FindPackageShare("kiss_icp"), "rviz", "kiss_icp.rviz"]
            ),
        ],
        condition=IfCondition(visualize),
    )

    return LaunchDescription([
        lidar_node,
        tf_sonar_to_lidar,
        kiss_icp_node,
        rviz_node,
    ])
