#!/usr/bin/env python
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")

VECFILE, VOCAB, LANG, OUTPUT_FILE = sys.argv[1:4]

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
vocab = list()
with open(VOCAB) as f:
    for line in f:
        vocab.append(line)

with open(VECFILE) as f:
    with open(OUTPUT_FILE) as fout:
        for line in f:
            sp = line.find(' ')
            label = clean(line[:sp])
            if ' ' in line[sp+1:-1] and label in vocab:
                vocab.remove(label)
                fout.write(label + line[sp:-1])
        print "Out of vocabulary: " + len(vocab)
        for item in vocab:
            fout.write(item + ' ' + def_val+ "\n")

