from random import random
from math import comb

# Return a Erdös-Renyi graph's matrix (considering non-directional graphs)
# N if the graph's number of vertices
# p is the Erdös-Renyi parameter
def genErdösRenyiMatrix(N: int, p: float):
    M = [ [ 0 for _ in range(N) ] for _ in range(N) ]
    for i in range(N):
        for j in range(N):
            M[i][j] = M[j][i] = ( int(random() > p) if i > j else M[i][j] )

    return M


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