#!/usr/bin/env python
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")

VECFILE, VOCAB, LANG, OUTPUT_FILE = sys.argv[1:5]

def clean(string):
    string = string.replace("http://dbpedia.org/ontology/", "dbo_")
    string = string.replace("http://dbpedia.org/property/", "dbp_")
    string = string.replace("http://dbpedia.org/resource/", "dbr_en_")
    string = string.replace("http://" + LANG + ".dbpedia.org/property/", "dbp_" + LANG + "_")
    string = string.replace("http://" + LANG + ".dbpedia.org/resource/", "dbr_" + LANG + "_")
    string = re.sub(r'\W+', '', string)
    string = string.lower()
    return string

def_val = ' '.join([str(v) for v in [0.0]*500])
vocab = set()
with open(VOCAB) as f:
    for line in f:
        vocab.add(clean(line))
print 'Vocabulary size:', len(vocab)
with open(VECFILE) as f:
    with open(OUTPUT_FILE, "w") as fout:
        for line in f:
            sp = line.find(' ')
            label = clean(line[:sp])
            cond1 = ' ' in line[sp+1:-1]
            cond2 = label in vocab
            if cond1 and cond2:
                fout.write(label + line[sp:-1]+'\n')
                vocab.remove(label)
        print 'Vocab words without embeddings:', len(vocab)
        for oov_word in vocab:
            fout.write(oov_word+' '+def_val+'\n')