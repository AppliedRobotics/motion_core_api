#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2017-2020 VECTIONEER.
#

import motorcortex
from robot_control import to_radians
from robot_control.robot_command import RobotCommand
from robot_control.motion_program import MotionProgram, Waypoint
from robot_control.system_defs import InterpreterStates
import time


def main():
    # Creating empty object for parameter tree
    parameter_tree = motorcortex.ParameterTree()

    # Loading protobuf types and hashes
    motorcortex_types = motorcortex.MessageTypes()

    # Open request connection
    req, sub = motorcortex.connect("wss://localhost:5568:5567", motorcortex_types, parameter_tree,
                                   certificate="mcx.cert.pem", timeout_ms=1000,
                                   login="", password="")

    # Create robot commands
    robot = RobotCommand(req, motorcortex_types)

    # Building example program
    motion_program = MotionProgram(req, motorcortex_types)

    start_position_jnt = Waypoint(to_radians([0.0, 0.0, 90.0, 0.0, 90.0, 0.0]))
    jpos_1 = Waypoint(to_radians([15.0, 0.0, 90.0, 0.0, 90.0, 0.0]))
    jpos_2 = Waypoint(to_radians([30.0, 15.0, 90.0, 0.0, 90.0, 0.0]))
    jpos_3 = Waypoint(to_radians([-30.0, -15.0, 90.0, 15.0, 90.0, 15.0]))

    motion_program.addMoveJ([start_position_jnt], 0.5, 0.5)
    motion_program.addMoveJ([jpos_1, jpos_2], 1.0, 0.5)
    motion_program.addMoveJ([jpos_2, jpos_3], 0.5, 1.0)
    motion_program.addMoveJ([start_position_jnt], 1.0, 0.3)

    # engage the robot
    if robot.engage():
        print('Robot is at Engage')
    else:
        print('Failed to set robot to Engage')

    robot.reset()

    # send the program
    program_sent = motion_program.send("example1").get()
    if program_sent.status == motorcortex.OK:
        print("Motion Program sent")
    else:
        raise RuntimeError("Failed to send Motion Program")

    # try to play the program
    if robot.play() == InterpreterStates.PROGRAM_RUN_S.value:
        print("Playing program")
    elif robot.play() == InterpreterStates.MOTION_NOT_ALLOWED_S.value:
        print("Can not play program, Robot is not at start")
        print("Moving to start")
        if robot.moveToStart(100):
            print("Move to start completed")
            if robot.play() == InterpreterStates.PROGRAM_RUN_S.value:
                print("Playing program")
            else:
                raise RuntimeError("Failed to play program, state: %s" % robot.getState())
        else:
            raise RuntimeError('Failed to move to start')
    else:
        raise RuntimeError("Failed to play program, state: %s" % robot.getState())

    # waiting until the program is finished
    while robot.getState() != InterpreterStates.PROGRAM_IS_DONE.value:
        time.sleep(1)

    # switch off the robot
    if robot.off():
        print('Robot is Off')
    else:
        print('Failed to set robot to Off')

    req.close()
    sub.close()


if __name__ == '__main__':
    main()
