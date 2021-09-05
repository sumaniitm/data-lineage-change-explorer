"""
This class implements the Vertices of a graph. It is initialized by passing the id of the vertex and by declaring a
variable which denotes whether the vertex have already been visited during a search.
The get_connection method accepts a graph and returns the adjacency list of the vertex in that graph
The get_vertex_id method returns the id of the vertex
The set_vertex_id method sets the id of the vertex
Explicit call to __str__ ensures that the vertex id is represented as a string
"""

import sys

sys.path.append('.')


class Vertex:
    def __init__(self, node):
        self.id = node
        self.visited = False

    def get_connections(self, g):
        return g.adjMatrix[self.id]
    
    def get_vertex_id(self):
        return self.id
        
    def set_vertex_id(self, node_id):
        self.id = node_id
        
    def __str__(self):
        return str(self.id)
