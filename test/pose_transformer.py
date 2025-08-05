#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2020 VECTIONEER.
#

import motorcortex
import math
from robot_control.motion_program import PoseTransformer


def is_close(n1, n2, abs_tol=1e-09):
    if len(n1) != len(n2):
        return False
    for n1, n2 in zip(n1, n2):
        if not math.isclose(n1, n2, abs_tol=abs_tol):
            return False
    return True


def main():
    # Creating empty object for parameter tree
    parameter_tree = motorcortex.ParameterTree()

    # Loading protobuf types and hashes
    motorcortex_types = motorcortex.MessageTypes()

    # Open request connection
    req, sub = motorcortex.connect("wss://localhost:5568:5567", motorcortex_types, parameter_tree,
                                   certificate="mcx.cert.pem", timeout_ms=1000,
                                   login="", password="")

    pose_transformer = PoseTransformer(req, motorcortex_types)

    ref_joint_coord = [0, 0, math.radians(90), 0, math.radians(90), 0]
    cart = pose_transformer.calcJointToCartPose(joint_coord_rad=ref_joint_coord)
    ref_cart_coord = cart.jointtocartlist[0].cartpose.coordinates
    print(f"system: {cart}")

    cart1 = pose_transformer.calcJointToCartPose(joint_coord_rad=ref_joint_coord, system_id=1)
    print(f"system1: {cart1}")

    cart2 = pose_transformer.calcJointToCartPose(joint_coord_rad=ref_joint_coord,
                                                 system_id=2)
    print(f"system2: {cart2}")

    joint = pose_transformer.calcCartToJointPose(cart_coord=ref_cart_coord)
    print(f"system: {joint}")
    new_joint_coord = joint.carttojointlist[0].jointpose.coordinates
    if is_close(new_joint_coord, ref_joint_coord):
        print("Reference joint values are equal to calculated values")
    else:
        print("Reference joint values are NOT equal to calculated values")

    joint1 = pose_transformer.calcCartToJointPose(cart_coord=[0.536, -0.23, 1.66, math.pi, 0, math.pi], system_id=1)
    print(f"system1: {joint1}")

    joint2 = pose_transformer.calcCartToJointPose(cart_coord=[0.536, 0.23, 1.66, math.pi, 0, math.pi], system_id=2)
    print(f"system2: {joint2}")

    req.close()
    sub.close()


if __name__ == '__main__':
    main()
