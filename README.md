# TurtleBot3 Gazebo Simulation & Nav2 Autonomous Navigation

ROS 2 Jazzy package for simulating a TurtleBot3 Burger robot in Gazebo Harmonic with the Navigation2 (Nav2) stack and autonomous goal dispatching.

## Prerequisites

- **OS:** Ubuntu 24.04 LTS
- **ROS Version:** ROS 2 Jazzy Jalisco
- **Simulator:** Gazebo Sim (Harmonic)

Required packages:
```bash
sudo apt update
sudo apt install -y \
  ros-jazzy-ros-gz \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-ros-gz-bridge \
  ros-jazzy-turtlebot3-description \
  ros-jazzy-nav2-bringup \
  ros-jazzy-nav2-simple-commander \
  ros-jazzy-nav2-minimal-tb3-sim
```

## Build

Clone or place this repository into your ROS 2 workspace `src/` directory, then build:

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select antropi_turtlebot3_assignment
source install/setup.bash
```

## Running the Simulation & Nav2

Launch Gazebo, the robot description, sensor bridges, Nav2 stack, and RViz:

```bash
source install/setup.bash
ros2 launch antropi_turtlebot3_assignment tb3_simulation.launch.py
```

### Launch Arguments

| Argument | Default | Description |
|---|---|---|
| `headless` | `False` | Run Gazebo GUI (`False`) or headless server (`True`) |
| `use_rviz` | `True` | Launch RViz with Nav2 visualization |
| `map` | `maps/tb3_sandbox.yaml` | Path to occupancy grid map |
| `params_file` | `config/nav2_params.yaml` | Path to Nav2 configuration parameters |
| `robot_name` | `turtlebot3_burger` | Name of the robot to simulate |
| `robot_sdf` | `models/turtlebot3_burger/model.sdf` | Path to robot SDF model |
| `slam` | `False` | Run SLAM instead of AMCL localization |

Example running headless:
```bash
ros2 launch antropi_turtlebot3_assignment tb3_simulation.launch.py headless:=True
```

## Autonomous Navigation

Once Nav2 is active, run the autonomous navigation node in a separate terminal:

```bash
source install/setup.bash
ros2 run antropi_turtlebot3_assignment navigate_to_goal
```

### Navigating to a Custom Goal

```bash
ros2 run antropi_turtlebot3_assignment navigate_to_goal --ros-args -p goal_x:=0.5 -p goal_y:=1.5 -p goal_yaw:=1.57
```

### Waypoint Navigation Mode

To navigate through a sequence of waypoints:
```bash
ros2 run antropi_turtlebot3_assignment navigate_to_goal --ros-args -p use_waypoints:=True
```

## Testing

Run unit tests and linters:
```bash
colcon test --packages-select antropi_turtlebot3_assignment
colcon test-result --all
```

