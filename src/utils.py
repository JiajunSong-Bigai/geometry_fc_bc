import sympy
from sympy import sympify
from math import sqrt, sin, pi
from src.my_unification import *


def test_and_subst(str_set, bodies, head):
    n_body = len(bodies)
    theta = {}
    _result = []

    for jj in range(n_body):
        _theta = unify(bodies[jj], str_set[jj], {})
        for _key in _theta.keys():
            if _key not in theta.keys():
                theta[_key] = _theta[_key]
            else:
                if theta[_key] != _theta[_key]:
                    return _result

    _result.append(subst(theta, kg_parser.parse(head)))
    return _result


def test_and_subst_assign(str_set, bodies, head, fact):

    #pdb.set_trace()

    n_body = len(bodies)
    theta = {}
    _result = []

    fact_theta = unify(head, fact, {})

    for jj in range(n_body):
        _theta = unify(bodies[jj], str_set[jj], {})
        for _key in _theta.keys():
            if _key not in theta.keys():
                theta[_key] = _theta[_key]
            else:
                if theta[_key] != _theta[_key]:
                    return _result

    for _key in theta:
        if _key in fact_theta.keys() and fact_theta[_key] != theta[_key]:
            return _result

    _result.append(fact[:-1])
    return _result


def test_and_subst_assign_generate(str_set, bodies, head, bodies_assign):

    #pdb.set_trace()

    n_body = len(bodies)
    theta = {}
    _result = []

    for jj in range(n_body):
        _theta = unify(bodies[jj], str_set[jj], {})
        for _key in _theta.keys():
            if _key not in theta.keys():
                theta[_key] = _theta[_key]
            else:
                if theta[_key] != _theta[_key]:
                    return _result

    key_set = []
    value_set = []
    for key in theta.keys():
        key_set.append(key)
        value_set.append(theta[key])
    vars = sympy.var(','.join(key_set))

    for bdy_assign in bodies_assign:
        bdy_side = bdy_assign.split('=')
        sub_set = [(_var, _value) for _var, _value in zip(vars, value_set)]
        right = sympify(bdy_side[1].strip()).subs(sub_set)
        theta[bdy_side[0]] = str(right)

    _result.append(subst(theta, kg_parser.parse(head)))
    return _result


def add_undeduced_facts(fact, theorem, gen_facts, original_gen_facts):

    original_fact = fact
    parts = theorem.split(":-")
    head = parts[0].strip()
    bodies_ = parse_predicates(parts[1].strip())
    theorem_reduced = head + ":-"
    for _body in bodies_:
        if ("==" in _body) or ("=" in _body) or (">" in _body) or (
                "<" in _body) or (len(_body.strip()) > 3
                                  and _body.strip()[:3] == 'not'):
            continue
        else:
            theorem_reduced = theorem_reduced + _body + ","
    theorem_reduced = theorem_reduced[:-1] + "."

    fact_variable = []
    fact_theta = unify(head, fact, {})
    fact_variable = [_k for _k in fact_theta.values()]

    bodies = []
    bodies_not = []
    bodies_other = []
    bodies_assign = []
    for body in bodies_:
        if body.strip()[0:3] == "not":
            bodies_not.append(body.strip())
        elif ("==" in body.strip()) or (">"
                                        in body.strip()) or ("<"
                                                             in body.strip()):
            bodies_other.append(body.strip())
        elif ("=" in body.strip()):
            bodies_assign.append(body.strip())
        else:
            bodies.append(body.strip())

    if bodies_assign != []:

        body_var_tmp = []
        for body in bodies:
            body_var_tmp.extend(extract_var_simple(kg_parser.parse(body), []))

        remove_set = []
        for _k in fact_theta:
            if _k not in body_var_tmp:
                remove_set.append(_k)

        for _k in remove_set:
            fact_variable.remove(fact_theta[_k])
            fact_theta.pop(_k)

    body_predicate_set = []
    for body in bodies:
        key = key_from_predicates(kg_parser.parse(body))
        body_predicate_set.append(key)

    n_body = len(body_predicate_set)

    fact_set = []
    for fct in gen_facts:
        key = key_from_predicates(kg_parser.parse(fct))
        fact_set.append(key)

    n_fact = len(fact_set)

    num_set = []
    body_related_fact_set = []
    body_related_fact_set_all = []
    variable_set = []
    for bdy_idx, body_key in enumerate(body_predicate_set):
        tmp = []
        tmp_var = []
        tmp_all = []
        for ii in range(n_fact):
            if body_key == fact_set[ii]:
                tmp_all.append(gen_facts[ii])

                _flag_1 = True
                _set = []
                _body_unify = {}
                _body_unify = unify(bodies[bdy_idx], gen_facts[ii], {})
                if _body_unify == None:  #needs to revise
                    continue
                _set = _body_unify.values()

                for jj in _body_unify:
                    if (jj in fact_theta) and (fact_theta[jj] !=
                                               _body_unify[jj]):
                        _flag_1 = False
                        break

                if not _flag_1:
                    continue

                tmp.append(gen_facts[ii])
                tmp_var.append(_set)

        num_set.append(len(tmp))
        body_related_fact_set.append(tmp)
        body_related_fact_set_all.append(tmp_all)
        variable_set.append(tmp_var)

    n_iter = int(np.prod(num_set))
    data_one = np.ones(num_set)
    idx = np.argwhere(data_one == 1)

    rules = []

    print('n_iteration ', n_iter)

    bool_recursive = True
    for ii in range(n_iter):
        __var_set = []
        for jj in range(n_body):
            __var_set.extend(variable_set[jj][idx[ii, jj]])
        __var_set = np.unique(__var_set)
        is_iter = True
        for _v in fact_variable:
            if _v not in __var_set:
                is_iter = False
                break

        if not is_iter:
            continue

        _str = ""
        _str_set = []
        for jj in range(n_body):
            _str = _str + body_related_fact_set[jj][idx[ii, jj]]
            _str_set.append(body_related_fact_set[jj][idx[ii, jj]])

        _answers = []
        if bodies_assign != []:
            #pdb.set_trace()
            _answers = test_and_subst_assign(_str_set, bodies, head,
                                             original_fact)
        else:
            _answers = test_and_subst(_str_set, bodies, head)
        _answers = [tmp + "." for tmp in _answers if tmp + "." not in _str_set]

        flag = True
        if fact in _answers:

            if bodies_assign != []:
                _tmp_rule = []
                for jj in range(n_body):
                    _tmp_rule.append(body_related_fact_set[jj][idx[ii, jj]])
                _tmp_rule.append(fact)
                rules.append(_tmp_rule)
                bool_recursive = False
                break

            theta = unify(head, fact, {})
            for jj in range(n_body):
                _theta = unify(bodies[jj],
                               body_related_fact_set[jj][idx[ii, jj]], {})
                for _key in _theta.keys():
                    if _key in theta.keys():
                        if theta[_key] != _theta[_key]:
                            flag = False
                            break
                    else:
                        theta[_key] = _theta[_key]
                if not flag:
                    break

            if flag:
                key_set = []
                value_set = []
                for key in theta.keys():
                    key_set.append(key)
                    value_set.append(theta[key])
                vars = sympy.var(','.join(key_set))

                for body_not in bodies_not:
                    if ("==" in body_not) or (">"
                                              in body_not) or ("<"
                                                               in body_not):
                        body_not = body_not[4:]
                        if ("==" in body_not):
                            two_side = body_not.split("==")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left == right:
                                flag = False
                                break

                        elif (">=" in body_not):
                            two_side = body_not.split(">=")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left >= right:
                                flag = False
                                break

                        elif (">" in body_not):
                            two_side = body_not.split(">")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left > right:
                                flag = False
                                break

                        elif ("<=" in body_not):
                            two_side = body_not.split("<=")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left <= right:
                                flag = False
                                break

                        elif ("<" in body_not):
                            two_side = body_not.split("<")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left < right:
                                flag = False
                                break

                    else:
                        body_fact = subst(theta, kg_parser.parse(body_not[4:]))
                        if body_fact + '.' in original_gen_facts:
                            flag = False
                            break

                for body_other in bodies_other:
                    if ("==" in body_other) or (">" in body_other) or (
                            "<" in body_other):

                        if ("==" in body_other):
                            two_side = body_other.split("==")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left != right:
                                flag = False
                                break

                        elif (">=" in body_other):
                            two_side = body_other.split(">=")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if not (left >= right):
                                flag = False
                                break

                        elif (">" in body_other):
                            #pdb.set_trace()
                            two_side = body_other.split(">")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if not (left > right):
                                flag = False
                                break

                        elif ("<=" in body_other):
                            two_side = body_other.split("<=")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if not (left <= right):
                                flag = False
                                break

                        elif ("<" in body_other):
                            two_side = body_other.split("<")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if not (left < right):
                                flag = False
                                break

            if flag:
                _tmp_rule = []
                for jj in range(n_body):
                    _tmp_rule.append(body_related_fact_set[jj][idx[ii, jj]])
                _tmp_rule.append(fact)
                rules.append(_tmp_rule)
                bool_recursive = False
                break

    return rules, bool_recursive, body_related_fact_set, body_related_fact_set_all


def single_step_forward(facts, theorem, gen_facts, rules_backup):

    parts = theorem.split(":-")
    head = parts[0].strip()
    bodies_ = parse_predicates(parts[1])
    theorem_reduced = head + ":-"
    for _body in bodies_:
        if ("==" in _body) or ("=" in _body) or (">" in _body) or (
                "<" in _body) or (len(_body.strip()) > 3
                                  and _body.strip()[:3] == 'not'):
            continue
        else:
            theorem_reduced = theorem_reduced + _body + ","
    theorem_reduced = theorem_reduced[:-1] + "."

    bodies = []
    bodies_not = []
    bodies_other = []
    bodies_assign = []
    for body in bodies_:
        if body.strip()[0:3] == "not":
            bodies_not.append(body.strip())
        elif ("==" in body.strip()) or (">"
                                        in body.strip()) or ("<"
                                                             in body.strip()):
            bodies_other.append(body.strip())
        elif ("=" in body.strip()):
            bodies_assign.append(body.strip())
        else:
            bodies.append(body.strip())

    body_predicate_set = []
    for body in bodies:
        key = key_from_predicates(kg_parser.parse(body))
        body_predicate_set.append(key)

    n_body = len(body_predicate_set)

    t = facts[-1]
    n_body = len(facts) - 1
    t_other = [it for it in range(n_body)]
    t_other.remove(t)
    t_other.append(t)
    shuffle_index = np.argsort(t_other)
    body_fact_set = [facts[ishuffle] for ishuffle in shuffle_index]

    fact_variable = []
    fact_theta = unify(bodies[t], facts[-2][0], {})
    fact_variable = fact_theta.values()

    original_fact = facts[-2][0]

    if bodies_assign != []:

        body_var_tmp = []
        for body in bodies:
            body_var_tmp.extend(extract_var_simple(kg_parser.parse(body), []))

        remove_set = []
        for _k in fact_theta:
            if _k not in body_var_tmp:
                remove_set.append(_k)

        for _k in remove_set:
            fact_variable.remove(fact_theta[_k])
            fact_theta.pop(_k)

    num_set = []
    body_related_fact_set = []

    for bdy_idx in range(n_body):

        if bdy_idx == t:

            num_set.append(len(body_fact_set[t]))
            body_related_fact_set.append(body_fact_set[t])
            continue

        tmp = []
        tmp_var = []
        tmp_all = []
        for ii in range(len(body_fact_set[bdy_idx])):

            _flag_1 = True
            _set = []
            _body_unify = {}
            _body_unify = unify(bodies[bdy_idx], body_fact_set[bdy_idx][ii],
                                {})
            _set = _body_unify.values()

            for jj in _body_unify:
                if (jj in fact_theta) and (fact_theta[jj] != _body_unify[jj]):
                    _flag_1 = False
                    break

            if not _flag_1:
                continue

            tmp.append(body_fact_set[bdy_idx][ii])
            tmp_var.append(_set)

        num_set.append(len(tmp))
        body_related_fact_set.append(tmp)

    n_iter = np.prod(num_set)
    data_one = np.ones(num_set)
    idx = np.argwhere(data_one == 1)

    rules = []

    for ii in range(n_iter):

        _str = ""
        _str_set = []
        for jj in range(n_body):
            _str = _str + body_related_fact_set[jj][idx[ii, jj]]
            _str_set.append(body_related_fact_set[jj][idx[ii, jj]])

        _answers = []
        if bodies_assign != []:
            #print('single_step')
            #print(head)
            #print(original_fact)
            #pdb.set_trace()
            _answers = test_and_subst_assign_generate(_str_set, bodies, head,
                                                      bodies_assign)
        else:
            _answers = test_and_subst(_str_set, bodies, head)
        _answers = [tmp + "." for tmp in _answers if tmp + "." not in _str_set]

        #_answers = test_and_subst(_str_set, bodies, head)
        #_answers = [tmp+"." for tmp in _answers if tmp+"." not in _str_set]

        if _answers != []:

            for fct in _answers:

                body_backup = []

                flag = True
                theta = unify(head, fct, {})
                for jj in range(n_body):
                    body_backup.append(body_related_fact_set[jj][idx[ii, jj]])

                    _theta = unify(bodies[jj],
                                   body_related_fact_set[jj][idx[ii, jj]], {})
                    for _key in _theta.keys():
                        if _key not in theta.keys():
                            theta[_key] = _theta[_key]

                key_set = []
                value_set = []
                for key in theta.keys():
                    key_set.append(key)
                    value_set.append(theta[key])
                vars = sympy.var(','.join(key_set))

                for body_not in bodies_not:
                    if ("==" in body_not) or (">"
                                              in body_not) or ("<"
                                                               in body_not):
                        body_not = body_not[4:]
                        if ("==" in body_not):
                            two_side = body_not.split("==")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left == right:
                                flag = False
                                break

                        elif (">=" in body_not):
                            two_side = body_not.split(">=")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left >= right:
                                flag = False
                                break

                        elif (">" in body_not):
                            two_side = body_not.split(">")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left > right:
                                flag = False
                                break

                        elif ("<=" in body_not):
                            two_side = body_not.split("<=")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left <= right:
                                flag = False
                                break

                        elif ("<" in body_not):
                            two_side = body_not.split("<")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left < right:
                                flag = False
                                break

                    else:
                        body_fact = subst(theta, kg_parser.parse(body_not[4:]))
                        if body_fact + "." in gen_facts:
                            flag = False
                            break

                for body_other in bodies_other:
                    if ("==" in body_other) or (">" in body_other) or (
                            "<" in body_other):

                        if ("==" in body_other):
                            two_side = body_other.split("==")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if left != right:
                                flag = False
                                break

                        elif (">=" in body_other):
                            two_side = body_other.split(">=")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if not (left >= right):
                                flag = False
                                break

                        elif (">" in body_other):
                            two_side = body_other.split(">")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if not (left > right):
                                flag = False
                                break

                        elif ("<=" in body_other):
                            two_side = body_other.split("<=")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if not (left <= right):
                                flag = False
                                break

                        elif ("<" in body_other):
                            two_side = body_other.split("<")
                            sub_set = [
                                (_var, _value)
                                for _var, _value in zip(vars, value_set)
                            ]
                            # a bug from sympy which cannot interpret 'E'
                            if two_side[0] == 'E':
                                two_side[0] = sympy.var('E')
                            if two_side[1] == 'E':
                                two_side[1] = sympy.var('E')
                            left = sympify(two_side[0]).subs(sub_set)
                            right = sympify(two_side[1]).subs(sub_set)
                            if not (left < right):
                                flag = False
                                break

                if flag:
                    rules.append(fct)
                    if fct not in rules_backup.keys():
                        rules_backup[fct] = [body_backup]
                    else:
                        rules_backup[fct].append(body_backup)

    return rules


def iterate_add_undeduced_facts(fact, theorem, original_gen_facts):

    gen_facts = original_gen_facts.copy()

    rules_backup = {}
    ite_num = 10
    for ii in range(ite_num):

        print(fact)
        print(theorem)
        #pdb.set_trace()
        _rules, _bool_recursive, _body_related_fact_set, _body_related_fact_set_all = add_undeduced_facts(
            fact, theorem, gen_facts, original_gen_facts)

        new_facts = []
        if _bool_recursive:
            n_body = len(_body_related_fact_set)
            for jj in range(n_body):
                n_fact = len(_body_related_fact_set[jj])
                for kk in range(n_fact):
                    tmp = [
                        _body_related_fact_set_all[tt] for tt in range(n_body)
                        if tt != jj
                    ]
                    tmp.append([_body_related_fact_set[jj][kk]])
                    tmp.append(jj)

                    _tmp_rule = single_step_forward(tmp, theorem,
                                                    original_gen_facts,
                                                    rules_backup)
                    new_facts.extend(_tmp_rule)

            for jj in range(n_body):
                new_facts.extend(_body_related_fact_set[jj])
            gen_facts = new_facts

        else:
            return _rules, rules_backup


def generate_deduce_path(rules, rules_dict_traj, undeduced_set, gen_facts):

    rnd_idx = np.random.randint(len(rules))
    rule = rules[rnd_idx]

    paths = []
    bodies = rule[:-1]
    head = rule[-1]
    pth = head[:-1] + ":-"
    for bdy in bodies:
        pth = pth + bdy[:-1] + ","
    paths.append(pth[:-1] + '.')

    unproved = [
        bdy for bdy in bodies if (bdy not in gen_facts) and (
            bdy in rules_dict_traj.keys()) and (rules_dict_traj[bdy] != [])
    ]
    proved = [bdy for bdy in bodies if (bdy in gen_facts)]
    undeduced_set.extend(proved)
    while unproved != []:
        for _up in unproved:
            pth = _up[:-1] + ":-"
            rnd_idx = np.random.randint(len(rules_dict_traj[_up]))
            unproved_rule = rules_dict_traj[_up][rnd_idx]

            for bdy in unproved_rule:
                pth = pth + bdy[:-1] + ","
            paths.append(pth[:-1] + '.')

            unproved.remove(_up)
            tmp = [
                bdy for bdy in unproved_rule
                if (bdy not in gen_facts) and (bdy in rules_dict_traj.keys())
                and (rules_dict_traj[bdy] != [])
            ]
            unproved.extend(tmp)
            undeduced_set.extend(
                [bdy for bdy in unproved_rule if (bdy in gen_facts)])

    return paths
