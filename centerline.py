import bpy
import bmesh
import numpy as np 

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

v=points[0]-points[1]
magnitude = np.sqrt(v.dot(v))

nstep=magnitude/0.05
step=v/int(nstep)

for i in range (int(nstep)): 
    arr=points[1]+step*i
    verts.append([arr[0],arr[1],arr[2]])

emptyMesh.from_pydata(vets, [], [])
emptyMesh.update()