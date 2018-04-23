#!/usr/bin/env python
import sys
from itertools import izip

reload(sys)
sys.setdefaultencoding("utf-8")

src, tgt, tgt_nmt, src_test = sys.argv[1:5]

# build translation dictionary: [src_word] => [tgt_word_1: occ; ... ; tgt_word_n: occ]
translate = dict()
j = 0
with open(src) as textfile1, open(tgt) as textfile2: 
    for x, y in izip(textfile1, textfile2):
        xr = x.strip().split(' ')
        yr = y.strip().split(' ')
        for i in range(3):
            if i == 1:
                continue
            try:
                if xr[i] not in translate:
                    translate[xr[i]] = dict()
                if yr[i] not in translate[xr[i]]:
                    translate[xr[i]][yr[i]] = 0
                translate[xr[i]][yr[i]] += 1
            except IndexError:
                continue
        j += 1
        # if j > 20:
        #     break

# prediction phase
with open(src_test) as f, open (tgt_nmt) as tgt_nmt_file:
    for line, nmt in izip(f, tgt_nmt_file):
        line = line[:-1].split(' ')
        nmt = nmt[:-1].split(' ')
        words = list()
        for i in range(3):
            if i == 1: # predicates
                word = nmt[i]
                if line[i] not in translate:
                    translate[line[i]] = dict()
                if word not in translate[line[i]]:
                    translate[line[i]][word] = 0
                translate[line[i]][word] += 1
            else:
                x = line[i]
                high = 0
                word = None
                if x not in translate:
                    word = nmt[i]
                else:
                    for w, c in translate[x].items():
                        if c > high:
                            high = c
                            word = w
            words.append(word)
        print " ".join(words)

# write stats
with open('hybrid_translations.txt', 'w') as f:
    for x in translate:
        f.write("{} {}\n".format(x, translate[x]))
