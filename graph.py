from math import sqrt
from queue import Queue
from random import random


class Graph:
    """
    This is a class for testing search algorithms for graphs.

    Class constructor - generates a random KNN Graph.

    Parameters:
            nVertices (int): number of random vertices to be generated.
            nEdges (int): number of edges to be generated from each vertex.
    """

    def __init__(self, nVertices: int, nEdges: int):
        """
        Class constructor - generates a random KNN Graph.

        Parameters:
            nVertices (int): number of random vertices to be generated.
            nEdges (int): number of edges to be generated from each vertex.
        """

        vertices = [ ( nVertices*random(), nVertices*random() ) for _ in range(nVertices) ]
        edges = [ [ 0 for _ in range(nVertices) ] for _ in range(nVertices) ]
        adjacencies = []

        def findClosestVertices(current: tuple) -> list:
            """
            Calculates the vertex that's closest from the current one.

            Parameters:
                current (int): the current vertex' index in the "vertices" list.

            Return value:
                int: the closes vertex' index in the "vertices list".
            """

            # list of distances between all vertices and the current one
            # (does not include the distance with itself)
            distancies = [
                ( i, sqrt((vertex[0] - current[0])**2 + (vertex[1] - current[1])**2) )
                for i, vertex in enumerate(vertices) if vertex != current
            ]

            # sorts by distance
            return sorted(distancies, key=lambda vertex: vertex[1])[0:nEdges]

        for current_index, current_vertex in enumerate(vertices):
            # gets "nEdges" closest vertices
            closest = findClosestVertices(current_vertex)

            # for each of the closest vertices, create an edge between them
            for vertex_index, _ in closest:
                edges[current_index][vertex_index] = edges[vertex_index][current_index] = 1

        for current_vertex, row in enumerate(edges): adjacencies.append({
            "vertex": current_vertex,
            "adjacencies": [ vertex for vertex, hasEdge in enumerate(row) if hasEdge ]
        })

        self.nVertices = nVertices
        self.vertices = vertices
        # self.edges = edges
        self.adjacencies = adjacencies

    def __str__(self) -> str:
        """
        The function to convert a graph into a string of it's adjacency list.

        Return value:
            str: represents the graph's adjacency list.
        """

        string = ''

        for vertex in self.adjacencies:
            string += f'{vertex["vertex"]}: {", ".join(sorted(vertex["adjacencies"]))}\n\n'

        return string

    def getAdjacentVertices(self, index: int):
        """
        The function for getting a vertex's adjacent vertices.

        Parameters:
            index (int): The queried vertex's index.

        Return value:
            list<int>: list of adjacent vertices' index.
        """

        vertexFiltered = [ v for v in self.adjacencies if v["vertex"] == index ]

        return vertexFiltered[0]['adjacencies'] if len(vertexFiltered) else []

    def breadthFirstSearch(self, index: int) -> tuple:
        """
        The function performs a Breadth First Search, returning the list of distances between the vertex at "index" and every other vertex the graph has as well of the list of all visited vertices (in the order they were visited).

        Parameters:
            index (int): The initial vertex's position (index + 1).

        Return value:
            tuple<[int],[int]>: (visitedVertices, distances).

             * visitedVertexes, [ int ]: list containing all of the visited vertices' positions in the order they were visited.
             * distances, [ int ]: list in which the indexes are the vertices' positions - 1 and the values are their distances to the vertex at "index".

            If index is invalid, None will be returned.
        """

        if not (1 <= index <= self.nVertices): return None

        # list of all vertices not yet passed (analyzed)
        white = list(range(1, self.nVertices+1))

        # adjacent vertex to the ones already passed
        # they're queued to be analyzed
        grey = Queue()

        # list of all vertices already passed (analyzed) in order
        black = []

        # starts the distances list as -1 for all vertices
        # (-1 in this case means infinity)
        distances = [ -1 for _ in white ]

        grey.put(index)
        distances[vertexPosition-1] = 0

        # while the queue is not empty
        while grey.qsize():
            black.append(grey.get())

            # gets the vertex currently being analyzed vertex's adjacency list
            adjacencies = self.getAdjacentVertices(black[-1])

            # loops through the currently being analyzed vertex's adjacency list
            for vertex in adjacencies:

                # looks through any adjacent vertices that were not analyzed yet
                if vertex in white:
                    # removes them from the white list
                    white.remove(vertex)

                    # adds them to the grey list
                    grey.put(vertex)

                    # marks their distances as an increment of the currently being analyzed vertex's
                    distances[vertex-1] = distances[black[-1]-1] + 1

        return black, distances
