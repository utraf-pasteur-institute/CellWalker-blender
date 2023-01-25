import os
import sys

import numpy as np
np.set_printoptions(threshold=sys.maxsize)

import bmesh
import bpy

def import_global():
    global sk, kimimaro, multiprocess, trimesh, creation, scipy
    import skeletor as sk
    import kimimaro
    import multiprocess
    import trimesh
    from trimesh.voxel import creation
    import scipy


# Future work: Use this section to define skeleton import function.
#axis_forward = 'Y'
#axis_up = 'Z'
#bpy.ops.import_scene.obj(filepath=fname, axis_forward=axis_forward, axis_up=axis_up)
# Currently, importing a skeleton OBJ file through Blender's OBJ import may not align it correctly. Setting the orientations is important.
    
def saveSkeletonObjFile(fname=""):
    if fname == "":
        print("No output file specified.")
        return(0)
    bpy.ops.export_scene.obj(filepath=fname+"/"+bpy.context.object.name+".obj", use_selection=True)

class export_operator_sk(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "sk.export"
    bl_label = "Save skeleton"
    bl_description = "Save skeleton as a .OBJ file"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        saveSkeletonObjFile(fname=bpy.context.scene.my_tool_skeleton.path_skeleton)
        return {'FINISHED'}

class MESH_OT_skeletonize(bpy.types.Operator):
    bl_idname = "mesh.skeletonize"
    bl_label = "Skeletonize"
    bl_description = "Skeletonize selected mesh/object"

    def execute(self, context):
        import_global()
        
        bm = bmesh.new()
        bm.from_mesh(bpy.context.object.data)

        verts = np.array([list(v.co) for v in bm.verts])
        edges = np.array([list([e.verts[0].index,e.verts[1].index]) for e in bm.edges])

        # To get triangulated meshes, do this
        bmt = bmesh.ops.triangulate(bm, faces=bm.faces[:])
        faces = np.array([list([f.verts[0].index,f.verts[1].index,f.verts[2].index]) for f in bmt['faces']])

        #bmt['faces'][1].verts[0].index

        print("Vertices:", verts.shape)
        print("Edges:", edges.shape)
        print("Faces:", faces.shape)

        mesh = trimesh.Trimesh(vertices=verts, faces=faces)

        #print(mesh)
        #print(mesh.vertices)
        min_mesh = np.min(mesh.vertices, axis=0)
        max_mesh = np.max(mesh.vertices, axis=0)
        print("Minimum of mesh vertices:", min_mesh)
        print("Maximum of mesh vertices:", max_mesh)

        self.translate_x = min_mesh[0]
        self.translate_y = min_mesh[1]
        self.translate_z = min_mesh[2]
        print("Translation parameters:", self.translate_x, self.translate_y, self.translate_z)

        ######### Depricated section
        def skeletonize_skeletor():
            # Optional skeletonization method.
            #sk.pre.simplify(mesh, 0.5)

            fixed = sk.pre.fix_mesh(mesh, remove_disconnected=5, inplace=False)
            skel = sk.skeletonize.by_wavefront(fixed, waves=1, step_size=10)

            print("Skeleton before cleanup:", skel)
            sk.post.clean_up(skel, inplace=True)
            print("Skeleton after cleanup:", skel)

            skelmesh = bpy.data.meshes.new('emptyMesh')
            skelobj = bpy.data.objects.new("skeleton", skelmesh)
            bpy.context.collection.objects.link(skelobj)
            skelmesh.from_pydata(skel.vertices, skel.edges, [])
            skelmesh.update()

            #mesh = sk.example_mesh()
            #fixed = sk.pre.fix_mesh(mesh, remove_disconnected=5, inplace=False)
            #skel = sk.skeletonize.by_wavefront(fixed, waves=1, step_size=1)
            #print(skel)

        #skeletonize_skeletor()
        ######### END Depricated section

        def skeletonize_kimimaro():
            # Preferred skeletonization method.
            
            voxelsize = 0.05#0.1 #0.5 # 0.03
            volume = trimesh.voxel.creation.voxelize(mesh, voxelsize, method='subdivide')
            voxels = scipy.ndimage.morphology.binary_fill_holes(volume.matrix)
            #print(voxels.astype(int))
            #print(volume)
            #print("***** voxels")
            #print(type(voxels))
            #print("***")

            skels = kimimaro.skeletonize(
                voxels,
                teasar_params={
                    'scale': float(1), #self.kimimaro_scale_entry.get()),  # 1,#0.1,#4,
                    'const': float(500), #self.kimimaro_const_entry.get()),  # 2000,#500,
                    'pdrf_exponent': 4,
                    'pdrf_scale': 100000,
                    'soma_detection_threshold': 1100,
                    'soma_acceptance_threshold': 3500,
                    'soma_invalidation_scale': 1.0,
                    'soma_invalidation_const': 300,
                },
                dust_threshold=1000,
                anisotropy=(voxelsize, voxelsize, voxelsize), #(nm_x, nm_y, nm_z),
                fix_branching=True,
                progress=False,  # default False, show progress bar
                fix_borders=True,  # default True
                parallel=1,  # <= 0 all cpu, 1 single process, 2+ multiprocess
                parallel_chunk_size=100  # how many skeletons to process before updating progress bar
            )

            print("Skeletonization done.")
            print(skels)

            # Merge skeletons into one skeleton object
            if not skels:
                print("No skeleton found")
                return{'FINISHED'}
            skel_keys = sorted(skels.keys())
            self.skel_full = skels[skel_keys[0]]
            for l in skel_keys[1:]:
                print("Merging skeleton", skel_keys[0], "with skeleton", l, ".")
                self.skel_full = self.skel_full.merge(skels[l])

            print("Merged skeleton.")
            print(self.skel_full)
            
            # Use translation parameters (see above) to reposition the skeleton.
            print("Before skel_full vertices shape:", self.skel_full.vertices.shape)
            print(self.skel_full.vertices[:5])
            self.skel_full.vertices = self.skel_full.vertices + np.array([self.translate_x, self.translate_y, self.translate_z])
            print("After skel_full vertices shape:", self.skel_full.vertices.shape)
            print(self.skel_full.vertices[:5])
            
            skelmesh = bpy.data.meshes.new('emptyMesh')
            skelobj = bpy.data.objects.new(bpy.context.object.name+".skeleton", skelmesh)
            bpy.context.collection.objects.link(skelobj)
            skelmesh.from_pydata(self.skel_full.vertices, self.skel_full.edges, [])
            skelmesh.update()

        skeletonize_kimimaro()
        
        return{'FINISHED'}

class MySettings_skeleton(bpy.types.PropertyGroup):
    path_skeleton: bpy.props.StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )
