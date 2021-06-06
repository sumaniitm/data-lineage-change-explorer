import os
import sys
import json

sys.path.append('.')

from createGraph import createGraph
from vertex import Vertex
from graph import Graph

## This module will display the graph in plain english

class displayDataLineage:
    def __init__(self):
        self.cg = createGraph()
        
    def getRootAttribute(self):
        valueMatrix = self.cg.createValueMatrix()
        for i in range(len(valueMatrix.getVertices())):
            vtx = Vertex(valueMatrix.getVertex(valueMatrix.getVertices()[i]))
            conn = vtx.getConnections(valueMatrix)
            if not any(conn):
                #return valueMatrix.getVertices()[i]
                return i
    
    ## The data attributes will display as a result of BFS on the attributes graph            
    def showAttributeLineage(self):
        valueMatrix = self.cg.createValueMatrix()
        start = self.getRootAttribute()
        BFSlist,BFSedgeList = valueMatrix.BFS(start)
        finalVertexList = []
        for i in range(len(BFSlist)):
            finalVertexList.append({'name':valueMatrix.getVertices()[BFSlist[i]], 'id':BFSlist[i]})
        return finalVertexList,BFSedgeList
    
    ## The delta (percentages) will display as a result of BFS on the attributes graph
    def showDeltaLineage(self):
        deltaMatrix = self.cg.createDeltaMatrix()
        start = self.getRootAttribute()
        BFSlist,BFSedgeList = deltaMatrix.BFS(start)
        finalVertexList = []
        edgeLabels = []
        for i in range(len(BFSlist)-1):
            finalVertexList.append(deltaMatrix.getEdges()[BFSlist[i]])
        for i in range(len(BFSlist)-1):
            edgeLabels.append(finalVertexList[i][2])
        #return finalVertexList
        finalVertexList,BFSedgeList = self.showAttributeLineage()
        for i in range(len(edgeLabels)):
            BFSedgeList[i]['label']=edgeLabels[i]
        return BFSedgeList
        