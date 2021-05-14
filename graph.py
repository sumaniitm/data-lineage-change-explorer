import os
import sys
sys.path.append('.')

from vertex import Vertex

class Graph:
    def __init__(self, numVertices, cost=0):
        self.adjMatrix = [[0]*numVertices for _ in range(numVertices)]
        self.numVertices = numVertices
        self.vertices = []
        for i in range(0,numVertices):
            newVertex = Vertex(i)
            self.vertices.append(newVertex)
            
    def setVertex(self, vtx, id):
        if 0 <= vtx < self.numVertices:
            self.vertices[vtx].setVertexId(id)
            
    def getVertex(self, n):
        vtx = -1
        for v in range(0, self.numVertices):
            if n == self.vertices[v].getVertexId():
                vtx = v
        return vtx
                
    def addEdge(self, frm, to, cost=(0,0)):
        self.adjMatrix[self.getVertex(frm)][self.getVertex(to)] = cost
        
    def getVertices(self):
        vertices = []
        for v in range(0, self.numVertices):
            vertices.append(self.vertices[v].getVertexId())
        return vertices
        
    def getEdges(self):
        edges = []
        for v in range(0, self.numVertices):
            for u in range(0, self.numVertices):
                if self.adjMatrix[u][v] != -1:
                    vid = self.vertices[v].getVertexId()
                    wid = self.vertices[u].getVertexId()
                    edges.append((vid, wid, self.adjMatrix[u][v]))
        return edges
    
    def printMatrix(self):
        for u in range(0, self.numVertices):
            row = []
            for v in range(0, self.numVertices):
                row.append(self.adjMatrix[u][v])
            print(row)
            
    