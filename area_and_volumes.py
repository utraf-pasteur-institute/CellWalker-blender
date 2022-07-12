import bpy
import os
import glob
model_dir = "C:/Users/utraf/Documents/Nathaly/inesprojecto/"
model_files = glob.glob(os.path.join(model_dir, "*.obj"))
for f in model_files:
    head, tail = os.path.split(f)
    collection_name = tail.replace(".obj", "")
    bpy.ops.import_scene.obj(filepath=f, axis_forward="Y",axis_up="Z")


import bpy
import bmesh
context = bpy.context
scene = context.scene

bm = bmesh.new()
# import from obj file here, only imported objects will be 
# in context.selected_objects after import.    
for o in context.selected_objects:
    # test here to continue if not mesh, can obj import other???
    # load bmesh
    bm.from_mesh(o.data)
    # find boundaries
    bound_edges = set(e for e in bm.edges if e.is_boundary)
    # used sets, may not be required.
    zero_edges = set(e for e in bound_edges 
        if all(abs(v.co.x) < 0.001 for v in e.verts))
    right_edges = bound_edges - zero_edges
    # use bmesh "F" tool
    result = bmesh.ops.contextual_create(bm, geom=list(bound_edges))
    # poke the resulting faces to make triangular fan.
    bmesh.ops.poke(bm, faces=result["faces"])
    bm.to_mesh(o.data)
    o.data.update() # mainly only need for UI really
    bm.clear()
bm.free()

import bpy
import bmesh
import pandas as pd

context = bpy.context
scene = context.scene

bm = bmesh.new()
df = pd.DataFrame(columns=['obj_name', 'area', 'volume'])
columns = list(df)
data = []

# import from obj file here, only imported objects will be 
# in context.selected_objects after import.    
for obj in context.selected_objects:
    bm.from_mesh(obj.data)

    area = sum(f.calc_area() for f in bm.faces)
    volume = float( bm.calc_volume() )
    values = [obj.name,area,volume]
    zipped = zip(columns, values)
    a_dictionary = dict(zipped)
    data.append(a_dictionary)

bm.free()

df = df.append(data, True)
print(df)