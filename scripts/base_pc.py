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
import geometry_msgs.msg
from math import pi, dist, fabs, cos
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import sensor_msgs.msg as sensor_msgs
from std_msgs.msg import Bool, String

# ---------------------------------------------------------------------
# sites info:
#


def btn_shutdown(data):
    rospy.loginfo(f'{rospy.get_caller_id()} shutdown button {data.data}')


if __name__ == '__main__':
    node_name = 'base_pc'
    # registering node in ros master
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node(node_name, log_level=rospy.INFO)
    # begin node code
    rospy.loginfo(f'{node_name} Starting ')
    # sub
    #rospy.Subscriber("/base/btn_shutdown", Bool, btn_shutdown)
    # pub
    #pub_display8x8 = rospy.Publisher('/sensehat/led_panel', String, queue_size=10)
    #
    rate = rospy.Rate(1)  # hz
    try:
        while not rospy.is_shutdown():

            rate.sleep()
    except Exception as error:
        rospy.logerr(f'{node_name} Error on Main: {error}')
    except rospy.ROSInterruptException:
        rospy.loginfo(f'{node_name} Shutdown')
