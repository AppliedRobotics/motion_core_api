#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2020 VECTIONEER.
#

import motorcortex
import math
import time
from robot_control.motion_program import MotionProgram, Waypoint
from robot_control.robot_command import RobotCommand
from robot_control.system_defs import InterpreterStates


def main():
    # Creating empty object for parameter tree
    parameter_tree = motorcortex.ParameterTree()

    # Loading protobuf types and hashes
    motorcortex_types = motorcortex.MessageTypes()

    # Open request connection
    req, sub = motorcortex.connect("wss://localhost:5568:5567", motorcortex_types, parameter_tree,
                                   certificate="mcx.cert.pem", timeout_ms=1000,
                                   login="", password="")

    robot = RobotCommand(req, motorcortex_types)

    if robot.engage():
        print('Robot is at Engage')
    else:
        raise Exception('Failed to set robot to Engage')

    robot.stop()
    robot.reset()

    cart_pos_1 = Waypoint([0.4, 0, 0.295, 0, math.pi, 0])
    cart_pos_2 = Waypoint([0.3, 0, 0.295, 0, math.pi, 0])
    cart_pos_3 = Waypoint([0.3, 0.1, 0.295, 0, math.pi, 0])

    cart_pos_1 = Waypoint([0.4, 0.00, 0.35, 0, math.pi, 0])
    cart_pos_2 = Waypoint([0.4, -0.15, 0.35, 0, math.pi, 0])
    cart_pos_2c = Waypoint([0.4, -0.200, 0.3, 0, math.pi, 0])
    cart_pos_3 = Waypoint([0.4, -0.15, 0.25, 0, math.pi, 0])
    cart_pos_4 = Waypoint([0.4, 0.00, 0.25, 0, math.pi, 0])
    cart_pos_4c = Waypoint([0.4, 0.05, 0.30, 0, math.pi, 0])

    # point to point move
    motion_pr_1 = MotionProgram(req, motorcortex_types)
    motion_pr_1.addMoveL([cart_pos_1], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_2], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_2c], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_3], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_4], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_4c], 0.5, 0.5)

    # waypoint move
    motion_pr_2 = MotionProgram(req, motorcortex_types)
    motion_pr_2.addMoveL([cart_pos_1, cart_pos_2, cart_pos_2c, cart_pos_3, cart_pos_4, cart_pos_4c], 0.1, 0.1)

    print('Start to play: {}'.format(robot.getState()))
    motion_pr_1.send("test1").get()
    if robot.play() is InterpreterStates.MOTION_NOT_ALLOWED_S.value:
        print('Robot is not at a start position, moving to the start')
        if robot.moveToStart(10):
            print('Robot is at the start position')
        else:
            raise Exception('Failed to move to the start position')

        robot.play()

    while robot.getState() is InterpreterStates.PROGRAM_RUN_S.value:
        time.sleep(0.1)
        print('Playing, robot state: {}'.format(robot.getState()))

    print('Continue to play: {}'.format(robot.getState()))
    motion_pr_1.send("test2").get()
    while robot.getState() is InterpreterStates.PROGRAM_IS_DONE.value:
        time.sleep(0.1)
        print('Waiting for the program to start, robot state: {}'.format(robot.getState()))
    while robot.getState() is InterpreterStates.PROGRAM_RUN_S.value:
        time.sleep(0.1)
        print('Playing, robot state: {}'.format(robot.getState()))

    print('Continue to play: {}'.format(robot.getState()))
    motion_pr_2.send("test3").get()
    while robot.getState() is InterpreterStates.PROGRAM_IS_DONE.value:
        time.sleep(0.1)
        print('Waiting for the program to start, robot state: {}'.format(robot.getState()))
    while robot.getState() is InterpreterStates.PROGRAM_RUN_S.value:
        time.sleep(0.1)
        print('Playing, robot state: {}'.format(robot.getState()))

    print('Done!')

    req.close()
    sub.close()


if __name__ == '__main__':
    main()
