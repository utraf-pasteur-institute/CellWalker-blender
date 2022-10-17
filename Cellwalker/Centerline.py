import bpy
import bmesh
import numpy as np

class MESH_OT_make_centerline(bpy.types.Operator):
    bl_idname = "mesh.make_centerline"
    bl_label = "Create centerline"
    bl_description = "Create a line between selected vertices"

    def execute(self, context):
        bm = bmesh.new()
        ob = bpy.context.active_object
        bm = bmesh.from_edit_mesh(bpy.context.active_object.data)

        points = []
        for v in bm.verts:
            if (v.select == True):
                obMat = ob.matrix_world
                points.append(obMat @ v.co)

        emptyMesh = bpy.data.meshes.new('emptyMesh')
        theObj = bpy.data.objects.new("centerline", emptyMesh)
        bpy.context.collection.objects.link(theObj)

        verts = []

        v = points[0] - points[1]
        magnitude = np.sqrt(v.dot(v))

        nstep = magnitude / 0.1#0.05
        step = v / int(nstep)

        for i in range(int(nstep)):
            arr = points[1] + step * i
            verts.append([arr[0], arr[1], arr[2]])

        emptyMesh.from_pydata(verts, [], [])
        emptyMesh.update()

        return {'FINISHED'}