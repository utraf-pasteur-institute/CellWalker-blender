import bpy
import os
import glob

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------
def import_env(context):
    print("Importing enviroment from directory ", context.scene.my_tool_env.path_env)


class import_enviroment_class(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "import.env"
    bl_label = "Import enviroment"

    def execute(self, context):
        import_env(context)
        return {'FINISHED'}


class MyProperties_import_enviroment(bpy.types.PropertyGroup):
    path_env: bpy.props.StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
