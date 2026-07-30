from collections import deque

def water_jug(cap1, cap2, target):
    visited = set()
    queue = deque([((0, 0), [])])

    while queue:
        (jug1, jug2), path = queue.popleft()

        if (jug1, jug2) in visited:
            continue

        visited.add((jug1, jug2))
        path = path + [(jug1, jug2)]

        # Check if target is reached
        if jug1 == target or jug2 == target:
            print("Solution Found:")
            for step in path:
                print(step)
            return

        # Possible operations
        next_states = [
            (cap1, jug2),                     # Fill Jug 1
            (jug1, cap2),                     # Fill Jug 2
            (0, jug2),                        # Empty Jug 1
            (jug1, 0),                        # Empty Jug 2
            # Pour Jug 1 -> Jug 2
            (jug1 - min(jug1, cap2 - jug2),
             jug2 + min(jug1, cap2 - jug2)),
            # Pour Jug 2 -> Jug 1
            (jug1 + min(jug2, cap1 - jug1),
             jug2 - min(jug2, cap1 - jug1))
        ]

        for state in next_states:
            if state not in visited:
                queue.append((state, path))

    print("No solution exists.")

# Example
jug1_capacity = 4
jug2_capacity = 3
target = 2

water_jug(jug1_capacity, jug2_capacity, target)
