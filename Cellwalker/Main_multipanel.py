import bpy

class VIEW3D_PT_main_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "CellWalker"
    bl_idname = "view3d.main_panel"
    bl_category = "CellWalker"
    bl_space_type = 'VIEW_3D'#'PROPERTIES'
    bl_region_type = 'UI'#'WINDOW'
    #bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        ########################Importing enviroment subpanel caption ########################
        row = layout.row()
        icon = 'TRIA_DOWN' if context.scene.subpanel_import_env_status else 'TRIA_RIGHT'
        row.prop(context.scene, 'subpanel_import_env_status', icon=icon, icon_only=True)
        row.label(text='Import Python environment')

        # some data on the subpanel
        if context.scene.subpanel_import_env_status:
            box = layout.box()
            col = box.column()
            row = col.row()

            # Importing button
            row.label(text="Select folder of a python-environment")
            row = col.row()
            row.prop(scene.my_tool_env, "path_env", text="")
            row = col.row()
            row.operator("import.env")        
        
        ########################Importing subpanel caption ########################
        row = layout.row()
        icon = 'TRIA_DOWN' if context.scene.subpanel_import_status else 'TRIA_RIGHT'
        row.prop(context.scene, 'subpanel_import_status', icon=icon, icon_only=True)
        row.label(text='Import objects')

        # some data on the subpanel
        if context.scene.subpanel_import_status:
            box = layout.box()
            col = box.column()
            row = col.row()

            # Importing button
            row.label(text="Select a folder containing .OBJ files")
            row = col.row()
            row.prop(scene.my_tool_import_objs, "path", text="")
            row = col.row()
            row.operator("import.objs")

        ######################## Volume and areas subpanel caption ########################
        row = layout.row()
        icon = 'TRIA_DOWN' if context.scene.subpanel_VA_status else 'TRIA_RIGHT'
        row.prop(context.scene, 'subpanel_VA_status', icon=icon, icon_only=True)
        row.label(text='Surface area and Volume')

        # some data on the subpanel
        if context.scene.subpanel_VA_status:
            box = layout.box()
            col = box.column()

            """
            row = col.row()
            row.label(text="For a single object")
            row = col.row()
            row.prop(scene.my_tool_VA, "SO_vol", text="Volume")
            row = col.row()
            row.prop(scene.my_tool_VA, "SO_area", text="Area")
            row = col.row()
            row.operator("object.singlevolsurf")
            """
            
            row = col.row()
            row.label(text="Select a folder to save output")
            row = col.row()
            row.prop(scene.my_tool_VA, "path", text="")
            row = col.row()
            row.operator("object.surfvol_multi")


        ######################## Centerline and Crosssectional ########################
        row = layout.row()
        icon = 'TRIA_DOWN' if context.scene.subpanel_Centerline_status else 'TRIA_RIGHT'
        row.prop(context.scene, 'subpanel_Centerline_status', icon=icon, icon_only=True)
        row.label(text='Cross-setional Tool')


        # some data on the subpanel
        if context.scene.subpanel_Centerline_status:
            box = layout.box()
            col = box.column()
            row = col.row()

            row.label(text="Create centerline")
            col = box.column()
            row = col.row()
            row.label(text="Step size")
            row.prop(scene.my_tool_cross, "slider", text="Unit")
            row = col.row()
            row.operator("object.centerline")


            # display the properties
            mytool = scene.my_tool_cross
            col = box.column()
            row = col.row()
            row.label(text="Choose cross-section properties to calculate")
            col.prop(mytool, "my_bool_area", text="Area")
            col.prop(mytool, "my_bool_perimeter", text="Perimeter")
            col.prop(mytool, "my_bool_convexarea", text="Convex Area")
            col.prop(mytool, "my_bool_convexperimeter", text="Convex Perimeter")
            col.prop(mytool, "my_bool_equidiameter", text="Equi Diameter")
            col.prop(mytool, "my_bool_convexity_area", text="Convexity Area")
            col.prop(mytool, "my_bool_convexity_perimeter", text="Convexity Perimeter")
            col.prop(mytool, "my_bool_Minor_Axis", text="Minor Axis")
            col.prop(mytool, "my_bool_Major_Axis", text="Major Axis")

            # Saving file path
            row = col.row()
            row.label(text="Select a folder to save output")
            col = box.column(align=True)
            col.prop(scene.my_tool_cross, "path", text="")

            # Exporting cross-sectional properties
            row = col.row()
            row.operator("object.export")

        ######################## Distance ########################
        row = layout.row()
        icon = 'TRIA_DOWN' if context.scene.subpanel_Centerline_status else 'TRIA_RIGHT'
        row.prop(context.scene, 'subpanel_distance', icon=icon, icon_only=True)
        row.label(text='Distance Tool')

        # some data on the subpanel
        if context.scene.subpanel_distance:
            box = layout.box()
            col = box.column()
            # row = col.row()
            # row.label(text="Max generations")
            # row = col.row()
            # row.prop(scene.my_tool_dist, "max_generations", text="Unit")

            # row = col.row()
            # row.label(text="Population size")
            # row = col.row()
            # row.prop(scene.my_tool_dist, "population_size", text="Unit")

            # row = col.row()
            # row.label(text="Top percentage")
            # row = col.row()
            # row.prop(scene.my_tool_dist, "top_percentage", text="Unit")

            # row = col.row()
            # row.prop(scene.my_tool_dist, "Node_distance", text="Node distance")
            # row = col.row()
            # row.operator("object.distance")

            #row = col.row()
            #row.label(text="Dijkstra Distance")
            row = col.row()
            row.prop(scene.my_tool_dist, "dijkstra_distance", text="Dijkstra distance")
            row = col.row()
            row.operator("object.dijkstra")

            #row = col.row()
            #row.label(text="Straight Distance")
            row = col.row()
            row.prop(scene.my_tool_dist, "straight_distance", text="Straight distance")
            row = col.row()
            row.operator("object.distance")
            

        ######################## Skeleton ########################
        row = layout.row()
        icon = 'TRIA_DOWN' if context.scene.subpanel_sk_status else 'TRIA_RIGHT'
        row.prop(context.scene, 'subpanel_sk_status', icon=icon, icon_only=True)
        row.label(text='Skeletonize')

        # some data on the subpanel
        if context.scene.subpanel_sk_status:
            box = layout.box()
            col = box.column()
            row = col.row()
            # Mesh Skeleton
            row.label(text="Create skeleton of selected object")
            col.operator("mesh.skeletonize")
            # Path to save Skeleton
            row = col.row()
            row.label(text="Save skeleton in .OBJ format")
            col = box.column()
            col.prop(scene.my_tool_skeleton, "path_skeleton", text="")
            # Export Skeleton
            row = col.row()
            row.operator("sk.export")

        ######################## Angular distribution########################
        row = layout.row()
        icon = 'TRIA_DOWN' if context.scene.subpanel_AD_status else 'TRIA_RIGHT'
        row.prop(context.scene, 'subpanel_AD_status', icon=icon, icon_only=True)
        row.label(text='Angular Distribution')

        # some data on the subpanel
        if context.scene.subpanel_AD_status:
            box = layout.box()
            col = box.column()

            # Object 1- Cell or Nucleus. Used to calculate a centroid around which the distribution of Object 2 is calculated
            row = col.row()
            row.label(text="Select a cell/nucleus")
            row = col.row()
            row.prop_search(scene.my_tool_angle, "Cell", scene, "objects")

            # Object 2- Organelle. This is the object whose distribution is calculated around the centroid of Object 1.
            row = col.row()
            row.label(text="Select an organelle")
            row = col.row()
            row.prop_search(scene.my_tool_angle, "Organelle", scene, "objects")

            row = col.row()
            row.prop(scene.my_tool_angle, "Mean", text="Mean")
            row = col.row()
            row.prop(scene.my_tool_angle, "Std", text="Standard deviation")

            row = col.row()
            row.operator("angle.distribution")

        ######################## Orientation ########################
        # Future work. Omitted from this version
        """
        row = layout.row()
        icon = 'TRIA_DOWN' if context.scene.subpanel_Or_status else 'TRIA_RIGHT'
        row.prop(context.scene, 'subpanel_Or_status', icon=icon, icon_only=True)
        row.label(text='Orientation')

        # some data on the subpanel
        if context.scene.subpanel_Or_status:
            box = layout.box()
            col = box.column()

            # Object 1 Orientation
            row = col.row()
            row.label(text="Object 1")
            row = col.row()
            row.prop_search(scene.my_tool_or, "Obj1", scene, "objects")

            # Object 2 Orientation
            row = col.row()
            row.label(text="Object 2")
            row = col.row()
            row.prop_search(scene.my_tool_or, "Obj2", scene, "objects")

            # Object 3 Orientation
            row = col.row()
            row.label(text="Plane as reference")
            row = col.row()
            row.prop_search(scene.my_tool_or, "pointer_Plane", scene, "objects") #, text="Mean"

            row = col.row()
            row.prop(scene.my_tool_or, "Angle_Or", text="Orientation (°)")

            row = col.row()
            row.operator("angle.orientation")
        """