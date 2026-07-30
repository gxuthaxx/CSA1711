from collections import deque

# BFS function
def bfs(graph, start):
    visited = set()          # To track visited nodes
    queue = deque([start])   # Queue for BFS

    visited.add(start)

    while queue:
        node = queue.popleft()   # Remove from front
        print(node, end=" ")

        # Visit all neighbors
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# Example graph (Adjacency List)
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# Start BFS
bfs(graph, 'A')
