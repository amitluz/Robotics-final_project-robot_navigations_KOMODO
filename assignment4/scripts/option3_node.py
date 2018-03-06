#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import os
import sys

def move(msg):
  msg=Twist()
  msg.linear.x=0.2
  continue_moving = True
  start_time = rospy.Time.now().to_sec()
  while(continue_moving):
    pub.publish(msg)
    current_time = rospy.Time.now().to_sec()
    continue_moving = (current_time - start_time) < int(sys.argv[1])
  os.system('rosnode kill option5_node')
  
rospy.init_node('option5_node', anonymous=False)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
sub = rospy.Subscriber("/scan", LaserScan, move)
rospy.spin()