from copy import deepcopy
import numpy as np
import pdb

from src.formula_parser import FormulaParser
from src.extended_definition import ExtendedDefinition
from src.logic_parser import LogicParser

kg_parser = LogicParser(ExtendedDefinition(debug=True))
fm_parser = FormulaParser(ExtendedDefinition(debug=True))

kb = {}
list_of_predicates = []
list_of_explored_rules = []
unproved_premise = []
unproved_query = []
unproved_single_chain = []
unproved_chain = []


def fetch_rules(goal):
    global kb
    global list_of_predicates

    print("fetch_rules for goal:- ", goal)
    list_of_rules = []
    #predicate = goal.partition('(')[0]

    predicate = key_from_predicates(kg_parser.parse(goal))
    predicate = predicate[:-1]

    print("\t", predicate, kb[predicate]['conc'])
    list_of_rules = list_of_rules + kb[predicate]['conc']
    return list_of_rules


def subst(theta, res):
    #print("\tsubst: ", theta, res)

    fact = ""
    nl = len(res)
    for ii in range(nl):
        if isinstance(res[ii], str) and (ii == 0):
            fact = fact + res[ii] + "("

        elif isinstance(res[ii], str) and (ii > 0) and (ii < nl - 1):
            if variable(res[ii]) and (res[ii] in theta):
                fact = fact + theta[res[ii]] + ","
            else:
                fact = fact + res[ii] + ","

        elif isinstance(res[ii], str) and (ii == nl - 1):
            if variable(res[ii]) and (res[ii] in theta):
                fact = fact + theta[res[ii]]
            else:
                fact = fact + res[ii]

        elif not isinstance(res[ii], str) and (ii > 0) and (ii < nl - 1):
            _fact = subst(theta, res[ii])
            fact = fact + _fact + ","

        elif not isinstance(res[ii], str) and (ii == nl - 1):
            _fact = subst(theta, res[ii])
            fact = fact + _fact

    fact = fact + ")"

    return fact


"""
def variable(x):
    if not isinstance(x, str):
        return False
    else:
        if x[0].islower():
            return False
        else:
            return True
"""


def variable(x):
    if not isinstance(x, str):
        return False
    else:
        if x[0].isupper():
            return True
        else:
            return False


def compound(x):
    if not isinstance(x, str):
        return False
    else:
        if '(' in x and ')' in x:
            return True
        else:
            return False


def list(x):
    if not isinstance(x, str):
        return True
    else:
        return False


def key_from_predicates(res):

    nl = len(res)
    keys = ""

    for ii in range(nl):
        if isinstance(res[ii], str) and (ii == 0):
            keys = keys + res[ii] + "-"

        elif not isinstance(res[ii], str) and (ii > 0) and (ii < nl - 1):
            _key = key_from_predicates(res[ii])
            keys = keys + _key

        elif not isinstance(res[ii], str) and (ii == nl - 1):
            _key = key_from_predicates(res[ii])
            keys = keys + _key

    return keys


def unify_var(var, x, theta):
    #print("IN unify_var", var, x, theta)
    if var in theta:
        #print("var in theta", var, theta)
        return unify(theta[var], x, theta)
    elif x in theta:
        #print("x in theta", x, theta)
        return unify(var, theta[x], theta)
    else:
        theta[var] = x
        #print("not in theta", theta[var])
        return theta


def check_theta(theta):
    for entry in theta:
        if variable(theta[entry]):
            if theta[entry] in theta:
                print("in check_theta. theta changed")
                theta[entry] = theta[theta[entry]]
    return theta


def reverse_parse(res):

    fact = ""
    nl = len(res)
    for ii in range(nl):
        if isinstance(res[ii], str) and (ii == 0):
            fact = fact + res[ii] + "("

        elif isinstance(res[ii], str) and (ii > 0) and (ii < nl - 1):
            fact = fact + res[ii] + ","

        elif isinstance(res[ii], str) and (ii == nl - 1):
            fact = fact + res[ii]

        elif not isinstance(res[ii], str) and (ii > 0) and (ii < nl - 1):
            _fact = reverse_parse(res[ii])
            fact = fact + _fact + ","

        elif not isinstance(res[ii], str) and (ii == nl - 1):
            _fact = reverse_parse(res[ii])
            fact = fact + _fact

    fact = fact + ")"

    return fact


def unify(x, y, theta):
    #print("\tunify", x, y, theta)
    if theta == None:
        #print("\tin theta is None")
        return None
    elif x == y:
        #print("\tin x=y")
        return check_theta(theta)
    elif variable(x) is True:
        #print("\tin variable(x)")
        return unify_var(x, y, theta)
    elif variable(y) is True:
        #print("\tin variable(y)")
        return unify_var(y, x, theta)
    elif compound(x) and compound(y):
        #print("\tin compound")

        x_parse = kg_parser.parse(x)
        y_parse = kg_parser.parse(y)

        x_op = x_parse[0]
        y_op = y_parse[0]

        x_args = []

        for item in range(len(x_parse) - 1):  #temp.split(','):
            if isinstance(x_parse[item + 1], str):
                x_args.append(x_parse[item + 1])
            else:
                x_args.append(reverse_parse(x_parse[item + 1]))

        y_args = []

        for item in range(len(y_parse) - 1):  #temp.split(','):
            if isinstance(y_parse[item + 1], str):
                y_args.append(y_parse[item + 1])
            else:
                y_args.append(reverse_parse(y_parse[item + 1]))

        return unify(x_args, y_args, unify(x_op, y_op, theta))

    elif list(x) and list(y) and x != [] and y != []:
        #print("\tin list")
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    elif x == [] or y == []:
        return None
    else:
        #print("\tin else")
        return None


#_body_unify={}
#_body_unify = unify('pointPosition(B,Xb,Yb)', 'pointPosition(n,1055,1060).', {})
#print(_body_unify)


def var_exist(res):

    fact = False
    nl = len(res)
    for ii in range(nl):
        if isinstance(res[ii], str) and (ii > 0) and res[ii][0].isupper():
            fact = True
            return fact

        elif not isinstance(res[ii], str):
            _fact = var_exist(res[ii])
            fact = fact or _fact

    return fact


def parse_match(res, fact):

    matched = True

    nl = len(res)
    for ii in range(nl):
        if isinstance(res[ii], str) and (ii == 0) and isinstance(
                fact[ii], str):
            if res[ii] == fact[ii]:
                matched = True
            else:
                matched = False
                return matched
        elif isinstance(res[ii], str) and (
                ii > 0) and res[ii][0].islower() and isinstance(res[ii], str):
            if res[ii] == fact[ii]:
                matched = True
            else:
                matched = False
                return matched
        elif isinstance(res[ii], str) and (
                ii > 0) and res[ii][0].isupper() and isinstance(res[ii], str):
            matched = True

        elif (not isinstance(res[ii], str)) and (not isinstance(fact[ii],
                                                                str)):
            _matched = parse_match(res[ii], fact[ii])
            matched = matched and _matched
        else:
            matched = False
            return matched

    return matched


def inst(temp, facts):

    results = []
    temp_parse = kg_parser.parse(temp)

    for fact in facts:
        if fact[:len(temp_parse[0])] == temp_parse[0]:
            fact_parse = kg_parser.parse(fact)
            if parse_match(temp_parse, fact_parse):
                results.append(fact)

    return results


def filterInst(temp_list, list_of_premises):

    filterlist = []
    temp = []

    n = len(temp_list)
    nlist = [len(ii) for ii in temp_list]
    for ii in range(n):
        temp.append(
            temp_list[ii] *
            (int(np.prod(nlist[:ii])) * int(np.prod(nlist[(ii + 1):]))))

    for ii in range(np.prod(nlist)):
        each_query = []
        query_str = "Predicate("
        premise_str = "Predicate("
        for jj in range(n):

            each_query.append(temp[jj][ii])
            if temp[jj][ii] == "()" and list_of_premises[jj] == "":
                continue
            else:
                if temp[jj][ii][-1] == '.':
                    temp[jj][ii] = temp[jj][ii][:-1]

                query_str = query_str + temp[jj][ii] + ","
                premise_str = premise_str + list_of_premises[jj] + ","

        #if query_str[-2]=='.':
        #    query_str = query_str[:-2]+")"
        #else:
        query_str = query_str[:-1] + ")"

        #if premise_str[-2]=='.':
        #    premise_str = premise_str[:-2]+")"
        #else:
        premise_str = premise_str[:-1] + ")"

        sucess = unify(premise_str, query_str, {})
        if sucess != None:
            filterlist.append(each_query)

    return filterlist


def existed(temp_list, facts):

    val = True
    for temp in temp_list:
        if not (temp in facts):
            val = False
            break

    return val


def extract_var(res, variable_names, label):
    nl = len(res)
    fact = ""
    #label=0
    for ii in range(nl):
        if isinstance(res[ii], str) and (ii == 0):
            fact = fact + res[ii][0].lower() + res[ii][1:] + "("

        elif isinstance(res[ii], str) and (ii > 0) and (ii < nl - 1):
            item = res[ii].upper()
            if item not in variable_names:
                variable_names[item] = "X" + repr(label)
                item = "X" + repr(label)
                label = label + 1
            else:
                item = variable_names[item]

            fact = fact + item + ","

        elif isinstance(res[ii], str) and (ii == nl - 1):
            item = res[ii].upper()
            if item not in variable_names:
                variable_names[item] = "X" + repr(label)
                item = "X" + repr(label)
                label = label + 1
            else:
                item = variable_names[item]

            fact = fact + item

        elif not isinstance(res[ii], str) and (ii > 0) and (ii < nl - 1):
            _fact, variable_names, label = extract_var(res[ii], variable_names,
                                                       label)
            fact = fact + _fact + ","

        elif not isinstance(res[ii], str) and (ii == nl - 1):
            _fact, variable_names, label = extract_var(res[ii], variable_names,
                                                       label)
            fact = fact + _fact

    fact = fact + ")"

    return fact, variable_names, label


def extract_premise_var(res, variable_names, vars):
    nl = len(res)

    for ii in range(nl):
        if isinstance(res[ii], str) and (ii > 0) and (ii <= nl - 1):
            item = res[ii]
            vars.append(item)
            if item not in variable_names:
                variable_names[item] = "unknown"
            else:
                item = variable_names[item]

        elif not isinstance(res[ii], str) and (ii > 0) and (ii <= nl - 1):
            variable_names, vars = extract_premise_var(res[ii], variable_names,
                                                       vars)

    return variable_names, vars


def extract_var_simple(res, vars):
    nl = len(res)

    for ii in range(nl):
        if isinstance(res[ii], str) and (ii > 0) and (ii <= nl - 1):
            item = res[ii]
            vars.append(item)

        elif not isinstance(res[ii], str) and (ii > 0) and (ii <= nl - 1):
            vars = extract_var_simple(res[ii], vars)

    return vars


#print(extract_var_simple(kg_parser.parse('a(X, b(Y,Z))'), []))


def extract_element(res, vars):
    nl = len(res)

    for ii in range(nl):
        if isinstance(res[ii], str) and (ii > 0) and (ii <= nl - 1):
            item = res[ii]
            vars.append(item)

        elif not isinstance(res[ii], str) and (ii > 0) and (ii <= nl - 1):
            vars = extract_element(res[ii], vars)

    return vars


def matchUnify(premise, theta):
    #predicate, vars, theta2, hasUnified = matchUnify(premise[ii], theta)

    vars_ = []
    parse_premise = kg_parser.parse(premise)
    theta2, vars_ = extract_premise_var(parse_premise, theta, vars_)

    hasUnifed = []
    for key in vars_:
        if theta2[key] == 'unknown':
            hasUnifed.append(False)
        else:
            hasUnifed.append(True)

    return vars_, theta2, hasUnifed


def parse_predicates(rule_str):

    left_index = []
    right_index = []
    left_count = 0
    right_count = 0

    strset = []
    start_index = 0

    for ii in range(len(rule_str) - 1):
        if rule_str[ii] == "(":
            left_index.append(ii)
            left_count = left_count + 1
        elif rule_str[ii] == ")":
            right_index.append(ii)
            right_count = right_count + 1

        if right_count == left_count and left_count != 0 and (
                rule_str[ii + 1:].strip()[0] == ','
                or rule_str[ii + 1:].strip()[0] == '.'):

            _tmp = rule_str[start_index:ii + 1].strip()
            #pdb.set_trace()
            if _tmp[0] == "," or _tmp[0] == ".":
                _tmp = _tmp[1:]
            strset.append(_tmp.strip())
            start_index = ii + 1
            #left_count=0
            #right_count=0

    #pdb.set_trace()
    return strset


#test_str ="equals(measureOf(angle(A,B,F)),measureOf(angle(E,D,F))) :- parallel(line(A,B),line(D,E)), line(B, D), on_same_line(B, D, F), pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), pointPosition(F,Xf,Yf), (Xa-Xb)*(Xe-Xd)>0, (Ya-Yb)*(Ye-Yd)>0, (Xf-Xb)*(Xf-Xd)>0, (Yf-Yb)*(Yf-Yd)>0, not A==C."

#strset = parse_predicates(test_str)
#print(strset)
