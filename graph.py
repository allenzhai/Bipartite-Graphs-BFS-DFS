from stack_array import * #Needed for Depth First Search
from queue_array import * #Needed for Breadth First Search
import copy

class Vertex:
    '''Add additional helper methods if necessary.'''
    def __init__(self, key):
        '''Add other attributes as necessary'''
        self.id = key
        self.adjacent_to = []
        self.visited1 = False
        self.visited = False
        self.color = None

    # def __repr__(self):
    #     return (" {}".format(self.id))

    def __lt__(self, other):
        return self.id < other.id

    def adj_sort(self):
        self.adjacent_to.sort()

    def set_visit(self, visit):
        self.visited = visit

    def set_color(self, color):
        self.color = color

class Graph:
    '''Add additional helper methods if necessary.'''
    def __init__(self, filename):
        '''reads in the specification of a graph and creates a graph using an adjacency list representation.  
           You may assume the graph is not empty and is a correct specification.  E.g. each edge is 
           represented by a pair of vertices.  Note that the graph is not directed so each edge specified 
           in the input file should appear on the adjacency list of each vertex of the two vertices associated 
           with the edge.'''
        self.vertices = self.build_adj(filename)

    def build_adj(self, filename):

        adj = {}
        temp = []
        
        f = open(filename, 'r')

        for line in f:
            temp = (line.strip().split())

            v1 = Vertex(temp[0])
            v2 = Vertex(temp[1]) 
            
            #if both vertices aren't in the list
            if temp[0] not in adj and temp[1] not in adj:

                v1.adjacent_to.append(v2)
                v2.adjacent_to.append(v1)
                adj[temp[0]] = v1
                adj[temp[1]] = v2

            #if first one is in the list but the second isn't
            elif temp[0] in adj and temp[1] not in adj:
                v2.adjacent_to.append(adj[temp[0]])
                adj[temp[1]] = v2
                adj[temp[0]].adjacent_to.append(v2)

            #if the first one isn't in the list but the second is
            elif temp[0] not in adj and temp[1] in adj:
                v1.adjacent_to.append(adj[temp[1]])
                adj[temp[0]] = v1
                adj[temp[1]].adjacent_to.append(v1)

            #if both are in the list
            else:
                adj[temp[0]].adjacent_to.append(v2)
                adj[temp[1]].adjacent_to.append(v1)

        f.close()
        return adj

    def add_vertex(self, key):
        '''Add vertex to graph, only if the vertex is not already in the graph.'''
        if key != self.get_vertex(key):
            vertex = Vertex(key)
            self.vertices[key] = vertex

    def get_vertex(self, key):
        '''Return the Vertex object associated with the id. If id is not in the graph, return None'''
        if key in self.vertices:
            return self.vertices[key]
        else:
            return None

    def add_edge(self, v1, v2):
        '''v1 and v2 are vertex id's. As this is an undirected graph, add an 
           edge from v1 to v2 and an edge from v2 to v1.  You can assume that
           v1 and v2 are already in the graph'''
        self.get_vertex(v1).adjacent_to.append(self.get_vertex(v2))
        self.get_vertex(v2).adjacent_to.append(self.get_vertex(v1))

    def get_vertices(self):
        '''Returns a list of id's representing the vertices in the graph, in ascending order'''
        ids = sorted(self.vertices)
        return ids

    def conn_components(self): 
        '''Returns a list of lists.  For example, if there are three connected components 
           then you will return a list of three lists.  Each sub list will contain the 
           vertices (in ascending order) in the connected component represented by that list.
           The overall list will also be in ascending order based on the first item of each sublist.
           This method MUST use Depth First Search logic!'''

        ids = self.get_vertices()
        conn_components = []
        stack = Stack(len(ids))
        vertex = self.vertices[ids[0]]
        
        stack.push(vertex)
        self.vertices[vertex.id].visited1 = True
        vertex.adj_sort()
        previous = vertex
        previousprevious = previous
        

        temp = []
        possible_val = None
        while not stack.is_empty():

            #determine next value in adjacent list
            for i in vertex.adjacent_to:
                if self.vertices[i.id].visited1 == False:
                    possible_val = i.id
                    break
                possible_val = None

            #if there are no possible values or the possible values aren't in the ids, pop it
            if possible_val == None:
                temp.append(stack.pop().id)
                if vertex == previous:
                    vertex = previousprevious
                else:
                    vertex = previous

            else:
                next_val = self.vertices[possible_val]
                stack.push(next_val)
                self.vertices[next_val.id].visited1 = True
                previousprevious = previous
                previous = vertex
                vertex = next_val
                vertex.adj_sort()

            #if you reach the end of one part of the graph but there's still more
            if stack.is_empty():
                temp.sort()
                conn_components.append(temp)
                temp = []

                for k in ids:
                    if self.vertices[k].visited1 == False:
                        vertex = self.vertices[k]
                        stack.push(vertex)
                        self.vertices[k].visited1 = True
                        vertex.adj_sort()
                        break
                        
        return conn_components

    def is_bipartite(self):
        '''Returns True if the graph is bicolorable and False otherwise.
           This method MUST use Breadth First Search logic!'''

        ids = self.get_vertices()

        queue = Queue(len(ids))
        queue.enqueue(self.vertices[ids[0]])
        self.vertices[ids[0]].set_color("Red")
        self.vertices[ids[0]].set_visit(True)

        color = "Red"

        while not queue.is_empty():
            vertex = queue.dequeue()
            self.vertices[vertex.id].set_visit(True)
            vertex.adj_sort()
            adj = vertex.adjacent_to

            if vertex.color == "Red":
                color = "Black"
            else:
                color = "Red"

            for i in adj:
                if self.vertices[i.id].color == None:
                    self.vertices[i.id].set_color(color)
                else:
                    if self.vertices[i.id].color != color:
                        return False

                if self.vertices[i.id].visited == False:
                    queue.enqueue(self.vertices[i.id])
                    self.vertices[i.id].set_visit(True)
                    
            if queue.is_empty():
                for k in ids:
                    if self.vertices[k].visited == False:
                        queue.enqueue(self.vertices[k])
                        self.vertices[k].set_color("Red")
                        self.vertices[k].set_visit(True)
                        color = "Red"
                        break

        return True
