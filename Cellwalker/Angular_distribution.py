import bpy
from math import pi
import numpy as np


def CALCULATE_Angle(A, B):
    cos_angle = np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))
    angle = np.arccos(cos_angle) / pi * 180
    return angle

def CALCULATE_Centroid(x,y,z):
    return(np.array([np.mean(x), np.mean(y), np.mean(z)]))

def CALCULATE_Angle_distribution(context):
    FA1 = context.scene.objects[context.scene.my_tool_angle.Cell] # Cell/Nucleus
    FA2 = context.scene.objects[context.scene.my_tool_angle.Organelle] # Organelle

    # Get coordinates of Object- Cell/Nucleus object (A cell or a nucleus if nucleus can be assumed to be center of cell)
    FA1vcos = [FA1.matrix_world  @ v.co for v in FA1.data.vertices]
    Cx1, Cy1, Cz1 = [[v[i] for v in FA1vcos] for i in range(3)]

    # Calculating Centerpoint of Object- Cell/Nucleus
    FA1center = CALCULATE_Centroid(Cx1, Cy1, Cz1)

    # Get coordinates of Object- Organelle
    FA2vcos = [FA2.matrix_world  @ v.co for v in FA2.data.vertices]
    Cx2, Cy2, Cz2 = [[v[i] for v in FA2vcos] for i in range(3)]

    # Calculate angles between vectors- 'Cell center to reference point in Oranelle' and 'Cell center to another point in Organelle'
    # Reference point is always the first point in Object1
    angles = []
    C_ref = np.array([Cx2[0], Cy2[0], Cz2[0]])
    for i in range(len(Cx2)):
        C = [Cx2[i], Cy2[i], Cz2[i]]
        C = np.array(C)
        angles.append(CALCULATE_Angle(C_ref - FA1center, C - FA1center))

    angles = np.array(angles)
    
    print('Mean')
    print(angles.mean())
    print('Standard Deviation')
    print(angles.std())

    context.scene.my_tool_angle.Mean = angles.mean()
    context.scene.my_tool_angle.Std = angles.std()

    return(angles)


class OPERATOR_Angle_distribution(bpy.types.Operator):
    bl_idname = "angle.distribution"
    bl_label = "Calculate distribution"
    bl_description = "Measure the angle distribution of all the voxel in one object regarding one point"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        CALCULATE_Angle_distribution(context)
        return {'FINISHED'}


class MySettings_Angle(bpy.types.PropertyGroup):
    Cell: bpy.props.StringProperty()
    Organelle: bpy.props.StringProperty()

    Mean: bpy.props.FloatProperty()
    Std: bpy.props.FloatProperty()
