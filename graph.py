from functools import reduce
from os import path
from queue import Queue

class Graph:
    """ This is a class for graphs manipulation, primarily working with it's adjacency list.  """

    def __init__(self, filePath: str) -> list:
        """
        The constructor for the Graph class.

        Parameters:
            filePath (str): The pajek file's path

        Return value:
            Graph, if the passed parameters are valid.
            None, if not.
        """

        # reads the pajek file
        if path.exists(filePath):
            with open(filePath, 'r') as f: lines = f.read().splitlines()

        else: return None
        
        # number of vertices
        N = int(lines[0].replace('*Vertices ', ''))
    
        # deletes the files' header
        lines.pop(0)
        lines.pop(0)
        
        # this function will be used to reduce the "lines" list
        def parseData(acc, cur):
            currentVertex, adjacentVertex = cur.split(' ')

            # parses int from string
            currentVertex = int(currentVertex)
            adjacentVertex = int(adjacentVertex)
            
            # if the current vertex is already listed on the adjacency list,
            # add the current adjacent vertex to it
            if len(acc) and acc[-1]['vertex'] == currentVertex: acc[-1]['adjacencies'].append(adjacentVertex)

            # if it's not, add it to the adjacency list with only the current adjacent vertex
            else: acc.append({ 'vertex': currentVertex, 'adjacencies': [ adjacentVertex ] })
            
            return acc
        
        # the adjacency list will be formated as a list of objects in which each object 
        # has a "vertex" attribute indicating it's position as well a "adjacencies" list 
        # indicating to what other vertex that one is adjacent
        # [ { vertex: int, adjacencies: [ int ] } ]

        self.N = N
        self.adjacencies = reduce(parseData, lines, [])

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

    def getAdjacencyList(self) -> list: 
        """ The getter for the graph's adjacency list.  """
        return self.adjacencies

    def getAdjacentVertices(self, vertexPosition: int):
        """
        The function for getting a vertex's adjacency list.

        Parameters:
            vertexPosition (int): The queried vertex's position (index + 1).

        Return value: 
            [ int ], if vertexPosition is valid (between 1 and self.N).
                List of adjacent vertices' positions (index + 1).
            None, if not.
        """
        if not (1 <= vertexPosition <= self.N): return None

        vertexObject = list(filter(lambda v: v['vertex'] == vertexPosition, self.adjacencies))
        adjacencies = vertexObject[0]['adjacencies'] if len(vertexObject) else []

        return adjacencies

    def breadthFirstSearch(self, vertexPosition: int) -> tuple:
        """
        The function performs a Breadth First Search, returning the list of distances between the vertex at "vertexPosition" and every other vertex the graph has as well of the list of all visited vertices (in the order they were visited).

        Parameters:
            vertexPosition (int): The initial vertex's position (index + 1).

        Return value: 
            tuple, ([int], [int]): (visitedVertices, distances).

             * visitedVertexes, [ int ]: list containing all of the visited vertices' positions in the order they were visited.
             * distances, [ int ]: list in which the indexes are the vertices' positions - 1 and the values are their distances to the vertex at "vertexPosition".
             
            If vertexPosition is invalid, None will be returned.

        """
        if not (1 <= vertexPosition <= self.N): return None

        # list of all vertices not yet passed (analyzed)
        white = list(range(1, self.N+1))

        # adjacent vertex to the ones already passed
        # they're queued to be analyzed
        grey = Queue()
        
        # list of all vertices already passed (analyzed) in order
        black = []
        
        # starts the distances list as -1 for all vertices
        # (-1 in this case means infinity)
        distances = [ -1 for _ in white ]

        grey.put(vertexPosition)
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