#!/usr/bin/env python
import sys
from itertools import izip

reload(sys)
sys.setdefaultencoding("utf-8")

src, tgt, src_test = sys.argv[1:4]

# build translation dictionary: [src_word] => [tgt_word_1: occ; ... ; tgt_word_n: occ]
translate = dict()
j = 0
with open(src) as textfile1, open(tgt) as textfile2: 
    for x, y in izip(textfile1, textfile2):
        xr = x.strip().split(' ')
        yr = y.strip().split(' ')
        for i in range(3):
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
unk = 0
with open(src_test) as f:
    for line in f:
        line = line[:-1].split(' ')
        words = list()
        for x in line:
            high = 0
            word = None
            if x not in translate:
                word = "<UNK>"
                unk += 1
            else:
                for w, c in translate[x].items():
                    if c > high:
                        high = c
                        word = w
            words.append(word)
        print " ".join(words)

# write stats
with open('baseline_translations.txt', 'w') as f:
    f.write("<UNK> occurrences: {}\n".format(unk))
    for x in translate:
        f.write("{} {}\n".format(x, translate[x]))
