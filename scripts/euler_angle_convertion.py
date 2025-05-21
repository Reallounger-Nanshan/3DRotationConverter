# Coordinate system definition:
#     X: forward direction
#     Y: left direction
#     Z: up direction

import argparse
import math
import numpy as np
from rich import print

class EulerAngleConverter():
    def __init__(self, args):
        self.order = args.order

        roll = args.roll * math.pi / 180 if args.unit == "degree" else args.roll
        pitch = args.pitch * math.pi / 180 if args.unit == "degree" else args.pitch
        yaw = args.yaw * math.pi / 180 if args.unit == "degree" else args.yaw

        self.roll_matrix = np.array([[1, 0, 0],
                                     [0, math.cos(roll), math.sin(roll)],
                                     [0, -math.sin(roll), math.cos(roll)]])
        self.pitch_matrix = np.array([[math.cos(pitch), 0, -math.sin(pitch)],
                                      [0, 1, 0],
                                      [math.sin(pitch), 0, math.cos(pitch)]])
        self.yaw_matrix = np.array([[math.cos(yaw), math.sin(yaw), 0],
                                    [-math.sin(yaw), math.cos(yaw), 0],
                                    [0, 0, 1]])
        
        self.epsilon = 1e-6


    def EulerAngle2RotationMatrix(self):
        if self.order == "XYZ":
            self.rotation = self.roll_matrix @ self.pitch_matrix @ self.yaw_matrix
        elif self.order == "XZY":
            self.rotation = self.roll_matrix @ self.yaw_matrix @ self.pitch_matrix
        elif self.order == "YXZ":
            self.rotation = self.pitch_matrix @ self.roll_matrix @ self.yaw_matrix
        elif self.order == "YZX":
            self.rotation = self.pitch_matrix @ self.yaw_matrix @ self.roll_matrix
        elif self.order == "ZXY":
            self.rotation = self.yaw_matrix @ self.roll_matrix @ self.pitch_matrix
        elif self.order == "ZYX":
            self.rotation = self.yaw_matrix @ self.pitch_matrix @ self.roll_matrix

        print(f"\nRotation Matrix:\n{self.rotation}\n")


    def RotationMatrix2Quaternion(self):
        trace = self.rotation[0][0] + self.rotation[1][1] + self.rotation[2][2]

        if (1 + trace) ** 0.5 > self.epsilon:
            q0 = (1 + trace) ** 0.5 / 2
            q1 = (self.rotation[2][1] - self.rotation[1][2]) / (4 * q0)
            q2 = (self.rotation[0][2] - self.rotation[2][0]) / (4 * q0)
            q3 = (self.rotation[1][0] - self.rotation[0][1]) / (4 * q0)
        elif max(self.rotation[0][0], self.rotation[1][1], self.rotation[2][2]) == self.rotation[0][0]:
            t = (1 - trace + 2 * self.rotation[0][0]) ** 0.5
            q0 = (self.rotation[2][1] - self.rotation[1][2]) / t
            q1 = t / 4
            q2 = (self.rotation[0][2] + self.rotation[2][0]) / t
            q3 = (self.rotation[0][1] + self.rotation[1][0]) / t
        elif max(self.rotation[0][0], self.rotation[1][1], self.rotation[2][2]) == self.rotation[1][1]:
            t = (1 - trace + 2 * self.rotation[1][1]) ** 0.5
            q0 = (self.rotation[0][2] - self.rotation[2][0]) / t
            q1 = (self.rotation[0][1] + self.rotation[1][0]) / t
            q2 = t / 4
            q3 = (self.rotation[2][1] + self.rotation[1][2]) / t
        elif max(self.rotation[0][0], self.rotation[1][1], self.rotation[2][2]) == self.rotation[2][2]:
            t = (1 - trace + 2 * self.rotation[2][2]) ** 0.5
            q0 = (self.rotation[1][0] - self.rotation[0][1]) / t
            q1 = (self.rotation[0][2] + self.rotation[2][0]) / t
            q2 = (self.rotation[1][2] + self.rotation[2][1]) / t
            q3 = t / 4

        self.quaternion = np.array([q0, q1, q2, q3])

        print(f"\nQuaternion(w, x, y, z):\n{self.quaternion}\n")


    def Run(self):
        euler_angle_converter.EulerAngle2RotationMatrix()
        euler_angle_converter.RotationMatrix2Quaternion()


def LoadParameters():
    parser = argparse.ArgumentParser()

    parser.add_argument("--order", type = str, default = "XYZ", help = "Rotation order, i.e. XYZ, XZY, YXZ, YZX, ZXY, ZYX")
    parser.add_argument("--roll", type = float, default = "0", help = "Roll angle, right roll for a positive direction")
    parser.add_argument("--pitch", type = float, default = "0", help = "Pitch angle, head down for a positive direction")
    parser.add_argument("--yaw", type = float, default = "0", help = "Yaw angle, left deflection for a positive direction")
    parser.add_argument("--unit", type = str, default = "degree", help = "Rotation angle unit, i.e. degree and radian")

    args = parser.parse_args()

    return args


if __name__=="__main__":
    args = LoadParameters()
    euler_angle_converter = EulerAngleConverter(args)
    euler_angle_converter.Run()
    