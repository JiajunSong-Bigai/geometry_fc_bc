% similar triangles


equals(div(lengthOf(line(A,B)),lengthOf(line(D,E))),div(lengthOf(line(B,C)),lengthOf(line(E,F)))):-similar(triangle(A,B,C),triangle(D,E,F)).
equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))):-similar(triangle(A,B,C),triangle(D,E,F)).

similar(triangle(A,D,E),triangle(A,B,C)):-triangle(A,B,C),pointLiesOnLine(point(D),line(A,B)),pointLiesOnLine(point(E),line(A,C)),parallel(line(D,E),line(B,C)).
similar(triangle(A,B,C),triangle(D,E,F)):-triangle(A,B,C),triangle(D,E,F),equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))),equals(measureOf(angle(B,C,A)),measureOf(angle(E,F,D))).
similar(triangle(A,B,C),triangle(D,E,F)):-equals(div(lengthOf(line(A,B)),lengthOf(line(D,E))),div(lengthOf(line(B,C)),lengthOf(line(E,F)))),equals(measureOf(angle(A,B,C)),measureOf(angle(D,E,F))).
similar(triangle(A,B,C),triangle(D,E,F)):-equals(div(lengthOf(line(A,B)),lengthOf(line(D,E))),div(lengthOf(line(B,C)),lengthOf(line(E,F)))),equals(div(lengthOf(line(B,C)),lengthOf(line(E,F))),div(lengthOf(line(C,A)),lengthOf(line(F,D)))).
