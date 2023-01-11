import os


def read_query(query_path):
    query_set = []
    f1 = open(query_path, "r")
    input = f1.readlines()
    for clause in input:
        if clause[0] != "%" and clause != "\n":
            query_set.append(clause.strip().replace("^", ","))
    f1.close()

    return query_set


def read_rules(rule_folder_path):
    rule_set = []
    rule_files = os.listdir(rule_folder_path)
    for rule_file in rule_files:
        f1 = open(os.path.join(rule_folder_path, rule_file), "r")
        input = f1.readlines()
        for clause in input:
            if clause[0] != "%" and clause != "\n":
                rule_set.append(clause.strip().replace("^", ","))
        f1.close()

    return list(set(rule_set))


def read_fact(fact_path):
    fact_set = []
    f1 = open(fact_path, "r")
    input = f1.readlines()
    for clause in input:
        if clause[0] != "%" and clause != "\n":
            fact_set.append(clause.strip().replace("^", ","))
    f1.close()

    return fact_set
