from src.input_reader import read_query, read_fact, read_rules
from src.generator import generate
from src.deductor import deduct

basic_path = "src/knowledge_base/basic_clingo.pl"
facts_path = "src/knowledge_base/facts_clingo.pl"
theorem_path = "src/knowledge_base/theorem_clingo.pl"
query_path = "src/knowledge_base/quest_clingo.pl"


def main():
    query_set = read_query(query_path)
    theorem_set = read_rules(basic_path, theorem_path)
    fact_set = read_fact(facts_path)

    gen_facts_dict, used_theorem_set = generate(query_set=query_set,
                                                fact_set=fact_set,
                                                theorem_set=theorem_set)

    undeduced_set, deduced_procedure_str = deduct(
        gen_facts_dict=gen_facts_dict,
        query_set=query_set,
        used_theorem_set=used_theorem_set,
        n_theorem=len(used_theorem_set))

    if len(undeduced_set) == 0:
        print("Proof finished!")

    for item in undeduced_set:
        if item not in gen_facts_dict[0]:
            print("Proof failed")
            break

    print("\n\n\nThe process of proving:----------------------------------")
    for item in undeduced_set:
        print(item)

    n_deduce_step = len(deduced_procedure_str)
    for ii in range(n_deduce_step - 1, -1, -1):
        for jj in range(len(deduced_procedure_str[ii]) - 1, -1, -1):
            print(deduced_procedure_str[ii][jj])


if __name__ == "__main__":
    main()
