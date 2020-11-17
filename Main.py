import re


# Or Cohen 307852681

# Define a class of Vertex
class Vertex:
    def __init__(self, name):
        # Is number
        self.name = name
        self.new_or_old = 'new'
        # Both is edges in G and in reserve G
        self.outgoing_edges = []
        self.outgoing_opposite_edges = []


# Define a class of Edge
class Edge:
    def __init__(self, from_vertex, to_vertex):
        # The vertex which the edge going out
        self.from_vertex = from_vertex
        # The vertex which the edge going in
        self.to_vertex = to_vertex


# Function that create our edges and vertex lists and already create also the opposite edges for the second part of
# the algo
def create_edges_vertex(str_list):
    edge_list = []
    opposite_edge_list = []
    vertex_list = []
    max_vertex_number = 0
    name_attr = []
    # If we get '1 0' or '0 2' that means our vertex has no edge it all
    for s in str_list:
        # Split the pairs of vertex from str in the form of '1 2' to '1' and '2'
        vertex = s.split(' ')
        # Check if the edge is vertex and himself if so doesn't create 2 vertex obj
        if int(vertex[0]) != int(vertex[1]):
            from_vertex = Vertex(int(vertex[0]))
            to_vertex = Vertex(int(vertex[1]))
        else:
            from_vertex = Vertex(int(vertex[0]))
            to_vertex = from_vertex
        # Checks for the max number of vertex name in the input
        if max_vertex_number < int(vertex[1]):
            max_vertex_number = int(vertex[1])
        if max_vertex_number < int(vertex[0]):
            max_vertex_number = int(vertex[0])
        # Create also the vertex list by adding each vertex that in edge does not add the name '0'
        # because '0' symbol that the vertex stands alone
        if from_vertex.name not in name_attr and from_vertex.name != 0:
            vertex_list.append(from_vertex)
            name_attr.append(from_vertex.name)
        elif from_vertex.name != 0:
            index = name_attr.index(from_vertex.name)
            from_vertex = vertex_list[index]
        if to_vertex.name not in name_attr and to_vertex.name != 0:
            vertex_list.append(to_vertex)
            name_attr.append(to_vertex.name)
        elif to_vertex.name != 0:
            index = name_attr.index(to_vertex.name)
            to_vertex = vertex_list[index]
        # Checks if we need to add edge by checking if 1 of the vertex.name value is '0' which
        # means that we wanted a vertex standing alone
        # else adds the edge to the list and also already create the opposite edge
        if from_vertex.name != 0 and to_vertex.name != 0:
            edge = Edge(from_vertex, to_vertex)
            opposite_edge = Edge(to_vertex, from_vertex)
            edge_list.append(edge)
            opposite_edge_list.append(opposite_edge)
            from_vertex.outgoing_edges.append(edge)
            to_vertex.outgoing_opposite_edges.append(opposite_edge)
    return edge_list, opposite_edge_list, vertex_list, max_vertex_number


def dfs_a(vertex_list, edge_list, max_vertex_number):
    # initialize color list and parent list and finish time list and time
    parent_list = max_vertex_number * ['none']
    finish_time_list = max_vertex_number * [-1]
    time = 1
    # Checks if we still have vertex which we didn't visit if so continue
    while 'new' in (u.new_or_old for u in vertex_list):
        # list which contain the vertex attribue which saya if they been visited already
        attr = []
        for u in vertex_list:
            attr.append(u.new_or_old)
        # Find the first unvisited vertex
        index = attr.index('new')
        vertex = vertex_list[index]
        # Change is status to visited
        vertex.new_or_old = 'old'
        # Check if the vertex has outgoing edges which we didn't checked yet or he has a parent
        while len(vertex.outgoing_edges) != 0 or parent_list[vertex.name - 1] != 'none':
            # If we have a edge which we didn't checked yet we will move to the vertex which the
            # edge point to and delete this edge
            if len(vertex.outgoing_edges) != 0:
                edge = vertex.outgoing_edges[0]
                vertex.outgoing_edges.remove(edge)
                v = edge.to_vertex
                # Check if the neighbor has been visited if not we make the vertex is father and continue the
                # dfs with the neighbor
                if v.new_or_old is 'new':
                    v.new_or_old = 'old'
                    parent_list[v.name - 1] = vertex
                    vertex = v
            # If we don't have outgoing edges we didn't visited we check if the vertex has a father
            # if so return to him and mark the vertex finished and the time we finish with him
            elif parent_list[vertex.name - 1] != 'none':
                finish_time_list[vertex.name - 1] = time
                time = time + 1
                vertex = parent_list[vertex.name - 1]
        finish_time_list[vertex.name - 1] = time
        time = time + 1
    return finish_time_list


def dfs_b(vertex_list, opposite_edge_list, finish_time_list, max_vertex_number):
    # Initialize color list and parent list and finish time list
    parent_list = max_vertex_number * ['none']
    scc_list = []
    # Initialize all the vertex to unvisited
    for vertex in vertex_list:
        vertex.new_or_old = 'new'
    # Checks if we still have vertex which we didn't visit if so continue
    while 'new' in (u.new_or_old for u in vertex_list):
        # Looking for the max finishing time in our list
        max_time = 0
        max_time = max(finish_time_list)
        index = finish_time_list.index(max_time)
        finish_time_list[index] = -1
        # Get the vertex name with the max finish time
        vertex
        for v in vertex_list:
            if v.name == index + 1:
                vertex = v
        # Create new scc group and add the vertex also mark the vertex visited
        group = []
        group.append(vertex.name)
        vertex.new_or_old = 'old'
        # If we don't have outgoing edges we didn't visited we check if the vertex has a father
        # if so return to him and mark the vertex finished and the time we finish with him
        while len(vertex.outgoing_opposite_edges) != 0 or parent_list[vertex.name - 1] != 'none':
            # If we have a edge which we didn't checked yet we will move to the vertex which the
            # edge point to and delete this edge
            if len(vertex.outgoing_opposite_edges) != 0:
                edge = vertex.outgoing_opposite_edges[0]
                vertex.outgoing_opposite_edges.remove(edge)
                v = edge.to_vertex
                # Check if the neighbor has been visited if not we make the vertex is father and continue the
                # dfs with the neighbor also we add him to our scc
                if v.new_or_old is 'new':
                    v.new_or_old = 'old'
                    parent_list[v.name - 1] = vertex
                    finish_time_list[v.name - 1] = -1
                    vertex = v
                    group.append(vertex.name)
            # If we don't have outgoing edges we didn't visited we check if the vertex has a father
            # if so return to him
            elif parent_list[vertex.name - 1] != 'none':
                vertex = parent_list[vertex.name - 1]
        scc_list.append(group)
    return scc_list


# Function that prints all of our scc by order
def print_scc(scc_list):
    # Order the groups
    scc_list = sorted(scc_list, key=min)
    # Print the vertex with X next to their names
    for scc in scc_list:
        for i in range(0, len(scc)):
            value = scc[i]
            v_str = 'X' + str(value)
            scc[i] = v_str
        print(scc, end=',')
    print()
    return


# Checks for valid input
def get_input():
    good_input = False
    # While we enter unvalid input we continue to ask for valid input
    while not good_input:
        input_str = input('Please enter your graph or ''EXIT'' if you want to exit the software\n')
        good_input = True
        # If we got EXIT we exit the system
        if input_str == 'EXIT':
            exit(0)
        # Split our entered input by in every ,
        input_str = input_str.split(',')
        for s in input_str:
            # Checks if every node entered in the pattern('1 2') we wanted else say the input is not valid
            matched = re.match("[0-9]+ [0-9]+", s)
            match = bool(matched)
            if not match:
                good_input = False
            #Check if we entered 2 vertex only between ','
            vertexes = s.split(' ')
            if len(vertexes) != 2:
                good_input = False
    return input_str


# Main function
def main_func():
    while 1:
        input_str = get_input()
        edge_list, opposite_edge_list, vertex_list, max_vertex_number = create_edges_vertex(input_str)
        finish_time_list = dfs_a(vertex_list, edge_list, max_vertex_number)
        scc_list = dfs_b(vertex_list, opposite_edge_list, finish_time_list, max_vertex_number)
        print_scc(scc_list)


if __name__ == '__main__':
    main_func()
