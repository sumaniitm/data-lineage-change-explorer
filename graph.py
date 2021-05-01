import os
import sys
sys.path.append('.')

from vertex import Vertex

class Graph:
    def __init__(self, numVertices, cost=0):
        self.adjMatrix = [[-1]*numVertices for _ in range(numVertices)]
        self.numVertices = numVertices
        self.vertices = []
        for i in range(0,numVertices):
            newVertex = Vertex(i)
            self.vertices.append(newVertex)
            
    def setVertex(self, vtx, id):
        if 0 <= vtx < self.numVertices:
            self.vertices[vtx].setVertexId(id)
            
    def getVertex(self, n):
        for v in range(0, self.numVertices):
            if n == self.vertices[v].getVertexId():
                return v
            else:
                return -1
                
    def addEdge(self, frm, to, cost=0):
        self.adjMatrix[self.getVertex(frm)][self.getVertex(to)] = cost