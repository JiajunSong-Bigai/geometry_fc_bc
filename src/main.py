from sympy import *
from src.input_reader import read_query, read_fact, read_rules
from src.backward_chainer import bc
from src.forward_chainer import fc


def results_stdout(gen_facts_dict, undeduced_set, deduced_procedure_str):
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


def main(facts_path, query_path, rule_folder_path):

    query_set = read_query(query_path=query_path)
    fact_set = read_fact(fact_path=facts_path)
    theorem_set = read_rules(rule_folder_path=rule_folder_path)

    gen_facts_dict, used_theorem_set = fc(fact_set, theorem_set, query_set)
    undeduced_set, deduced_procedure_str = bc(gen_facts_dict, query_set,
                                              len(used_theorem_set),
                                              used_theorem_set)

    results_stdout(gen_facts_dict, undeduced_set, deduced_procedure_str)


if __name__ == "__main__":
    main(facts_path="examples/p2/facts.pl",
         query_path="examples/p2/quest.pl",
         rule_folder_path="src/knowledge_base")
