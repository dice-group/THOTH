#!/usr/bin/env python
import sys
from itertools import izip

reload(sys)
sys.setdefaultencoding("utf-8")

test, nn_out, baseline_out = sys.argv[1:4]

count = 0
unk = 0
cases = 0
corr = [0, 0, 0]
corr_base = [0, 0, 0]
with open(test) as textfile1, open(nn_out) as textfile2, open(baseline_out) as textfile3: 
    for t, n, b in izip(textfile1, textfile2, textfile3):
        t = t.strip().split(' ')
        n = n.strip().split(' ')
        b = b.strip().split(' ')
        pr = False
        for i in range(3):
            try:
                if b[i] == "<UNK>":
                    unk += 1
                    # print t[i], n[i]
                    if t[i] == n[i]:
                        count += 1
                if b[i] != t[i]:
                    pr = True
            except IndexError:
                continue
        if pr and "<UNK>" not in b:
            cases += 1
            for i in range(3):
                if n[i] == t[i]:
                    corr[i] += 1
                if b[i] == t[i]:
                    corr_base[i] += 1
                    # print "{}\n{}\n{}\n------".format(t,n,b)
        # if unk > 2:
        #     break

leg = ['sub', 'pred', 'obj']
for i in range(3):
    print leg[i]
    print "\tNN correct:", corr[i], "/", cases, float(corr[i])/cases
    print "\tBL correct:", corr_base[i], "/", cases, float(corr_base[i])/cases

print "number of <UNK>:", unk
print "resource accuracy: {}".format(float(count)*100/unk)
