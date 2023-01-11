% line definition
line(A,B) :- line(B,A).


% point & line
pointLiesOnLine(A,line(B,C)) :- pointLiesOnLine(A,line(C,B)).
pointLiesOnLine(A,line(B,C)) :- pointLiesOnLine(B,line(A,C)).
pointLiesOnLine(A,line(B,C)) :- on_same_line(A,B,C).

% on same line
on_same_line(A,B,C) :- pointLiesOnLine(A,line(B,C)).
on_same_line(A,C,B) :- on_same_line(A,B,C).
on_same_line(B,A,C) :- on_same_line(A,B,C).
on_same_line(C,A,B) :- on_same_line(A,B,C).
%on_same_line(A,C,D) :- on_same_line(A,B,C) ^ on_same_line(A,B,D) ^ not C==D.

%equals(lengthOf(line(A,C)),sumOf(lengthOf(line(A,B)),lengthOf(line(B,C)))) :- on_same_line(A,B,C)^ pointPosition(A, Xa, Ya)^ pointPosition(B, Xb, Yb)^ pointPosition(C, Xc, Yc)^ (Xb-Xa)*(Xb-Xc)<0.
%equals(lengthOf(line(A,C)),sumOf(lengthOf(line(B,A)),lengthOf(line(B,C)))) :- equals(lengthOf(line(A,C)),sumOf(lengthOf(line(A,B)),lengthOf(line(B,C)))).
%equals(lengthOf(line(A,C)),sumOf(lengthOf(line(A,B)),lengthOf(line(C,B)))) :- equals(lengthOf(line(A,C)),sumOf(lengthOf(line(A,B)),lengthOf(line(B,C)))).
%equals(lengthOf(line(A,C)),sumOf(lengthOf(line(B,C)),lengthOf(line(A,B)))) :- equals(lengthOf(line(A,C)),sumOf(lengthOf(line(A,B)),lengthOf(line(B,C)))).
%equals(sumOf(lengthOf(line(A,B)),lengthOf(line(C,D))), sumOf(lengthOf(line(X,Y)),lengthOf(line(Z,W)))) :- equals(lengthOf(line(A,B)),lengthOf(line(X,Y)))^ equals(lengthOf(line(C,D)),lengthOf(line(Z,W))).

% middle point
isMidpointOf(point(D),line(B,C)) :- isMidpointOf(point(D),line(C,B)).
on_same_line(A,B,C) :- isMidpointOf(point(A),line(B,C)).
equals(lengthOf(line(B,A)),lengthOf(line(A,C))) :- isMidpointOf(point(A),line(B,C)).


% flat angle
equals(sumOf(measureOf(angle(D,B,A)),measureOf(angle(D,B,C))),180) :- angle(D,B,A)^ angle(D,B,C)^ on_same_line(A,B,C)^ pointPosition(A,Xa,Ya)^ pointPosition(B,Xb,Yb)^ pointPosition(C,Xc,Yc)^ (Xb-Xa)*(Xb-Xc)<0.
equals(sumOf(measureOf(angle(D,E,F)),measureOf(angle(A,B,C))),X) :- equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))),X).
equals(sumOf(measureOf(angle(C,B,A)),measureOf(angle(D,E,F))),X) :- equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))),X).
equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(F,E,D))),X) :- equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))),X).
equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))) :- equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(G,H,I))),X)^ equals(sumOf(measureOf(angle(D,E,F)),measureOf(angle(J,K,L))),X)^ equals(measureOf(angle(G,H,I)),measureOf(angle(J,K,L)))^ not same_angle(angle(A,B,C),angle(D,E,F)).


% equal angle from same line
equals(measureOf(angle(A,B,C)),measureOf(angle(A,B,D))) :- angle(A,B,C)^ angle(A,B,D)^ on_same_line(B,C,D)^ pointPosition(B,Xb,Yb)^ pointPosition(C,Xc,Yc)^ pointPosition(D,Xd,Yd)^ (Xc-Xb)*(Xd-Xb)>0.


% equal angle 
equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))) :- equals(measureOf(angle(D,E,F)),measureOf(angle(A,B,C))).
equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))) :- equals(measureOf(angle(C,B,A)),measureOf(angle(D,E,F))).
equals(measureOf(angle(A,B,C)),X) :- equals(X, measureOf(angle(A,B,C))).
equals(measureOf(angle(H,I,J)),measureOf(angle(D,E,F))) :- equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F)))^ equals(measureOf(angle(A,B,C)),measureOf(angle(H,I,J)))^ not same_angle(angle(D,E,F), angle(H,I,J))^ angle(A,B,C)^ angle(D,E,F)^angle(H,I,J).
equals(measureOf(angle(D,E,F)),measureOf(angle(G,H,I))) :- equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))),X)^ equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(G,H,I))),X)^ not same_angle(angle(D,E,F),angle(G,H,I)).

equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))),X) :- equals(measureOf(angle(D,E,F)),measureOf(angle(G,H,I)))^ equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(G,H,I))),X)^ not same_angle(angle(D,E,F),angle(G,H,I)).
equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))),X) :- equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(G,H,I))),X)^ equals(measureOf(angle(G,H,I)),measureOf(angle(D,E,F))).


% same angle
same_angle(angle(A,B,C), angle(D,E,F)) :- angle(A,B,C)^ angle(D,E,F)^ B==E^ A==D^ F==C.
same_angle(angle(A,B,C), angle(D,E,F)) :- angle(A,B,C)^ angle(D,E,F)^ B==E^ C==D^ F==A.


% equal line length
equals(lengthOf(line(A,B)),lengthOf(line(D,E))) :- equals(lengthOf(line(B,A)),lengthOf(line(D,E)))^ line(A,B)^ line(D,E)^ not same_segment(line(A,B),line(D,E)).
equals(lengthOf(line(A,B)),lengthOf(line(D,E))) :- equals(lengthOf(line(D,E)),lengthOf(line(A,B)))^ line(A,B)^ line(D,E)^ not same_segment(line(A,B),line(D,E)).
equals(lengthOf(line(C,D)),lengthOf(line(E,F))) :- equals(lengthOf(line(A,B)),lengthOf(line(E,F)))^ equals(lengthOf(line(A,B)),lengthOf(line(C,D)))^ line(A,B)^ line(C,D)^ line(E,F)^ not same_segment(line(E,F),line(C,D)).


% same line
same_segment(line(A,B),line(C,D)) :- line(A,B)^ line(C,D)^ A==C^ B==D.
same_segment(line(A,B),line(C,D)) :- line(A,B)^ line(C,D)^ A==D^ B==C.
same_segment(line(A,B),line(A,B)) :- line(A,B).
same_segment(line(A,B),line(B,A)) :- line(A,B).

same_line(line(A,B),line(A,C)) :- line(A,B)^ line(A,C)^ on_same_line(A,B,C).
same_line(line(A,B),line(B,C)) :- line(A,B)^ line(A,C)^ on_same_line(A,B,C).
same_line(line(A,C),line(B,C)) :- line(A,B)^ line(A,C)^ on_same_line(A,B,C).
same_line(line(B,A),line(A,C)) :- line(A,B)^ line(A,C)^ on_same_line(A,B,C).
same_line(line(A,B),line(C,A)) :- line(A,B)^ line(A,C)^ on_same_line(A,B,C).

same_line(line(A,B),line(C,D)) :- on_same_line(A,B,C)^ on_same_line(B,C,D)^ line(A,B)^ line(C,D).

% same triangle
same_triangle(triangle(A,B,C),triangle(B,C,A)) :- triangle(A,B,C)^ triangle(B,C,A). 