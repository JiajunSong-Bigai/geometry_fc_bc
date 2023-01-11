import pytest

from src.mmain import ProofStep


@pytest.mark.skip()
def test01():
    list_of_premises = [
        "line(A,B),line(C,D).",
        "triangle(A,B,C),isMidpointOf(point(D),line(A,B)),isMidpointOf(point(E),line(A,C)),line(D,E).",
        "parallel(line(A,B),line(C,D)).",
        "parallel(line(A,B),line(C,D)),areAlternateInteriorangles(angle(A,B,C),angle(B,C,D)).",
        "triangle(A,B,C),equals(lengthOf(line(A,B))).",
        "line(A,B),line(C,D),areAlternateInteriorangles(angle(A,B,C),angle(B,C,D)),equals(measureOf(angle(A,B,C)),measureOf(angle(B,C,D)))."
    ]

    for premises in list_of_premises:
        print(premises)
        print(ProofStep._split_premises(premises_str=premises), "\n\n")


def test02():
    list_of_fact_and_rule = [
        [
            "similar(triangle(c,a,f),triangle(c,e,d)).",
            "similar(triangle(A,D,E),triangle(A,B,C)):-triangle(A,B,C),pointLiesOnline(point(D),line(A,B)),pointLiesOnline(point(E),line(A,C)),parallel(line(D,E),line(B,C))."
        ],
        [
            "equals(measureOf(angle(a,c,f)),measureOf(angle(a,d,e))).",
            "equals(measureOf(angle(E,A,B)),measureOf(angle(E,C,D))):-parallel(line(A,B),line(C,D)),intersectAt(line(E,C),line(A,B),point(A)),areCorrespondingangles(angle(E,A,B),angle(E,C,D))."
        ]
    ]

    for (fact, rule) in list_of_fact_and_rule:
        pstep = ProofStep(fact=fact, rule=rule, level=-1)
        print(pstep.premises)