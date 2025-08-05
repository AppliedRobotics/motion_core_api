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
                                   certificate="mcx.cert.pem", timeout_ms=5000,
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

    # Circular move
    motion_pr_2 = MotionProgram(req, motorcortex_types)
    motion_pr_2.addMoveC([cart_pos_1, cart_pos_2, cart_pos_3], 3 * math.pi, 0.1, 0.1)

    print('Start to play: {}'.format(robot.getState()))
    motion_pr_2.send("test1").get()
    if robot.play() is InterpreterStates.MOTION_NOT_ALLOWED_S.value:
        print('Robot is not at a start position, moving to the start')
        if robot.moveToStart(10):
            print('Robot is at the start position')
        else:
            raise Exception('Failed to move to the start position')

        robot.play()

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
