%平行四边形

quadrilateral(A,B,C,D) :- parallelogram(A,B,C,D).

parallelogram(B,C,D,A) :- parallelogram(A,B,C,D).
parallelogram(C,D,A,B) :- parallelogram(A,B,C,D).
parallelogram(D,A,B,C) :- parallelogram(A,B,C,D).


%35.平行四边形的两组对边分别平行
parallel(line(A,B),line(C,D)):-parallelogram(A,B,C,D).
parallel(line(A,D),line(B,C)):-parallelogram(A,B,C,D).

%36.平行四边形的两组对边分别相等
equals(lengthOf(line(A,B)),lengthOf(line(C,D))):-parallelogram(A,B,C,D).
equals(lengthOf(line(A,D)),lengthOf(line(B,C))):-parallelogram(A,B,C,D).

%37.平行四边形的对角相等
equals(measureOf(angle(A,B,C)),measureOf(angle(C,D,A))):-parallelogram(A,B,C,D).
equals(measureOf(angle(B,C,D)),measureOf(angle(D,A,B))):-parallelogram(A,B,C,D).



%判定
%39.两组对边分别平行的四边形是平行四边形
parallelogram(A,B,C,D):-parallel(line(A,B),line(C,D))^ parallel(line(A,D),line(B,C))^ quadrilateral(A,B,C,D).

%40.两组对边分别相等的四边形是平行四边形
parallelogram(A,B,C,D):-equals(lengthOf(line(A,B)),lengthOf(line(C,D)))^ equals(lengthOf(line(A,D)),lengthOf(line(B,C)))^ quadrilateral(A,B,C,D).

%41.一组对边平行且相等的四边形是平行四边形
parallelogram(A,B,C,D):-parallel(line(A,B),line(C,D))^ equals(lengthOf(line(A,B)),lengthOf(line(C,D)))^ quadrilateral(A,B,C,D).

%42.两组对角分别相等的四边形是平行四边形
parallelogram(A,B,C,D):-equals(measureOf(angle(A,B,C)),measureOf(angle(C,D,A)))^ equals(measureOf(angle(B,C,D)),measureOf(angle(D,A,B)))^ quadrilateral(A,B,C,D).

%43.两条对角线互相平分的四边形是平行四边形
parallelogram(A,B,C,D):-line(A,B),line(B,C),line(C,D),line(D,A),intersectAt(line(A,C),line(B,D),point(O)),equals(lengthOf(line(A,O)),lengthOf(line(C,O))),equals(lengthOf(line(B,O)),lengthOf(line(D,O))), quadrilateral(A,B,C,D).%not on_same_line(A, B, C), not on_same_line(B, C, D), not on_same_line(A, C, D).
