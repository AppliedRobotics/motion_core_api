#
# Created by Alexander Filchenkov by 04.02.2025
#
import motorcortex
import os
import time
from math import pi

from robot_control.motion_program import Waypoint, MotionProgram, PoseTransformer
from robot_control import RobotCommand
from robot_control.system_defs import InterpreterStates 

class MCX():
    def __init__(self):
        self._path = os.path.dirname(os.path.abspath(__file__))
        self.__connect = False
     
    def connect(self, ip: str) -> bool:
        parameter_tree = motorcortex.ParameterTree()
        self.motorcortex_types = motorcortex.MessageTypes()
        license_file = os.path.join(
            self._path, 'license', 'mcx.cert.pem')
        try:
            self.req, self.sub = motorcortex.connect(f'wss://{ip}:5568:5567', self.motorcortex_types, parameter_tree,
                                                    timeout_ms=1000, certificate=license_file,
                                                    login="admin", password="vectioneer")
            self.subscription = self.sub.subscribe(
                ["root/ManipulatorControl/manipulatorToolPoseActual"], 'group1', 1)

        except Exception as e:
            print(f"ip: {ip}")
            print(f"license path: {license_file}")
            print(f"Failed to establish connection: {e}")
            return False

        self.robot = RobotCommand(self.req, self.motorcortex_types)

        if self.robot.engage():
            print('Robot is at Engage')
        else:
            print('Failed to set robot to Engage')
            self.__connect = False
            return self.__connect

        self.robot.reset()
        self.__connect = True
        return self.__connect
        
    def move_to_start(self) -> None:
        motion_program = MotionProgram(self.req, self.motorcortex_types)
        motion_program.addMoveJ([Waypoint(pose=[0.0, 0.0, pi/2, 0.0, pi/2, 0.0])], 0.5, 0.5)
        self.move_program(motion_program)
                 
    def move_program(self, motion_program: MotionProgram):
        motion_program.send()

        if self.robot.play(0.5) is InterpreterStates.MOTION_NOT_ALLOWED_S.value:
            print('Robot is not at a start position, moving to the start')
            if self.robot.moveToStart(200):
                print('Robot is at the start position')
            else:
                raise Exception('Failed to move to the start position')

        self.robot.play(0.5)
        if self.robot.getState() is InterpreterStates.PROGRAM_RUN_S.value:
            pass

        while self.robot.getState() is InterpreterStates.PROGRAM_RUN_S.value:
            params = self.subscription.read()
            value = params[0].value
            time.sleep(0.1)
    
    def set_tool(self, value: bool) -> bool:
        return self.req.setParameter("root/UserParameters/IO/Gripper", value).get()
    
    def get_connection(self) -> bool:
        return self.__connect
    
    def get_joint_pos(self):
        return self.req.getParameter("root/ManipulatorControl/jointPositionsActual").get()[2]
    
    def get_cart_pos(self):
        return self.req.getParameter("root/ManipulatorControl/manipulatorToolPoseActual").get()[2]
    
    def calc_inverse_kinematic(self, cart: list[float]) -> list[float] | None:
        pose_transformer = PoseTransformer(self.req, self.motorcortex_types)
        return pose_transformer.calcCartToJointPose(cart_coord=cart).carttojointlist[0].jointpose.coordinates
        
    def calc_forward_kinematic(self, joints: list[float]) -> list[float] | None:
        pose_transformer = PoseTransformer(self.req, self.motorcortex_types)
        return pose_transformer.calcJointToCartPose(joint_coord_rad=joints).jointtocartlist[0].cartpose.coordinates
            
if __name__ == "__main__":
    mcx = MCX()
    try:
        mcx.connect("192.168.2.100")
        
        if mcx.get_connection():
            # Example MOVL
            # pose - x, y, z (meter) rz, ry, rx - radian
            motion_program = MotionProgram(mcx.req, mcx.motorcortex_types)
            p1 = Waypoint(pose=[0.8, 0.0, 0.5, pi/2, 0.0, pi])
            p2 = Waypoint(pose=[0.5, 0.0, 0.5, pi/2, 0.0, pi])
            p3 = Waypoint(pose=[0.5, 0.2, 0.5, pi/2, 0.0, pi])
            motion_program.addMoveL([p1, p2, p3])
            mcx.move_program(motion_program)
            
            mcx.move_to_start()
            
            # Example MOVJ
            motion_program = MotionProgram(mcx.req, mcx.motorcortex_types)
            p1 = Waypoint(pose=[0.0, 0.0, pi/2, 0.0, pi/2, 0.0])
            p2 = Waypoint(pose=[0.0, 0.0, 0.0, 0.0, pi/2, 0.0])
            p3 = Waypoint(pose=[pi/2, 0.0, 0.0, 0.0, pi/2, 0.0])
            motion_program.addMoveJ([p1, p2, p3], rotational_velocity=0.5, rotational_acceleration=0.5)
            mcx.move_program(motion_program)
            
            mcx.move_to_start()
            
            # Example MOVC
            # pose - x, y, z (meter) rz, ry, rx - radian
            motion_program = MotionProgram(mcx.req, mcx.motorcortex_types)
            p1 = Waypoint(pose=[0.8, 0.0, 0.5, pi/2, 0.0, pi])
            p2 = Waypoint(pose=[0.5, 0.0, 0.5, pi/2, 0.0, pi])
            p3 = Waypoint(pose=[0.5, 0.2, 0.5, pi/2, 0.0, pi])
            motion_program.addMoveC([p1, p2, p3], 0.0)
            mcx.move_program(motion_program)
            
            # On/Off Tool
            mcx.set_tool(True)
            time.sleep(5)
            mcx.set_tool(False)
            
            # Get joint position coordinate
            joints = mcx.get_joint_pos()
            print("\nGet joint position:", joints)
            print("j1:", joints[0])
            
            # Get cartesian position coordinate
            cart = mcx.get_cart_pos()
            print("\nGet cart position:", cart)
            print("x:", cart[0])
            
            # Inverse Kinematic
            print("\nInverse kinematic:", mcx.calc_inverse_kinematic([0.85, -0.191, 0.7835, pi/2, 0.0, pi]))
            
            # Forward Kinematic
            print("\nForward Kinematic:", mcx.calc_forward_kinematic([0.0, 0.0, pi/2, 0.0, pi/2, 0.0]))
        
    except Exception as e:
        print(e)