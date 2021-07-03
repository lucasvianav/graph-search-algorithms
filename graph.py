from math import dist
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

        # nodes' 2D coordinates (x, y)
        nodes = [ ( nNodes*random(), nNodes*random() ) for _ in range(nNodes) ]

        # adjacency matrix
        # (i rows and j columns are nodes and the [i][j]
        # element is the number of edges between node i and j)
        edges = [ [ 0 for _ in range(nNodes) ] for _ in range(nNodes) ]

        # euclidian distances matrix
        # (i rows and j columns are nodes and the [i][j]
        # element is the distance between node i and j)
        distances = [ [] for _ in range(nNodes) ]

        # wheighted adjacency matrix
        # (i rows and j columns are nodes and the [i][j]
        # element is the wheight of the edge between node i and j)
        # (nonexistant edges are considered to have wheight 0)
        wheighted = [ [ 0 for _ in range(nNodes) ] for _ in range(nNodes) ]

        def euclidianDistance(i: int, j: int):
            """
            Calculates the Euclidian Distance between two nodes.

            Parameters:
                i (int): the node's index in the "nodes" list.
                j (int): the node's index in the "nodes" list.

            return:
                float: the Euclidian Distance between the two nodes.
            """

            return dist(nodes[i], nodes[j])

        # generates the edges and calculates the distances
        for current_index in range(nNodes):
            distances[current_index] = [
                distances[node][current_index] if (node < current_index)
                else euclidianDistance(current_index, node)
                for node in range(nNodes)
            ]

            # "nEdges" closest nodes
            _nodes = [
                ( node, distances[current_index][node] )
                for node in range(nNodes) if node != current_index
            ]
            closest = sorted( _nodes, key=lambda n: n[1])[0:nEdges]

            # for each of the closest nodes, create an edge between them
            for node, distance in closest:
                edges[current_index][node] = edges[node][current_index] = 1
                wheighted[current_index][node] = wheighted[node][current_index] = distance

        # each index is a node (node number) and the value is the list of neighbouring the nodes' indexes
        self.adjacencies = [ [ node for node, hasEdge in enumerate(row) if hasEdge ] for row in edges ]

        # other attributes
        self.nNodes      = nNodes
        self.distances   = distances
        self.wheighted   = wheighted


    # PRIVATE TEMPLATE METHODS

    def __template_first_search(self, search_type: str, root: int, target: int) -> list:
        """
        Performs a Breadth First Search or a Depth First Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            serach_type (str): 'breadth' to perform a Breadth First Search, 'depth' to perform a Depth First Search or 'best' to perform a Best First Search.
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        if search_type not in [ 'breadth', 'depth', 'best' ]: return []

        # list of all paths to be analyzed (the next node to
        # be visited is the last one on each path)
        to_analyze = [[ root ]]

        # list of all nodes already analyzed
        history = []

        # list of the distances between all nodes in to_analyze
        # and the target (only used for Best First Searches)
        distances = [ self.distances[target][root] ] if search_type == 'best' else []

        # while to_analyze is not empty
        while to_analyze:
            # if it's performing a Best First Search, select the node that's closest to the
            # target (aka the node at the same index as the lowest value in distances)
            if search_type == 'best':
                # index of the lowest element in the distances list
                selected_index = distances.index(min(distances))

                # removes it from the list (as the path'll be removed from to_analyze as well)
                distances.pop(selected_index)

            # for DST, make it LIFO
            # fot BST, make FIFO
            else: selected_index = -1 if search_type == 'depth' else 0

            # gets the current path
            path = to_analyze.pop(selected_index)

            # currently being analyzed node
            current = path[-1]

            # gets the current node's adjacency list
            adjacencies = [ node for node in self.adjacencies[current] if node not in history ]

            # if the target is found
            if target in adjacencies: return path + [ target ]

            # appends the current node to the history
            history.append(current)

            # loops through each adjacent node, marking
            # a new path that ends in it to be analyzed
            to_analyze.extend([ path + [ node ] for node in adjacencies ])

            # if it's performing a Best First Search, append distances for adjacent nodes to the list
            if search_type == 'best': distances.extend([ self.distances[target][node] for node in adjacencies ])

        # if it got out of the loop, it means no path was found
        return []

    def __a_search_template(self, root: int, target: int, star: bool = False) -> list:
        """
        The function performs an A or A* algorithm Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        def generateNodeObject(acc_cost: float, path: list) -> dict:
            """
            This function simply generates a dict with that node's relevant info (the path that led to it as well as that path's cost to the target).

            Parameters:
                acc_cost (float): the actual cost accumulated on the current path.
                path (list): the path that led to the current node (it being the last one).

            Return value:
                dict<{"index": int, "score": float, "path": list<int>}>: score is an underguess of the full cost to the target on the current path and path is the same as the argument.
            """

            def heuristic(current_node):
                return self.distances[target][current_node] * ( 1 if star else 10 )

            return { "index": path[-1], "score": heuristic(path[-1]) + acc_cost, "path": path.copy() }

        # list of all paths enqued (the next node to
        # be analyzed is the last one on each path)
        to_analyze = [ generateNodeObject(0, [root]) ]

        # list of all nodes already analyzed
        history = []

        # receives a node dict and checks if it's already on the history
        # or if the current node's score is lower than the history's
        def validateFromHistory(node: dict) -> bool:
            # list containing all times the current node was visited
            filtered_history = [ n for n in history if n['index'] == node['index'] ]

            # the last time this node was visited is the one with the lowest score
            lowest_score_path = filtered_history[-1] if filtered_history else None

            return not bool(lowest_score_path) or lowest_score_path['score'] < node['score']

        # while to_analyze is not empty
        while to_analyze:
            # finds the node yet to be analyzed that has the lowest score
            scores = [ node['score'] for node in to_analyze ]
            best_index = scores.index(min(scores))
            current = to_analyze.pop(best_index)

            # if the target is found, return the path to it
            if target in self.adjacencies[current['index']]: return current['path'] + [ target ]

            # appends the current node to the history
            history.append(current)

            # gets the current node's adjacency list as node dicts
            adjacencies = [
                generateNodeObject(self.distances[current['index']][node], current["path"] + [ node ])
                for node in self.adjacencies[current['index']]
            ]

            # adds the adjacencies nodes to the "to_analyze" list and
            # filters nodes that have a lower score on history
            to_analyze = [ node for node in to_analyze + adjacencies if validateFromHistory(node) ]

        # if it got out of the loop, it means no path was found
        return []



    # ACTUAL SEARCH ALGORITHM PUBLIC METHODS

    def breadthFirstSearch(self, root: int, target: int) -> list:
        """
        The function performs a Breadth First Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        # performs the Breadth First Search
        return self.__template_first_search('breadth', root, target)

    def depthFirstSearch(self, root: int, target: int) -> list:
        """
        The function performs a Depth First Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        # performs the Depth First Search
        return self.__template_first_search('depth', root, target)

    def bestFirstSearch(self, root, target):
        """
        The function performs a Best First Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        # performs the Best First Search
        return self.__template_first_search('best', root, target)

    def aSearch(self, root: int, target: int):
        """
        The function performs an A-Algorithm Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        return self.__a_search_template(root, target)

    def aStarSearch(self, root: int, target: int):
        """
        The function performs an A*-Algorithm Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        return self.__a_search_template(root, target, True)

