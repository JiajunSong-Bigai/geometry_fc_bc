from src.utils import (generate_deduce_path, iterate_add_undeduced_facts)


def bc(gen_facts_dict, query_set, n_theorem, used_theorem_set):
    diff_set = []
    for ii in range(n_theorem):
        tmp = [
            fact for fact in gen_facts_dict[ii + 1]
            if fact not in gen_facts_dict[ii]
        ]
        diff_set.append(tmp)

    deduced_procedure_str = []

    deduced_set = []
    undeduced_set = query_set
    nset = len(diff_set)

    for ii in range(nset - 1, -1, -1):
        if diff_set[ii] == []:
            continue

        print("deduced step: ", ii)

        loop_index = 0
        while loop_index < len(undeduced_set):
            undeduced_fact = undeduced_set[loop_index]

            #for undeduced_fact in undeduced_set:
            #pdb.set_trace()

            if undeduced_fact in gen_facts_dict[0]:
                del undeduced_set[loop_index]
                #loop_index = loop_index-1
                print("undeduced_fact in gen_facts_dict: ", undeduced_fact)
                continue

            if undeduced_fact in diff_set[ii]:

                deduced_set.append(undeduced_fact)
                del undeduced_set[loop_index]

                rules, rules_dict_traj = iterate_add_undeduced_facts(
                    undeduced_fact, used_theorem_set[ii], gen_facts_dict[ii])

                print('len(undeduced_set) ', len(undeduced_set))
                print(undeduced_set)
                print(rules)
                deduce_path = generate_deduce_path(rules, rules_dict_traj,
                                                   undeduced_set,
                                                   gen_facts_dict[ii])
                for _path in deduce_path:
                    print(_path + "\n")

                deduced_procedure_str.append(deduce_path)
                #loop_index = loop_index-1
                continue

            loop_index = loop_index + 1

    return undeduced_set, deduced_procedure_str


def fol_bc_ask(kb, query):
    """
    [Figure 9.6]
    A simple backward-chaining algorithm for first-order logic.
    KB should be an instance of FolKB, and query an atomic sentence.
    """
    return fol_bc_or(kb, query, {})


def fol_bc_or(kb, goal, theta):
    # for each rule that could be used to prove the goal
    # and the existing theta
    for rule in kb.fetch_rules_for_goal(
            goal):  # no need of this layer, cuz we know the rule

        # lhs ==> rhs, parse and standardize
        lhs, rhs = parse_definite_clause(standardize_variables(rule))

        # for each premise in the lhs
        #   1. unify the rhs goal theta
        #   2. try finding a theta that matches kb, lhs, and the unified theta
        for theta1 in fol_bc_and(kb, lhs, unify_mm(rhs, goal, theta)):
            yield theta1


def fol_bc_and(kb, goals, theta):
    """
    Args:
        kb: a knowledge base
        goals: facts to achieve
        theta: existing substitution dictionary
    
    """
    # no unification existed so far
    if theta is None:
        pass

    # all goals are proved
    elif not goals:
        yield theta
    else:

        # first goal and the rest goals
        #   1. any rule that satisfies the first goal
        #   2. rule that satisfies all the rest goals
        first, rest = goals[0], goals[1:]
        for theta1 in fol_bc_or(kb, subst(theta, first), theta):
            for theta2 in fol_bc_and(kb, rest, theta1):
                yield theta2


def parse_definite_clause(s):
    """Return the antecedents and the consequent of a definite clause."""
    assert is_definite_clause(s)
    if is_symbol(s.op):
        return [], s
    else:
        antecedent, consequent = s.args
        return conjuncts(antecedent), consequent


def unify_mm(x, y, s={}):
    """Unify expressions x,y with substitution s using an efficient rule-based
    unification algorithm by Martelli & Montanari; return a substitution that
    would make x,y equal, or None if x,y can not unify. x and y can be
    variables (e.g. Expr('x')), constants, lists, or Exprs.
    >>> unify_mm(x, 3, {})
    {x: 3}
    """

    set_eq = extend(s, x, y)
    s = set_eq.copy()
    while True:
        trans = 0
        for x, y in set_eq.items():
            if x == y:
                # if x = y this mapping is deleted (rule b)
                del s[x]
            elif not is_variable(x) and is_variable(y):
                # if x is not a variable and y is a variable, rewrite it as y = x in s (rule a)
                if s.get(y, None) is None:
                    s[y] = x
                    del s[x]
                else:
                    # if a mapping already exist for variable y then apply
                    # variable elimination (there is a chance to apply rule d)
                    s[x] = vars_elimination(y, s)
            elif not is_variable(x) and not is_variable(y):
                # in which case x and y are not variables, if the two root function symbols
                # are different, stop with failure, else apply term reduction (rule c)
                if x.op is y.op and len(x.args) == len(y.args):
                    term_reduction(x, y, s)
                    del s[x]
                else:
                    return None
            elif isinstance(y, Expr):
                # in which case x is a variable and y is a function or a variable (e.g. F(z) or y),
                # if y is a function, we must check if x occurs in y, then stop with failure, else
                # try to apply variable elimination to y (rule d)
                if occur_check(x, y, s):
                    return None
                s[x] = vars_elimination(y, s)
                if y == s.get(x):
                    trans += 1
            else:
                trans += 1
        if trans == len(set_eq):
            # if no transformation has been applied, stop with success
            return s
        set_eq = s.copy()


def standardize_variables(sentence, dic=None):
    """Replace all the variables in sentence with new variables."""
    if dic is None:
        dic = {}
    if not isinstance(sentence, Expr):
        return sentence
    elif is_var_symbol(sentence.op):
        if sentence in dic:
            return dic[sentence]
        else:
            v = Expr('v_{}'.format(next(standardize_variables.counter)))
            dic[sentence] = v
            return v
    else:
        return Expr(sentence.op,
                    *[standardize_variables(a, dic) for a in sentence.args])


def unify(x, y, s={}):
    """
    [Figure 9.1]
    Unify expressions x,y with substitution s; return a substitution that
    would make x,y equal, or None if x,y can not unify. x and y can be
    variables (e.g. Expr('x')), constants, lists, or Exprs.
    >>> unify(x, 3, {})
    {x: 3}
    """
    if s is None:
        return None
    elif x == y:
        return s
    elif is_variable(x):
        return unify_var(x, y, s)
    elif is_variable(y):
        return unify_var(y, x, s)
    elif isinstance(x, Expr) and isinstance(y, Expr):
        return unify(x.args, y.args, unify(x.op, y.op, s))
    elif isinstance(x, str) or isinstance(y, str):
        return None
    elif issequence(x) and issequence(y) and len(x) == len(y):
        if not x:
            return s
        return unify(x[1:], y[1:], unify(x[0], y[0], s))
    else:
        return None


def is_variable(x):
    """A variable is an Expr with no args and a lowercase symbol as the op."""
    return isinstance(x, Expr) and not x.args and x.op[0].islower()


def unify_var(var, x, s):
    if var in s:
        return unify(s[var], x, s)
    elif x in s:
        return unify(var, s[x], s)
    elif occur_check(var, x, s):
        return None
    else:
        new_s = extend(s, var, x)
        cascade_substitution(new_s)
        return new_s


def occur_check(var, x, s):
    """Return true if variable var occurs anywhere in x
    (or in subst(s, x), if s has a binding for x)."""
    if var == x:
        return True
    elif is_variable(x) and x in s:
        return occur_check(var, s[x], s)
    elif isinstance(x, Expr):
        return (occur_check(var, x.op, s) or occur_check(var, x.args, s))
    elif isinstance(x, (list, tuple)):
        return first(e for e in x if occur_check(var, e, s))
    else:
        return False


def subst(s, x):
    """Substitute the substitution s into the expression x.
    >>> subst({x: 42, y:0}, F(x) + y)
    (F(42) + 0)
    """
    if isinstance(x, list):
        return [subst(s, xi) for xi in x]
    elif isinstance(x, tuple):
        return tuple([subst(s, xi) for xi in x])
    elif not isinstance(x, Expr):
        return x
    elif is_var_symbol(x.op):
        return s.get(x, x)
    else:
        return Expr(x.op, *[subst(s, arg) for arg in x.args])
