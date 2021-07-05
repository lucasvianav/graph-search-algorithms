from random import randint
from time import time

from graph import Graph

# no_vertices = [ 500 ]
no_vertices = [ 500, 5000, 10000 ]
no_edges    = [ 3,   5,    7     ]

filename = './output/' + str(time()).replace('.','')

with open(filename + '.out', 'w') as f:
    for n in no_vertices:
        root   = randint(0, n-1)
        target = randint(0, n-1)

        for k in no_edges:
            graph = Graph(n, k)

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

            f.write(f'\n\n\n\n###  n = {n}  ###  k = {k}  ### root = {root}  ###  target = {target}  ###\n')
            f.write(f'Breadth First Search: {breadth_time}s\n')
            f.write(str(breadth) + '\n\n')
            f.write(f'Depth First Search: {depth_time}s\n')
            f.write(str(depth) + '\n\n')
            f.write(f'Best First Search: {best_time}s\n')
            f.write(str(best) + '\n\n')
            f.write(f'A Search: {a_time}s\n')
            f.write(str(a) + '\n\n')
            f.write(f'A Star Search: {a_star_time}s\n')
            f.write(str(a_star) + '\n\n')


            print(f'\n\n\n\n###  n = {n}  ###  k = {k}  ### root = {root}  ###  target = {target}  ###\n')
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

            graph.plot(filename + '-breadth' , breadth)
            graph.plot(filename + '-depth'   , depth)
            graph.plot(filename + '-best'    , best)
            graph.plot(filename + '-a'       , a)
            graph.plot(filename + '-a_star'  , a_star)

