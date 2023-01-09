import os
import json
import time
import random

import operator
import numbers
import pkg_resources
from collections import OrderedDict
import numpy as np
import pickle

from clyngor import ASP, solve, answer_set_to_str
from clyngor import grounded_program, solve_from_grounded
# from explain import bk_explain
import sympy
from sympy import *
import pdb

from src.input_reader import read
from src.utils import (test_and_subst, test_and_subst_assign,
                       test_and_subst_assign_generate, add_undeduced_facts,
                       iterate_add_undeduced_facts, single_step_forward,
                       generate_deduce_path)
from src.uutils import isNumber

query_set, fact_set, theorem_set = read()

used_theorem_set = []
n_theorem = len(theorem_set)
gen_facts_dict = []
gen_facts_dict.append(fact_set)
n_iter = 10000

for ii in range(n_iter):
    solved_again = False
    print("iteration ...... " + str(ii + 1))

    for jj in range(n_theorem):
        print("      theorem ...... " + str(jj + 1) + "   facts ...... " +
              str(len(fact_set)))

        solved = False
        fact_str = ""
        for _str in fact_set:
            fact_str = fact_str + _str

        answers = ASP(fact_str + theorem_set[jj])
        used_theorem_set.append(theorem_set[jj])

        _answers = []
        for answer in answers:
            _answers = answer_set_to_str(answer).split(" ")
            break

        _answers = [ans + "." for ans in _answers]
        new_fact_set = [fct
                        for fct in fact_set if fct not in _answers] + _answers

        gen_facts_dict.append(new_fact_set)
        fact_set = new_fact_set

        for query in query_set:
            if query in _answers:
                solved = True
                break

        if solved:
            solved_again = True
            print("solved!")
            break

    if solved_again:
        break

nsteps = len(gen_facts_dict)
n_theorem = len(used_theorem_set)

if nsteps != n_theorem + 1:
    print("failed!")

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

if len(undeduced_set) == 0:
    print("Proof finished!")
else:
    for item in undeduced_set:
        if item not in gen_facts_dict[0]:
            print("Proof failed")
            break
    print("Proof finished!")

print("The process of proving:----------------------------------")
for item in undeduced_set:
    print(item)

n_deduce_step = len(deduced_procedure_str)
for ii in range(n_deduce_step - 1, -1, -1):
    for jj in range(len(deduced_procedure_str[ii]) - 1, -1, -1):
        print(deduced_procedure_str[ii][jj])
