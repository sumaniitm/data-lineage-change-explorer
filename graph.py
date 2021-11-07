"""
This class implements a directed graph using adjacency matrix. It accepts the number of vertices and an initial cost to
build the default adjacency matrix representing a directed graph without any edges.
This class is initialized with a default adjacency matrix, the transpose of the adjacency matrix, the accepted number
of vertices passed as an argument and a list of objects of the Vertex class.
The set_vertex method accepts a position within the range of the number of vertices and a vertex id, then assigns
the vertex id to the vertex at that position.
The get_vertex method returns the position of a vertex in the list of vertices.
The add_edge method creates an edge between the source and destination with the associated cost which is going to be a
tuple of the percentage changes in the data of the source and destination.
The get_vertices method returns a list of vertex ids of the vertices building the directed graph.
The get_edges method returns a list of the edges (along with their costs) between the vertices of the directed graph.
print_matrix method is purely for debugging purpose and is not used anywhere else, it merely prints the adjacency
matrix.
The breadth_first_search method accepts the starting vertex as the input and traverses the directed graph in a breadth
first manner and returns a list of the vertices and the edges (in terms of source and destination of an edge)
in breadth first order. The method starts by transposing the adjacency matrix of the directed graph, then uses a queue
to keep track of the visited vertices. For each visited vertex, it looks for the non-zero entries in the row
corresponding to the vertex in the adjacency matrix to get the immediate neighbours of the vertex and then marks those
as visited.
The breadth_first_search_with_label method does the same as breadth_first_search but returns the cost of the
edges as well, the percentage changes of the data entities are represented as the cost of the edges.
"""

from vertex import Vertex
from q import Queue
import sys

sys.path.append('.')


class Graph:
    def __init__(self, number_of_vertices, cost=0):
        self.adjMatrix = [[0]*number_of_vertices for _ in range(number_of_vertices)]
        self.adjMatrixTranspose = [
            [self.adjMatrix[j][i] for j in range(len(self.adjMatrix))]
            for i in range(len(self.adjMatrix[0]))
        ]
        self.number_of_vertices = number_of_vertices
        self.vertices = []
        for i in range(0, number_of_vertices):
            new_vertex = Vertex(i)
            self.vertices.append(new_vertex)
            
    def set_vertex(self, vtx, v_id):
        if 0 <= vtx < self.number_of_vertices:
            self.vertices[vtx].set_vertex_id(v_id)
            
    def get_vertex(self, n):
        vtx = -1
        for v in range(0, self.number_of_vertices):
            if n == self.vertices[v].get_vertex_id():
                vtx = v
        return vtx
                
    def add_edge(self, frm, to, cost=(0, 0)):
        self.adjMatrix[self.get_vertex(frm)][self.get_vertex(to)] = cost
        
    def get_vertices(self):
        vertices = []
        for v in range(0, self.number_of_vertices):
            vertices.append(self.vertices[v].get_vertex_id())
        return vertices
        
    def get_edges(self):
        edges = []
        for v in range(0, self.number_of_vertices):
            for u in range(0, self.number_of_vertices):
                if self.adjMatrix[u][v] != 0:
                    vid = self.vertices[v].get_vertex_id()
                    wid = self.vertices[u].get_vertex_id()
                    edges.append((wid, vid, self.adjMatrix[u][v]))
        return edges
    
    def print_matrix(self):
        for u in range(0, self.number_of_vertices):
            row = []
            for v in range(0, self.number_of_vertices):
                row.append(self.adjMatrix[u][v])
            print(row)

    def breadth_first_search(self, start):
        visited = [False] * self.number_of_vertices
        bfs_list = []
        bfs_edge_list = []
        adj_matrix_trans = [
            [self.adjMatrix[j][i] for j in range(len(self.adjMatrix))] for i in range(len(self.adjMatrix[0]))
        ]
        q = Queue()
        q.enqueue(start)
        visited[start] = True
        while not q.is_empty():
            vis = q.dequeue()
            bfs_list.append(vis)
            for i in range(self.number_of_vertices):
                if (adj_matrix_trans[vis][i] != 0) and (visited[i] is False):
                    q.enqueue(i)
                    visited[i] = True
                    bfs_edge_list.append({'source': i, 'destination': vis})
        return bfs_list, bfs_edge_list
        
    def breadth_first_search_with_label(self, start):
        visited = [False] * self.number_of_vertices
        bfs_list = []
        bfs_edge_list = []
        adj_matrix_trans = [
            [self.adjMatrix[j][i] for j in range(len(self.adjMatrix))] for i in range(len(self.adjMatrix[0]))
        ]
        q = Queue()
        q.enqueue(start)
        visited[start] = True
        while not q.is_empty():
            vis = q.dequeue()
            bfs_list.append(vis)
            for i in range(self.number_of_vertices):
                if (adj_matrix_trans[vis][i] != 0) and (visited[i] is False):
                    q.enqueue(i)
                    visited[i] = True
                    bfs_edge_list.append({'source': i, 'destination': vis, 'label': str(adj_matrix_trans[vis][i])})
        return bfs_list, bfs_edge_list

    def breadth_first_search_for_api(self, start):
        visited = [False] * self.number_of_vertices
        bfs_list = []
        bfs_edge_list = []
        adj_matrix_trans = [
            [self.adjMatrix[j][i] for j in range(len(self.adjMatrix))] for i in range(len(self.adjMatrix[0]))
        ]
        q = Queue()
        q.enqueue(start)
        visited[start] = True
        while not q.is_empty():
            vis = q.dequeue()
            bfs_list.append(vis)
            for i in range(self.number_of_vertices):
                if (adj_matrix_trans[vis][i] != 0) and (visited[i] is False):
                    q.enqueue(i)
                    visited[i] = True
                    bfs_edge_list.append({'source': self.get_vertices()[i], 'destination': self.get_vertices()[vis],
                                          'deltas': str(adj_matrix_trans[vis][i])})
        return bfs_list, bfs_edge_list


