% parallel
parallel(line(C,B),line(D,E)) :- parallel(line(B,C), line(D,E)).
parallel(line(B,C),line(D,E)) :- parallel(line(B,C), line(E,D)).
parallel(line(D,E),line(B,C)) :- parallel(line(B,C), line(D,E)).

parallel(line(B,C),line(D,E)) :- parallel(line(A,B),line(D,E))^ on_same_line(A,B,C)^ not same_line(line(B,C),line(D,E))^ not same_segment(line(B,C),line(D,E)).
parallel(line(A,B),line(C,D)) :- parallel(line(A,B),line(E,F))^ parallel(line(C,D),line(E,F))^ not same_line(line(A,B),line(C,D))^ not same_segment(line(A,B),line(C,D)).


% equal angle from parallel
equals(measureOf(angle(A,B,D)),measureOf(angle(B,D,E))) :- parallel(line(A,B),line(D,E))^ not A==D^ not B==D^ line(B, D)^ pointPosition(A,Xa,Ya)^ pointPosition(B,Xb,Yb)^ pointPosition(D,Xd,Yd)^ pointPosition(E,Xe,Ye)^ (Xa-Xb)*(Xe-Xd)<0.
equals(measureOf(angle(A,B,F)),measureOf(angle(E,D,F))) :- parallel(line(A,B),line(D,E))^ not A==F^ not E==F^ line(B, D)^ on_same_line(B, D, F)^ pointPosition(A,Xa,Ya)^ pointPosition(B,Xb,Yb)^ pointPosition(D,Xd,Yd)^ pointPosition(E,Xe,Ye)^ pointPosition(F,Xf,Yf)^ (Xa-Xb)*(Xe-Xd)>0^ (Xf-Xb)*(Xf-Xd)>0.

equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(B,C,D))),180) :- parallel(line(A,B),line(C,D))^ quadrilateral(A,B,C,D).

% parallel from equal angles
parallel(line(A,B),line(D,E)) :- equals(measureOf(angle(A,B,D)),measureOf(angle(B,D,E)))^ quadrilateral(A,B,E,D).