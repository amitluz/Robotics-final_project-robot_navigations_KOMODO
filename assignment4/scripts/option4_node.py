#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import os
import numpy as np
from std_msgs.msg import String
import sys

red= []

def get_min_distance(msg):
  br = CvBridge()
  img = br.imgmsg_to_cv2(msg)
  distances = [img[x][y] for (x, y) in red]
  if sys.argv[1] == '3':
    print('The minimum distance to the red object is {}'.format(min([d for d in distances if not np.isnan(d)])))
  else:
    tmp_file = open("tmp_file.txt", "w")
    tmp_file.write('{}'.format(min([d for d in distances if not np.isnan(d)])))
  os.system('rosnode kill option3_node')

def find_red(msg):
  global red
  br = CvBridge()
  img = br.imgmsg_to_cv2(msg,'bgr8')
  height, width, depth = img.shape
  img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  lower_red1 = np.array([150,90,90])
  upper_red1 = np.array([180,255,255])
  
  lower_red2 = np.array([0,50,50])
  upper_red2 = np.array([10,255,255])
  
  mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)
  mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
  
  img1= cv2.bitwise_and(img, img, mask=mask1)
  img2= cv2.bitwise_and(img, img, mask=mask2)
  
  gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
  
  blurred_img1 = cv2.GaussianBlur(gray1, (5, 5), 0)
  blurred_img2 = cv2.GaussianBlur(gray2, (5, 5), 0)
  
  threshold1 = cv2.threshold(blurred_img1, 20, 255, 0)[1]
  threshold2 = cv2.threshold(blurred_img2, 20, 255, 0)[1]
  
  cv2.imshow("1", threshold1 )
  cv2.imshow("2", threshold2 )
  for x in range(0, height):
    for y in range(0, width):
      if threshold1[x][y] == 255 or threshold2[x][y] == 255:
	red.append((x, y))
  if not red:
    if sys.argv[1] == '3':
      print('No red object')
    else:
      tmp_file = open("tmp_file.txt", "w")
      tmp_file.write('None')
    os.system('rosnode kill option3_node')
  else:
    sub = rospy.Subscriber("/torso_camera/depth_registered/image_raw", Image, get_min_distance)





rospy.init_node('option3_node', anonymous=False)
sub = rospy.Subscriber('/torso_camera/rgb/image_raw', Image, find_red)
rospy.spin()