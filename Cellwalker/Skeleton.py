import os
import sys

import numpy as np
np.set_printoptions(threshold=sys.maxsize)

import bmesh
import bpy

if os.name == 'posix':
    sys.path.append("/home/harsh/anaconda3/envs/blender/lib/python3.9/site-packages")
elif os.name == 'nt':
    sys.path.append("C:\\Users\\harsh\\anaconda3\\envs\\cellwalker-blender\\Lib\\site-packages")
else:
    print("Operating system not recognized! os.name =", os.name)
    print("Some modules may not be imported.")

def import_global():
    global sk, kimimaro, multiprocess, trimesh, creation, scipy
    import skeletor as sk
    import kimimaro
    import multiprocess
    import trimesh
    from trimesh.voxel import creation
    import scipy


def saveSkeletonObjFile_line(skel_full,fname=None,translate_x=0,translate_y=0,translate_z=0):
    ### THIS FUNCTION IS NOT BEING USED.
    ### OBJ file: (Importing in Blender: Select transformation Y Forward, Z up)
    ### NOTE: ALL THESE CALCULATIONS WILL GIVE COORDINATES IN MICROMETERS. NOT IN PIXEL UNITS.

    print(skel_full)

    components = skel_full.components()
    print("Components:", type(components))
    print(components)

    # Scale translation parameters according to the mip level.
    # translate_x = translate_x/(2^miplevel)
    ###mip_level = self.skel_widgets['mip_level']['entry'].get()
    ###translate_x = translate_x / (2 ** int(mip_level))
    ###translate_y = translate_y / (2 ** int(mip_level))
    # ??? MAY BE DO NOT DO FOR transate_z
    # translate_z = translate_z / (2**int(mip_level))

    # ???This scaling factor is to convert from nano meters to micrometers
    ###s = 0.001

    objfile = open(fname, "w")

    v_num_offset = 1  # len(verts)+1

    i = 1
    for skel in components:
        skel = skel.downsample(2)
        objfile.write("#Skeleton " + str(i) + "\n")

        # print("skel.edges:", type(skel.edges))
        # lines = skel.edges+1

        # print(skel.vertices)
        for item in skel.vertices:
            # objfile.write("v {0} {1} {2}\n".format(item[0],item[1],item[2]))
            # print("vert", item)
            # print("vert", np.array([item[0]/32.0,item[1]/32.0,item[2]/30.0]))
            # objfile.write("v {0} {1} {2}\n".format(item[0]/32.0,item[1]/32.0,item[2]/30.0))
            # NOTE: Swap translation offsets x and y. This is because the X and Y axes considered by VAST are Y and X respectively in numpy ndarrays.
            # -1 is for inverting z axis.
            ###objfile.write("v {0} {1} {2}\n".format('{:.6f}'.format(((item[0] / self.mip_dict[mip_level][0]) + translate_y) * self.mip_dict[mip_level][0] * s),
            ###                                       '{:.6f}'.format(((item[1] / self.mip_dict[mip_level][1]) + translate_x) * self.mip_dict[mip_level][1] * s),
            ###                                       '{:.6f}'.format(((item[2] / self.mip_dict[mip_level][2]) + translate_z) * self.mip_dict[mip_level][2] * s * -1)))

            objfile.write("v {0} {1} {2}\n".format('{:.6f}'.format(item[0] + translate_x),
                                                   '{:.6f}'.format(item[1] + translate_y),
                                                   '{:.6f}'.format(item[2] + translate_z)
                                                   ))

        # print(skel.edges)
        for item in skel.edges:
            # print("edge", item)
            objfile.write("l {0} {1}\n".format(item[0] + v_num_offset, item[1] + v_num_offset))

        v_num_offset += len(skel.vertices)
        i += 1

    objfile.close()

    axis_forward = 'Y'
    axis_up = 'Z'
    bpy.ops.import_scene.obj(filepath=fname, axis_forward=axis_forward, axis_up=axis_up)

class export_operator_sk(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "sk.export"
    bl_label = "Save Skeleton"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        saveSkeletonObjFile_line(self.skel_full, fname=bpy.context.scene.my_tool_skeleton.path_skeleton,
                                 translate_x=self.translate_x, translate_y=self.translate_y, translate_z=self.translate_z)
        return {'FINISHED'}

class MESH_OT_skeletonize(bpy.types.Operator):
    bl_idname = "mesh.skeletonize"
    bl_label = "Skeletonize mesh"
    bl_description = "Skeletonize mesh using skeletor package"

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

        print(mesh)
        print(mesh.vertices)
        min_mesh = np.min(mesh.vertices, axis=0)
        max_mesh = np.max(mesh.vertices, axis=0)
        print("Minimum of mesh vertices:", min_mesh)
        print("Maximum of mesh vertices:", max_mesh)

        self.translate_x = min_mesh[0]
        self.translate_y = min_mesh[1]
        self.translate_z = min_mesh[2]
        print("Translation parameters:", self.translate_x, self.translate_y, self.translate_z)

        def skeletonize():
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

        #skeletonize()

        voxelsize = 0.05#0.1 #0.5 # 0.03
        volume = trimesh.voxel.creation.voxelize(mesh, voxelsize, method='subdivide')
        voxels = scipy.ndimage.morphology.binary_fill_holes(volume.matrix)
        #print(voxels.astype(int))
        #print(volume)

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
            parallel=0,  # <= 0 all cpu, 1 single process, 2+ multiprocess
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

        return{'FINISHED'}

class MySettings_skeleton(bpy.types.PropertyGroup):
    path_skeleton: bpy.props.StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )
