
from random import random
from functools import reduce

class Graph:
    # N if the graph's number of vertices
    # p is the Erdös-Renyi parameter
    # M is a graph's matrix (will be used if no p is given)
    def __init__(self, N: int, p=None, M=None):
        M = [ [ 0 for _ in range(N) ] for _ in range(N) ]

        # if p is passed, generates an Erdös-Renyi adjacency matrix (considering non-directional graphs)
        if p != None:
            for i in range(N):
                for j in range(N):
                    M[i][j] = M[j][i] = ( int(random() > p) if i > j else M[i][j] )
                    
        # if p is not passed and either M is not passed or is passed but invalid, returns None
        elif not M or len(M) != N or any(len(row) != N for row in M): return None

        # if everything is ok, store the data
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

    # checks if the graph has at least one edge
    def hasEdge(self):
        # If an edge is found in any row
        # returns True
        for row in self.matrix:
            if any(x > 0 for x in row): return True

        # If no edge is found, returns False
        return False

    # returns the vertex's degree
    def getVertexDegree(self, vertexPosition: int):
        # Sums all edges from the vertex's row
        return reduce(lambda acc, cur: acc+cur, self.matrix[vertexPosition-1], 0) if 1 <= vertexPosition <= self.N else None
    
    # returns the vertex's list of adjacent vertices
    def getAdjacentVertices(self, vertexPosition: int):
        return list(filter(
            # filter list for indexes
            lambda e: e != None, 
            
            # generates list of indexes (for the adjacent vertices) and None for the non-adjacent vertices
            [ vertex+1 if isAdjacent else None for vertex, isAdjacent in enumerate(self.matrix[vertexPosition-1]) ]
        )) if 1 <= vertexPosition <= self.N else None

    # returns the vertex's degree and list of adjacency
    def getVertexInfo(self, vertexPosition: int):
        return self.getVertexDegree(self, vertexPosition), self.getAdjacentVertices(vertexPosition) if 1 <= vertexPosition <= self.N else None

    # checks if the vertex in position i is adjacent to the vertex in position j
    # (checks if there is at least an edge between the two vertices)
    # returns None if either i or j is invalid
    def areAdjacents(self, i: int, j: int):
        return bool(self.matrix[i-1][j-1] or self.matrix[j-1][i-1]) if 1 <= i <= self.N and 1 <= j <= self.N else None