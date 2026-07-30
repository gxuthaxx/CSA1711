# Vacuum Cleaner Problem (Simple Reflex Agent)

# Environment: rooms A and B
# State format: (location, A_status, B_status)

def vacuum_agent(state):
    location, A, B = state

    if location == 'A':
        if A == 'D':
            return 'Clean'
        else:
            return 'Right'
    
    elif location == 'B':
        if B == 'D':
            return 'Clean'
        else:
            return 'Left'

def run_vacuum():
    # Initial state (you can change this)
    state = ['A', 'D', 'D']  # Start at A, both rooms dirty

    print("Initial State:", state)

    steps = 0

    while True:
        action = vacuum_agent(state)
        print("Action:", action)

        if action == 'Clean':
            if state[0] == 'A':
                state[1] = 'C'
            else:
                state[2] = 'C'

        elif action == 'Right':
            state[0] = 'B'

        elif action == 'Left':
            state[0] = 'A'

        print("Current State:", state)
        steps += 1

        # Goal check: both rooms clean
        if state[1] == 'C' and state[2] == 'C':
            print("Goal Reached! Both rooms are clean.")
            print("Total Steps:", steps)
            break

# Run the program
run_vacuum()
