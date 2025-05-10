
import time
import tracemalloc

# Example CNF test cases
test_cases = {
    "easy_sat": [{1, 2}, {-1, 3}, {-2, -3}],
    "unsat_small": [{1}, {-1}],
    "medium": [{1, -2, 3}, {-1, 2}, {-2, 3}, {-3}]
}

def resolution_algorithm(clauses):
    def resolve(c1, c2):
        for lit in c1:
            if -lit in c2:
                return (c1 - {lit}) | (c2 - {-lit})
        return None

    def is_tautology(clause):
        return any(-lit in clause for lit in clause)

    clauses = [set(c) for c in clauses]
    new = set()
    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
        for c1, c2 in pairs:
            resolvent = resolve(c1, c2)
            if resolvent is not None:
                if not resolvent:
                    return False  # UNSAT
                if not is_tautology(resolvent):
                    new.add(frozenset(resolvent))
        if new.issubset(set(map(frozenset, clauses))):
            return True  # SAT
        clauses.extend([set(c) for c in new])

def dp_algorithm(clauses):
    def resolve(c1, c2, var):
        return (c1 - {var}) | (c2 - {-var})

    def is_tautology(clause):
        return any(-lit in clause for lit in clause)

    clauses = [set(clause) for clause in clauses]
    while clauses:
        all_literals = {lit for clause in clauses for lit in clause}
        vars_to_eliminate = {abs(lit) for lit in all_literals}
        if not vars_to_eliminate:
            return True

        var = vars_to_eliminate.pop()
        pos_clauses = [c for c in clauses if var in c]
        neg_clauses = [c for c in clauses if -var in c]
        new_clauses = []
        for c1 in pos_clauses:
            for c2 in neg_clauses:
                new_c = resolve(c1, c2, var)
                if not new_c:
                    return False
                if not is_tautology(new_c):
                    new_clauses.append(new_c)

        clauses = [c for c in clauses if var not in c and -var not in c]
        clauses.extend(new_clauses)
    return True

def dpll(clauses, assignment={}):
    clauses = simplify(clauses, assignment)
    if not clauses:
        return True
    if [] in clauses:
        return False
    var = choose_variable(clauses, assignment)
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = val
        result = dpll(clauses, new_assignment)
        if result:
            return True
    return False

def simplify(clauses, assignment):
    simplified = []
    for clause in clauses:
        if any((lit > 0 and assignment.get(lit) is True) or
               (lit < 0 and assignment.get(-lit) is False) for lit in clause):
            continue
        new_clause = {lit for lit in clause
                      if not ((lit > 0 and assignment.get(lit) is False) or
                              (lit < 0 and assignment.get(-lit) is True))}
        simplified.append(list(new_clause))
    return simplified

def choose_variable(clauses, assignment):
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                return var
    return None

def benchmark(algorithm, clauses):
    tracemalloc.start()
    start = time.time()
    result = algorithm(clauses)
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "result": "SAT" if result else "UNSAT",
        "time": end - start,
        "memory_kb": peak / 1024
    }

algorithms = {
    "Resolution": resolution_algorithm,
    "DP": dp_algorithm,
    "DPLL": dpll
}

print(f"{'Algorithm':<12} | {'Test Case':<12} | {'Result':<6} | {'Time (s)':<10} | {'Memory (KB)':<12}")
print("-" * 60)
for name, algo in algorithms.items():
    for case_name, cnf in test_cases.items():
        result = benchmark(algo, cnf)
        print(f"{name:<12} | {case_name:<12} | {result['result']:<6} | {result['time']:<10.4f} | {result['memory_kb']:<12.2f}")
