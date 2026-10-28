import math
import sys

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy


def create_pose_stamped(navigator, x, y, yaw):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = float(x)
    pose.pose.position.y = float(y)
    pose.pose.position.z = 0.0
    pose.pose.orientation.x = 0.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)
    return pose


def main(args=None):
    rclpy.init(args=args)

    navigator = BasicNavigator()

    navigator.declare_parameter('set_initial_pose', True)
    navigator.declare_parameter('initial_x', -2.0)
    navigator.declare_parameter('initial_y', -0.5)
    navigator.declare_parameter('initial_yaw', 0.0)
    navigator.declare_parameter('goal_x', 1.8)
    navigator.declare_parameter('goal_y', -0.5)
    navigator.declare_parameter('goal_yaw', 0.0)
    navigator.declare_parameter('use_waypoints', False)

    set_initial_pose = navigator.get_parameter('set_initial_pose').value
    initial_x = navigator.get_parameter('initial_x').value
    initial_y = navigator.get_parameter('initial_y').value
    initial_yaw = navigator.get_parameter('initial_yaw').value
    goal_x = navigator.get_parameter('goal_x').value
    goal_y = navigator.get_parameter('goal_y').value
    goal_yaw = navigator.get_parameter('goal_yaw').value
    use_waypoints = navigator.get_parameter('use_waypoints').value

    if set_initial_pose:
        initial_pose = create_pose_stamped(navigator, initial_x, initial_y, initial_yaw)
        navigator.setInitialPose(initial_pose)

    navigator.waitUntilNav2Active()

    if use_waypoints:
        waypoint_coords = [
            (-0.5, 1.2, 0.0),
            (1.5, 1.0, -1.57),
            (1.8, -0.5, 3.14),
            (-2.0, -0.5, 0.0),
        ]
        poses = [create_pose_stamped(navigator, x, y, yaw) for x, y, yaw in waypoint_coords]
        navigator.goThroughPoses(poses)
    else:
        goal_pose = create_pose_stamped(navigator, goal_x, goal_y, goal_yaw)
        navigator.goToPose(goal_pose)

    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback and hasattr(feedback, 'distance_remaining'):
            navigator.get_logger().info(
                f'Distance remaining: {feedback.distance_remaining:.2f} m'
            )
        rclpy.spin_once(navigator, timeout_sec=0.5)

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        navigator.get_logger().info('Navigation succeeded.')
        status_code = 0
    elif result == TaskResult.FAILED:
        navigator.get_logger().error('Navigation failed.')
        status_code = 1
    elif result == TaskResult.CANCELED:
        navigator.get_logger().warn('Navigation was canceled.')
        status_code = 2
    else:
        navigator.get_logger().error('Navigation returned unknown result.')
        status_code = 3

    navigator.destroy_node()
    rclpy.shutdown()
    sys.exit(status_code)


if __name__ == '__main__':
    main()
