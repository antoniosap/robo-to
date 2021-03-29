#!/usr/bin/env python3

""" ground station base cam pant tilt controller """

__author__ = "Antonio Sapuppo"
__copyright__ = "Copyright 2021"

__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Antonio Sapuppo"
__email__ = "antoniosapuppo@yahoo.it"
__status__ = "Development"

import sys
import rospy
from std_msgs.msg import Bool, String, Int16
from control_msgs.msg import FollowJointTrajectoryAction
from sensor_msgs.msg import JointState


# ---------------------------------------------------------------------
# sites info:
#

class PanTiltMessageAdapter:
    def __init__(self):
        self.node_name = 'pan_tilt_group_controller'
        # registering node in ros master
        rospy.init_node(self.node_name, log_level=rospy.INFO)
        # begin node code
        self.joint_names = ['pan_joint', 'tilt_joint']
        # pub
        self.pub_cam_pan = rospy.Publisher('/base/cam_pan', Int16, queue_size=10)
        self.pub_cam_tilt = rospy.Publisher('/base/cam_tilt', Int16, queue_size=10)
        # sub - Don't subscribe until everything has been initialized.
        rospy.Subscriber("/move_group/fake_controller_joint_states", JointState, self.follow_joint_trajectory)
        rospy.loginfo(f'{self.node_name} Starting')

    def spin(self):
        rospy.sleep(0.1)
        rate = rospy.Rate(1)  # hz
        while not rospy.is_shutdown():
            rate.sleep()

    def follow_joint_trajectory(self, msg):
        rospy.logdebug(f'{rospy.get_caller_id()}: joint_states {msg}')
        for idx, name in enumerate(msg.name):
            if name == 'pan_joint':
                self.pub_cam_pan.publish(int(round(msg.position[idx])))
            if name == 'tilt_joint':
                self.pub_cam_tilt.publish(int(round(msg.position[idx])))


if __name__ == '__main__':
    adapter = PanTiltMessageAdapter()
    try:
        adapter.spin()
    except Exception as error:
        rospy.logerr(f'{cam_controller.node_name} Error on Main: {error}')
    except rospy.ROSInterruptException:
        rospy.loginfo(f'{cam_controller.node_name} Shutdown')
