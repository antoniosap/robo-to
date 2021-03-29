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
import rospy
import moveit_commander
import moveit_msgs.msg
from moveit_commander.conversions import pose_to_list
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool, String, Int16
from geometry_msgs.msg import Twist, Pose


# ---------------------------------------------------------------------
# sites info:
#

class BasePc:
    def __init__(self):
        self.node_name = 'pan_tilt_moveit_base_pc'
        # registering node in ros master
        rospy.init_node(self.node_name, log_level=rospy.INFO)
        rospy.on_shutdown(self.shutdown)
        # moveit
        moveit_commander.roscpp_initialize(sys.argv)
        self.pan_tilt_robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.group_name = "pan_tilt_group"
        self.move_group = moveit_commander.MoveGroupCommander(self.group_name)
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                       moveit_msgs.msg.DisplayTrajectory,
                                                       queue_size=20)
        # begin node code
        rospy.loginfo(f'{self.node_name} Starting: please, arm motors ')
        # pub
        self.pub_cam_pan = rospy.Publisher('/base/cam_pan', Int16, queue_size=10)
        self.pub_cam_tilt = rospy.Publisher('/base/cam_tilt', Int16, queue_size=10)
        # sub - Don't subscribe until everything has been initialized.
        rospy.Subscriber("front_camera/cmd_vel", Twist, self.joy_command_front_camera)

    @staticmethod
    def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

    def shutdown(self):
        rospy.loginfo(f'{base_pc.node_name} Shutdown on progess')

    def home_off(self):
        pass

    def home_on(self):
        pass

    def spin(self):
        rospy.sleep(0.1)
        self.home_on()
        rate = rospy.Rate(1)  # hz
        while not rospy.is_shutdown():
            rate.sleep()

    def joy_command_front_camera(self, data):
        rospy.loginfo(f'{rospy.get_caller_id()}: joy_front_camera(x:{data.linear.x},y:{data.linear.y})')
        # moveit version
        rospy.loginfo("11")
        joint_goal = self.move_group.get_current_joint_values()
        rospy.loginfo("12")
        joint_goal[0] += data.linear.x * 30
        joint_goal[1] += data.linear.y * 30
        rospy.loginfo(f'{rospy.get_caller_id()}: joint_goal: {joint_goal}')
        rospy.loginfo("1")
        self.move_group.go(joint_goal, wait=True)
        rospy.loginfo("2")
        self.move_group.stop()
        rospy.loginfo("3")
        joint_goal_final = self.move_group.get_current_joint_values()
        rospy.loginfo("4")
        rospy.loginfo(f'{rospy.get_caller_id()}: joint_goal_final(x:{joint_goal[0]},y:{joint_goal[1]})')


if __name__ == '__main__':
    base_pc = BasePc()
    try:
        base_pc.spin()
    except Exception as error:
        rospy.logerr(f'{base_pc.node_name} Error on Main: {error}')
    except rospy.ROSInterruptException:
        rospy.loginfo(f'{base_pc.node_name} Shutdown')
