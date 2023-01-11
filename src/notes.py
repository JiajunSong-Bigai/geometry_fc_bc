"""
Rules: R1, R2, ... Rx
Facts: F1, F2, ... Fy
Quest: Q

Inference machine: f( Rules, Facts ) -> New Facts

Examples

1. 
Q   = R1( NF1, F3 )
    = R1( R2( F1, F2 ), F3 )


2. 
Q   = R2( NF1, F3 )
    = R2( R1( F1, F2 ), F3 )


# forward chaining

proofsteps = []

WHILE iter_num < max_iters:

    for each rule in Rules
        apply the rule and facts in the inference machine
        obtain new facts
    
    maintain proofsteps at step iter_num:
        a list of ProofStep(rule, fact, premises)  

    SOLVED = check(Q, a list of ProofSteps)

    UPDATE proofsteps

    if SOLVED:
        return iter_num, ProofStep

return UNSOLVED


# Recover the proving process

PATH = []
CUR_TO_SOLVE = [final_proofstep]

while CUR_TO_SOLVE AND not all(CUR_TO_SOLVE.is_solved):
    TMP = []
    for p in CUR_TO_SOLVE:
        IF NOT p.is_solve:
            TMP += p.children
    
    for p in TMP:
        PATH.append( PROVING_PROCESS(p) )
    
    CUR_TO_SOLVE = TMP

return PATH



class ProofStep:
    def __init__(self, fact: Fact, rule: Rule, level: int):
        self.fact = fact
        self.rule = rule
        self.level = level
    
    @property
    def premises(self) -> List[Fact]:
        return find_premises(self)
    
    @property
    def is_solved(self) -> bool:
        return self.fact in GIVEN_FACTS
    
    @property
    def children(self):
        # match the premises with the fact in proofsteps of
        # level self.level - 1 or lower
        return list()
"""