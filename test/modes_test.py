#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2017-2020 VECTIONEER.
#

import motorcortex
from robot_control.robot_command import RobotCommand
import time


def main():
    # Creating empty object for parameter tree
    parameter_tree = motorcortex.ParameterTree()

    # Loading protobuf types and hashes
    motorcortex_types = motorcortex.MessageTypes()

    # Open request connection
    req, sub = motorcortex.connect("wss://192.168.2.100:5568:5567", motorcortex_types, parameter_tree,
                                   certificate="mcx.cert.pem", timeout_ms=1000,
                                   login="", password="")

    # Create robot commands
    robot = RobotCommand(req, motorcortex_types)

    robot.reset()

    if robot.engage():
        print('Robot is at Engage')
    else:
        print('Failed to set robot to Engage')

    time.sleep(1)

    if robot.manualCartMode():
        print('Robot is in Manual Cartesian Mode')
    else:
        print('Failed to set robot to Manual Cartesian Mode')

    time.sleep(1)

    if robot.manualJointMode():
        print('Robot is in Manual Joint Mode')
    else:
        print('Failed to set robot to Manual Joint Mode')

    time.sleep(1)

    if robot.manualCartMode():
        print('Robot is in Manual Cartesian Mode')
    else:
        print('Failed to set robot to Manual Cartesian Mode')

    time.sleep(1)

    if robot.off():
        print('Robot is Off')
    else:
        print('Failed to set robot to Off')

    time.sleep(1)

    req.close()
    sub.close()


if __name__ == '__main__':
    main()
