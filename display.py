import os
import sys
import json

sys.path.append('.')

from createGraph import createGraph
from vertex import Vertex

## This module will display the graph in plain english

class displayDataLineage:
    def __init__(self):
        self.cg = createGraph()
        
    def showAttributeLineage(self):
        valueMatrix = self.cg.createValueMatrix()
        for i in range(len(valueMatrix.getVertices())):
            vtx = Vertex(valueMatrix.getVertex(valueMatrix.getVertices()[i]))
            conn = vtx.getConnections(valueMatrix)
            for j in range(len(conn)):
                if conn[j] != 0:
                    print(valueMatrix.getVertices()[i]+' generates '+valueMatrix.getVertices()[j])
    
    def showDeltaLineage(self):
        deltaMatrix = self.cg.createDeltaMatrix()
        for i in range(len(deltaMatrix.getVertices())):
            vtx = Vertex(deltaMatrix.getVertex(deltaMatrix.getVertices()[i]))
            conn = vtx.getConnections(deltaMatrix)
            for j in range(len(conn)):
                if conn[j] != 0:
                    print(deltaMatrix.getVertices()[i]+' has changed by '+str(conn[j][0])+'% and '+deltaMatrix.getVertices()[j]+' has changed by '+str(conn[j][1])+'%')