def is_tautology(clause):
    return any(-lit in clause for lit in clause)

def resolve(c1, c2):
    for lit in c1:
        if -lit in c2:
            return (c1 - {lit}) | (c2 - {-lit})
    return None

def resolution_algorithm(clauses):
    clauses = [set(c) for c in clauses]
    new = set()

    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses))
                 for j in range(i + 1, len(clauses))]
        for (c1, c2) in pairs:
            resolvent = resolve(c1, c2)
            if resolvent is not None:
                if not resolvent:
                    return False  # UNSAT
                if not is_tautology(resolvent):
                    new.add(frozenset(resolvent))
        if new.issubset(set(map(frozenset, clauses))):
            return True  # SAT
        clauses.extend([set(c) for c in new])
