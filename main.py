import time

from graph import Graph

v = [500, 5000, 10000]
k = [3, 5, 7]
paths = [[[] for _ in range(5)] for _ in range(9)]
times = [[0 for _ in range(5)] for _ in range(9)]
i = 0
names = ["Breadth", "Depth", "A", "A*", "Best first"]
for nodes in v:
    for edges in k:
        grafo = Graph(nodes, edges)
        start_time = time.time()
        paths[0][i] = grafo.breadthFirstSearch(1, nodes)
        times[0][i] = time.time() - start_time
        print(f"done {names[i]} {nodes} {edges}\n")
        start_time = time.time()
        paths[1][i] = grafo.depthFirstSearch(1, nodes)
        times[1][i] = time.time() - start_time
        print(f"done depth {nodes} {edges}\n")
        start_time = time.time()
        paths[2][i] = grafo.ASearch(1, nodes, False)
        times[2][i] = time.time() - start_time
        print(f"done A {nodes} {edges}\n")
        start_time = time.time()
        paths[3][i] = grafo.ASearch(1, nodes, True)
        times[3][i] = time.time() - start_time
        print(f"done A* {nodes} {edges}\n")
        start_time = time.time()
        paths[4][i] = grafo.BestFirstSearch(1, nodes)
        times[4][i] = time.time() - start_time
        print(f"done Best First {nodes} {edges}\n")
        i += 1
i = 0
for i in range(len(names)):
    for nodes in v:
        for edges in k:
            print(f"{names[i]} Search:\n"
                  f"v = {nodes} k = {edges}\n"
                  f"path: {paths[0][i]}\n"
                  f"time: {times[0][i]}\n")
            i += 1
