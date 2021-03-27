#!/usr/bin/env python3

""" ground station base utils """

__author__ = "Antonio Sapuppo"
__copyright__ = "Copyright 2021"

__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Antonio Sapuppo"
__email__ = "antoniosapuppo@yahoo.it"
__status__ = "Development"

import rospy
from std_msgs.msg import Bool, String, Int16
from geometry_msgs.msg import Twist, Pose


# ---------------------------------------------------------------------
# sites info:
#

class BasePc:
    def __init__(self):
        self.node_name = 'base_pc'
        # registering node in ros master
        rospy.init_node(self.node_name, log_level=rospy.INFO)
        rospy.on_shutdown(self.shutdown)
        # begin node code
        rospy.loginfo(f'{self.node_name} Starting: please, arm motors ')
        self.cam_pan = 90
        self.cam_tilt = 90
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.cam_pan_range = (32, 120)
        self.cam_tilt_range = (70, 185)
        # pub
        self.pub_cam_pan = rospy.Publisher('/base/cam_pan', Int16, queue_size=10)
        self.pub_cam_tilt = rospy.Publisher('/base/cam_tilt', Int16, queue_size=10)
        # sub - Don't subscribe until everything has been initialized.
        rospy.Subscriber("front_camera/cmd_vel", Twist, self.joy_front_camera)

    @staticmethod
    def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

    def shutdown(self):
        rospy.loginfo(f'{base_pc.node_name} Shutdown on progess')
        self.home_off()
        self.pub_cam_pan.publish(self.cam_pan)
        self.pub_cam_tilt.publish(self.cam_tilt)

    def home_off(self):
        self.cam_pan = 90  # zeroing pan tilt camera mount
        self.cam_tilt = 90

    def home_on(self):
        self.cam_pan = 90  # zeroing pan tilt camera mount
        self.cam_tilt = 185
        self.pub_cam_pan.publish(self.cam_pan)
        self.pub_cam_tilt.publish(self.cam_tilt)

    def spin(self):
        rospy.sleep(0.1)
        self.home_on()
        rate = rospy.Rate(1)  # hz
        while not rospy.is_shutdown():
            rate.sleep()

    def joy_front_camera(self, data):
        rospy.logdebug(f'{rospy.get_caller_id()}: joy_front_camera(x:{data.linear.x},y:{data.linear.y})')
        self.cam_pan += int(data.linear.y * self.scale_y)
        self.cam_pan = self.clamp(self.cam_pan, self.cam_pan_range[0], self.cam_pan_range[1])
        self.cam_tilt += int(data.linear.x * self.scale_x)
        self.cam_tilt = self.clamp(self.cam_tilt, self.cam_tilt_range[0], self.cam_tilt_range[1])
        self.pub_cam_pan.publish(self.cam_pan)
        self.pub_cam_tilt.publish(self.cam_tilt)
        rospy.logdebug(f'{rospy.get_caller_id()}: current(x:{self.cam_pan},y:{self.cam_tilt})')


if __name__ == '__main__':
    base_pc = BasePc()
    try:
        base_pc.spin()
    except Exception as error:
        rospy.logerr(f'{base_pc.node_name} Error on Main: {error}')
    except rospy.ROSInterruptException:
        rospy.loginfo(f'{base_pc.node_name} Shutdown')
