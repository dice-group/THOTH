#!/usr/bin/env python
import sys
from itertools import izip

reload(sys)
sys.setdefaultencoding("utf-8")

test = sys.argv[1]
output = sys.argv[2]

count = 0
acc = 0
lines = 0
corr = [0, 0, 0]
with open(test) as textfile1, open(output) as textfile2: 
    for x, y in izip(textfile1, textfile2):
        lines += 1
        x = x.strip()
        xr = x.split(' ')
        y = y.strip()
        yr = y.split(' ')
        if x == y:
            acc += 1
        # print x,y
        for i in range(3):
            try:
                if xr[i] == yr[i]:
                    corr[i] += 1
                    count += 1
            except IndexError:
                continue

print ""
print "number of triples:", lines
print "number of resources:", lines*3
print ""

res = []

leg = ['sub', 'pred', 'obj']
for i in range(3):
    res.append(float(corr[i])/lines)
    print "%", leg[i], "accuracy:", corr[i], "/", lines, "=", res[i]*100

res.append(float(acc)/lines)
print "% triple accuracy: {}".format(res[3]*100)
res.append(float(count)/(lines*3))
print "% resource accuracy: {}".format(res[4]*100)

print ""
print "\t".join([str(r) for r in res])
