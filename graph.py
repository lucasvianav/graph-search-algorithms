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
        # element is the number of edjes between node i and j)
        edges               = [ [ 0 for _ in range(nNodes) ] for _ in range(nNodes) ]

        # distances matrix
        # (i rows and j columns are nodes and the [i][j]
        # element is the distance between node i and j)
        euclidian_distances = [ [] for _ in range(nNodes) ]
        manhattan_distances = [ [] for _ in range(nNodes) ]

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

        def manhattanDistance(i: int, j: int):
            """
            Calculates the Manhattan Distance between two nodes.

            Parameters:
                i (int): the node's index in the "nodes" list.
                j (int): the node's index in the "nodes" list.

            return:
                float: the Manhattan Distance between the two nodes.
            """

            # nodes[a][0] -> x coordenate of a
            # nodes[a][1] -> y coordenate of a
            return abs(nodes[i][0] - nodes[j][0]) + abs(nodes[i][1] - nodes[j][1])

        # generates the edges and calculates the distances
        for current_index in range(nNodes):
            euclidian_distances[current_index] = [
                euclidian_distances[node][current_index] if (node < current_index)
                else euclidianDistance(current_index, node)
                for node in range(nNodes)
            ]

            manhattan_distances[current_index] = [
                manhattan_distances[node][current_index] if (node < current_index)
                else manhattanDistance(current_index, node)
                for node in range(nNodes)
            ]

            # "nEdges" closest nodes
            _nodes = [
                ( node, euclidian_distances[current_index][node] )
                for node in range(nNodes) if node != current_index
            ]
            closest = sorted( _nodes, key=lambda n: n[1])[0:nEdges]

            # for each of the closest nodes, create an edge between them
            for node_index, _ in closest:
                edges[current_index][node_index] = edges[node_index][current_index] = 1

        # each index is a node (node number) and the value is the list of neighbouring the nodes' indexes
        self.adjacencies = [ [ node for node, hasEdge in enumerate(row) if hasEdge ] for row in edges ]

        self.nNodes              = nNodes
        self.euclidian_distances = euclidian_distances
        self.manhattan_distances = manhattan_distances


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

        # list of all paths enqued (the next node to
        # be analyzed is the last one on each path)
        to_analyze = [[ root ]]

        # list of all nodes already analyzed
        history = []

        # while to_analyze is not empty
        while to_analyze:
            # gets the current path
            path = to_analyze.pop(0 if search_type == 'breadth' else -1)

            # currently being analyzed node
            current = path[-1]

            # appends the current node to the history
            history.append(current)

            # gets the current node's adjacency list
            adjacencies = [ node for node in self.adjacencies[current] if node not in history ]

            # if the target is found
            if target in adjacencies: return path + [ target ]

            # sorts adjacency list from closest to farthest node
            # (only if it's performing a Best First Search)
            if search_type == 'best':
                adjacencies.sort(key=lambda node: self.euclidian_distances[current][node])

            # loops through each adjacent node, marking
            # a new path that ends in it to be analyzed
            to_analyze.extend([ path + [ node ] for node in adjacencies ])

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
                return self.euclidian_distances[target][current_node] if star else self.manhattan_distances[target][current_node]

            return { "index": path[-1], "score": heuristic(path[-1]) + acc_cost, "path": path.copy() }

        # list of all paths enqued (the next node to
        # be analyzed is the last one on each path)
        to_analyze = [ generateNodeObject(0, [root]) ]

        # list of all nodes already analyzed
        history = []

        # receives a node dict and checks if it's already on the history
        # or if the current node's score is lower than the history's
        def validateFromHistory(node: dict) -> bool:
            filtered_history = [ n for n in history if n['index'] == node['index'] ]
            found_in_history = filtered_history[0] if filtered_history else None

            return not bool(found_in_history) or found_in_history['score'] < node['score']

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
                generateNodeObject(self.euclidian_distances[current['index']][node], current["path"] + [ node ])
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

