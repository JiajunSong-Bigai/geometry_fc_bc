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