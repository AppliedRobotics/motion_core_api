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

    jpos_1 = Waypoint(
        [math.radians(0.0), math.radians(0.0), math.radians(90.0),
         math.radians(0.0), math.radians(90.0), math.radians(0.0)])
    jpos_2 = Waypoint(
        [math.radians(0.0), math.radians(0.0), math.radians(0.0),
         math.radians(0.0), math.radians(0.0), math.radians(0.0)])
    jpos_3 = Waypoint(
        [math.radians(15.0), math.radians(0.0), math.radians(0.0),
         math.radians(0.0), math.radians(0.0), math.radians(0.0)])
    jpos_4 = Waypoint(
        [math.radians(15.0), math.radians(0.0), math.radians(90.0),
         math.radians(0.0), math.radians(90.0), math.radians(0.0)])

    # point to point move
    motion_pr_1 = MotionProgram(req, motorcortex_types)
    motion_pr_1.addMoveJ([jpos_1], 1, 1)
    motion_pr_1.addMoveJ([jpos_2], 1, 1)
    motion_pr_1.addMoveJ([jpos_3], 1, 1)
    motion_pr_1.addMoveJ([jpos_4], 1, 1)

    # waypoint move
    motion_pr_2 = MotionProgram(req, motorcortex_types)
    motion_pr_2.addMoveJ([jpos_1, jpos_2, jpos_3, jpos_4, jpos_1], 1, 1)

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
