from math import dist
from random import random


class ASearchStructNode:
    def __init__(self, heuristic: float, cost_of_path: int, id: int, path: list):
        self.score = heuristic + cost_of_path
        # heuristic = underguess of how much would take to get to the objective
        self.heuristic = heuristic
        # cost_of_path = total cost until getting to the node
        self.cost_of_path = cost_of_path
        # id = id of the node
        self.id = id
        # path_to_node records the path until reaching the node, list(path) to clone the list so that modifying the first do not affect the list on the node
        self.path_to_node = list(path)

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

    # private method
    def __breadth_depth_search_template(self, breadthFirst: bool, root: int, target: int) -> list:
        """
        Performs a Breadth First Search or a Depth First Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            beadthFirst (bool): true to perform a Breadth First Search, false to perform a Depth First Search.
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        # list of all paths enqued (the next node to
        # be analyzed is the last one on each path)
        to_analyze = [[ root ]]

        # list of all nodes already analyzed
        history = []

        # while to_analyze is not empty
        while to_analyze:
            # gets the current path
            path = to_analyze.pop(0 if breadthFirst else -1)

            # currently being analyzed node
            current = path[-1]

            # appends the current node to the history
            history.append(current)

            # gets the current node's adjacency list
            adjacencies = [ node for node in self.adjacencies[current] if node not in history ]

            # if the target is found
            if target in adjacencies: return path + [ target ]

            # loops through each adjacent node, marking
            # a new path that ends in it to be analyzed
            to_analyze.extend([ path + [ node ] for node in adjacencies ])

        # if it got out of the loop, it means no path was found
        return []

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
        return self.__breadth_depth_search_template(True, root, target)

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
        return self.__breadth_depth_search_template(False, root, target)



    # removes nodes that were found 2 times but have different scores, maintaining the one with least score
    def __remove_dup_leaf(self, start, leaves):
        for i in range(start, len(leaves)):
            for j in range(i+1, len(leaves)):
                if leaves[i].id == leaves[j].id:
                    if leaves[i].score > leaves[j].score:
                        leaves.pop(i)
                    else:
                        leaves.pop(j)
                    return self.__remove_dup_leaf(i, leaves)
        return leaves


    def __node_in_path(self, node: int, path: list):
        for i in range(len(path)):
            if node == path[i].id:
                return True
        return False

    def __remove_leaf(self, leaf: list, leaves: list):
        for i in range(len(leaves)):
            if leaves[i].id == leaf.id:
                leaves.pop(i)
                return leaves
        return leaves

    def ASearch(self, root: int, target: int, asterisk: bool) -> list:
        """
        The function performs an A or A* algorithm Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """
        path = []
        # leaves are all the leaves of the tree
        leaves = []
        # initializes the root node
        root_node = ASearchStructNode(0, 0, root, path)
        path.append(root_node)
        while path[-1].id != target:
            parent_node = path[-1]
            # expands the leaves of the tree
            for i in self.adjacencies[parent_node.id-1]: # -1 because is array pos
                if not self.__node_in_path(i, path):
                    if asterisk: # if its the A* algorithm, the euclidian distance will be used
                        # finds the euclidian distance between the current node and the target
                        heuristic = self.euclidian_distances[i-1][target-1]
                    else:       # if its the A algorithm
                        # finds the manhattan distance between the current node and the target
                        heuristic = self.manhattan_distances[i-1][target-1]
                    # creates the leaf node
                    leaf = ASearchStructNode(heuristic, len(path), i, path)
                    leaves.append(leaf)

            # remove duplicated nodes that were found on different paths
            leaves = self.__remove_dup_leaf(0, leaves)

            # choosing the leaf with the least score
            leaf_to_expand = leaves[0]
            smallest_score = leaves[0].score
            for leaf in leaves:
                if leaf.score < smallest_score:
                    smallest_score = leaf.score
                    leaf_to_expand = leaf
            # updating the path to the one of the current leaf
            path = leaf_to_expand.path_to_node

            # adding the leaf to the path
            path.append(leaf_to_expand)

            # removing the now visited ex-leaf
            leaves = self.__remove_leaf(leaf_to_expand, leaves)

        # path_of_ids is the path with the numbers of the nod and not the class A_search_struct_node
        path_of_ids = []
        for node in path:
            path_of_ids.append(node.id)
        return path_of_ids

    def BestFirstSearch(self, root, target):
        """
        The function performs a Best First Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        to_analyze   = [ root ]
        history = []

        # while to_analyze is not empty
        while to_analyze:

            # if all nodes were analyzed and the target was not found
            if not to_analyze: return []

            # closest node to the target that's yet to be analyzed's index
            # it's the node that have the lowest euclidian distance
            closest_node_index = to_analyze.index(min([ self.euclidian_distances[target][node] for node in to_analyze ]))

            # closest node to the target that's yet to be analyzed
            # (it's the one most likely be on the best path)
            closest_node       = to_analyze[closest_node_index]

            if closest_node not in history: history.append(closest_node)
            to_analyze.remove(closest_node)

            # gets the current node's adjacency list
            adjacencies = [ node for node in self.adjacencies[closest_node] if node not in history ]

            # if the target is found
            if target in adjacencies: return history + [ target ]

            to_analyze.extend(adjacencies)

        # if it got out of the loop, it means no path was found
        return []

