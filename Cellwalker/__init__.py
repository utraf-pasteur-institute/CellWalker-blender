# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/
#
# ##### END GPL LICENSE BLOCK #####

### HELP TOPICS
# Blender autocomplete setup for PyCharm
# https://b3d.interplanety.org/en/using-external-ide-pycharm-for-writing-blender-scripts/
# https://github.com/Korchy/blender_autocomplete
###

# Setting and displaying properties
#https://medium.com/geekculture/creating-a-custom-panel-with-blenders-python-api-b9602d890663

# New ideas:
# Create rendering setup for a selected mesh/meshes: Add lights and camera using some logic based on the cell shape.
# Setup materials for meshes.
# Add background


bl_info = {
	"name": "CellWalker",
	"author": "Harshavardhan Khare, Nathaly Dongo",
	"version": (0, 0, 1),
	"blender": (3, 0, 1),
	"description": "Tools for analysis of segmented 3D microscopy images",
	"location": "View3D",
	"category": "Morphology"
}

import bpy
#import os
#import sys
#sys.path.append(os.getcwd)

from . Main_multipanel import VIEW3D_PT_main_panel

from . Import_enviroment import (import_enviroment_class, MyProperties_import_enviroment)

from . Import_objects_class import (import_objects_class, MyProperties_import_objs)

from . Surface_and_Volumes import (Measure_volume_area_multi_obj, MyProperties_VA)

from . Centerline import MESH_OT_make_centerline

from . Crosssections import ( MySettings,export_operator,centerline)

from . Skeleton import (MESH_OT_skeletonize,MySettings_skeleton,export_operator_sk)

from . Angular_distribution import  ( MySettings_Angle,OPERATOR_Angle_distribution)

from . Distance import  (MySettings_Distance, Dijkstra_distance, Straigth_distance)

# Future work
# Omitted from this version
#from . Orientation_two_objs_plane import (MySettings_Orientation,OPERATOR_Orientation)


#V
classes = (VIEW3D_PT_main_panel,  import_enviroment_class, MyProperties_import_enviroment, 
			MESH_OT_make_centerline, centerline, export_operator,MySettings, MESH_OT_skeletonize,
			Measure_volume_area_multi_obj, MyProperties_VA,
		   	MySettings_skeleton, export_operator_sk,
		   	import_objects_class, MyProperties_import_objs,
		   	MySettings_Angle, OPERATOR_Angle_distribution,
		   	#MySettings_Orientation, OPERATOR_Orientation, # Future work. Omitted from this version
		   	MySettings_Distance, Dijkstra_distance, Straigth_distance)

#register, unregister = bpy.utils.register_classes_factory(classes)

#props = [('foo', bpy.props.StringProperty(name="Foo",description=":",default="",maxlen=1024)),
#		 ('flt', bpy.props.FloatProperty(name='Flt', description=':'))]



#"""
def register():
	#for (prop_name, prop_value) in props:
	#	setattr(bpy.types.Scene, prop_name, prop_value)

	for cls in classes:
		bpy.utils.register_class(cls)

	# bpy.utils.register_module(classes)
	# Pointers registraion
	bpy.types.Scene.my_tool_cross = bpy.props.PointerProperty(type=MySettings)
	bpy.types.Scene.my_tool_skeleton = bpy.props.PointerProperty(type=MySettings_skeleton)
	bpy.types.Scene.my_tool_import_objs = bpy.props.PointerProperty(type=MyProperties_import_objs)
	bpy.types.Scene.my_tool_VA = bpy.props.PointerProperty(type=MyProperties_VA) #? Rename to MySettings_VA
	bpy.types.Scene.my_tool_angle = bpy.props.PointerProperty(type=MySettings_Angle)
	#bpy.types.Scene.my_tool_or = bpy.props.PointerProperty(type=MySettings_Orientation) # Future work. Omitted from this version
	bpy.types.Scene.my_tool_dist = bpy.props.PointerProperty(type=MySettings_Distance)
	bpy.types.Scene.my_tool_env = bpy.props.PointerProperty(type=MyProperties_import_enviroment)

	# Subpanels registration
	bpy.types.Scene.subpanel_import_env_status = bpy.props.BoolProperty(default=False)
	bpy.types.Scene.subpanel_import_status = bpy.props.BoolProperty(default=False)
	bpy.types.Scene.subpanel_VA_status = bpy.props.BoolProperty(default=False)
	bpy.types.Scene.subpanel_Centerline_status = bpy.props.BoolProperty(default=False)
	bpy.types.Scene.subpanel_sk_status = bpy.props.BoolProperty(default=False)
	bpy.types.Scene.subpanel_AD_status = bpy.props.BoolProperty(default=False)
	#bpy.types.Scene.subpanel_Or_status = bpy.props.BoolProperty(default=False) # Future work. Omitted from this version
	bpy.types.Scene.subpanel_distance = bpy.props.BoolProperty(default=False)

def unregister():
	#for (prop_name, _) in props:
	#	delattr(bpy.types.Scene, prop_name)

	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

	# bpy.utils.unregister_module(classes)
	del bpy.types.Scene.my_tool_cross
	del bpy.types.Scene.my_tool_skeleton
	del bpy.types.Scene.my_tool_import_objs
	del bpy.types.Scene.my_tool_VA
	del bpy.types.Scene.my_tool_angle
	#del bpy.types.Scene.my_tool_or # Future work. Omitted from this version
	del bpy.types.Scene.my_tool_dist
	del bpy.types.Scene.my_tool_env 

	del bpy.types.Scene.subpanel_import_status
	del bpy.types.Scene.subpanel_VA_status
	del bpy.types.Scene.subpanel_Centerline_status
	del bpy.types.Scene.subpanel_sk_status
	del bpy.types.Scene.subpanel_AD_status
	#del bpy.types.Scene.subpanel_Or_status # Future work. Omitted from this version
	del bpy.types.Scene.subpanel_distance

#"""

#def register():
#	bpy.utils.register_class(MainPanel)
#	print("Namaskar! Welcome to CellWalker!")

#def unregister():
#	bpy.utils.unregister_class(MainPanel)
#	print("Tata :)")
# register()
