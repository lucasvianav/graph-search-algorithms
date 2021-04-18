from random import random

# Return a Erdös-Renyi graph's matrix (considering non-directional graphs)
# N if the graph's number of vertices
# p is the Erdös-Renyi parameter
def genErdösRenyiMatrix(N: int, p: float):
    # Populates the matrix's elements
    # The main diagonal's null
    M = [ [ int(random() > p) if i != j else 0 for j in range(N) ] for i in range(N) ]

    # Unites the number of edges between i and j and between j and i
    return [ [ M[i][j] + M[j][i] for j in range(N) ] for i in range(N) ]


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