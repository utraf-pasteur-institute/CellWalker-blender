import random
import math
import bpy
import bmesh
import numpy as np

############ Functions ###############################################################

def find_nearest(possible_next_vertices, goal):
    weigths=[]
    for vert2 in possible_next_vertices:
        weigths.append(np.sqrt((goal[0]-vert2[0])**2+(goal[1]-vert2[1])**2+(goal[2]-vert2[2])**2))
    weigths=np.asarray(weigths)
    sorted_top= random.choice(np.sort(weigths)[:2])
    #print(np.where(weigths==sorted_top)[0][0])
    return possible_next_vertices[np.where(weigths==sorted_top)[0][0]]


def _show_final_path(verts_keys, population, path_lengths, gen):
    index_min = np.argmin(path_lengths)
    chromosome = population[index_min]

    path_x = [verts_keys[j][0] for j, c in enumerate(chromosome) if c == '1']
    path_y = [verts_keys[j][1] for j, c in enumerate(chromosome) if c == '1']
    path_z = [verts_keys[j][2] for j, c in enumerate(chromosome) if c == '1']

    # RESULTS
    print('results')
    #print(path_x)
    #print(path_y)
    #print(path_z)

    print('The minimun path length is',path_lengths[index_min],'units')

    emptyMesh = bpy.data.meshes.new('emptyMesh')
    theObj = bpy.data.objects.new("Node_distance", emptyMesh)
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

    bpy.context.scene.my_tool_dist.Node_distance=path_lengths[index_min]


##### start
def start(sel_vert,verts_keys,radius,max_generations,top_percentage,population_size):
    population = _generate_population(sel_vert,verts_keys,radius,population_size)
    path_lengths = []

    for chromosome in population:
        path_lengths.append(_calculate_path_length(chromosome, verts_keys))

    generations = int(max_generations)

    for gen in range(generations - 1):
        new_population = []
        path_lengths.clear()

        fitness_list = _sort_by_fitness(population, verts_keys)
        for chromosome in population:
            while True:
                parent1 = _choose_random_parent(fitness_list,top_percentage)
                parent2 = _choose_random_parent(fitness_list,top_percentage)

                child = _crossover(parent1, parent2,False,0.5)
                if child!='':
                    break

            path_lengths.append(_calculate_path_length(child, verts_keys))
            new_population.append(child)
        population = new_population

    _show_final_path(verts_keys, population, path_lengths, gen)

def _crossover(parent1, parent2,crossover_split_random,crossover_split_size):
    if crossover_split_random:
        split_size = random.randint(0, len(parent1))

    else:
        fraction = float(crossover_split_size)
        split_size = math.floor(fraction * len(parent1))

    ## Mine
    indexs_p1 = [idx for idx, s in enumerate(parent1) if '1' in s]
    indexs_p2 = [idx for idx, s in enumerate(parent2) if '1' in s]
    possible_split_idx=[]

    for index_p1 in indexs_p1:
        if index_p1 in indexs_p2:
            possible_split_idx.append(index_p1)

    split_size=random.choice(possible_split_idx)

    if possible_split_idx!=[]:
        return ''.join([parent1[:split_size], parent2[split_size:]])
    else:
        return ''

def _choose_random_parent(fitness_list,top_percentage):

    till_index = len(fitness_list) * float(top_percentage)
    till_index = int(till_index)
    idx=random.randint(0, till_index)
    #print(idx)
    parent_to_fitness = fitness_list[idx]

    return parent_to_fitness[0]

##### _generate_population
def _generate_population(sel_vert,verts_keys,radius,population_size):
    population_size = int(population_size)

    population = []
    print('Generating initial population, please wait ....')
    for i in range(population_size):
        while True:
            chromosome = _generate_chromosome(sel_vert, verts_keys, radius)
            if chromosome not in population:
                break
        population.append(chromosome)
        #print('chromosome',i)

    print('Successfully created initial population')
    print('Simulating genetic algorithm for path planning .... (Press Ctrl+C to stop)')
    return population

######
def _generate_chromosome(sel_vert,verts_keys,radius):

    chromosome=''
    random_path = [sel_vert[0]]
    next_vert = []
    previous_vert = sel_vert[0]

    while next_vert != sel_vert[1]:
        possible_next_vertices = []
        for vert in verts_keys:
            if vert not in random_path:
                dx = abs(vert[0] - previous_vert[0])
                dy = abs(vert[1] - previous_vert[1])
                dz = abs(vert[2] - previous_vert[2])
                rad_posvert = max(dx, dy, dz)
                if rad_posvert <= radius * 1.1:
                    # print(vert)
                    possible_next_vertices.append(vert)
        #print('possible',possible_next_vertices)
        next_vert = find_nearest(possible_next_vertices, sel_vert[1])
        #print('nearest',next_vert)
        random_path.append(next_vert)
        previous_vert = next_vert


    for vert in verts_keys:
        if vert in random_path:
            gene = '1'
        else:
            gene = '0'
        chromosome += gene

    return chromosome

def _calculate_path_length(chromosome, verts_keys):
    path_point_1, path_point_2 = (), ()
    length = 0

    for i, gene in enumerate(chromosome):
        if gene == '1':
            last_path_point = verts_keys[i]

            if not path_point_1:
                path_point_1 = verts_keys[i]
            else:
                path_point_2 = verts_keys[i]

            if path_point_1 and path_point_2:
                length += _distance(path_point_1, path_point_2)

                path_point_1 = path_point_2
                path_point_2 = ()

    return length

def _distance(path_point_1, path_point_2):
    return math.sqrt((path_point_2[0] - path_point_1[0]) ** 2 + (path_point_2[1] - path_point_1[1]) ** 2 + (
                path_point_2[2] - path_point_1[2]) ** 2)

def _fitness(chromosome, path_points):
    length = _calculate_path_length(chromosome, path_points)
    fitness = 1 / length if length != 0 else 0

    return fitness


def _sort_by_fitness(population, path_points):
    fitness_list = []

    for chromosome in population:
        chromosome_to_fitness = (chromosome, _fitness(chromosome, path_points))
        fitness_list.append(chromosome_to_fitness)

    fitness_list.sort(reverse=True, key=lambda tuple: tuple[1])

    return fitness_list

def distance_GA_fc():
    ############### Information of the Mesh
    print('Running')
    ob = bpy.context.active_object
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)

    obMat = ob.matrix_world
    edges_keys = bpy.context.active_object.data.edge_keys
    verts_keys = [tuple(obMat @ vert.co) for vert in bm.verts]

    sel_vert = [tuple(obMat @ vert.co) for vert in bm.verts if vert.select == True]
    start_idx = verts_keys.index(sel_vert[0])
    end_idx = verts_keys.index(sel_vert[1])
    sel_edges = [edges_keys[start_idx], edges_keys[end_idx]]
    del verts_keys[start_idx]

    ############### Parametrize node selecion

    x = 1
    x_1 = 2
    dx = abs(verts_keys[x][0] - verts_keys[x_1][0])
    dy = abs(verts_keys[x][1] - verts_keys[x_1][1])
    dz = abs(verts_keys[x][2] - verts_keys[x_1][2])

    radius = max(dx, dy, dz)


    ### Initialize
    max_generations=bpy.context.scene.my_tool_dist.max_generations
    top_percentage=bpy.context.scene.my_tool_dist.top_percentage
    population_size=bpy.context.scene.my_tool_dist.population_size

    #(max_generations)
    start(sel_vert,verts_keys,radius,max_generations,top_percentage,population_size)


######################################################################################
#                               Straigth Distance
######################################################################################

def straigth_distance_fc():
    ob = bpy.context.active_object
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)

    obMat = ob.matrix_world
    sel_vert = [tuple(obMat @ vert.co) for vert in bm.verts if vert.select == True]

    emptyMesh = bpy.data.meshes.new('emptyMesh')
    theObj = bpy.data.objects.new("Straight_distance", emptyMesh)
    bpy.context.collection.objects.link(theObj)

    emptyMesh.from_pydata(sel_vert, [(0,1)], [])
    emptyMesh.update()
    bpy.context.view_layer.update()

    bpy.context.scene.my_tool_dist.Straight_distance=_distance(sel_vert[0], sel_vert[1])
    return(_distance(sel_vert[0], sel_vert[1]))

class straigth_distance(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.distance2"
    bl_label = "Straight distance"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print('The minimun path length is', straigth_distance_fc(), 'units')
        return {'FINISHED'}

######################################################################################
#                               Dijkstra Distance
######################################################################################

from math import inf


class Node:
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
    
    d = {v : Node(v) for v in bm.verts}
    node = d[v_start]
    node.length = 0
    
    visiting = [node]

    while visiting:
        node = visiting.pop(0)
        
        if node.vert is v_target:
            return d
        
        for e in node.edges:
            e.tag = True
            length = node.length + e.calc_length()
            v = e.other_vert(node.vert)
            
            visit = d[v]
            visiting.append(visit)
            if visit.length > length:
                visit.length = length
                visit.shortest_path = node.shortest_path + [e]
      
        visiting.sort(key=lambda n: n.length)

    return d

# test call select two verts edit mode

def run_dijkstra():         
    context = bpy.context
    ob = context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    v1, v2 = bm.select_history[-2:]            
               
    # calc shortest paths to one vert
    nodes = dijkstra(bm, v1)
    # specific target vert (quicker)
    #nodes = dijkstra(bm, v1, v_target=v2)
    # results of other vert
    node = nodes[v2]

    bpy.context.scene.my_tool_dist.dijkstra_distance_pointer = float(node.length) 
    print('The minimun path length is', node.length, 'units')

    for e in node.shortest_path:
        e.select_set(True)
    
    sel_vert = [node.shortest_path[0].verts[0].co]
    #print(node.shortest_path[0].verts[0].co)
   
    for i in range(len(node.shortest_path)): #node.shortest_path[3].verts
        sel_vert.append(node.shortest_path[i].verts[0].co)
        sel_vert.append(node.shortest_path[i].verts[1].co)
        
    print(sel_vert)


    path_x = [sel_vert[j][0] for j in range(len(sel_vert))]
    path_y = [sel_vert[j][1] for j in range(len(sel_vert))]
    path_z = [sel_vert[j][2] for j in range(len(sel_vert))]


    #print(sel_vert)

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

class dijkstra_distance(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.dijkstra"
    bl_label = "Dijkstra distance"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        run_dijkstra()
        return {'FINISHED'} 


############ Functions ###############################################################

class distance_GA(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.distance"
    bl_label = "Node distance"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print('Starting Genetic Algorithm')
        distance_GA_fc()
        return {'FINISHED'}



class MySettings_Distance(bpy.types.PropertyGroup):
    max_generations: bpy.props.IntProperty(
        name="Slider",
        description="Allow Change Some Size",
        default= 2,
        min =2,
        max = 100
    )

    population_size: bpy.props.IntProperty(
        name="Slider",
        description="Allow Change Some Size",
        default= 10,
        min =10,
        max = 1000
    )

    top_percentage: bpy.props.FloatProperty(
        name="Slider",
        description="Allow Change Some Size",
        default= 0.4,
        min =0.1,
        max = 1
    )
    Node_distance: bpy.props.FloatProperty()
    Straight_distance: bpy.props.FloatProperty()
    dijkstra_distance_pointer: bpy.props.FloatProperty()