from clyngor import ASP, answer_set_to_str


def generate(fact_set, theorem_set, query_set):

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
            new_fact_set = [fct for fct in fact_set if fct not in _answers
                            ] + _answers

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
    return gen_facts_dict, used_theorem_set
