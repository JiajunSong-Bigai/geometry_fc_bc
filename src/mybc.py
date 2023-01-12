"""
## High level inputs and output

Inputs
    1. Rule. e.g.
        (1) parallel(line(A,C),line(D,E)) :- parallel(line(A,B),line(D,E)), on_same_line(A,B,C).
        (2) equals(measureOf(angle(A,B,C)),measureOf(angle(D,B,E))) :- line(A,B), line(B,C), line(D,B), line(B,E), not on_same_line(A,B,C), not on_same_line(D,B,E), on_same_line(A, B, D), on_same_line(B, C, E), pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), pointPosition(C,Xc,Yc), (Xa-Xb)*(Xd-Xb)>=0, (Ya-Yb)*(Yd-Yb)>=0, (Xc-Xb)*(Xe-Xb)>=0, (Yc-Yb)*(Ye-Yb)>=0, not same_angle_from_line(line(A,B), line(B,C), line(D,B), line(B,E)).
    
    2. Quest: the fact to prove
        (1) parallel(line(d,e),line(a,c)).
        (2) equals(measureOf(angle(e,a,c)),measureOf(angle(d,a,b))).
    
    3. Facts: A list of facts

    x. Assumed: The quest can be derived with the rule and the facts. The question is how.


Output
    1. the unification character dictionary/ theta




## Algorithm

AND: all the premises must conform to the theta
OR : only one of the rule satisfies


We can omit the OR part as we know the rule for each facts.


def AND( proofsteps, goals, theta ):
    '''
    Args:
        proofsteps: A list of ProofStep(rule: Rule(Fact_head, Fact_bodies) , fact: Fact)
        goals: a list of premises
        theta: a dictionary with key value pairs of (variable, instantination)
    
    Returns:
        theta that suffices all the goals
    '''

    if theta is None:
        pass

    elif not goals:
        yield theta

    first, rest = goals[0], goals[1:]

    theta1 = update_theta( first, theta )
    for theta2 in AND( proofsteps, rest, theta1 ):
        yield theta2


* Deal with negation

"""