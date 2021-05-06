
from random import random
from functools import reduce

class Graph:
    """ This is a class for graphs manipulation, primarily working with it's adjacency matrix.  """

    def __init__(self, N: int, p=None, M=None):
        """
        The constructor for the Graph class.

        If p is passed, an Erdös-Renyi matrix is used. Else, M will be used.

        Parameters:
            N (int): The graph's number of vertices.
            p (float, default None): The Erdös-Renyi parameter.
            M ([ [ int ] ], default None): The graph's adjacency matrix.

        Return value:
            Graph, if the passed parameters are valid.
            None, if not.
        """

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
        """
        The function to convert a graph into a string of it's adjacency matrix.

        Return value:
            str: represents the graph's adjacency matrix.
        """

        string = ''

        for i in range(self.N):
            string += '[  '
            for j in range(self.N): string += str(self.matrix[i][j]) + '  '
            string += ']\n'

        return string

    def getMatrix(self): 
        """ The getter for the graph's adjacency matrix.  """
        return self.matrix

    def hasEdge(self) -> bool:
        """
        The function for checking if the graph has at least one edge.

        Return value: 
            bool, if vertexPosition is valid (between 1 and self.N).
            None, if not.
        """


        # If an edge is found in any row
        # returns True
        for row in self.matrix:
            if any(x > 0 for x in row): return True

        # If no edge is found, returns False
        return False

    def getVertexDegree(self, vertexPosition: int) -> int:
        """
        The function for checking a vertex's degree.

        Parameters:
            vertexPosition (int): The queried vertex's position (index + 1).

        Return value: 
            int, if vertexPosition is valid (between 1 and self.N).
            None, if not.

        """

        # Sums all edges from the vertex's row
        return reduce(lambda acc, cur: acc+cur, self.matrix[vertexPosition-1], 0) if 1 <= vertexPosition <= self.N else None
    
    def getAdjacentVertices(self, vertexPosition: int):
        """
        The function for getting a vertex's list of adjacent vertices.

        Parameters:
            vertexPosition (int): The queried vertex's position (index + 1).

        Return value: 
            [ int ], if vertexPosition is valid (between 1 and self.N).
                List of adjacent vertices' positions (index + 1).
            None, if not.
        """

        return list(filter(
            # filter list for indexes
            lambda e: e != None, 
            
            # generates list of indexes+1 (for the adjacent vertices) and None for the non-adjacent vertices
            [ vertex+1 if isAdjacent else None for vertex, isAdjacent in enumerate(self.matrix[vertexPosition-1]) ]
        )) if 1 <= vertexPosition <= self.N else None

    def getVertexInfo(self, vertexPosition: int):
        """
        The function for getting both a vertex's degree and it's list of adjacent vertices.

        Parameters:
            vertexPosition (int): The queried vertex's position (index + 1).

        Return value:
            ( int, [ int ] ), if vertexPosition is valid (between 1 and self.N).
                Represents the vertex degree and it's list of adjacent vertices' positions (index + 1), respectively.
            None, if not.
        """

        return self.getVertexDegree(self, vertexPosition), self.getAdjacentVertices(vertexPosition) if 1 <= vertexPosition <= self.N else None

    def areAdjacent(self, i: int, j: int) -> bool:
        """
        The function for checking if two vertices are adjacent (e.g.: if there is at least an edge between them).

        Parameters:
            i (int): The first queried vertex's position (index + 1).
            j (int): The second queried vertex's position (index + 1).

        Return value: 
            bool, if i and j are valid (between 1 and self.N).
            None, if not.
        """

        return bool(self.matrix[i-1][j-1] or self.matrix[j-1][i-1]) if 1 <= i <= self.N and 1 <= j <= self.N else None