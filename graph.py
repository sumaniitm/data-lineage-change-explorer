import os
import sys
sys.path.append('.')

from vertex import Vertex
from queue import Queue

class Graph:
    def __init__(self, numVertices, cost=0):
        self.adjMatrix = [[0]*numVertices for _ in range(numVertices)]
        self.adjMatrixTranspose = [[self.adjMatrix[j][i] for j in range(len(self.adjMatrix))] for i in range(len(self.adjMatrix[0]))]
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
        print('\n')
        rez = [[self.adjMatrix[j][i] for j in range(len(self.adjMatrix))] for i in range(len(self.adjMatrix[0]))]
        for r in rez:
            print(r)
            
    # Function to perform BFS on the graph
    def BFS(self, start):
        visited = [False] * self.numVertices
        adjMatrixTrans = [[self.adjMatrix[j][i] for j in range(len(self.adjMatrix))] for i in range(len(self.adjMatrix[0]))]
        #q = [start]
        q = Queue()
        q.enQueue(start)
        visited[start] = True
        while q:
            #vis = q[0]
            vis = q.deQueue()
            #print('in while')
            print(vis)
            #q.pop(0)
            for i in range(self.numVertices):
                #print('i is ', i)
                #print('inside for ',adjMatrixTrans[vis][i])
                if ( adjMatrixTrans[vis][i] != 0 and ( visited[i] == False ) ):
                    #print('inside if')
                    q.enQueue(i)
                    visited[i] = True