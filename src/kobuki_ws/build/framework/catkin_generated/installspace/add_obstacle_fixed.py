#!/usr/bin/env python3

import rospy
from costmap_converter.msg import ObstacleArrayMsg, ObstacleMsg
from geometry_msgs.msg import Point32, Point
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA

rospy.init_node("circle_obstacle_publisher")

obstacle_publisher = rospy.Publisher("/move_base/TebLocalPlannerROS/obstacles", ObstacleArrayMsg, queue_size=1)
marker_publisher = rospy.Publisher("cylinder_marker", Marker, queue_size=1)

rate = rospy.Rate(1)  # 1 Hz

while not rospy.is_shutdown():
    obstacle_array = ObstacleArrayMsg()

    circle_obstacle = ObstacleMsg()
    circle_obstacle.id = 1
    circle_obstacle.radius = 0.5  # Set the radius of the circle
    circle_obstacle.polygon.points.append(Point32(3.0, 3.0, 0.0))  # Set the center of the circle

    obstacle_array.obstacles.append(circle_obstacle)

    obstacle_publisher.publish(obstacle_array)

    # Create a vertical cylinder Marker
    cylinder_marker = Marker()
    cylinder_marker.header.frame_id = "map"
    cylinder_marker.header.stamp = rospy.Time.now()
    cylinder_marker.ns = "circle_obstacle"
    cylinder_marker.id = 1
    cylinder_marker.type = Marker.CYLINDER
    cylinder_marker.action = Marker.ADD

    # Set the cylinder dimensions
    cylinder_marker.scale.x = 2 * circle_obstacle.radius
    cylinder_marker.scale.y = 2 * circle_obstacle.radius
    cylinder_marker.scale.z = 1.0

    # Set the cylinder position
    cylinder_marker.pose.position = Point(circle_obstacle.polygon.points[0].x,
                                          circle_obstacle.polygon.points[0].y,
                                          cylinder_marker.scale.z / 2)

    # Set the cylinder orientation (identity quaternion)
    cylinder_marker.pose.orientation.x = 0.0
    cylinder_marker.pose.orientation.y = 0.0
    cylinder_marker.pose.orientation.z = 0.0
    cylinder_marker.pose.orientation.w = 1.0

    # Set the cylinder color (RGBA)
    cylinder_marker.color = ColorRGBA(0.0, 1.0, 0.0, 0.5)  # Green, 50% transparent

    # Set the cylinder lifetime
    cylinder_marker.lifetime = rospy.Duration(1)

    marker_publisher.publish(cylinder_marker)

    rate.sleep()
