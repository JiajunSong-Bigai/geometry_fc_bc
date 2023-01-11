% basic

equals(measureOf(angle(A,B,C)),measureOf(angle(A,C,B))) :- triangle(A,B,C)^ equals(lengthOf(line(A,B)),lengthOf(line(A,C))).