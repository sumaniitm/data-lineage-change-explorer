"""
This class will aim to create the directed graphs based on the list of vertices and two list of edges, one of which
holds the current values of the entities and the other holding the past values (which acts as a lookup).
These inputs are provided via three json files
The method check_for_valid_lookup verifies whether the structure and entries present in lookup (holding past) json
matches with that of the edge (holding current) json
The method create_value_matrix creates a graph with the vertices passed to it and based on the relationships between
the vertices defined in edge.json. The cost of the edges returned by this method doesn't hold any significance.
The graph is represented in the form of an adjacency matrix which depicts three
aspects
1. if an entry A(i,j) in the adjacency matrix A is not -1 then there exists a transformation from i to j
2. in the tuple (i,j), i represents the starting value of the data attribute corresponding to the vertex i before
any transformation is applied on it and j is the final value of the vertex j after all the transformations are applied
(which can have contributions from other vertices as well)
The method create_delta_matrix performs the same action as create_value_matrix, however, in addition to the edges and
vertices of the graph, it also adds the changes in the data entities as the cost of the edge
"""

import sys
import json
from graph import Graph

sys.path.append('.')


class CreateGraph:
    def __init__(self, vertex_json_file='json_files/vertices.json', edge_json_file='json_files/edges.json',
                 lookup_json_file='json_files/lookupPast.json'):
        self.vertexJsonFile = vertex_json_file
        self.edgeJsonFile = edge_json_file
        self.lookupJsonFile = lookup_json_file
        
        with open(vertex_json_file, 'r') as f:
            vertices_config = json.load(f)
    
        self.listOfVertices = []

        for i in range(0, len(vertices_config['vertices'])):
            self.listOfVertices.append(vertices_config['vertices'][i]['vertex_id'])
        
        with open(edge_json_file, 'r') as f:
            edges_config = json.load(f)
            
        self.listOfEdges = []
        self.listOfEdgesToCompare = []
        
        for i in range(0, len(edges_config['edges'])):
            self.listOfEdges.append((edges_config['edges'][i]['from_vertex_id'],
                                     edges_config['edges'][i]['to_vertex_id'],
                                     (edges_config['edges'][i]['edge_value'],
                                      edges_config['edges'][i]['from_vertex_value'])))
            self.listOfEdgesToCompare.append((edges_config['edges'][i]['from_vertex_id'],
                                              edges_config['edges'][i]['to_vertex_id']))
        
        with open(lookup_json_file, 'r') as f:
            lookup_config = json.load(f)
            
        self.listOfLookupEdges = []
        self.listOfLookupEdgesToCompare = []
        
        for i in range(0, len(lookup_config['edges'])):
            self.listOfLookupEdges.append((lookup_config['edges'][i]['from_vertex_id'],
                                           lookup_config['edges'][i]['to_vertex_id'],
                                           (lookup_config['edges'][i]['edge_value'],
                                            lookup_config['edges'][i]['from_vertex_value'])))
            self.listOfLookupEdgesToCompare.append((lookup_config['edges'][i]['from_vertex_id'],
                                                    lookup_config['edges'][i]['to_vertex_id']))

    def check_for_valid_lookup(self):
        result = True
        if len(self.listOfLookupEdges) != len(self.listOfEdges):
            print("the total number of edges in edges.json and lookupPast.json are different; cannot create delta")
            result = False
        else:
            for e in range(0, len(self.listOfEdges)):
                if self.listOfEdgesToCompare[e] != self.listOfLookupEdgesToCompare[e]:
                    print("The {0}th edge between edges.json and lookupPast.json are different; cannot create delta"
                          .format(e))
                    result = False
                    break
        return result

    def create_value_matrix(self):
        g = Graph(len(self.listOfVertices))
        for v in range(0, len(self.listOfVertices)):
            g.set_vertex(v, self.listOfVertices[v])
        from_dict = []
        to_dict = []
        for e in range(0, len(self.listOfEdges)):
            frm, to, cost = self.listOfEdges[e]
            if (self.listOfVertices.count(frm) == 0) or (self.listOfVertices.count(to) == 0):
                print("any one of the provided vertex is not in the list of vertices, this edge won't be created")
            else:
                from_dict.append(frm)
                to_dict.append(to)
                if (from_dict.count(to) > 0) and (to_dict.count(frm) > 0):
                    print("only directed graph is allowed, this edge won't be created")
                else:
                    g.add_edge(frm, to, cost)
        return g
        
    def create_delta_matrix(self):
        if not self.check_for_valid_lookup():
            return
        g_delta = Graph(len(self.listOfVertices))
        for v in range(0, len(self.listOfVertices)):
            g_delta.set_vertex(v, self.listOfVertices[v])
        from_dict = []
        to_dict = []
        for e in range(0, len(self.listOfLookupEdges)):
            frm_lkp, to_lkp, cost_lkp = self.listOfLookupEdges[e]
            frm, to, cost_curr = self.listOfEdges[e]
            if cost_lkp != (0, 0):
                cost = tuple(map(lambda i, j: round((i - j)/j, 3) if j != 0 else 0, cost_curr, cost_lkp))
            else:
                cost = (0, 0)
            if (self.listOfVertices.count(frm) == 0) or (self.listOfVertices.count(to) == 0):
                print("any one of the provided vertex is not in the list of vertices, this edge won't be created")
            else:
                from_dict.append(frm)
                to_dict.append(to)
                if (from_dict.count(to) > 0) and (to_dict.count(frm) > 0):
                    print("only directed graph is allowed, this edge won't be created")
                else:
                    g_delta.add_edge(frm, to, cost)
        return g_delta
