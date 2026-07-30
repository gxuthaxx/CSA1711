from itertools import permutations

def tsp(graph, start):
    cities = list(graph.keys())
    cities.remove(start)

    min_cost = float('inf')
    best_path = None

    # Generate all possible paths
    for perm in permutations(cities):
        current_cost = 0
        current_city = start

        # Calculate cost of this path
        for city in perm:
            current_cost += graph[current_city][city]
            current_city = city

        # Return to start
        current_cost += graph[current_city][start]

        # Update minimum cost
        if current_cost < min_cost:
            min_cost = current_cost
            best_path = (start,) + perm + (start,)

    return min_cost, best_path


# Example graph (cost matrix)
graph = {
    'A': {'A':0, 'B':10, 'C':15, 'D':20},
    'B': {'A':10, 'B':0, 'C':35, 'D':25},
    'C': {'A':15, 'B':35, 'C':0, 'D':30},
    'D': {'A':20, 'B':25, 'C':30, 'D':0}
}

cost, path = tsp(graph, 'A')

print("Minimum Cost:", cost)
print("Best Path:", path)
