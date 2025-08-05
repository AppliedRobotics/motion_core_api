#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2020 VECTIONEER.
#

import motorcortex
import math
import time
from robot_control.motion_program import Waypoint, MotionProgram
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

    jpos_1 = [math.radians(0.0), math.radians(0.0), math.radians(90.0),
              math.radians(0.0), math.radians(90.0), math.radians(0.0)]
    jpos_2 = [math.radians(0.0), math.radians(0.0), math.radians(0.0),
              math.radians(0.0), math.radians(0.0), math.radians(0.0)]
    jpos_3 = [math.radians(15.0), math.radians(0.0), math.radians(0.0),
              math.radians(0.0), math.radians(0.0), math.radians(0.0)]
    jpos_4 = [math.radians(15.0), math.radians(0.0), math.radians(90.0),
              math.radians(0.0), math.radians(90.0), math.radians(0.0)]

    print("Moving to jpos_1")
    if robot.moveToPoint(jpos_1):
        print("Moved robot to jpos_1")
    else:
        print("Failed to move robot to jpos_1")

    print("Setting new tool tip offset")
    if robot.toolTipOffset([0.1, 0, 0.0]):
        print("Set new tool tip offset")
    else:
        raise Exception("Failed to set new tool tip offset")

    print("Moving to jpos_2")
    if robot.moveToPoint(jpos_2):
        print("Moved robot to jpos_2")
    else:
        print("Failed to move robot to jpos_2")

    print("Setting new tool tip offset")
    if robot.toolTipOffset([0, 0, 0.2]):
        print("Set new tool tip offset")
    else:
        raise Exception("Failed to set new tool tip offset")

    print("Moving to jpos_3")
    if robot.moveToPoint(jpos_3):
        print("Moved robot to jpos_3")
    else:
        print("Failed to move robot to jpos_3")

    print("Setting new tool tip offset")
    if robot.toolTipOffset([0, 0.1, 0.1]):
        print("Set new tool tip offset")
    else:
        raise Exception("Failed to set new tool tip offset")

    print("Moving to jpos_4")
    if robot.moveToPoint(jpos_4):
        print("Moved robot to jpos_4")
    else:
        print("Failed to move robot to jpos_4")

    robot.stop()
    robot.reset()

    cart_pos_1 = Waypoint([0.4, 0, 0.295, 0, math.pi, 0])
    cart_pos_2 = Waypoint([0.3, 0, 0.295, 0, math.pi, 0])
    cart_pos_3 = Waypoint([0.3, 0.1, 0.295, 0, math.pi, 0])

    # point to point move
    motion_pr_1 = MotionProgram(req, motorcortex_types)
    motion_pr_1.addMoveL([cart_pos_1], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_2], 0.5, 0.5)
    motion_pr_1.addMoveL([cart_pos_3], 0.5, 0.5)

    # waypoint move
    motion_pr_2 = MotionProgram(req, motorcortex_types)
    motion_pr_2.addMoveL([cart_pos_1, cart_pos_2, cart_pos_3], 0.1, 0.1)
    motion_pr_1.send("test1").get()

    print("Setting new tool tip offset")
    if robot.toolTipOffset([0, 0, 0.0]):
        print("Set new tool tip offset")
    else:
        raise Exception("Failed to set new tool tip offset")

    print('Start to play: {}'.format(robot.getState()))
    robot.play()
    if robot.moveToStart(10):
        print('Robot is at the start position')
        robot.play()
    else:
        raise Exception('Failed to move to the start position')
    while robot.getState() is InterpreterStates.PROGRAM_IS_DONE.value:
        time.sleep(0.1)
        print('Waiting for the program to start, robot state: {}'.format(robot.getState()))
    while robot.getState() is InterpreterStates.PROGRAM_RUN_S.value:
        time.sleep(0.1)
        print('Playing, robot state: {}'.format(robot.getState()))

    motion_pr_1.send("test2").get()
    print("Setting new tool tip offset")
    if robot.toolTipOffset([0.1, 0.1, 0.0]):
        print("Set new tool tip offset")
    else:
        raise Exception("Failed to set new tool tip offset")

    print('Start to play: {}'.format(robot.getState()))
    robot.play()
    if robot.moveToStart(10):
        print('Robot is at the start position')
        robot.play()
    else:
        raise Exception('Failed to move to the start position')
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

    print("Setting new tool tip offset")
    if robot.toolTipOffset([0.0, 0.0, 0.1]):
        print("Set new tool tip offset")
    else:
        raise Exception("Failed to set new tool tip offset")

    print('Done!')

    req.close()
    sub.close()


if __name__ == '__main__':
    main()
