from clyngor import ASP, answer_set_to_str


def generate(fact_set, theorem_set, query_set):
    used_theorem_set = []
    n_theorem = len(theorem_set)
    gen_facts_dict = []
    gen_facts_dict.append(fact_set)
    max_n_iter = 10
    i = 0

    while True and i < max_n_iter:
        print("iteration ...... " + str(i + 1))
        print(f"Facts from {len(fact_set)}", end=" ")

        for j in range(n_theorem):
            fact_str = "".join(fact_set)

            answers = ASP(fact_str + theorem_set[j])
            used_theorem_set.append(theorem_set[j])

            _answers = answer_set_to_str(next(answers)).split(" ")
            _answers = [ans + "." for ans in _answers]

            new_fact_set = list(set(fact_set + _answers))
            gen_facts_dict.append(new_fact_set)

            fact_set = new_fact_set

            for query in query_set:
                if query in _answers:

                    n_steps = len(gen_facts_dict)
                    n_theorem = len(used_theorem_set)
                    assert n_steps == n_theorem + 1

                    print(f"\nStopped at iteration {i} and theorem {j}.")

                    return gen_facts_dict, used_theorem_set

        print(f"to {len(fact_set)}")

        i = i + 1

    raise ValueError("Proof unsolved!")


if __name__ == "__main__":
    from src.input_reader import read
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
    print(len(gen_facts_dict), len(used_theorem_set))