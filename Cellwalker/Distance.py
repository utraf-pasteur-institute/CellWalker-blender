import random
import math
import bpy
import bmesh
import numpy as np

def _distance(path_point_1, path_point_2):
    return math.sqrt((path_point_2[0] - path_point_1[0]) ** 2 + (path_point_2[1] - path_point_1[1]) ** 2 + (
                path_point_2[2] - path_point_1[2]) ** 2)


######################################################################################
#                               Straigth Distance
######################################################################################

def calc_straigth_distance():
    ob = bpy.context.active_object
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)

    print("select history:", bm.select_history[-2:])
    sel_vert = [tuple(vert.co) for vert in bm.select_history[-2:]]

    emptyMesh = bpy.data.meshes.new('emptyMesh')
    theObj = bpy.data.objects.new("straight_distance", emptyMesh)
    bpy.context.collection.objects.link(theObj)

    emptyMesh.from_pydata(sel_vert, [(0,1)], [])
    emptyMesh.update()
    bpy.context.view_layer.update()

    bpy.context.scene.my_tool_dist.straight_distance = str(_distance(sel_vert[0], sel_vert[1]))
    return(_distance(sel_vert[0], sel_vert[1]))

class Straigth_distance(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.distance"
    bl_label = "Straight distance"
    bl_description = "It measures the straight distance between two nodes"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print('The minimun path length is', calc_straigth_distance(), 'units')
        return {'FINISHED'}

######################################################################################
#                               Dijkstra Distance
######################################################################################

# Dijktra distance was based in the code of: 
# https://blender.stackexchange.com/questions/186067/what-is-the-bmesh-equivalent-to-bpy-ops-mesh-shortest-path-select
# TODO: This Dijkstra's algorithm implementation sometimes creates loops. Need to fix it.
# Alternative: Use Dijkstra's algorithm in the Networkx package

from math import inf

class Node_class:
    @property
    def edges(self):
        return (e for e in self.vert.link_edges if not e.tag)
    
    def __init__(self, v):
        self.vert = v
        self.length = inf
        self.shortest_path = []
        

def dijkstra(bm, v_start, v_target=None):
    for e in bm.edges:
        e.tag = False
    
    nodes_in_object = {v : Node_class(v) for v in bm.verts}
    node = nodes_in_object[v_start]
    node.length = 0
    
    visiting_list = [node]

    while visiting_list:
        node = visiting_list.pop(0)
        
        if node.vert is v_target:
            return nodes_in_object
        
        for e in node.edges:
            e.tag = True
            node_length = node.length + e.calc_length()
            v = e.other_vert(node.vert)
            
            visited_node = nodes_in_object[v]
            visiting_list.append(visited_node)
            if visited_node.length > node_length:
                visited_node.length = node_length
                visited_node.shortest_path = node.shortest_path + [e]
      
        visiting_list.sort(key=lambda nod: nod.length)

    return nodes_in_object

# test call select two verts edit mode

def run_dijkstra():         
    context = bpy.context
    bm = bmesh.from_edit_mesh(context.object.data)
    v1, v2 = bm.select_history[-2:]            
               
    # calc shortest paths to one vert
    nodes = dijkstra(bm, v1)
    node = nodes[v2]

    context.scene.my_tool_dist.dijkstra_distance = str(float(node.length)) 
    print('The minimun path length is', node.length, 'units')

    # Create object for dijkstra distance
    for e in node.shortest_path:
        e.select_set(True)
    
    sel_vert = [node.shortest_path[0].verts[0].co]
    #print(node.shortest_path[0].verts[0].co)
   
    for i in range(len(node.shortest_path)): #node.shortest_path[3].verts
        sel_vert.append(node.shortest_path[i].verts[0].co)
        sel_vert.append(node.shortest_path[i].verts[1].co)
        
    print("Dijkstra sel_vert:", sel_vert)


    path_x = [sel_vert[j][0] for j in range(len(sel_vert))]
    path_y = [sel_vert[j][1] for j in range(len(sel_vert))]
    path_z = [sel_vert[j][2] for j in range(len(sel_vert))]

    emptyMesh = bpy.data.meshes.new('emptyMesh')
    theObj = bpy.data.objects.new("dijkstra_distance", emptyMesh)
    bpy.context.collection.objects.link(theObj)
    verts = []
    edges = []
    for i in range(len(path_y)):
        verts.append([path_x[i], path_y[i], path_z[i]])
        if i > 0:
            edges.append([i - 1, i])

    emptyMesh.from_pydata(verts, edges, [])
    emptyMesh.update()
    bpy.context.view_layer.update()

class Dijkstra_distance(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.dijkstra"
    bl_label = "Dijkstra distance"
    bl_description = "It measures the shortest path between two nodes employing Dijkstra's Algorithm"
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run_dijkstra()
        return {'FINISHED'} 


class MySettings_Distance(bpy.types.PropertyGroup):

    #straight_distance: bpy.props.FloatProperty()
    #dijkstra_distance: bpy.props.FloatProperty()
    
    straight_distance: bpy.props.StringProperty(default="0", maxlen=10)
    dijkstra_distance: bpy.props.StringProperty(default="0", maxlen=10)