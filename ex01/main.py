from random import random

# Return a Erdös-Renyi graph's matrix (considering non-directional graphs)
# N if the graph's number of vertices
# p is the Erdös-Renyi parameter
def genErdösRenyiMatrix(N: int, p: float):
    # The lower half of a matrix (excluding the main diagonal) has (N^2-N)/2 elements
    noElements = int((N**2-N)/2)

    elements = [ 0 for _ in range(noElements) ]

    # Populates the matrix's elements
    # No need to do it for the main diagonal because it's gonna be null
    for i in range(2*noElements): elements[i if i < noElements else i-noElements] += 1 if random() > p else 0

    # Generates the symmetrical matrix
    M = [ [ elements[max(i,j)] if i != j else 0 for j in range(N) ] for i in range(N) ]

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