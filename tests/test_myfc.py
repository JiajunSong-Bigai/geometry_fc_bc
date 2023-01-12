import pytest

from src.myfc import sbs_fc
from src.input_reader import read_fact, read_query, read_rules


@pytest.fixture()
def rules():
    return read_rules(rule_folder_path="src/old_kb")


@pytest.fixture()
def facts_1():
    return read_fact(fact_path="examples/p1/facts.pl")


@pytest.fixture()
def quest_1():
    return read_query(query_path="examples/p1/quest.pl")


@pytest.fixture()
def facts_2():
    return read_fact(fact_path="examples/p2/facts.pl")


@pytest.fixture()
def quest_2():
    return read_query(query_path="examples/p1/quest.pl")


@pytest.mark.skip()
def test_p1(facts_1, rules, quest_1):
    sbs_fc(facts=facts_1, rules=rules, quest=quest_1)


def test_p2(facts_2, rules, quest_2):
    print(len(rules))
    sbs_fc(facts=facts_2, rules=rules, quest=quest_2)
