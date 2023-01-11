import pytest

from src.mmain import FCMachine


def test01():
    from src.input_reader import read
    basic_path = "src/knowledge_base/basic_clingo.pl"
    facts_path = "src/knowledge_base/facts_clingo.pl"
    theorem_path = "src/knowledge_base/theorem_clingo.pl"
    query_path = "src/knowledge_base/quest_clingo.pl"

    quest, facts, rules = read(basic_path=basic_path,
                               query_path=query_path,
                               facts_path=facts_path,
                               theorem_path=theorem_path)

    FCMachine(facts, rules)