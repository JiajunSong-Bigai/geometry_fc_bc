import re
from typing import List


class Rule(str):
    pass


class Fact(str):
    pass


class Quest(str):
    pass


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
