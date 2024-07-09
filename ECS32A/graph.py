
import copy as copy

class Graph():
    def __init__(self):
        #Adjacency List
        self.adj = [] #list with no edges or vertices
    def addVertex(self, data):
        self.adj.append([data]) #Python list is a dynamic array
    def removeVertex(self, data):
        #for loops finds index of the vertex we want to remove
        for i, lis in enumerate(self.adj):
            if lis[0] == data:
                vertexIndex = i
        self.adj.pop(vertexIndex) #remove entry (linked list)
        
        #for loop goes through all other vertices to get rid of all the incident edges
        for i, lis in enumerate(self.adj):
            for edge in lis[1:]:
                if edge[0] == data:
                    lis.remove(edge)
    def addEdge(self, src, dest, weight = 1):
        #for loop goes through array
        for vertex in self.adj: 
            #once we find the entry with our vertex, we add in the edge from src to dest with weight
            if vertex[0] == src: 
                vertex.append([dest, weight])
    def addUndirectedEdge(self, A, B, weight = 1):
        #adds an undirected edge with weight btwn the vertex A and the vertex B
        Graph.addEdge(self, A, B, weight)
        Graph.addEdge(self, B, A, weight)
    def removeEdge(self,src,dest):
        for i in range(len(self.adj)):
            if self.adj[i][0] == src:
                for j in range(1, len(self.adj[i])):
                    if self.adj[i][j][0] == dest:
                        self.adj[i].pop(j)
    def removeUndirectedEdge(self, A, B, weight = 1):
        #remove all undirected edge btwn the vertex A and the vertex B
        Graph.removeEdge(A, B, weight)
        Graph.removeEdge(B, A, weight)
    def __repr__(self):
        return str(self.adj)
    def V(self):
        vertex_list = []
        for i in range(len(self.adj)):
            vertex_list.append(self.adj[i][0])
        return vertex_list
    def E(self):
        edge_list = []
        for i in range(len(self.adj)):
            for j in range(1, len(self.adj[i])):
                edge_list.append([self.adj[i][0], self.adj[i][j][0], self.adj[i][j][1]])
        return edge_list
    def neighbors(self,value):
        #list that holds all the neighbors of value
        neighbors = []
        #for loop to find neighbors
        for i in range(len(self.adj)):#go through each vertex
            if self.adj[i][0] == value:#find the vertex storing the information of value
                for j in range(1, len(self.adj[i])):#find edges of vertex
                    vertex = self.adj[i][j][0] #get edge
                    neighbors.append(vertex)#add to list of neighbors                    
        return neighbors
    def dft(self, src):
        #stack:first in last out
        stack = []
        visited = []#keep track of visited vertices
        ret = []#keep track of outputted vertices
        
        stack.append(src)
        while len(stack) != 0:
            v = stack.pop()
            #check if vertex is in visited
            if v not in visited:
                ret.append(v)
                visited.append(v)
                
                neighbors = sorted(self.neighbors(v), reverse=True)
                
                for n in neighbors:
                    stack.append(n)
        
        return ret
    def bft(self, src):
        #queue:first in first out
        queue = []
        visited = []#keep track of visited vertices
        ret = []#vertices that get returned
        
        queue.append(src)#add starting vertex to queue
        
        while len(queue) != 0:
            v = queue.pop(0)#enforce first in first out property
            #check if vertex is in visited
            if v not in visited:
                ret.append(v)
                visited.append(v)
                
                neighbors = sorted(self.neighbors(v), reverse = False)
                
                for n in neighbors:
                    queue.append(n)
        
        return ret    
    def isDirected(self):
        for i in self.V():
            for j in self.neighbors(i):
                if i not in self.neighbors(j):
                    return True
        
        return False
    def isCyclic(self):
        #helper function to see if node has degree of 0
        def inDegree0(graph, node):
            #go through adj list to see if it contains node
            for _, edgeList in graph.adj.items():
                #see if node appears in edge list
                for dest, _ in edgeList:
                    if node == dest:
                        return False
                    
            return True
        
        if self.isDirected():
            newGraph = Graph()
            #copy so we can remove vertices without messing up orginial graph
            newGraph.adj = copy.deepcopy(self.adj)
        
            while len(newGraph.V()) != 0:
                n = None
            
                #find node which has 0 degree
                for node in newGraph.V():
                    if inDegree0(newGraph, node):
                        n = node
                        break
            
                #if none exists then is cyclic    
                if n == None:
                    return True
            
                #remove it if it has 0 degree
                newGraph.removeVertex(n)
        
            return False
        else:
            stack = []
            visited = []
            parent = {}
            
            src = self.V()[0]
            stack.append(src)
            visited.append(src)
            parent[src] = None
            
            while len(stack) != 0:
                v = stack.pop()
                
                neighbors = self.neighbors(v)
                
                if parent[v] != None:
                    neighbors.remove(parent[v])
                    
                for n in neighbors:
                    if n not in visited:
                        visited.append(n)
                        stack.append(n)
                        
                        parent[n] = v
                    else:
                        return True
                    
            return False
            
                    
    def isConnected(self):
        traverse_list = self.dft(self.V()[0])
        if len(traverse_list) == len(self.V()):
            return True
        else:
            return False
    def isTree(self):
        return not self.isCyclic() and self.isConnected()
    def __repr__(self):
        return str(self.adjacency_list)
