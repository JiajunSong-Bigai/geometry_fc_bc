point(a).
pointPosition(a,942,1169).
point(b).
pointPosition(b,799,1827).
point(c).
pointPosition(c,1592,1834).
point(d).
pointPosition(d,1194,1264).
point(e).
pointPosition(e,1194,1827).
point(f).
pointPosition(f,1080,1220).
point(m).
pointPosition(m,1018,855).
point(n).
pointPosition(n,1055,1060).
line(a,b).
line(a,m).
line(a,f).
line(a,d).
line(b,m).
line(b,e).
line(b,c).
line(c,d).
line(c,n).
line(c,e).
line(d,n).
line(d,f).
line(e,m).
line(e,n).
line(e,f).
line(f,n).
line(f,m).
line(m,n).
pointLiesOnLine(n,line(m,e)).
pointLiesOnLine(a,line(m,b)).
pointLiesOnLine(f,line(m,e)).
pointLiesOnLine(f,line(a,d)).
pointLiesOnLine(d,line(n,c)).
pointLiesOnLine(e,line(b,c)).
quadrilateral(a,b,c,d).
equals(lengthOf(line(a,b)),lengthOf(line(c,d))).
isMidpointOf(point(e),line(b,c)).
isMidpointOf(point(f),line(a,d)).
connectTwoPoints(point(e),point(f)).
extendLine(line(e,f),line(e,m)).
extendLine(line(b,a),line(b,m)).
intersectAt(line(b,m),line(e,m),point(m)).
extendLine(line(c,d),line(c,n)).
intersectAt(line(e,m),line(c,n),point(n)).

line(b,d).
pointLiesOnLine(h,line(b,d)).
isMidpointOf(point(h),line(b,d)).
line(h,f).
line(h,e).
line(b,h).
line(h,d).
point(h).
