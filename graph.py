from math import sqrt
from random import random


class Graph:
    """
    This is a class for testing search algorithms for graphs.

    Class constructor - generates a random KNN Graph.

    Parameters:
            nNodes (int): number of random nodes to be generated.
            nEdges (int): number of edges to be generated from each node.
    """

    def __init__(self, nNodes: int, nEdges: int):
        """
        Class constructor - generates a random KNN Graph.

        Parameters:
            nNodes (int): number of random nodes to be generated.
            nEdges (int): number of edges to be generated from each node.
        """

        nodes = [ ( nNodes*random(), nNodes*random() ) for _ in range(nNodes) ]
        edges = [ [ 0 for _ in range(nNodes) ] for _ in range(nNodes) ]

        def findClosestNodes(current: tuple) -> list:
            """
            Calculates the node that's closest from the current one.

            Parameters:
                current (int): the current node' index in the "nodes" list.

            Return value:
                int: the closes node' index in the "nodes list".
            """

            # list of distances between all nodes and the current one
            # (does not include the distance with itself)
            distancies = [
                ( i, sqrt((node[0] - current[0])**2 + (node[1] - current[1])**2) )
                for i, node in enumerate(nodes) if node != current
            ]

            # sorts by distance
            return sorted(distancies, key=lambda node: node[1])[0:nEdges]

        for current_index, current_node in enumerate(nodes):
            # gets "nEdges" closest nodes
            closest = findClosestNodes(current_node)

            # for each of the closest nodes, create an edge between them
            for node_index, _ in closest:
                edges[current_index][node_index] = edges[node_index][current_index] = 1

        self.nNodes = nNodes
        self.nodes = nodes
        self.adjacencies = [ [ node for node, hasEdge in enumerate(row) if hasEdge ] for row in edges ]
        self.edges = edges

    def breadthFirstSearch(self, root: int, target: int) -> list:
        """
        The function performs a Breadth First Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): The initial node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        # list of all paths enqued (the next node to
        # be analyzed is the last one on each path)
        # queue --> FIFO
        queue = [[ root ]]

        # list of all nodes already analyzed
        history = []

        # while the queue is not empty
        while queue:
            # gets the current path
            path = queue.pop(0)

            # currently being analyzed node
            current = path[-1]

            # appends the current node to the history
            history.append(current)

            # gets the current node's adjacency list
            adjacencies = [ node for node in self.adjacencies[current] if node not in history ]

            # if the target is found
            if target in adjacencies: return path + [ target ]

            # loops through each adjacent node,
            # enqueuing a new path that ends in it
            queue.extend([ path + [ node ] for node in adjacencies ])

        # if it got out of the loop, it means no path was found
        return []

    def depthFirstSearch(self, root: int, target: int) -> list:
        """
        The function performs a Depth First Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): The initial node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        # list of all paths enqued (the next node to
        # be analyzed is the last one on each path)
        # stack --> LIFO
        stack = [[ root ]]

        # list of all nodes already analyzed
        history = []

        # while the stack is not empty
        while stack:
            # gets the current path
            path = stack.pop()

            # currently being analyzed node
            current = path[-1]

            # appends the current node to the history
            history.append(current)

            # gets the current node's adjacency list (excluding nodes that were already analyzed)
            adjacencies = [ node for node in self.adjacencies[current] if node not in history ]

            # if the target is found
            if target in adjacencies: return path + [ target ]

            # loops through each adjacent node,
            # stacking a new path that ends in it
            stack.extend([ path + [ node ] for node in adjacencies ])

        # if it got out of the loop, it means no path was found
        return []

