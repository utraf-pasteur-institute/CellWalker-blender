import os
import sys
import bpy
import mathutils
import bmesh
import numpy as np
from bpy.utils import *

def import_global():
    global ConvexHull, Polygon, LineString
    from scipy.spatial import ConvexHull
    from shapely.geometry import Polygon, LineString

def create_planes_along_centerline(context, centerline, obj):
    # bpy.data.objects[0]
    # centerline = bpy.data.objects[0]
    object_name = bpy.context.object.name
    out = open(bpy.context.scene.my_tool_cross.path + "/" + "_".join([obj.name,centerline.name]) + ".cross-section_param.csv", 'w')
    out.write(
        "IND,Area,Perimeter,ConvexArea,ConvexPerimeter,EquivDiameter,Convexity_area,Convexity_perimeter,MinorAxis,MajorAxis\n")

    ind = 0
    for v in centerline.data.vertices:
        print("Processing", v.co)
        plane, quaternion_original = create_plane(centerline, ind)

        # Perform cross-sectioning here: apply modifier
        # Create modifier and apply to plane
        bool_mod = plane.modifiers.new('modifier1', 'BOOLEAN')
        bool_mod.operation = 'INTERSECT'
        bool_mod.object = obj
        bool_mod.double_threshold = 0.0001  # thresh  # .0001? .00001? emperical; default e-7 sometimes returns just a few edges
        bpy.ops.object.modifier_apply(modifier='modifier1')

        # """
        # Calculate area of plane after applying the modifier
        # bm = bmesh_copy_from_object(plane, apply_modifiers=True)# Not using this function from Neuromorph as it provides triangulated surface making it difficult to calculate perimeter.
        bm = bmesh.new()
        me = plane.data
        bm.from_mesh(me)

        # check if bool property is enabled
        if (context.scene.my_tool_cross.my_bool_area == True):
            area = bmesh_calc_area(bm)
        else:
            area = 0
            # print ("Property Disabled")

        # Calculate perimeter
        # ???CAUTION: Assuming that the vertices are in the order around the perimeter. Need to confirm this again.
        perimeter = 0
        # verts = [v for v in bm.verts]

        # check if bool property is enabled
        if (context.scene.my_tool_cross.my_bool_perimeter == True):
            edge_lengths = [np.linalg.norm(np.array(e.verts[0].co - e.verts[1].co)) for e in bm.edges]
            perimeter = np.sum(edge_lengths)
        else:
            perimeter = 0
            # print ("Property Disabled")

        ###out.write("bm.edges\n")
        ###for e in bm.edges:
        ###	out.write(str(e.verts[0].co) + "," + str(e.verts[1].co) + "\n")
        # for i in range(-1,len(verts)-1):
        #	out.write(str(i) + "," + str(i+1) + "," + str(verts[i].co) + "\n")
        #	perimeter += np.linalg.norm(list(verts[i].co-verts[i+1].co))

        # volume = bmesh_calc_volume(bm) # Not needed
        if (context.scene.my_tool_cross.my_bool_equidiameter == True):
            equivalent_diameter = 2 * np.sqrt(area / np.pi)
        else:
            equivalent_diameter = 0
            # print ("Property Disabled")

        # out.write("bm.transform\n")
        # bm.transform(quaternion_original.to_matrix().to_4x4())
        # verts = [v for v in bm.verts]
        # for i in range(-1,len(verts)-1):
        #	out.write(str(i) + "," + str(i+1) + "," + str(verts[i].co) + "\n")

        # Use the plane object to calculate 2D features.
        # Note: The plane is already rotated in the create_plane function. But there is no need to rotate it back to original.
        #       This is because the orientation of the original plane remains the same. It is only the quaternion operator
        #       that takes different values when the plane is rotated. Thus, the Z-coordinates of the vertices of the plane
        #       as well as the vertices of the cross-section are already zero (as they were in the original plane before rotation.)
        #       It is therefore possible to just discard the Z-coordinates of the vertices go get the 2D shape.
        # points = np.array([list(obj.data.vertices[i].co)[:2] for i in range(0,len(plane.data.vertices))])
        points = np.array([list(v.co)[:2] for v in bm.verts])
        convex_area = 0
        convex_perimeter = 0

        # print ("Property Disabled")

        if points.shape[0] >= 3:
            hull = ConvexHull(points)
            convex_area = hull.area
            for simplex in hull.simplices:
                convex_perimeter += np.linalg.norm(points[simplex[0]]-points[simplex[1]])
        #convex_perimeter += np.linalg.norm(obj.data.vertices[simplex[0]].co - obj.data.vertices[simplex[1]].co)

        # hull

        ############ bm.transform(quat.to_matrix().to_4x4())
        bm.free()

        # """

        #
        # Duplicate cross-section and rotate back original orientation.
        # Then Z-coordinates of all boundary points of the cross-section should be almost equal.
        # This is because the original plane was created perpendicular to Z-axis.
        # Now remove the Z-coordinates and take the X-Ycoordinates so that the cross-section can be represented as 2D object.
        # Use this 2D cross-section to calculate parameters such as convex area etc.
        ###out.write("plane\n")
        ###for i in range(0,len(plane.data.vertices)):
        ###	out.write(str(i) + " " + str(plane.data.vertices[i].co) + "\n")
        # select_obj(plane)
        # bpy.ops.object.duplicate()
        # plane_copy = bpy.context.object
        # plane_copy.rotation_mode = 'QUATERNION'
        # plane_copy.rotation_quaternion = quaternion_original
        # out.write("plane_copy\n")
        # for i in range(0,len(plane_copy.data.vertices)):
        #	out.write(str(i) + " " + str(plane_copy.data.vertices[i].co) + "\n")
        #	#print(plane_copy.data.vertices[i].co, "\n")

        convexity_area = 0.0
        convexity_perimeter = 0.0

        minor_axis = 0.0
        major_axis = 0.0

        if (context.scene.my_tool_cross.my_bool_convexity_area == True):
            if convex_area > 0:
                convexity_area = area / convex_area
        else:
            convexity_area = 0

        if (context.scene.my_tool_cross.my_bool_convexity_perimeter == True):
            if perimeter > 0:
                convexity_perimeter = convex_perimeter / perimeter
        else:
            convexity_perimeter = 0

        if (context.scene.my_tool_cross.my_bool_Minor_Axis == True):
            if len(points) >= 3:
                poly = Polygon(points)
                mbr_points = list(zip(*poly.minimum_rotated_rectangle.exterior.coords.xy))
                mbr_lengths = [LineString((mbr_points[i], mbr_points[i + 1])).length for i in
                               range(len(mbr_points) - 1)]
                # get major/minor axis measurements
                minor_axis = min(mbr_lengths)

        else:
            minor_axis = 0

        if (context.scene.my_tool_cross.my_bool_Major_Axis == True):
            if len(points) >= 3:
                poly = Polygon(points)
                mbr_points = list(zip(*poly.minimum_rotated_rectangle.exterior.coords.xy))
                mbr_lengths = [LineString((mbr_points[i], mbr_points[i + 1])).length for i in
                               range(len(mbr_points) - 1)]
                # get major/minor axis measurements
                major_axis = max(mbr_lengths)
        else:
            major_axis = 0

        out.write("" + str(ind) + "," + str(area) + "," + str(perimeter) + "," + str(convex_area) + "," + str(
            convex_perimeter) + ",")
        out.write(str(equivalent_diameter) + "," + str(convexity_area) + "," + str(
            convexity_perimeter) + ",")  # Also calculate farthest and closest points from centroid
        out.write(str(minor_axis) + "," + str(major_axis) + "\n")

        ind += 1

    out.close()


def bmesh_calc_area(bm):
    """Calculate the surface area."""
    return sum(f.calc_area() for f in bm.faces)


def bmesh_calc_volume(bm):
    """Calculate the volume."""
    return bm.calc_volume()


def create_plane(centerline, ind):
    # This function has been adapted from NeuroMorph (https://github.com/NeuroMorph-EPFL/NeuroMorph) which is distributed under GPL license.
    # For more information, please see https://github.com/NeuroMorph-EPFL/NeuroMorph and https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6064741/.
    #
    # Create a plane perpendicular to centerline and passing through vertex at index ind as follows.
    # Take weighted average of vectors defined by two vertices in either directions of the chosen vertex.
    # This average vector is used as the plane normal.
    # plane_size is the size of the initial plane which is used to perform cross-sectioning with the selected object.
    
    # TODO: User control on this parameter will be provided in future versions.
    # If the object is larger than this plane then the cross-section is imcomplete. Increase the plane_size for very large objects.
    plane_size = 10.0
    # print(plane_size)

    p = centerline.data.vertices[ind].co

    # Get vectors for two vertices before the chosen vertex.
    if ind == 0 or ind == 1:
        p1 = centerline.data.vertices[1].co
        p0 = centerline.data.vertices[0].co
        vec_before1 = p1 - p0
        vec_before2 = vec_before1
    else:
        p_before1 = centerline.data.vertices[ind-1].co
        p_before2 = centerline.data.vertices[ind-2].co
        vec_before1 = p - p_before1
        vec_before2 = p_before1 - p_before2

    # Get vectors for two vertices after the chosen vertex.
    num_vertices = len(centerline.data.vertices)
    if ind == num_vertices - 1 or ind == num_vertices - 2:
        p_last = centerline.data.vertices[num_vertices-1].co
        p_last_1 = centerline.data.vertices[num_vertices-2].co
        vec_after1 = p_last - p_last_1
        vec_after2 = vec_after1
    else:
        p_after1 = centerline.data.vertices[ind+1].co
        p_after2 = centerline.data.vertices[ind+2].co
        vec_after1 = p_after1 - p
        vec_after2 = p_after2 - p_after1

    vec_before1 = mathutils.Vector(vec_before1 / np.linalg.norm(vec_before1))
    vec_before2 = mathutils.Vector(vec_before2 / np.linalg.norm(vec_before2))
    vec_after1 = mathutils.Vector(vec_after1 / np.linalg.norm(vec_after1))
    vec_after2 = mathutils.Vector(vec_after2 / np.linalg.norm(vec_after2))
    vec = (vec_before1 + vec_after1 + vec_before2 / 2 + vec_after2 / 2) / 3

    # Create plane using the plane_size. Then assign rotation using the average vector, vec.
    bpy.ops.mesh.primitive_plane_add(location=p, size=2 * plane_size)
    plane = bpy.context.object
    quaternion_original = plane.rotation_quaternion
    plane.rotation_mode = 'QUATERNION'
    plane.rotation_quaternion = vec.to_track_quat('Z', 'Y')

    return (plane, quaternion_original)


def select_obj(ob):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)  # necessary


def calculate_cross_section_param(context):
    bpy.context.scene.unit_settings.system = 'NONE'

    centerline = None
    cnt = 0
    if len(bpy.context.selected_objects) != 2:
        print("You have to choose exactly two objects and one of them must have a name starting with 'centerline'.")
        return()
    for o in bpy.context.selected_objects:
        if 'centerline' in o.name.lower():
            centerline = o
        else:
            obj = o

    # Get directory name of the current blender file. This means that save the blender file before running this script in order to get the required directory name.
    dirname = bpy.path.abspath("//")

    object_name = bpy.context.object.name

    # Create collection and set it active so that the planes created hereafter are added to this collection
    collection = bpy.data.collections.new("_".join([obj.name,centerline.name]) + ".cross-sections")
    bpy.context.scene.collection.children.link(collection)
    # NOTE the use of 'collection.name' to account for potential automatic renaming
    layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]
    bpy.context.view_layer.active_layer_collection = layer_collection

    if centerline is None:
        print("Object named centerline not found.")
    else:
        if object_name in bpy.data.objects:
            print("Creating planes along centerline")
            create_planes_along_centerline(context, centerline, obj)
        else:
            print("Object not found.")


def create_centerline(context):
    bm = bmesh.new()
    ob = bpy.context.active_object
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)

    points = []
    for v in bm.verts:
        if (v.select == True):
            obMat = ob.matrix_world
            points.append(obMat @ v.co)

    emptyMesh = bpy.data.meshes.new('emptyMesh')
    theObj = bpy.data.objects.new(bpy.context.object.name+".centerline", emptyMesh)
    bpy.context.collection.objects.link(theObj)

    verts = []

    v = points[0] - points[1]
    magnitude = np.sqrt(v.dot(v))

    nstep = magnitude / context.scene.my_tool_cross.slider
    step = v / int(nstep)

    for i in range(int(nstep)):
        arr = points[1] + step * i
        verts.append([arr[0], arr[1], arr[2]])

    emptyMesh.from_pydata(verts, [], [])
    emptyMesh.update()


class centerline(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.centerline"
    bl_label = "Create centerline"
    bl_description = "Calculate a centerline"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        import_global()
        
        create_centerline(context)
        return {'FINISHED'}


class export_operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.export"
    bl_label = "Calculate and Save"
    bl_description = "Calculates the different cross-sectional parameters and export them in .CSV file"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        import_global()
        
        calculate_cross_section_param(context)
        return {'FINISHED'}


class MySettings(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )

    my_bool_area: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    my_bool_perimeter: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    my_bool_convexarea: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    my_bool_convexperimeter: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    my_bool_equidiameter: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    my_bool_convexity_area: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    my_bool_convexity_perimeter: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    my_bool_Minor_Axis: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    my_bool_Major_Axis: bpy.props.BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default=False
    )

    slider: bpy.props.FloatProperty(
        name="Slider",
        description="Allow Change Some Size",
        default= 0.01,
        min =0.05,
        max = 2
    )


