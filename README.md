# custom_launch

ROS2 launch files and utility nodes for the Pepper robot with Unitree L2 LiDAR and Intel RealSense D435.

## Requirements

- ROS2 Humble
- Packages: `kiss_icp`, `unitree_lidar_ros2`, `realsense2_camera`, `rtabmap_ros`, `tf2_ros`

## Launch files

### KISS-ICP odometry — `kiss_icp_pepper.launch.py`

Starts the Unitree L2 driver and KISS-ICP LiDAR odometry together.

```bash
ros2 launch custom_launch kiss_icp_pepper.launch.py
```

| Argument | Default | Description |
|---|---|---|
| `visualize` | `true` | Open RViz |
| `use_sim_time` | `false` | Use simulation clock |

Publishes `odom → base_footprint` via KISS-ICP. Requires the Pepper TF tree to be running (robot model / `robot_state_publisher`).

---

### RealSense camera — `my_realsense.launch.py`

Launches the Intel RealSense D435 with `publish_tf` disabled (Pepper's URDF owns the camera TF).

```bash
ros2 launch custom_launch my_realsense.launch.py
```

---

### RTABMap with RealSense — `rtabmap_realsense.launch.py`

Launches RTABMap RGB-D SLAM using the RealSense D435.

```bash
ros2 launch custom_launch rtabmap_realsense.launch.py
```

---

## Utility nodes

| Node | Description |
|---|---|
| `color_compressor.py` | Compresses raw RGB images for bandwidth-constrained links |
| `depth_roi_service.py` | ROS2 service that returns depth values within a specified ROI |

## Workspace

This package is part of the Pepper robot workspace. See [jetson_ws](https://github.com/yohatad/jetson_ws) for full setup instructions.
