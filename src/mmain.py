if __name__ == "__main__":
    # from src.input_reader import read
    # basic_path = "src/knowledge_base/basic_clingo.pl"
    # facts_path = "src/knowledge_base/facts_clingo.pl"
    # theorem_path = "src/knowledge_base/theorem_clingo.pl"
    # query_path = "src/knowledge_base/quest_clingo.pl"

    # quest, facts, rules = read(basic_path=basic_path,
    #                            query_path=query_path,
    #                            facts_path=facts_path,
    #                            theorem_path=theorem_path)
    # iter_num, proofsteps_levels, final_psteps = sbs_fc(set(facts), set(rules),
    #                                                    quest[0])
    # given_facts = facts

    # import pickle

    # with open("data/proofsteps_levels.pkl", "wb") as h:
    #     pickle.dump(proofsteps_levels, h)
    # with open("data/final_proofsteps.pkl", "wb") as h:
    #     pickle.dump(final_psteps, h)

    import pickle

    with open("data/proofsteps_levels.pkl", "rb") as h:
        proofsteps_levels = pickle.load(h)
    with open("data/final_proofsteps.pkl", "rb") as h:
        final_psteps = pickle.load(h)

    print(len(proofsteps_levels), final_psteps.level)
    print([len(ps) for ps in proofsteps_levels])

    print(final_psteps.rule)
    print(final_psteps.fact)
    print(final_psteps.premises)

    children = final_psteps.children(proofsteps_levels=proofsteps_levels)
    for child in children:
        print(child.fact)
        print(child.rule)