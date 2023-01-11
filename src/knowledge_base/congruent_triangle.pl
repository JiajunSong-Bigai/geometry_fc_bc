% congruent triangles

% basic
congruent(triangle(A,C,B),triangle(D,F,E)) :- congruent(triangle(A,B,C),triangle(D,E,F)).
congruent(triangle(B,A,C),triangle(E,D,F)) :- congruent(triangle(A,B,C),triangle(D,E,F)).
congruent(triangle(C,A,B),triangle(F,D,E)) :- congruent(triangle(A,B,C),triangle(D,E,F)).
congruent(triangle(D,E,F),triangle(A,B,C)) :- congruent(triangle(A,B,C),triangle(D,E,F)).

% 性质
equals(lengthOf(line(A,B)),lengthOf(line(D,E))) :- congruent(triangle(A,B,C),triangle(D,E,F))^ not same_segment(line(A,B),line(D,E)).
equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))) :- congruent(triangle(A,B,C),triangle(D,E,F))^ not same_angle(angle(A,B,C),angle(D,E,F)).

% 判定
congruent(triangle(A,B,C),triangle(D,E,F)) :- triangle(A,B,C)^ triangle(D,E,F)^ equals(lengthOf(line(A,B)),lengthOf(line(D,E)))^ equals(lengthOf(line(B,C)),lengthOf(line(E,F)))^ equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F)))^ not same_triangle(triangle(A,B,C),triangle(D,E,F)).
congruent(triangle(A,B,C),triangle(D,E,F)) :- triangle(A,B,C)^ triangle(D,E,F)^ equals(lengthOf(line(A,B)),lengthOf(line(D,E)))^ equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F)))^ equals(measureOf(angle(C,A,B)),measureOf(angle(F,D,E)))^ not same_triangle(triangle(A,B,C),triangle(D,E,F)).
congruent(triangle(A,B,C),triangle(D,E,F)) :- triangle(A,B,C)^ triangle(D,E,F)^ equals(lengthOf(line(A,B)),lengthOf(line(D,E)))^ equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F)))^ equals(measureOf(angle(B,C,A)),measureOf(angle(E,F,D)))^ not same_triangle(triangle(A,B,C),triangle(D,E,F)).
congruent(triangle(A,B,C),triangle(D,E,F)) :- triangle(A,B,C)^ triangle(D,E,F)^ equals(lengthOf(line(A,B)),lengthOf(line(D,E)))^ equals(lengthOf(line(B,C)),lengthOf(line(E,F)))^ equals(lengthOf(line(C,A)),lengthOf(line(F,D)))^ not same_triangle(triangle(A,B,C),triangle(D,E,F)).
congruent(triangle(A,B,C),triangle(D,E,F)) :- triangle(A,B,C)^ triangle(D,E,F)^ equals(measureOf(angle(A,B,C)),90)^ equals(measureOf(angle(D,E,F)),90)^ equals(lengthOf(line(A,B)),lengthOf(line(D,E)))^equals(lengthOf(line(A,C)),lengthOf(line(D,F))) ^ not same_triangle(triangle(A,B,C),triangle(D,E,F)).
