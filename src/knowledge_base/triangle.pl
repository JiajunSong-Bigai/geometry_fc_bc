%basic

triangle(A,C,B) :- triangle(A,B,C).
triangle(B,A,C) :- triangle(A,B,C).
triangle(C,A,B) :- triangle(A,B,C).

line(A,B) :- triangle(A,B,C).
angle(A,B,C) :- triangle(A,B,C).


% middle parallel line
parallel(line(D,E),line(B,C)) :- triangle(A,B,C)^ isMidpointOf(point(D),line(A,B))^ isMidpointOf(point(E),line(A,C))^ line(D,E)^ not same_line(line(D,E),line(B,C)).
equals(mul(lengthOf(line(D,E)),2),lengthOf(line(B,C))):-triangle(A,B,C)^ isMidpointOf(point(D),line(A,B))^ isMidpointOf(point(E),line(A,C))^ line(D,E).
