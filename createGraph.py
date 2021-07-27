import os
import sys
import json

sys.path.append('.')

from graph import Graph

## This module will aim to create the adjacency matrix based on inputs
## inputs are a list of vertices and a list of tuples where the tuples are made of the two vertices which makes an edge and the cost associated with that edge
## inputs are provided thru two json files
## e.g. createGraph('vertices.json','edges.json')
## The output matrix depicts three things
## 1. if an entry A(i,j) in the marix A is not -1 then there exists a transformation from i to j
## 2. in the tuple (i,j), i represents the starting value of the data attribute corresponding to the vertex i before any transformation is applied on it and
##    j is the final value of the vertex j after all the transformations are applied (which can have contributions from other vertices as well)

class createGraph:
    def __init__(self, vertexJsonFile='json_files/vertices.json', edgeJsonFile='json_files/edges.json', lookupJsonFile='json_files/lookupPast.json'):
        self.vertexJsonFile = vertexJsonFile
        self.edgeJsonFile = edgeJsonFile
        self.lookupJsonFile = lookupJsonFile
        
        ## provide json as vertices, edges and past edge lookups
        
        ## The edge value represents the output of applying the transformation rule mentioned in edge_description on the from_vertex_id
        ## The vertex value represents the starting value of the data attribute corresponding to the vertex before any transformation is applied on it
        ## e.g. if a and b are two vertices directed at c and the transformation to arrive at c is given by a^2 + b^2 + 2ab then it can represented as
        ## the edge values of a-c and b-c will be a^2 and b^2 respectively, while the vertex value of c will be a^2 + b^2 + 2ab
        ## the vertex value of a and b are a and b respectively
        
        with open(vertexJsonFile, 'r') as f:
            vertices_config = json.load(f)
    
        self.listOfVertices=[]

        for i in range(0, len(vertices_config['vertices'])):
            self.listOfVertices.append(vertices_config['vertices'][i]['vertex_id'])
        
        with open(edgeJsonFile, 'r') as f:
            edges_config = json.load(f)
            
        self.listOfEdges=[]
        self.listOfEdgesToCompare=[]
        
        for i in range(0,len(edges_config['edges'])):
            self.listOfEdges.append( (edges_config['edges'][i]['from_vertex_id'], edges_config['edges'][i]['to_vertex_id'], ( edges_config['edges'][i]['edge_value'], edges_config['edges'][i]['from_vertex_value'] ) ) )
            self.listOfEdgesToCompare.append( (edges_config['edges'][i]['from_vertex_id'], edges_config['edges'][i]['to_vertex_id']) )
        
        with open(lookupJsonFile, 'r') as f:
            lookup_config = json.load(f)
            
        self.listOfLookupEdges=[]
        self.listOfLookupEdgesToCompare=[]
        
        for i in range(0,len(lookup_config['edges'])):
            self.listOfLookupEdges.append( (lookup_config['edges'][i]['from_vertex_id'], lookup_config['edges'][i]['to_vertex_id'], ( lookup_config['edges'][i]['edge_value'], lookup_config['edges'][i]['from_vertex_value']) ) )
            self.listOfLookupEdgesToCompare.append( (lookup_config['edges'][i]['from_vertex_id'], lookup_config['edges'][i]['to_vertex_id']) )


    def checkForValidLookup(self):
        ## check if the lookup.json is of same structure as the edges.json . This is a hard requirement
        result = True
        if len(self.listOfLookupEdges) != len(self.listOfEdges):
            print("the total number of edges in edges.json and lookupPast.json are different; cannot create delta, exiting!")
            result = False
        else:
            for e in range(0,len(self.listOfEdges)):
                if self.listOfEdgesToCompare[e] != self.listOfLookupEdgesToCompare[e]:
                    print("The {0}th edge between edges.json and lookupPast.json are different; cannot create delta, exiting!".format(e))
                    result = False
                    break
        return result
        
    ## This method will represent the current value matrix
    def createValueMatrix(self):
        g = Graph(len(self.listOfVertices))
        # create the vertices of the graph
        for v in range(0,len(self.listOfVertices)):
            g.setVertex(v,self.listOfVertices[v])
        # establish the edges
        fromDict=[]
        toDict=[]
        for e in range(0,len(self.listOfEdges)):
            frm,to,cost = self.listOfEdges[e]
            # keeping a track of the starting and ending vertices of the edges. Is this the most optimal storage ??
            if (self.listOfVertices.count(frm) == 0 or self.listOfVertices.count(to) == 0):
                print("any one of the provided vertex is not in the list of vertices, this edge won't be created")
            else:
                fromDict.append(frm)
                toDict.append(to)
                #ensure only directed graphs are allowed. Is count the most optimal way of doing this ??
                if (fromDict.count(to) > 0 and toDict.count(frm) > 0):
                    print("only directed graph is allowed, this edge won't be created")
                else:
                    g.addEdge(frm, to, cost)
        #g.printMatrix()
        return g
        
    def createDeltaMatrix(self):
        ## check for equivalence of edges.json and lookup.json in terms of edges.
        if not self.checkForValidLookup():
            return
        
        gDelta = Graph(len(self.listOfVertices))
        # create the vertices of the graph
        for v in range(0,len(self.listOfVertices)):
            gDelta.setVertex(v,self.listOfVertices[v])
        # establish the edges
        fromDict=[]
        toDict=[]
        
        for e in range(0,len(self.listOfLookupEdges)):
            frmLkp,toLkp,costLkp = self.listOfLookupEdges[e]
            frm,to,costCurr = self.listOfEdges[e]
            print(costCurr)
            print(costLkp)
            if costLkp != (0, 0):
                cost = tuple(map(lambda i, j: round((i - j)/j, 3), costCurr, costLkp))
            else:
                cost = (0, 0)
            print(cost)
            #print(cost)
            # keeping a track of the starting and ending vertices of the edges. Is this the most optimal storage ??
            if (self.listOfVertices.count(frm) == 0 or self.listOfVertices.count(to) == 0):
                print("any one of the provided vertex is not in the list of vertices, this edge won't be created")
            else:
                fromDict.append(frm)
                toDict.append(to)
                #ensure only directed graphs are allowed. Is count the most optimal way of doing this ??
                if (fromDict.count(to) > 0 and toDict.count(frm) > 0):
                    print("only directed graph is allowed, this edge won't be created")
                else:
                    gDelta.addEdge(frm, to, cost)
        #gDelta.printMatrix()
        return gDelta