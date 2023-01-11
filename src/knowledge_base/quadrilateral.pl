% basic

line(A,B) :- quadrilateral(A,B,C,D).
angle(A,B,C) :- quadrilateral(A,B,C,D).

quadrilateral(B,C,D,A) :- quadrilateral(A,B,C,D).
quadrilateral(A,D,C,B) :- quadrilateral(A,B,C,D).

%34.四边形内角和360
equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(B,C,D)),measureOf(angle(C,D,A)),measureOf(angle(D,A,B))),360):-quadrilateral(A,B,C,D).
