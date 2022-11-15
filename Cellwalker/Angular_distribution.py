import bpy
from math import pi
import numpy as np


def CALCULATE_Angle(A, B):
    cos_angle = np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))
    angle = np.arccos(cos_angle) / pi * 180
    return angle


def CALCULATE_Angle_distribution(context):
    FA1=context.scene.objects[context.scene.my_tool_angle.A1]
    FA2=context.scene.objects[context.scene.my_tool_angle.Object1]

    # Calculating Centerpoint of Object 1
    FA1vcos = [FA1.matrix_world  @ v.co for v in FA1.data.vertices]
    findCenter = lambda l: (max(l) + min(l)) / 2

    Cx1, Cy1, Cz1 = [[v[i] for v in FA1vcos] for i in range(3)]
    FA1center = [findCenter(axis) for axis in [Cx1, Cy1, Cz1]]

    # Calculating Centerpoint of Object 1
    FA2vcos = [FA2.matrix_world  @ v.co for v in FA2.data.vertices]

    Cx2, Cy2, Cz2 = [[v[i] for v in FA2vcos] for i in range(3)]

    angles =[]
    C_ref = np.array([Cx2[0], Cy2[0], Cz2[0]])
    for i in range(len(Cx2)):
        C = [Cx2[i], Cy2[i], Cz2[i]]
        C = np.array(C)
        angles.append(CALCULATE_Angle(C_ref - FA1center, C - FA1center))

    ftangles = np.array(angles[1:len(angles)])

    print('Mean')
    print(ftangles.mean())
    print('Standard Deviation')
    print(ftangles.std())

    context.scene.my_tool_angle.Mean=ftangles.mean()
    context.scene.my_tool_angle.Std = ftangles.std()

    return(ftangles)


class OPERATOR_Angle_distribution(bpy.types.Operator):
    bl_idname = "angle.distribution"
    bl_label = "Calculate distribution"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        CALCULATE_Angle_distribution(context)
        return {'FINISHED'}


class MySettings_Angle(bpy.types.PropertyGroup):
    A1: bpy.props.StringProperty()
    Object1: bpy.props.StringProperty()
    Mean: bpy.props.FloatProperty()
    Std: bpy.props.FloatProperty()

