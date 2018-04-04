#!/usr/bin/env python
#Code taken from github previous year's team that was successful, will make changes to algorithm once i've tested
import rospy
import actionlib
import tf
import os

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import Joy


# Clockwise:
# waypoints = [
    # [(5.94, -1.64, 0.0), (0.0, 0.0, -0.9, 0.13)],
    # [(0.43, -1.16, 0.0), (0.0, 0.0, 0.69, 0.71)],
    # [(0.88, 1.56, 0.0), (0.0, 0.0, 0.0, 0.99)],
    # [(6.49, 0.99, 0.0), (0.0, 0.0, -0.7, 0.7)]
# ]

# Counterclockwise:
# waypoints = [
    # [(6.21, -1.83, 0.0), (0.0, 0.0, 0.7, 0.71)],
    # [(6.29, 1.37, 0.0), (0.0, 0.0, 1.0, 0.0)],
    # # [(6.29, 1.57, 0.0), (0.0, 0.0, 1.0, 0.0)],
    # [(0.48, 1.57, 0.0), (0.0, 0.0, -0.71, 0.7)],
    # [(0.47, -1.58, 0.0), (0.0, 0.0, -0.01, 0.99)]
# ]

# Counterclockwise safe:
waypoints = [
    [(0, 0, 0.0), (0.0, 0.0, 0.5, 0.5)],
    [(0, 0, 0.0), (0.0, 0.0, 0.5, 0)],
    [(0, 0, 0.0), (0.0, 0.0, 0, 0)],
    [(0, 0, 0.0), (0.0, 0.0, 0, 0)]
]


client = None
curr_pose = None
running = False


def goal_pose(pose):
    goal_pose = MoveBaseGoal()
    goal_pose.target_pose.header.frame_id = 'map'
    goal_pose.target_pose.pose.position.x = pose[0][0]
    goal_pose.target_pose.pose.position.y = pose[0][1]
    goal_pose.target_pose.pose.position.z = pose[0][2]
    goal_pose.target_pose.pose.orientation.x = pose[1][0]
    goal_pose.target_pose.pose.orientation.y = pose[1][1]
    goal_pose.target_pose.pose.orientation.z = pose[1][2]
    goal_pose.target_pose.pose.orientation.w = pose[1][3]
    return goal_pose


def joy_callback(msg):
    global running
    global client
    if msg.buttons[2]==1:
        running = not running
    elif msg.buttons[1]==1:
        print 'Exit...'
        client.cancel_goal()
        os._exit(0)


if __name__ == '__main__':
    rospy.init_node('patrol')
    joy_sub = rospy.Subscriber('joy', Joy, joy_callback)
    
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)  # <3>
    client.wait_for_server()

    # Go to the start point:
    client.send_goal(goal_pose(waypoints[0]))
    client.wait_for_result()

    print 'ready'
    
    '''
    while not running:
        pass
    '''
    while True:
    # for _ in range(3):
        for pose in waypoints:
            curr_pose = pose
            goal = goal_pose(pose)
            client.send_goal(goal)
client.wait_for_result()
