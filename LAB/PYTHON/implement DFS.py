# DFS function
def dfs(graph, node, visited):
    if node not in visited:
        print(node, end=" ")
        visited.add(node)

        # Visit all neighbors
        for neighbor in graph[node]:
            dfs(graph, neighbor, visited)

# Example graph (Adjacency List)
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

visited = set()

# Start DFS
dfs(graph, 'A', visited)
