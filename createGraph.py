import os
import sys
import json

sys.path.append('.')

from graph import Graph

## This module will aim to create the adjacency matrix based on inputs
## inputs are a list of vertices and a list of tuples where the tuples are made of the two vertices which makes an edge and the cost associated with that edge
## inputs are provided thru two json files
## e.g. createGraph(['a','b','c'], [('a','b',10),('a','c',20),('b','c',30)])

class createGraph:
    def __init__(self, vertexJsonFile='vertices.json', edgeJsonFile='edges.json'):
        self.vertexJsonFile = vertexJsonFile
        self.edgeJsonFile = edgeJsonFile
        
        ## provide json as vertices and edges
        with open('vertices.json','r') as f:
            vertices_config = json.load(f)
    
        listOfVertices=[]

        for i in range(0,len(vertices_config['vertices'])):
            listOfVertices.append(vertices_config['vertices'][i]['vertex_id'])
        
        with open('edges.json','r') as f:
            edges_config = json.load(f)
            
        listOfEdges=[]
        
        for i in range(0,len(edges_config['edges'])):
            listOfEdges.append( (edges_config['edges'][i]['from_vertex_id'], edges_config['edges'][i]['to_vertex_id'], edges_config['edges'][i]['edge_id']) )

        g = Graph(len(listOfVertices))
        # create the vertices of the graph
        for v in range(0,len(listOfVertices)):
            g.setVertex(v,listOfVertices[v])
        # establish the edges
        fromDict=[]
        toDict=[]
        for e in range(0,len(listOfEdges)):
            frm,to,cost = listOfEdges[e]
            # keeping a track of the starting and ending vertices of the edges. Is this the most optimal storage ??
            if (listOfVertices.count(frm) == 0 or listOfVertices.count(to) == 0):
                print("any one of the provided vertex is not in the list of vertices, this edge won't be created")
            else:
                fromDict.append(frm)
                toDict.append(to)
                #ensure only directed graphs are allowed. Is count the most optimal way of doing this ??
                if (fromDict.count(to) > 0 and toDict.count(frm) > 0):
                    print("only directed graph is allowed, this edge won't be created")
                else:
                    g.addEdge(frm, to, cost)
            
        g.printMatrix()
        