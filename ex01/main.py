from graph_ADT import Graph

# receives user input
noVertices = int(input('### Insert number of vertices (N): '))
parameter = float(input('### Insert the Erdös-Renyi parameter (p): '))

# generates and prints the graph's matrixh
graph = Graph(noVertices, parameter)
print(f'\n{graph}')

# receives user input and prints the vertex's info (degree + adjacent vertices)
vertex = int(input('### Select vertex to analyze: '))
degree, adjacent = graph.getVertexInfo(vertex)
print(f'\nVertex degree: {degree}\nAdjacent vertices: {", ".join(map(lambda e: str(e), adjacent))}')