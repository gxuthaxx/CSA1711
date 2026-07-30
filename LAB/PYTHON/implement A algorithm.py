import heapq

def a_star(graph, heuristic, start, goal):
    # Priority queue (min-heap)
    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {}   # To store path
    g_cost = {node: float('inf') for node in graph}
    g_cost[start] = 0

    while open_list:
        _, current = heapq.heappop(open_list)

        # Goal check
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        # Explore neighbors
        for neighbor, cost in graph[current].items():
            new_g = g_cost[current] + cost

            if new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                f = new_g + heuristic[neighbor]
                heapq.heappush(open_list, (f, neighbor))
                came_from[neighbor] = current

    return None


# Example graph
graph = {
    'A': {'B': 1, 'C': 3},
    'B': {'D': 3, 'E': 1},
    'C': {'F': 5},
    'D': {},
    'E': {'F': 1},
    'F': {}
}

# Heuristic values (estimated cost to goal F)
heuristic = {
    'A': 5,
    'B': 3,
    'C': 4,
    'D': 2,
    'E': 1,
    'F': 0
}

# Run A*
path = a_star(graph, heuristic, 'A', 'F')

print("Shortest Path:", path)
