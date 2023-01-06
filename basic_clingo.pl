line(A, B) :- line(B, A).

% point & line
pointLiesOnLine(A, line(B,C)) :- pointLiesOnLine(A, line(C,B)).
pointLiesOnLine(A, line(B,C)) :- pointLiesOnLine(B, line(A,C)).


on_same_line(A, B, C) :- pointLiesOnLine(A, line(B,C)).
on_same_line(A, B, C) :- on_same_line(B, C, A).
on_same_line(A, B, C) :- on_same_line(C, B, A).
on_same_line(A, B, C) :- on_same_line(B, A, C).
on_same_line(A, C, D) :- on_same_line(A, B,C), on_same_line(A, B,D), not C==D.

% middle point
isMidpointOf(point(D),line(B,C)) :- isMidpointOf(point(D),line(C,B)).

% triangle & quadrilateral
triangle(A,B,C) :- point(A), point(B), point(C), line(A,B), line(C,B), line(A,C), not A==B, not A==C, not B==C, not on_same_line(A, B,C).
quadrilateral(A,B,C,D) :- point(A), point(B), point(C), point(D), line(A,B), line(B,C), line(C,D), line(A,D), not A==B, not A==C, not A==D, not B==C, not B==D, not C==D, not on_same_line(A, B,C), not on_same_line(B,C,D), not on_same_line(A,C,D), not on_same_line(A,B,D).

% parallel
parallel(line(B,C),line(D,E)) :- parallel(line(B,C), line(E,D)).
parallel(line(B,C),line(D,E)) :- parallel(line(C,B), line(D,E)).
parallel(line(D,E),line(B,C)) :- parallel(line(B,C), line(D,E)).
parallel(line(A,C),line(D,E)) :- parallel(line(A,B),line(D,E)), on_same_line(A, B, C).
parallel(line(B,C),line(D,E)) :- parallel(line(A,B),line(D,E)), on_same_line(A, B, C).

% angle from parallel
pointPosition(A,X,Y) :- isMidpointOf(point(A),line(B,C)), pointPosition(B,X1,Y1), pointPosition(C,X2,Y2), X=(X1+X2)/2, Y=(Y1+Y2)/2.
equals(measureOf(angle(A,B,D)),measureOf(angle(B,D,E))) :- parallel(line(A,B),line(D,E)), line(B, D), pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), (Xa-Xb)*(Xe-Xd)<0, (Ya-Yb)*(Ye-Yd)<0.
equals(measureOf(angle(A,B,F)),measureOf(angle(E,D,F))) :- parallel(line(A,B),line(D,E)), line(B, D), on_same_line(B, D, F), pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), pointPosition(F,Xf,Yf), (Xa-Xb)*(Xe-Xd)>0, (Ya-Yb)*(Ye-Yd)>0, (Xf-Xb)*(Xf-Xd)>0, (Yf-Yb)*(Yf-Yd)>0.

% equal line length
equals(lengthOf(line(A,B)),lengthOf(line(D,E))) :- equals(lengthOf(line(B,A)),lengthOf(line(D,E))).
equals(lengthOf(line(A,B)),lengthOf(line(D,E))) :- equals(lengthOf(line(D,E)),lengthOf(line(A,B))).

same_line(line(A,B), line(C,D)) :- line(A,B), line(C,D), A==C, B==D.
same_line(line(A,B), line(C,D)) :- line(A,B), line(C,D), A==D, B==C.

equals(lengthOf(line(C,D)),lengthOf(line(E,F))) :- equals(lengthOf(line(A,B)),lengthOf(line(E,F))), equals(lengthOf(line(A,B)),lengthOf(line(C,D))), not same_line(line(E,F), line(C,D)).
equals(lengthOf(line(E,F)),lengthOf(line(G,H))) :- equals(lengthOf(line(A,B)),lengthOf(line(C,D))), equals(mul(lengthOf(line(E,F)),X),lengthOf(line(C,D))), equals(mul(lengthOf(line(G,H)),X),lengthOf(line(A,B))).

% equal angle 
equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))) :- equals(measureOf(angle(D,E,F)),measureOf(angle(A,B,C))).
equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))) :- equals(measureOf(angle(C,B,A)),measureOf(angle(D,E,F))).
% equals(measureOf(angle(A,B,C)),X) :- equals(X, measureOf(angle(A,B,C))).

equals(measureOf(angle(A,B,C)),measureOf(angle(D,B,E))) :- line(A,B), line(B,C), line(D,B), line(B,E), not on_same_line(A,B,C), not on_same_line(D,B,E), on_same_line(A, B, D), on_same_line(B, C, E), pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), pointPosition(C,Xc,Yc), (Xa-Xb)*(Xd-Xb)>=0, (Ya-Yb)*(Yd-Yb)>=0, (Xc-Xb)*(Xe-Xb)>=0, (Yc-Yb)*(Ye-Yb)>=0, not same_angle_from_line(line(A,B), line(B,C), line(D,B), line(B,E)).
equals(measureOf(angle(A,B,C)),measureOf(angle(D,B,E))) :- line(A,B), line(B,C), line(D,B), line(B,E), not on_same_line(A,B,C), not on_same_line(D,B,E), A==D, on_same_line(B, C, E), pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), pointPosition(C,Xc,Yc), (Xa-Xb)*(Xd-Xb)>=0, (Ya-Yb)*(Yd-Yb)>=0, (Xc-Xb)*(Xe-Xb)>=0, (Yc-Yb)*(Ye-Yb)>=0, not same_angle_from_line(line(A,B), line(B,C), line(D,B), line(B,E)).
equals(measureOf(angle(A,B,C)),measureOf(angle(D,B,E))) :- line(A,B), line(B,C), line(D,B), line(B,E), not on_same_line(A,B,C), not on_same_line(D,B,E), on_same_line(A, B, D), C==E, pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), pointPosition(C,Xc,Yc), (Xa-Xb)*(Xd-Xb)>=0, (Ya-Yb)*(Yd-Yb)>=0, (Xc-Xb)*(Xe-Xb)>=0, (Yc-Yb)*(Ye-Yb)>=0, not same_angle_from_line(line(A,B), line(B,C), line(D,B), line(B,E)).

% same_angle_from_angle(measureOf(angle(A,B,C)),measureOf(angle(D,B,E))) :- line(A,B), line(B,C), line(D,B), line(B,E), not on_same_line(A,B,C), not on_same_line(D,B,E), on_same_line(A, B, D), on_same_line(B, C, E), pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), pointPosition(C,Xc,Yc), (Xa-Xb)*(Xd-Xb)>=0, (Ya-Yb)*(Yd-Yb)>=0, (Xc-Xb)*(Xe-Xb)>=0, (Yc-Yb)*(Ye-Yb)>=0, not same_angle_from_line(line(A,B), line(B,C), line(D,B), line(B,E)).
% same_angle_from_angle(measureOf(angle(A,B,C)),measureOf(angle(D,B,E))) :- line(A,B), line(B,C), line(D,B), line(B,E), not on_same_line(A,B,C), not on_same_line(D,B,E), A==D, on_same_line(B, C, E), pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), pointPosition(C,Xc,Yc), (Xa-Xb)*(Xd-Xb)>=0, (Ya-Yb)*(Yd-Yb)>=0, (Xc-Xb)*(Xe-Xb)>=0, (Yc-Yb)*(Ye-Yb)>=0, not same_angle_from_line(line(A,B), line(B,C), line(D,B), line(B,E)).
% same_angle_from_angle(measureOf(angle(A,B,C)),measureOf(angle(D,B,E))) :- line(A,B), line(B,C), line(D,B), line(B,E), not on_same_line(A,B,C), not on_same_line(D,B,E), on_same_line(A, B, D), C==E, pointPosition(A,Xa,Ya), pointPosition(B,Xb,Yb), pointPosition(D,Xd,Yd), pointPosition(E,Xe,Ye), pointPosition(C,Xc,Yc), (Xa-Xb)*(Xd-Xb)>=0, (Ya-Yb)*(Yd-Yb)>=0, (Xc-Xb)*(Xe-Xb)>=0, (Yc-Yb)*(Ye-Yb)>=0, not same_angle_from_line(line(A,B), line(B,C), line(D,B), line(B,E)).

angle(A,B,C) :- equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))).
angle(D,E,F) :- equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))).

same_angle(angle(A,B,C), angle(D,E,F)) :- angle(A,B,C), angle(D,E,F), B==E, A==D, F==C.
same_angle(angle(A,B,C), angle(D,E,F)) :- angle(A,B,C), angle(D,E,F), B==E, C==D, F==A.

same_angle_from_line(line(A,B), line(B,C), line(D,B), line(B,E)) :- same_line(line(A,B), line(D,B)), same_line(line(B,C), line(B,E)), not on_same_line(A,B,C).

equals(measureOf(angle(H,I,J)),measureOf(angle(D,E,F))):-equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))),equals(measureOf(angle(A,B,C)),measureOf(angle(H,I,J))),not same_angle(angle(D,E,F),angle(H,I,J)).


