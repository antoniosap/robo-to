#!/usr/bin/env python3

""" ground station base utils """

__author__ = "Antonio Sapuppo"
__copyright__ = "Copyright 2021"

__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Antonio Sapuppo"
__email__ = "antoniosapuppo@yahoo.it"
__status__ = "Development"

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
from math import pi, dist, fabs, cos
from moveit_commander.conversions import pose_to_list
import sensor_msgs.msg as sensor_msgs
from std_msgs.msg import Bool, String
from geometry_msgs.msg import Twist


# ---------------------------------------------------------------------
# sites info:
#


class BasePc:
    def __init__(self):
        self.node_name = 'base_pc'
        # registering node in ros master
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node(self.node_name, log_level=rospy.INFO)
        # begin node code
        rospy.loginfo(f'{self.node_name} Starting ')
        self.cam_pan = 0        # zeroing pan tilt camera mount
        self.cam_tilt = 0
        # pub
        self.pub_cam_pan = rospy.Publisher('/base/cam_pan', Int16, queue_size=10)
        self.pub_cam_tilt = rospy.Publisher('/base/cam_tilt', Int16, queue_size=10)
        # sub - Don't subscribe until everything has been initialized.
        rospy.Subscriber("front_camera/cmd_vel", Twist, self.joy_front_camera)

    @staticmethod
    def spin():
        rate = rospy.Rate(1)  # hz
        while not rospy.is_shutdown():
            rate.sleep()

    @staticmethod
    def joy_front_camera(data):
        rospy.loginfo(f'{rospy.get_caller_id()}/joy_front_camera(x:{data.linear.x},y:{data.linear.y})')


if __name__ == '__main__':
    base_pc = BasePc()
    try:
        base_pc.spin()
    except Exception as error:
        rospy.logerr(f'{base_pc.node_name} Error on Main: {error}')
    except rospy.ROSInterruptException:
        rospy.loginfo(f'{base_pc.node_name} Shutdown')
