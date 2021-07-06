from math import dist
from random import random

import matplotlib.pyplot as plt
import networkx as nx


class Graph(nx.Graph):
    """
    This is a class for testing and visualizing Graph search algorithms. It extends the NetworkX Graph class.

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

        # initializes a networkx graph
        super().__init__()

        # nodes' 2D coordinates (x, y)
        coordinates = [ ( nNodes*random(), nNodes*random() ) for _ in range(nNodes) ]

        # adds nodes in the generated coordinates to the graph
        self.add_nodes_from([ ( i, { "pos": coordinates[i] } ) for i in range(nNodes) ])

        # euclidian distances matrix
        # (i rows and j columns are nodes and the [i][j]
        # element is the distance between node i and j)
        distances = [ [ 0. ] for _ in range(nNodes) ]

        def euclidianDistance(i: int, j: int):
            """
            Calculates the Euclidian Distance between two nodes.

            Parameters:
                i (int): the node's index in the "nodes" list.
                j (int): the node's index in the "nodes" list.

            return:
                float: the Euclidian Distance between the two nodes.
            """

            return dist(coordinates[i], coordinates[j])

        # generates the edges and calculates the distances
        for current_index in range(nNodes):
            # euclidian distances between the current node and all others
            distances[current_index] = [
                euclidianDistance(current_index, node) if node >= current_index
                else distances[node][current_index] for node in range(nNodes)
            ]

            # list of tuples for all nodes except the current one
            # ( current_node_index, node_index, distance between both )
            nodes = [
                ( current_index, node, distances[current_index][node] )
                for node in range(nNodes) if node != current_index
            ]

            # the node that's the farthest from the current one
            # ( in the "closest" list, see below )
            farthest_node = max(nodes, key=lambda n: n[2])

            # list of the closest "nEdges" from the current one
            # (initialized with only the farthest one, "nEdges" times)
            closest = [ farthest_node ] * nEdges

            # selects only the "nEdges" closest nodes from the
            # current one (it's cheaper than sorting the "nodes"
            # list and selecting the first "nEdges" elements)
            for node in nodes:
                # if this node is closer than the farthest node in
                # the "closest" list, then insert it in it's place
                if node[2] < farthest_node[2]:
                    closest[closest.index(farthest_node)] = node

                    # selects the new farthest node in "closest"
                    farthest_node = max(closest, key=lambda n: n[2])

            # creates edges between the selected nodes and the current
            # one (also register the distance between them as edge weight)
            self.add_weighted_edges_from(closest, 'distance')

        self.distances = distances
        self.nEdges = nEdges

    def plot(self, filename: str, path: list = [], edge_labels: bool = False, show: bool = False) -> None:
        """
        Plots the graph.

        Parameters:
            filename (str): the filename with which to save the figure (.pdf will be included).
            path (list<int>): path to highlight.
            edge_labels (bool): if the distances should be displayed as edge labels.
            show (bool): if the figure should be shown after saving to pdf.
        """

        # sets matplotlib axes and title
        _, ax = plt.subplots(figsize=(60,60))
        ax.set(xlabel='x', ylabel='y', title=f'KNN Graph | n = {self.order()} | k = {self.nEdges}')

        # nodes' coordiates
        position = nx.get_node_attributes(self, 'pos')

        # draws the nodes (with labels) and edges
        nx.draw_networkx(self, position, arrows=False, with_labels=True, node_size=900, ax=ax)

        # if edge_labels is enabled
        if edge_labels:
            # edge weights (distances)
            labels = nx.get_edge_attributes(self, 'distance')

            # draws the labels
            nx.draw_networkx_edge_labels(self, position, edge_labels=labels)

        if path:
            edges = [ ( path[i], path[i+1] ) for i in range(len(path)-1) ]
            nx.draw_networkx_nodes(self, position, nodelist=path, node_color='r', node_size=900, edgecolors='black', ax=ax)
            nx.draw_networkx_edges(self, position, edgelist=edges, edge_color='r', width=10, ax=ax)

        # displays x and y values
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

        # saves the fig to pdf
        plt.savefig(filename + '.pdf')

        # shows the figure if set
        if show: plt.show()

        # cleaning up all figures
        plt.close('all')

    def travelledDistance(self, path: list) -> float:
        """
        Calculates the distance travelled in a given path.

        Parameters:
            path (list<int>): path for which the distance is to be calculated.

        Return value:
            float: distance travelled.
        """

        travelled = 0.

        for i in range(len(path)-1): travelled += self.distances[path[i]][path[i+1]]

        return travelled


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

            # if the current node was already analyzed, go to the next
            if current in history: continue

            # gets the current node's adjacency list
            adjacencies = [ node for node in self.neighbors(current) if node not in history ]

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

            return { "index": path[-1], "score": heuristic(path[-1]) + acc_cost, "path": path.copy(), "acc_cost": acc_cost }

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

            return not bool(lowest_score_path) or (lowest_score_path['score'] > node['score'])

        # while to_analyze is not empty
        while to_analyze:
            # finds the node yet to be analyzed that has the lowest score
            scores = [ node['score'] for node in to_analyze ]
            best_index = scores.index(min(scores))
            current = to_analyze.pop(best_index)

            adjacencies = [ node for node in self.neighbors(current['index']) ]

            # if the target is found, return the path to it
            if target in adjacencies: return current['path'] + [ target ]

            # appends the current node to the history
            history.append(current)

            # gets the current node's adjacency list as node dicts
            adjacencies = [
                generateNodeObject(self.distances[current['index']][node] + current['acc_cost'],
                                   current["path"] + [ node ])
                for node in adjacencies
            ]

            # adds the adjacencies nodes to the "to_analyze" list and
            # filters nodes that have a lower score on history
            to_analyze = [ node for node in (to_analyze + adjacencies) if validateFromHistory(node) ]

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

        return self.__a_search_template(root, target, star=False)

    def aStarSearch(self, root: int, target: int):
        """
        The function performs an A*-Algorithm Search, returning the path that links the "root" node to the "target" node.

        Parameters:
            root (int): the initial node's index.
            target (int): the target node's index.

        Return value:
            list<int>: path starting at "root" and ending at "target".
        """

        return self.__a_search_template(root, target, star=True)

