from random import random
from math import comb

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
        for row in self.matrix:
            if any(x > 0 for x in row): return True

    # def getVertexDegree(self, vertexIndex):
        

# Receives user input and generates the matrix
# noVertices = int(input('Insert number of vertices (N): '))
# parameter = float(input('Insert the Erdös-Renyi parameter (p): '))
# matrix = genErdösRenyiMatrix(noVertices, parameter)