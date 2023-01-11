from src.utils import (generate_deduce_path, iterate_add_undeduced_facts)


def deduct(gen_facts_dict, query_set, n_theorem, used_theorem_set):
    """
    Args:
        gen_facts_dict: a list of generated facts. During the first iteration,
        each time one new theorem is added to the inference machine and
        facts are derived. For the second and more iterations, the fact will be
        updated to be the one at the last iteration.
        The generation process stops when the quest is found in the generated
        facts. Hence we acquire a list of generated facts.
    
    """

    # diff set
    #
    diff_set = []
    for i in range(n_theorem):
        tmp = [
            fact for fact in gen_facts_dict[i + 1]
            if fact not in gen_facts_dict[i]
        ]
        diff_set.append(tmp)

    deduced_procedure_str = []
    deduced_set = []
    undeduced_set = query_set
    nset = len(diff_set)

    for i in range(nset - 1, -1, -1):
        if diff_set[i] == []:
            continue

        print("deduced step: ", i)

        loop_index = 0
        while loop_index < len(undeduced_set):
            undeduced_fact = undeduced_set[loop_index]

            if undeduced_fact in gen_facts_dict[0]:
                del undeduced_set[loop_index]
                #loop_index = loop_index-1
                print("undeduced_fact in gen_facts_dict: ", undeduced_fact)
                continue

            if undeduced_fact in diff_set[i]:

                deduced_set.append(undeduced_fact)
                del undeduced_set[loop_index]

                rules, rules_dict_traj = iterate_add_undeduced_facts(
                    undeduced_fact, used_theorem_set[i], gen_facts_dict[i])

                print('len(undeduced_set) ', len(undeduced_set))
                print(undeduced_set)
                print(rules)
                deduce_path = generate_deduce_path(rules, rules_dict_traj,
                                                   undeduced_set,
                                                   gen_facts_dict[i])
                for _path in deduce_path:
                    print(_path + "\n")

                deduced_procedure_str.append(deduce_path)
                #loop_index = loop_index-1
                continue

            loop_index = loop_index + 1

    return undeduced_set, deduced_procedure_str


if __name__ == "__main__":
    from src.input_reader import read
    from src.generator import generate
    from src.deductor import deduct

    basic_path = "src/knowledge_base/basic_clingo.pl"
    facts_path = "src/knowledge_base/facts_clingo.pl"
    theorem_path = "src/knowledge_base/theorem_clingo.pl"
    query_path = "src/knowledge_base/quest_clingo.pl"

    query_set, fact_set, theorem_set = read(basic_path=basic_path,
                                            query_path=query_path,
                                            facts_path=facts_path,
                                            theorem_path=theorem_path)

    gen_facts_dict, used_theorem_set = generate(fact_set, theorem_set,
                                                query_set)

    undeduced_set, deduced_procedure_str = deduct(gen_facts_dict, query_set,
                                                  len(theorem_set),
                                                  used_theorem_set)
