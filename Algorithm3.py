def dpll(clauses, assignment={}):
    clauses = simplify(clauses, assignment)

    if not clauses:
        return assignment  # SAT
    if [] in clauses:
        return None  # UNSAT

    var = choose_variable(clauses, assignment)

    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = val
        result = dpll(clauses, new_assignment)
        if result is not None:
            return result

    return None

def simplify(clauses, assignment):
    simplified = []
    for clause in clauses:
        if any((lit > 0 and assignment.get(lit, None) is True) or
               (lit < 0 and assignment.get(-lit, None) is False) for lit in clause):
            continue  # clause is already satisfied
        new_clause = {lit for lit in clause
                      if (lit > 0 and assignment.get(lit, None) is not False) and
                         (lit < 0 and assignment.get(-lit, None) is not True)}
        simplified.append(list(new_clause))
    return simplified

def choose_variable(clauses, assignment):
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                return var
    return None
