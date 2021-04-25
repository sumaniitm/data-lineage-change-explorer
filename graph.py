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