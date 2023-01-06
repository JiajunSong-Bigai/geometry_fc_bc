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

