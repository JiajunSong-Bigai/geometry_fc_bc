import re
from typing import Set, List
from clyngor import ASP, answer_set_to_str


class Rule(str):
    pass


class Fact(str):
    pass


class Quest(str):
    pass


def FCMachine(facts: Set[Fact], rules: Set[Rule]) -> Set[Fact]:
    facts_str = "".join(facts)
    rules_str = "".join(rules)
    answers = ASP(facts_str + rules_str)

    _answers = answer_set_to_str(next(answers)).split(" ")
    _answers = [ans + "." for ans in _answers]
    updated_facts = facts.union(set(_answers))

    return updated_facts


class ProofStep:

    def __init__(self, fact: Fact, rule: Rule, level: int) -> None:
        self.fact = fact
        self.rule = rule
        self.level = level

    @property
    def is_solved(self, given_facts: List[Fact]) -> bool:
        return self.fact in given_facts

    @property
    def premises(self) -> List[Fact]:
        char_dic = self._match_fact_and_rule(fact=self.fact, rule=self.rule)
        org_premises_str = self.rule.split(":-")[1]
        org_premises = self._split_premises(premises_str=org_premises_str)
        subed_premises = []
        for premise in org_premises:
            subed_premises.append(
                self._substitute_premise(premise=premise, char_dic=char_dic))
        return subed_premises

    def children(
            self,
            proofsteps_levels: List[List['ProofStep']]) -> List['ProofStep']:
        childs = []
        for premise in self.premises:
            print("searching for ", premise)
            cur_level = self.level - 1
            while cur_level >= 0:
                child = self._search_premises(premise,
                                              proofsteps_levels[cur_level])
                if child is not None:
                    childs.append(child)
                    break
                cur_level -= 1
        return childs

    @staticmethod
    def _search_premises(premise,
                         proofsteps: List['ProofStep']) -> 'ProofStep':
        for pstep in proofsteps:
            if pstep.fact == premise:
                return pstep
        return None

    @staticmethod
    def _match_fact_and_rule(fact: Fact, rule: Rule):
        fact = fact.rstrip(".")
        rule_fact, rule_premises = rule.split(":-")
        char_dic = {}

        assert len(fact) == len(rule_fact)

        for fchar, rchar in zip(fact, rule_fact):
            if fchar == rchar:
                continue
            char_dic[rchar] = fchar
        return char_dic

    @staticmethod
    def _substitute_premise(premise: str, char_dic: dict):
        # substitute for
        # point, line, angle, triangle
        regexs = [
            r"point\(.\)",
            r"line\(.,.\)",
            r"triangle\(.,.,.\)",
            r"angle\(.,.,.\)",
            r"quadrilateral\(.,.,.,.\)",
            r"parallelogram\(.,.,.,.\)",
        ]

        retrieved_objs = []
        for regex in regexs:
            matches = re.finditer(regex, premise, re.MULTILINE)
            retrieved_objs += [m.group() for m in matches]

        for retrieved_obj in retrieved_objs:
            replace_obj = "".join(char_dic[c] if c in char_dic else c
                                  for c in retrieved_obj)
            regex = ""
            for c in retrieved_obj:
                if c not in ["(", ")"]:
                    regex += c
                else:
                    regex += f"\\{c}"

            premise = re.sub(regex, replace_obj, premise, 0, re.MULTILINE)

        return premise + "."

    @staticmethod
    def _split_premises(premises_str: str):
        splited_premises = []
        start_premise = i = 0
        parent_stack = []
        while i < len(premises_str):
            if premises_str[i] not in ["(", ")"]:
                i += 1
                continue

            if premises_str[i] == "(":
                parent_stack.append("(")
            elif premises_str[i] == ")":
                parent_stack.pop()

            if not parent_stack:
                splited_premises.append(premises_str[start_premise:i + 1])
                start_premise = i + 2

            i += 1
        return splited_premises


##########################################################
### Step by Step facts generation
### Because the proving is hidden in the ASP fc machine
### incrementally feeding the rules
##########################################################

MAX_ITER_NUM = 10


def sbs_fc(facts: Set[Fact], rules: Set[Rule], quest: Quest):
    proofsteps = []
    iter_num = 0

    facts_latest = facts.copy()
    while iter_num < MAX_ITER_NUM:
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


############################################
##### Recover the proving process
###########################################


def recover_prove_tree():
    pass


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