#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2020 VECTIONEER.
#

import motorcortex
import math
import time
from robot_control.motion_program import MotionProgram, Waypoint, sendProgramList
from robot_control.multirobot_command import MultiRobotCommand, isEqual
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

    dual_arm = MultiRobotCommand(req, motorcortex_types, [1, 2])

    if dual_arm.engage():
        print('Robot is at Engage')
    else:
        raise Exception('Failed to set robot to Engage')

    dual_arm.stop()
    dual_arm.reset()

    cart_pos_1 = Waypoint([0.4, 0, 1.4, 0, math.pi, 0])
    cart_pos_2 = Waypoint([0.3, 0, 1.4, 0, math.pi, 0])
    cart_pos_3 = Waypoint([0.3, 0.1, 1.4, 0, math.pi, 0])

    # point to point move
    motion_pr_1 = MotionProgram(req, motorcortex_types, True)
    motion_pr_1.addMoveL([cart_pos_1], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_2], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_3], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_1], 0.5, 0.5)

    # waypoint move
    motion_pr_2 = MotionProgram(req, motorcortex_types, True)
    motion_pr_2.addMoveC([cart_pos_1, cart_pos_2, cart_pos_3], 10, 0.1, 10)

    print('Start to play: {}'.format(dual_arm.getState()))
    sendProgramList(req, motorcortex_types, [motion_pr_1, motion_pr_1], [1, 2]).get()

    dual_arm.moveToStart(10)

    dual_arm.play()
    #
    while not isEqual(dual_arm.getState(), InterpreterStates.PROGRAM_RUN_S.value):
        time.sleep(0.1)
        print('Waiting for the program to start, robot state: {}'.format(dual_arm.getState()))
    #
    while not isEqual(dual_arm.getState(), InterpreterStates.PROGRAM_IS_DONE.value):
        time.sleep(0.1)
        print('Playing, robot state: {}'.format(dual_arm.getState()))

    print('Start to play: {}'.format(dual_arm.getState()))
    sendProgramList(req, motorcortex_types, [motion_pr_2, motion_pr_2], [1, 2]).get()
    #
    while not isEqual(dual_arm.getState(), InterpreterStates.PROGRAM_RUN_S.value):
        time.sleep(0.1)
        print('Waiting for the program to start, robot state: {}'.format(dual_arm.getState()))
    #
    while not isEqual(dual_arm.getState(), InterpreterStates.PROGRAM_IS_DONE.value):
        time.sleep(0.1)
        print('Playing, robot state: {}'.format(dual_arm.getState()))

    req.close()
    sub.close()


if __name__ == '__main__':
    main()
