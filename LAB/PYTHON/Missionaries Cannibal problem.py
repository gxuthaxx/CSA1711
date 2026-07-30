from collections import deque

# State: (M_left, C_left, Boat_position)
# Boat_position: 1 = left side, 0 = right side

start = (3, 3, 1)
goal = (0, 0, 0)

def is_valid(m, c):
    # Check valid range
    if m < 0 or c < 0 or m > 3 or c > 3:
        return False
    
    # Missionaries should not be outnumbered
    if (m > 0 and m < c):
        return False
    
    m_right = 3 - m
    c_right = 3 - c
    
    if (m_right > 0 and m_right < c_right):
        return False
    
    return True

def get_next_states(state):
    m, c, boat = state
    moves = [(1,0), (2,0), (0,1), (0,2), (1,1)]
    next_states = []

    for dm, dc in moves:
        if boat == 1:  # Boat on left → go to right
            new_state = (m - dm, c - dc, 0)
        else:          # Boat on right → go to left
            new_state = (m + dm, c + dc, 1)
        
        if is_valid(new_state[0], new_state[1]):
            next_states.append(new_state)

    return next_states

def bfs():
    queue = deque()
    queue.append((start, [start]))
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for next_state in get_next_states(current):
            queue.append((next_state, path + [next_state]))

    return None

# Run BFS
solution = bfs()

# Print Solution
if solution:
    print("Solution Steps:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
