class MapColoringCSP:
    def __init__(self, variables, domains, neighbors):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.assignment = {}

    def is_consistent(self, var, color):
        for neighbor in self.neighbors[var]:
            if neighbor in self.assignment and self.assignment[neighbor] == color:
                return False
        return True

    def select_unassigned_variable(self):
        for var in self.variables:
            if var not in self.assignment:
                return var
        return None

    def backtrack(self):
        if len(self.assignment) == len(self.variables):
            return self.assignment

        var = self.select_unassigned_variable()

        for color in self.domains[var]:
            if self.is_consistent(var, color):
                self.assignment[var] = color

                result = self.backtrack()
                if result is not None:
                    return result

                del self.assignment[var]

        return None

    def solve(self):
        result = self.backtrack()
        if result:
            print("Solution found:\n")
            for region in self.variables:
                print(f"{region} -> {result[region]}")
        else:
            print("No solution exists.")
        return result


variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

colors = ['Red', 'Green', 'Blue']

domains = {var: colors[:] for var in variables}

neighbors = {
    'WA':  ['NT', 'SA'],
    'NT':  ['WA', 'SA', 'Q'],
    'SA':  ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q':   ['NT', 'SA', 'NSW'],
    'NSW': ['SA', 'Q', 'V'],
    'V':   ['SA', 'NSW'],
    'T':   []
}

if __name__ == "__main__":
    csp = MapColoringCSP(variables, domains, neighbors)
    csp.solve()
