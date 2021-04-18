from random import random
from math import comb

# Return a Erdös-Renyi graph's matrix (considering non-directional graphs)
# N if the graph's number of vertices
# p is the Erdös-Renyi parameter
def genErdösRenyiMatrix(N: int, p: float):
    # The max number of edges is a combination between N and 2
    maxNoEdges = comb(N, 2)
    edges = [ int(random() > p) for _ in range(maxNoEdges) ]
    
    # The main diagonal is null
    return [ [ edges[i+j] if i != j else 0 for j in range(N) ] for i in range(N) ]


# Receives user input and generates the matrix
noVertices = int(input('Insert number of vertices (N): '))
parameter = float(input('Insert the Erdös-Renyi parameter (p): '))
matrix = genErdösRenyiMatrix(noVertices, parameter)

# Prints the matrix
for i in range(noVertices):
    print('[', end='  ')
    for j in range(noVertices):
        print(matrix[i][j], end='  ')
    print(']')