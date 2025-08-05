#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2020 VECTIONEER.
#

import motorcortex
import math
from robot_control.robot_command import RobotCommand


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

    if robot.moveToPoint(jpos_1):
        print("Moved robot to jpos_1")
    else:
        print("Failed to move robot to jpos_1")

    if robot.moveToPoint(jpos_2):
        print("Moved robot to jpos_2")
    else:
        print("Failed to move robot to jpos_2")

    if robot.moveToPoint(jpos_3):
        print("Moved robot to jpos_3")
    else:
        print("Failed to move robot to jpos_3")

    if robot.moveToPoint(jpos_4):
        print("Moved robot to jpos_4")
    else:
        print("Failed to move robot to jpos_4")

    print('Done!')

    req.close()
    sub.close()


if __name__ == '__main__':
    main()
