from random import randint
from statistics import mean
from time import time

from graph import Graph

no_vertices = [ 500, 5000, 10000 ]
no_edges    = [ 3,   5,    7     ]

OUTPUT_DIR = './output/'
FILENAME = OUTPUT_DIR + str(time()).replace('.','')

data = {
    'breadth': {
        500: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        5000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        10000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        }
    },

    'depth': {
        500: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        5000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        10000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        }
    },

    'best': {
        500: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        5000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        10000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        }
    },

    'a': {
        500: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        5000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        10000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        }
    },

    'a_star': {
        500: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        5000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        },

        10000: {
            3: { 'times': [], 'distances': [] },
            5: { 'times': [], 'distances': [] },
            7: { 'times': [], 'distances': [] }
        }
    }
}

NO_SAMPLES = 10

def avg(algorithm: str, n: int, k: int, list_type: str):
    return mean(data[algorithm][n][k][list_type])

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

            data['breadth'][n][k]['distances'].append(graph.travelledDistance(breadth))
            data['breadth'][n][k]['times'].append(breadth_time)


            # DEPTH FIRST SEARCH
            start_time   = time()
            depth        = graph.depthFirstSearch(root, target)
            depth_time   = time() - start_time

            data['depth'][n][k]['distances'].append(graph.travelledDistance(depth))
            data['depth'][n][k]['times'].append(depth_time)


            # BEST FIRST SEARCH
            start_time   = time()
            best         = graph.bestFirstSearch(root, target)
            best_time    = time() - start_time

            data['best'][n][k]['distances'].append(graph.travelledDistance(best))
            data['best'][n][k]['times'].append(best_time)


            # A ALGORITHM
            start_time   = time()
            a            = graph.aSearch(root, target)
            a_time       = time() - start_time

            data['a'][n][k]['distances'].append(graph.travelledDistance(a))
            data['a'][n][k]['times'].append(a_time)


            # A* ALGORITHM
            start_time   = time()
            a_star       = graph.aStarSearch(root, target)
            a_star_time  = time() - start_time

            data['a_star'][n][k]['distances'].append(graph.travelledDistance(a_star))
            data['a_star'][n][k]['times'].append(a_star_time)

        print(f'###  n = {n}  ###  k = {k}  ###', end='\n\n')

        print(f'Breadth First Search:')
        print(' * Time: %.2es', avg('breadth', n, k, 'times'))
        print(' * Distance: %.2e', avg('breadth', n, k, 'distances'), end='\n\n')

        print(f'Depth First Search:')
        print(' * Time: %.2es', avg('depth', n, k, 'times'))
        print(' * Distance: %.2e', avg('depth', n, k, 'distances'), end='\n\n')

        print(f'Best First Search:')
        print(' * Time: %.2es', avg('best', n, k, 'times'))
        print(' * Distance: %.2e', avg('best', n, k, 'distances'), end='\n\n')

        print(f'A Search:')
        print(' * Time: %.2es', avg('a', n, k, 'times'))
        print(' * Distance: %.2e', avg('a', n, k, 'distances'), end='\n\n')

        print(f'A Star Search:')
        print(' * Time: %.2es', avg('a_star', n, k, 'times'))
        print(' * Distance: %.2e', avg('a_star', n, k, 'distances'), end='\n\n\n\n\n')

