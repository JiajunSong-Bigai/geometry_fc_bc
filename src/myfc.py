from typing import Set
from clyngor import ASP, answer_set_to_str
from src.primitives import Fact, Rule, Quest, ProofStep


def FCMachine(facts: Set[Fact], rules: Set[Rule]) -> Set[Fact]:
    facts_str = "".join(facts)
    rules_str = "".join(rules)
    answers = ASP(facts_str + rules_str)

    _answers = answer_set_to_str(next(answers)).split(" ")
    _answers = [ans + "." for ans in _answers]
    updated_facts = facts.union(set(_answers))

    return updated_facts


##########################################################
### Step by Step facts generation
### incrementally feeding the rules
##########################################################


def sbs_fc(facts: Set[Fact],
           rules: Set[Rule],
           quest: Quest,
           max_iter_num: int = 100):
    proofsteps = []
    iter_num = 0

    facts_latest = facts.copy()
    while iter_num < max_iter_num:
        print(f"Iteration {iter_num}")
        print(f"Facts from {len(facts)}", end=" ")

        proofsteps_curlevel = []
        for rule in rules:
            new_facts = FCMachine(facts, {rule})

            for fact in new_facts:
                if fact in facts:
                    continue

                proofsteps_curlevel.append(
                    ProofStep(fact=fact, rule=rule, level=iter_num))
                facts_latest = facts_latest.union(new_facts)

            if quest in new_facts:
                print(f"to {len(facts_latest)}.\n")
                print(f"Found at iteration {iter_num}.")
                print(f"Using the rule {rule}")
                print(
                    f"Meanwhile {sum(len(ps) for ps in proofsteps)} proofsteps are produced."
                )

                return iter_num, proofsteps, ProofStep(fact=quest,
                                                       rule=rule,
                                                       level=iter_num)

        facts = facts_latest
        proofsteps.append(proofsteps_curlevel)

        print(f"to {len(facts_latest)}.\n")

        iter_num += 1

    raise ValueError("Problem unsolved!")
