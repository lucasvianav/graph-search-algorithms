from random import random
from functools import reduce

class Graph:
    # Generates a Erdös-Renyi graph's matrix (considering non-directional graphs)
    # N if the graph's number of vertices
    # p is the Erdös-Renyi parameter
    def __init__(self, N, p=None):
        M = [ [ 0 for _ in range(N) ] for _ in range(N) ]

        if p != None:
            for i in range(N):
                for j in range(N):
                    M[i][j] = M[j][i] = ( int(random() > p) if i > j else M[i][j] )

        self.N = N
        self.p = p
        self.matrix = M
        
    def __str__(self) -> str:
        string = ''

        for i in range(self.N):
            string += '[  '
            for j in range(self.N): string += str(self.matrix[i][j]) + '  '
            string += ']\n'
            
        return string
        
    def getMatrix(self): return self.matrix
    
    def existsEdge(self):
        # If an edge is found in any row
        # returns True
        for row in self.matrix:
            if any(x > 0 for x in row): return True
            
        # If no edge is found, returns False
        return False

    def getVertexDegree(self, vertexIndex):
        # Sums all edges from the vertex's row
        return reduce(lambda acc, cur: acc+cur, self.matrix[vertexIndex], 0) if vertexIndex < len(self.matrix) else None

# Receives user input and generates the matrix
noVertices = int(input('Insert number of vertices (N): '))
parameter = float(input('Insert the Erdös-Renyi parameter (p): '))
graph = Graph(noVertices, parameter)

print(graph)
print(graph.existsEdge())

vertex = int(input('Select vertex do get it\'s degree: '))

print(graph.getVertexDegree(vertex))