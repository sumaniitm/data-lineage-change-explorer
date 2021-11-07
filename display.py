"""
The aim of this class is to return the graphs in the form of a python dict. The rationale is that the user can use this
class to get the dictionaries and create their own visualisation if they choose not to go the flask route. The elements
of the dictionary is built in a way to support the requirements of the dagre-D3 library which is used to render the
directed graph. The methods show_attribute_lineage and show_delta_lineage calls the get_root_attribute to get the root
vertex and then use that to invoke the breadth first search (from the graph object) from that vertex
"""

import sys
from createGraph import CreateGraph
from vertex import Vertex

sys.path.append('.')


class DisplayDataLineage:
    def __init__(self, vertex_json_file='json_files/vertices.json', edge_json_file='json_files/edges.json',
                 lookup_json_file='json_files/lookupPast.json'):
        self.cg = CreateGraph(vertex_json_file, edge_json_file, lookup_json_file)
        
    def get_root_attribute(self):
        value_matrix = self.cg.create_value_matrix()
        for i in range(len(value_matrix.get_vertices())):
            vtx = Vertex(value_matrix.get_vertex(value_matrix.get_vertices()[i]))
            conn = vtx.get_connections(value_matrix)
            if not any(conn):
                return i

    def show_attribute_lineage(self):
        value_matrix = self.cg.create_value_matrix()
        start = self.get_root_attribute()
        bfs_list, bfs_edge_list = value_matrix.breadth_first_search(start)
        final_vertex_list = []
        for i in range(len(bfs_list)):
            final_vertex_list.append({'name': value_matrix.get_vertices()[bfs_list[i]], 'id': bfs_list[i],
                                      'width': len(value_matrix.get_vertices()[bfs_list[i]])})
        return final_vertex_list

    def show_delta_lineage(self):
        delta_matrix = self.cg.create_delta_matrix()
        start = self.get_root_attribute()
        bfs_list, bfs_edge_list_with_label = delta_matrix.breadth_first_search_with_label(start)
        return bfs_edge_list_with_label

    def delta_lineage_api(self):
        delta_matrix = self.cg.create_delta_matrix()
        start = self.get_root_attribute()
        bfs_list, bfs_edge_list_with_label = delta_matrix.breadth_first_search_for_api(start)
        return bfs_edge_list_with_label
