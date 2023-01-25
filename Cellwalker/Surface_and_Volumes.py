import bmesh
import bpy

# Functions

def volume_area_multi_obj(context):
    # Modifiers (like scale etc.) are not applied.
    # So do not use for calculating surface area and volume of manually scaled objects. Use only for directly imported objects.
    out = open(context.scene.my_tool_VA.path + "/" + "volume_and_areas.csv", 'w')
    print("Surface area and volume output file:", out)
    out.write("Object name,Surface area,Volume\n")

    for obj in context.selected_objects:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        name = obj.data.name
        area = sum(f.calc_area() for f in bm.faces)
        volume = float(bm.calc_volume())
        print(name, area, volume)
        out.write("" + str(name) + "," + str(area) + "," + str(volume) + "\n")

# Classes

class Measure_volume_area_multi_obj(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.surfvol_multi"
    bl_label = "Calculate and save"
    bl_description = "Calculate surface area and volume of multiple selected objects and save to file"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        #def_premeasure(context)
        volume_area_multi_obj(context)
        return {'FINISHED'}

class MyProperties_VA(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(
        name="",
        description="Path to folder where output will be saved",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
