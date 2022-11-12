import bmesh
import bpy

def def_premeasure(context):
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


def volume_and_area(context):
    bm = bmesh.new()
    out = open(context.scene.my_tool_VA.path + "/" + "volume_and_areas.csv", 'w')
    print(out)
    out.write("Object_name,surface_Area,Volume\n")

    for obj in context.selected_objects:
        bm.from_mesh(obj.data)
        name_obj = obj.data.name
        area = sum(f.calc_area() for f in bm.faces)
        volume = float(bm.calc_volume())
        out.write("" + str(name_obj) + "," + str(area) + "," + str(volume) + "\n")


class Measure_volume_area(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "measuring.volume"
    bl_label = "Volume and Surface Area"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        def_premeasure(context)
        volume_and_area(context)
        return {'FINISHED'}


class MyProperties_VA(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')

