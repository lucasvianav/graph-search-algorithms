from random import randint
from time import time

from graph import Graph

no_vertices = [ 500, 5000, 10000 ]
no_edges    = [ 3,   5,    7     ]

for n in no_vertices:
    for k in no_edges:
        graph = Graph(n, k)

        root   = randint(0, n-1)
        target = randint(0, n-1)

        while target == root: target = randint(0, n-1)

        start_time   = time()
        breadth      = graph.breadthFirstSearch(root, target)
        breadth_time = time() - start_time

        start_time   = time()
        depth        = graph.depthFirstSearch(root, target)
        depth_time   = time() - start_time

        start_time   = time()
        best         = graph.bestFirstSearch(root, target)
        best_time    = time() - start_time

        start_time   = time()
        a            = graph.aSearch(root, target)
        a_time       = time() - start_time

        start_time   = time()
        a_star       = graph.aStarSearch(root, target)
        a_star_time  = time() - start_time

        print(f'\n\n\n\n   ###  n = {n}  ###  k = {k}  ###')
        print(f'  ### root = {root}  ###  target = {target}  ###\n')

        print(f'Breadth First Search: {breadth_time}s')
        print(breadth, end='\n\n')

        print(f'Depth First Search: {depth_time}s')
        print(depth, end='\n\n')

        print(f'Best First Search: {best_time}s')
        print(best, end='\n\n')

        print(f'A Search: {a_time}s')
        print(a, end='\n\n')

        print(f'A Star Search: {a_star_time}s')
        print(a_star, end='\n\n')

