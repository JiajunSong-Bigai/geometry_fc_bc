def read_query(query_path):
    query_set = []
    f1 = open(query_path, "r")
    input = f1.readlines()
    for clause in input:
        if clause[0] != "%" and clause != "\n":
            query_set.append(clause.strip().replace("^", ","))
    f1.close()

    return query_set


def read_rules(*rule_paths):
    rule_set = []
    for rule_path in rule_paths:
        f1 = open(rule_path, "r")
        input = f1.readlines()
        for clause in input:
            if clause[0] != "%" and clause != "\n":
                rule_set.append(clause.strip().replace("^", ","))
        f1.close()

    return rule_set


def read_fact(fact_path):
    fact_set = []
    f1 = open(fact_path, "r")
    input = f1.readlines()
    for clause in input:
        if clause[0] != "%" and clause != "\n":
            fact_set.append(clause.strip().replace("^", ","))
    f1.close()

    return fact_set


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
