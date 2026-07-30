from itertools import permutations

def solve_crypt():
    letters = 'SENDMORY'   # Unique letters
    digits = permutations(range(10), len(letters))

    for perm in digits:
        S, E, N, D, M, O, R, Y = perm

        # Leading digits cannot be zero
        if S == 0 or M == 0:
            continue

        # Form numbers
        SEND  = S*1000 + E*100 + N*10 + D
        MORE  = M*1000 + O*100 + R*10 + E
        MONEY = M*10000 + O*1000 + N*100 + E*10 + Y

        # Check condition
        if SEND + MORE == MONEY:
            print("Solution Found:")
            print(f"SEND  = {SEND}")
            print(f"MORE  = {MORE}")
            print(f"MONEY = {MONEY}")
            print(f"Mapping: {dict(zip(letters, perm))}")
            return

    print("No solution found.")

# Run the function
solve_crypt()
