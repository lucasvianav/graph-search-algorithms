from random import randint
from statistics import mean
from time import time

from graph import Graph

no_vertices = [ 500, 5000, 10000 ]
no_edges    = [ 3,   5,    7     ]

OUTPUT_DIR = './output/'
FILENAME = OUTPUT_DIR + str(time()).replace('.','')

data = {
    'breadth': { 'times': [], 'distances': [] },
    'depth': { 'times': [], 'distances': [] },
    'best': { 'times': [], 'distances': [] },
    'a': { 'times': [], 'distances': [] },
    'a_star': { 'times': [], 'distances': [] },
}

NO_SAMPLES = 10

def avg(algorithm: str, list_type: str):
    return mean(data[algorithm][list_type])

for n in no_vertices:
    for k in no_edges:
        graph = Graph(n, k)

        for _ in range(NO_SAMPLES):
            root   = randint(0, n-1)
            target = randint(0, n-1)

            while target == root: target = randint(0, n-1)


            # BREADTH FIRST SEARCH
            start_time   = time()
            breadth      = graph.breadthFirstSearch(root, target)
            breadth_time = time() - start_time

            data['breadth']['distances'].append(graph.travelledDistance(breadth))
            data['breadth']['times'].append(breadth_time)


            # DEPTH FIRST SEARCH
            start_time   = time()
            depth        = graph.depthFirstSearch(root, target)
            depth_time   = time() - start_time

            data['depth']['distances'].append(graph.travelledDistance(depth))
            data['depth']['times'].append(depth_time)


            # BEST FIRST SEARCH
            start_time   = time()
            best         = graph.bestFirstSearch(root, target)
            best_time    = time() - start_time

            data['best']['distances'].append(graph.travelledDistance(best))
            data['best']['times'].append(best_time)


            # A ALGORITHM
            start_time   = time()
            a            = graph.aSearch(root, target)
            a_time       = time() - start_time

            data['a']['distances'].append(graph.travelledDistance(a))
            data['a']['times'].append(a_time)


            # A* ALGORITHM
            start_time   = time()
            a_star       = graph.aStarSearch(root, target)
            a_star_time  = time() - start_time

            data['a_star']['distances'].append(graph.travelledDistance(a_star))
            data['a_star']['times'].append(a_star_time)

        print(f"###  n = {n}  ###  k = {k}  ###", end='\n\n')

        print(f"Breadth First Search:")
        print(f" * Time: {avg('breadth', 'times'):.2e}s")
        print(f" * Distance: {avg('breadth', 'distances'):.2e}", end='\n\n')

        print(f"Depth First Search:")
        print(f" * Time: {avg('depth', 'times'):.2e}s")
        print(f" * Distance: {avg('depth', 'distances'):.2e}", end='\n\n')

        print(f"Best First Search:")
        print(f" * Time: {avg('best', 'times'):.2e}s")
        print(f" * Distance: {avg('best', 'distances'):.2e}", end='\n\n')

        print(f"A Search:")
        print(f" * Time: {avg('a', 'times'):.2e}s")
        print(f" * Distance: {avg('a', 'distances'):.2e}", end='\n\n')

        print(f"A Star Search:")
        print(f" * Time: {avg('a_star', 'times'):.2e}s")
        print(f" * Distance: {avg('a_star', 'distances'):.2e}", end='\n\n\n\n\n')

