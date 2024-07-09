class Graph:
    def __init__(self):
        self.adj = []
        self.indexToVertex = []
        self.vertex_num = 0
        self.vertices = []
    def addVertex(self, data):
        #Increase the number of vertexes being accounted for
        self.vertex_num = self.vertex_num + 1
        #add new vertex to vertex list
        self.vertices.append(data)
        #add an extra empty slot in vertexes so more can be added
        if self.vertex_num > 1:
            for vertex in self.adj:
                vertex.append(0)
        #increase length of temporary storage
        temp = []
        for i in range(self.vertex_num):
            temp.append(0)
        self.adj.append(temp)
    def addEdge(self, src, dest, weight):
        #add edge by indexing adjacency matrix
        self.adj[self.vertices.index(src)][self.vertices.index(dest)] = weight
    def addUndirectedEdge(self, src, dest, weight):
        #call addEdge to add undirected edge
        Graph.addEdge(self, src, dest, weight)
        Graph.addEdge(self, dest, src, weight)
    def prims(self):
        #Use infinity to act as initial minimum weight in comparison
        infinity = float('inf')
        #Initialize list to show which nodes have already been selected
        selected = [False for node in range(len(self.adj))]
        #Initialize Minimum Spanning Tree Matrix
        MST = [[0 for column in range(len(self.adj))] for y in range(len(self.adj))]
        while (False in selected):
            minimum = infinity
            #Starting and ending nodes
            start, end = 0, 0
            #go through each node and find lowest cost vertices
            for i in range(len(self.adj)):
                #if node part of MST, check vertices
                if selected[i]:
                    for j in range(len(self.adj)):
                        #if node is part of path and not in MST
                        if (not selected[j] and self.adj[i][j]>0):
                            #If vertex weight is less than MST minimum
                            if self.adj[i][j] < minimum:
                                #Put down new minimum weight, starting vertex, and ending vertex
                                minimum = self.adj[i][j]
                                start, end = i, j    
            #add new ending vertex
            selected[end] = True
            #assign newfound minimum weight
            MST[start][end] = minimum
            if minimum == infinity:
                MST[start][end] = 0
                
        #convert adjacency matrix to adjacency list
        MST_list = []
        for i in range(self.vertex_num):
            for j in range(self.vertex_num):   
                if MST[i][j] != 0:
                    MST_list.append([self.vertices[i], self.vertices[j], MST[i][j]])
        
        return MST_list


#Outside functions bc I accidentally coded prims as part of the Graphs class mb
def prim(graph):
    return graph.prims()
            
def runPrim():
    #module to calculate square root
    import math as math
    
    #Dictionary storing coordinate information:
    states = {"Wisconsin, USA": [44.5, -89.5], "West Virginia, USA": [39.0,-80.5], "Vermont, USA": [44.0,-72.699997],
    "Texas, USA": [31.0,-100.0], "South Dakota, US": [44.5,-100.0], "Rhode Island, US": [41.742325, -71.742332],
    "Oregon, US": [44.0,-120.5], "New York, USA": [43.0, -75.0], "New Hampshire, USA": [44.0, -71.5], 
    "Nebraska, USA": [41.5,-100.0]
    }

    #initiate map as part of Graph class
    map = Graph()

    #add cities as vertices
    cities = ['Wisconsin, USA', 'West Virginia, USA', 'Vermont, USA', 'Texas, USA', 'South Dakota, US', 'Rhode Island, US','Oregon, US', 'New York, USA', 'New Hampshire, USA', 'Nebraska, USA']
    for v in cities:
        map.addVertex(v)

    d = {'Wisconsin, USA': 0, 'West Virginia, USA': 1, 'Vermont, USA': 2, 'Texas, USA': 3, 'South Dakota, US': 4, 'Rhode Island, US': 5,'Oregon, US': 6, 'New York, USA': 7, 'New Hampshire, USA': 8, 'Nebraska, USA':9}
    #add edges between every city
    for i in (states):
        for j in list(states.keys())[d[i]+1:len(states)]:
            map.addUndirectedEdge(i, j, math.sqrt(((states[i][0]-states[j][0]) ** 2) + ((states[i][1]-states[j][1]) ** 2)))#distance formula
          
    #run prims algorithm
    return prim(map)
