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
    req, sub = motorcortex.connect("wss://192.168.2.101:5568:5567", motorcortex_types, parameter_tree,
                                   certificate="mcx.cert.pem", timeout_ms=1000,
                                   login="", password="")

    # Create robot commands
    robot = RobotCommand(req, motorcortex_types)

    if robot.acknowledge():
        print('Robot is Errors are acknowledged')
    else:
        print('Failed to acknowledge errors')

    if robot.engage():
        print('Robot is at Engage')
    else:
        print('Failed to set robot to Engage')

    time.sleep(1)

    if robot.disengage():
        print('Robot is at Disengage')
    else:
        print('Failed to set robot to disengage')

    time.sleep(1)

    if robot.off():
        print('Robot is Off')
    else:
        print('Failed to set robot to Off')

    time.sleep(1)

    if robot.engage():
        print('Robot is at Engage')
    else:
        print('Failed to set robot to Engage')

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
