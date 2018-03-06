#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import os
from math import radians, fabs, pi
from std_msgs.msg import String
import sys

roll = pitch = yaw = 0.0
rad_angle = -1
wanted_angle = -100
def turn(msg):
  global roll, pitch, yaw
  global rad_angle
  global wanted_angle
  direction=int(sys.argv[1])
  
  orientation_q = msg.pose.pose.orientation
  orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
  (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
  if rad_angle == -1:
    if sys.argv[2] == '5':
      rad_angle = radians(5)
    else:
      rad_angle = radians(int(sys.argv[2]))
    wanted_angle = yaw +direction*rad_angle
    if wanted_angle < -pi:
      diff = -pi - wanted_angle
      wanted_angle = pi - diff
    if wanted_angle > pi:
      diff = wanted_angle - pi
      wanted_angle = diff - pi
  if fabs(wanted_angle - yaw) < 0.2 * rad_angle:
    os.system('rosnode kill option2_node')
  new_msg = Twist()
  new_msg.angular.z = direction*0.1
  pub.publish(new_msg)

rospy.init_node('option2_node', anonymous=False)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber('/odometry/filtered', Odometry, turn)
rospy.spin()
