basic_path = "src/knowledge_base/basic_clingo.pl"
facts_path = "src/knowledge_base/facts_clingo.pl"
theorem_path = "src/knowledge_base/theorem_clingo.pl"
query_path = "src/knowledge_base/quest_clingo.pl"


def read():
    query_set = []
    f1 = open(query_path, "r")
    input = f1.readlines()
    for clause in input:
        if clause[0] != "%" and clause != "\n":
            query_set.append(clause.strip().replace("^", ","))
    f1.close()

    fact_set = []
    f1 = open(facts_path, "r")
    input = f1.readlines()
    for clause in input:
        if clause[0] != "%" and clause != "\n":
            fact_set.append(clause.strip().replace("^", ","))
    f1.close()

    theorem_set = []

    f1 = open(basic_path, "r")
    input = f1.readlines()
    for clause in input:
        if clause[0] != "%" and clause != "\n":
            theorem_set.append(clause.strip().replace("^", ","))
    f1.close()

    f1 = open(theorem_path, "r")
    input = f1.readlines()
    for clause in input:
        if clause[0] != "%" and clause != "\n":
            theorem_set.append(clause.strip().replace("^", ","))
    f1.close()

    return query_set, fact_set, theorem_set
