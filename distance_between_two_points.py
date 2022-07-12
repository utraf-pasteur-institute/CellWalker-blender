import bpy
import bmesh
import numpy as np 

objects = bpy.context.scene.objects
for obj in objects:
   obj.select_set(obj.type == "MESH")

selected_objects = bpy.context.selected_objects
points = []

for ob in selected_objects:
    bm = bmesh.from_edit_mesh(ob.data)

    for v in bm.verts:
            if (v.select == True):
                obMat = ob.matrix_world
                points.append(obMat @ v.co)

v=points[0]-points[1]
magnitude = np.sqrt(v.dot(v))
print(magnitude)