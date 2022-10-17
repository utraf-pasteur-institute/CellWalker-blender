import bpy
import os
import glob

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------
def import_obj(context):
    print(context.scene.my_tool_import_objs.path)
    model_files = glob.glob(os.path.join(context.scene.my_tool_import_objs.path, "*.obj"))
    for f in model_files:
        print(f)
        #head, tail = os.path.split(f)
        #collection_name = tail.replace(".obj", "")
        bpy.ops.import_scene.obj(filepath=f, axis_forward="Y",axis_up="Z")


class import_objects_class(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "import.objs"
    bl_label = "Import obj. files"

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


