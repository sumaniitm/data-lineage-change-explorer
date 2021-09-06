import os
import sys
import json

sys.path.append('.')

from createGraph import createGraph
from vertex import Vertex
from graph import Graph

## This module will display the graph in plain english

class displayDataLineage:
    def __init__(self, vertexJsonFile='json_files/vertices.json', edgeJsonFile='json_files/edges.json', lookupJsonFile='json_files/lookupPast.json'):
        self.cg = createGraph(vertexJsonFile, edgeJsonFile, lookupJsonFile)
        
    def getRootAttribute(self):
        valueMatrix = self.cg.createValueMatrix()
        for i in range(len(valueMatrix.get_vertices())):
            vtx = Vertex(valueMatrix.get_vertex(valueMatrix.get_vertices()[i]))
            conn = vtx.get_connections(valueMatrix)
            if not any(conn):
                #return valueMatrix.get_vertices()[i]
                return i
    
    ## The data attributes will display as a result of BFS on the attributes graph            
    def showAttributeLineage(self):
        valueMatrix = self.cg.createValueMatrix()
        start = self.getRootAttribute()
        BFSlist, BFSedgeList = valueMatrix.breadth_first_search(start)
        finalVertexList = []
        for i in range(len(BFSlist)):
            finalVertexList.append({'name': valueMatrix.get_vertices()[BFSlist[i]], 'id': BFSlist[i], 'width': len(valueMatrix.get_vertices()[BFSlist[i]])})
        return finalVertexList
    
    ## The delta (percentages) will display as a result of BFS on the attributes graph
    def showDeltaLineage(self):
        deltaMatrix = self.cg.createDeltaMatrix()
        start = self.getRootAttribute()
        BFSlist,BFSwithLabel = deltaMatrix.BFSwithLabel(start)
        finalVertexList = []
        edgeLabels = []
        return BFSwithLabel