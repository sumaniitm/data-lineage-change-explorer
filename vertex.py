import os
import sys
sys.path.append('.')

class Vertex:
    def __init__(self,node):
        self.id = node
        self.visited = False
    def addNeighbour(self,neighbour,g):
        g.addEdge(self.id,neighbour)
    def getConnections(self,g):
        return g.adjMatrix[self.id]