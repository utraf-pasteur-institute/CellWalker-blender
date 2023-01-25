import bpy
import os
import glob

def import_obj(context):
    print(context.scene.my_tool_import_objs.path)
    model_files = glob.glob(os.path.join(context.scene.my_tool_import_objs.path, "*.obj"))
    for f in model_files:
        print(f)
        # It is important to set axes as axis_forward="Y",axis_up="Z".
        # When exported from VAST with default options, the placement of objects is correct only in this orientation.
        # The distance measurement tool uses this orientation to place the paths to show distance.
        # With other orientations, this placement might fail. 
        bpy.ops.import_scene.obj(filepath=f, axis_forward="Y",axis_up="Z")

class import_objects_class(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "import.objs"
    bl_label = "Import .OBJ files"
    bl_description = "Import all the objects in the folder"

    def execute(self, context):
        import_obj(context)
        return {'FINISHED'}

class MyProperties_import_objs(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')


