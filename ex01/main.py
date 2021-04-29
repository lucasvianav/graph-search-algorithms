from graph_ADT import Graph

# Receives user input and generates the matrix
noVertices = int(input('Insert number of vertices (N): '))
parameter = float(input('Insert the Erdös-Renyi parameter (p): '))
graph = Graph(noVertices, parameter)

print(graph)
print(graph.existsEdge())

vertex = int(input('Select vertex do get it\'s degree: '))

print(graph.getVertexDegree(vertex))