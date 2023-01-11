% basic

cyclicquadrilateral(B,C,D,A) :- cyclicquadrilateral(A,B,C,D).
cyclicquadrilateral(A,D,C,B) :- cyclicquadrilateral(A,B,C,D).


%76.若四点连成的四边形对角互补或有一外角等于它的内对角,则这四点共圆
cyclicquadrilateral(A,B,C,D):-quadrilateral(A,B,C,D),equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(C,D,A))),180).

%77.若四点共圆,则这四点连成的四边形对角互补
equals(sumOf(measureOf(angle(A,B,C)),measureOf(angle(C,D,A))),180) :- cyclicquadrilateral(A,B,C,D)^ quadrilateral(A,B,C,D).

%78.若点C、D在线段AB的同侧,且$\angle ACB = \angle ADB$,则A、B、C、D四点共圆
cyclicquadrilateral(A,B,C,D):-quadrilateral(A,B,C,D)^ equals(measureOf(angle(A,C,B)),measureOf(angle(A,D,B))).

%79.若点C、D在线段AB的同侧,且A、B、C、D四点共圆,则$\angle ACB = \angle ADB$
equals(measureOf(angle(A,C,B)),measureOf(angle(A,D,B))):-cyclicquadrilateral(A,B,C,D).
