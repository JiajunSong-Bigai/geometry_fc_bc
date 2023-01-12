
parallel(line(D,E),line(B,C)):-triangle(A,B,C),isMidpointOf(point(D),line(A,B)),isMidpointOf(point(E),line(A,C)),line(D,E).
equals(mul(lengthOf(line(D,E)),2),lengthOf(line(B,C))):-triangle(A,B,C),isMidpointOf(point(D),line(A,B)),isMidpointOf(point(E),line(A,C)),line(D,E).

%三、相似三角形
%A.性质
%11.相似三角形对应角相等，对应边成比例
equals(div(lengthOf(line(A,B)),lengthOf(line(D,E))),div(lengthOf(line(B,C)),lengthOf(line(E,F)))):-similar(triangle(A,B,C),triangle(D,E,F)).
equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))):-similar(triangle(A,B,C),triangle(D,E,F)).
%B.判定
%12.平行于三角形一边的直线和其他两边(或两边的延长线）相交所构成的三角形与原三角形相似
similar(triangle(A,D,E),triangle(A,B,C)):-triangle(A,B,C),pointLiesOnline(point(D),line(A,B)),pointLiesOnline(point(E),line(A,C)),parallel(line(D,E),line(B,C)).
%13.如果一个三角形的两个角与另一个三角形的两个角对应相等,那么这两个三角形相似
similar(triangle(A,B,C),triangle(D,E,F)):-triangle(A,B,C),triangle(D,E,F),equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))),equals(measureOf(angle(B,C,A)),measureOf(angle(E,F,D))).
%14.如果一个三角形的两条边与另一个三角形的两条边对应成比例,且对应夹角相等，那么这两个三角形相似
similar(triangle(A,B,C),triangle(D,E,F)):-equals(div(lengthOf(line(A,B)),lengthOf(line(D,E))),div(lengthOf(line(B,C)),lengthOf(line(E,F)))),equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))).
%15.如果一个三角形的三条边与另一个三角形的三条边对应成比例，那么这两个三角形相似
similar(triangle(A,B,C),triangle(D,E,F)):-equals(div(lengthOf(line(A,B)),lengthOf(line(D,E))),div(lengthOf(line(B,C)),lengthOf(line(E,F)))),equals(div(lengthOf(line(B,C)),lengthOf(line(E,F))),div(lengthOf(line(C,A)),lengthOf(line(F,D)))).


%六、等腰三角形
%26.等边对等角
equals(measureOf(angle(A,B,C)),measureOf(angle(A,C,B))):-triangle(A,B,C),equals(lengthOf(line(A,B)),lengthOf(line(A,C))).
%27.等角对等边
equals(lengthOf(line(A,B)),lengthOf(line(A,C))):-triangle(A,B,C),equals(measureOf(angle(A,B,C)),measureOf(angle(A,C,B))).
%28.等腰三角形底边的中线也是该边的高线和顶角角平分线
perpendicular(line(A,D),line(B,C)):-triangle(A,B,C),equals(lengthOf(line(A,B)),lengthOf(line(A,C))),isMidpointOf(point(D),line(B,C)),line(A,D).
bisectsangle(line(A,D),angle(B,A,C)):-triangle(A,B,C),equals(lengthOf(line(A,B)),lengthOf(line(A,C))),isMidpointOf(point(D),line(B,C)),line(A,D).
%29.等腰三角形底边的高线也是该边的中线和顶角角平分线
isMidpointOf(point(D),line(B,C)):-triangle(A,B,C),equals(lengthOf(line(A,B)),lengthOf(line(A,C))),pointLiesOnline(point(D),line(B,C)),perpendicular(line(A,D),line(B,C)).
bisectsangle(line(A,D),angle(B,A,C)):-triangle(A,B,C),equals(lengthOf(line(A,B)),lengthOf(line(A,C))),pointLiesOnline(point(D),line(B,C)),perpendicular(line(A,D),line(B,C)).
%30.等腰三角形顶角角平分线也是底边的中线和高线
isMidpointOf(point(D),line(B,C)):-triangle(A,B,C),equals(lengthOf(line(A,B)),lengthOf(line(A,C))),pointLiesOnline(point(D),line(B,C)),bisectsangle(line(A,D),angle(B,A,C)).
perpendicular(line(A,D),line(B,C)):-triangle(A,B,C),equals(lengthOf(line(A,B)),lengthOf(line(A,C))),pointLiesOnline(point(D),line(B,C)),bisectsangle(line(A,D),angle(B,A,C)).


%十二、相交线和平行线
%A.性质
%56.两直线平行，内错角相等
equals(measureOf(angle(A,B,C)),measureOf(angle(B,C,D))):-parallel(line(A,B),line(C,D)),areAlternateInteriorangles(angle(A,B,C),angle(B,C,D)).
%57.两直线平行，同位角相等
equals(measureOf(angle(E,A,B)),measureOf(angle(E,C,D))):-parallel(line(A,B),line(C,D)),intersectAt(line(E,C),line(A,B),point(A)),areCorrespondingangles(angle(E,A,B),angle(E,C,D)).
%58.两直线平行，同旁内角互补
equals(sumOf(measureOf(angle(B,A,C)),measureOf(angle(A,C,D))),180):-parallel(line(A,B),line(C,D)),areSameSideInteriorangles(angle(B,A,C),angle(A,C,D)).
%59.对顶角相等
equals(measureOf(angle(A,O,C)),measureOf(angle(B,O,D))):-intersectAt(line(A,B),line(C,D),point(O)), not A==C, not A==D, not B==C, not B==D, not A==O, not O==D, not B==O, not C==O.
%60.补角之和为180度：直线AB、OC交于点O，O在A、B之间，则$\angle AOC + \angle BOC = 180^{\circ}$
equals(sumOf(measureOf(angle(A,O,C)),measureOf(angle(B,O,C))),180):-pointLiesOnline(point(O),line(A,B)),intersectAt(line(A,B),line(O,C),point(O)).
%61.一条线段的垂直平分线上任意一点到线段两端距离相等
equals(lengthOf(line(G,B)),lengthOf(line(G,C))):-pointLiesOnline(point(E),line(B,C)),equals(lengthOf(line(B,E)),lengthOf(line(C,E))),perpendicular(line(G,E),line(B,C)),line(G,B),line(G,C).
%B.判定
%62.内错角相等，两直线平行
parallel(line(A,B),line(C,D)):-line(A,B),line(C,D),areAlternateInteriorangles(angle(A,B,C),angle(B,C,D)),equals(measureOf(angle(A,B,C)),measureOf(angle(B,C,D))).
%63.同位角相等，两直线平行
parallel(line(A,B),line(C,D)):-line(A,B),line(C,D),intersectAt(line(E,C),line(A,B),point(A)),areCorrespondingangles(angle(E,A,B),angle(E,C,D)),equals(measureOf(angle(E,A,B)),measureOf(angle(E,C,D))).
%64.同旁内角互补，两直线平行
parallel(line(A,B),line(C,D)):-line(A,B),line(C,D),line(A,C),areSameSideInteriorangles(angle(B,A,C),angle(A,C,D)),equals(sumOf(measureOf(angle(B,A,C)),measureOf(angle(A,C,D))),180).




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


