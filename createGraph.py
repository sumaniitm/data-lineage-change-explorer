import os
import sys
sys.path.append('.')

from graph import Graph

## This module will aim to create the adjacency matrix based on inputs
## inputs are a list of vertices and a list of tuples where the tuples are made of the two vertices which makes an edge and the cost associated with that edge
## e.g. createGraph(['a','b','c'], [('a','b',10),('a','c',20),('b','c',30)])

class createGraph:
    def __init__(self, listOfVertices=[], listOfEdges=[]):
        self.listOfVertices = listOfVertices
        self.listOfEdges = listOfEdges
        g = Graph(len(listOfVertices))
        # create the vertices of the graph
        for v in range(0,len(listOfVertices)):
            g.setVertex(v,listOfVertices[v])
        # establish the edges
        fromDict=[]
        toDict=[]
        for e in range(0,len(listOfEdges)):
            frm,to,cost = listOfEdges[e]
            fromDict.append(frm)
            toDict.append(to)
            if (fromDict.count(to) > 0 and toDict.count(frm) > 0):
                print("only directed graph is allowed")
                return
            else:
                g.addEdge(frm, to, cost)
            
        g.printMatrix()
        