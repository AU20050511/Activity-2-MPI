def dp_is_tautology(clause):
    return any(-lit in clause for lit in clause)

def dp_resolve(c1, c2, var):
    return (c1 - {var}) | (c2 - {-var})

def dp_algorithm(clauses):
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
                new_c = dp_resolve(c1, c2, var)
                if not new_c:
                    return False
                if not dp_is_tautology(new_c):
                    new_clauses.append(new_c)

        clauses = [c for c in clauses if var not in c and -var not in c]
        clauses.extend(new_clauses)

    return True
