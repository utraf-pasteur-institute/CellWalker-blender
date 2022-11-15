import bpy
import numpy as np
import math
from math import pi
from mathutils import Matrix, Vector

def set_origin():
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.mode_set(mode='EDIT')

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))/ pi * 180

def calculate_plane(xs, ys, zs):
    # do fit
    tmp_A = []
    tmp_b = []
    for i in range(len(xs)):
        tmp_A.append([xs[i], ys[i], 1])
        tmp_b.append(zs[i])
    b = np.matrix(tmp_b).T
    A = np.matrix(tmp_A)

    # Manual solution
    fit = (A.T * A).I * A.T * b
    errors = np.mean(b - A * fit)
    residual = np.linalg.norm(errors)
    # Or use Scipy
    # from scipy.linalg import lstsq
    # fit, residual, rnk, s = lstsq(A, b)

    print("solution: %f x + %f y + %f = z" % (fit[0], fit[1], fit[2]))
    print("errors: \n", errors)
    print("residual:", residual)

    return(fit)

def CALCULATE_Orientation(context):
    findCenter = lambda l: (max(l) + min(l)) / 2

    Ob1 = context.scene.objects[context.scene.my_tool_or.Obj1]
    # Calculating Plane Equation
    Ob1vcos = [Ob1.matrix_world @ v.co for v in Ob1.data.vertices]
    x1, y1, z1 = [[v[i] for v in Ob1vcos] for i in range(3)]
    Ob1center = [findCenter(axis) for axis in [x1, y1, z1]]

    Ob2 = context.scene.objects[context.scene.my_tool_or.Obj2]
    # Calculating Plane Equation
    Ob2vcos = [Ob2.matrix_world @ v.co for v in Ob2.data.vertices]
    x2, y2, z2 = [[v[i] for v in Ob2vcos] for i in range(3)]
    Ob2center = [findCenter(axis) for axis in [x2, y2, z2]]

    ########### Calculating Plane Variables ###########
    Plane = context.scene.objects[context.scene.my_tool_or.pointer_Plane]
    Planevcos = [Ob1.matrix_world @ v.co for v in Plane.data.vertices]
    xs, ys, zs = [[v[i] for v in Planevcos] for i in range(3)]

    fit=calculate_plane(xs, ys, zs)

    ########### Orientation of Two  ###########
    print(Ob1center)
    print(Ob2center)
    v1=np.array(Ob1center)-np.array(Ob2center)
    v2=np.array([fit[0], fit[1], fit[2]])

    v1_v2_angle=angle(v1, v2)
    print(v1_v2_angle)
    context.scene.my_tool_or.Angle_Or=v1_v2_angle,
    return(v1_v2_angle)

class OPERATOR_Orientation(bpy.types.Operator):
    bl_idname = "angle.orientation"
    bl_label = "Calculate orientation"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        CALCULATE_Orientation(context)
        return {'FINISHED'}


class MySettings_Orientation(bpy.types.PropertyGroup):
    Obj1: bpy.props.StringProperty()
    Obj2: bpy.props.StringProperty()
    pointer_Plane: bpy.props.StringProperty()
    Angle_Or: bpy.props.FloatProperty()