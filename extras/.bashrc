# shellcheck shell=bash

# ros 2 - 4.2.2021
#source /opt/ros/foxy/setup.bash
#source /usr/share/colcon_cd/function/colcon_cd.sh
#export _colcon_cd_root=~/workspace-ros2
#export ROS_VERSION=2
#export ROS_PYTHON_VERSION=3
#export ROS_DISTRO=foxy
# ros 1 - 14.2.2021
source /opt/ros/noetic/setup.bash
export ROS_VERSION=1
export ROS_PYTHON_VERSION=3
export ROS_DISTRO=noetic

# ros - 31.12.2018
#ros-env kinetic
#source activate ros-env
#source /opt/ros/kinetic/setup.bash
# solo il nodo locale
#export ROS_HOSTNAME=localhost
#export ROS_MASTER_URI=http://localhost:11311
# anche con nodi remoti
export ROS_HOSTNAME=aldebaran
export ROS_MASTER_URI=http://192.168.147.85:11311  # rosrobot
export ROS_IP=192.168.147.70
#
#my ros workspace
source $HOME/workspace-ros1/devel/setup.bash || exit
