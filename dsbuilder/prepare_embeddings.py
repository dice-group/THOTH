#!/usr/bin/env python
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")

W2V, DICT, LANG = sys.argv[1:4]

def clean(string):
    string = string.replace("http://dbpedia.org/ontology/", "dbo_")
    string = string.replace("http://dbpedia.org/property/", "dbp_")
    string = string.replace("http://" + LANG + ".dbpedia.org/property/", "dbp_" + LANG + "_")
    string = string.replace("http://" + LANG + ".dbpedia.org/resource/", "dbr_" + LANG + "_")
    string = re.sub(r'\W+', '', string)
    return string

id2uri = dict()
with open(DICT) as f:
    for line in f:
        sp = line.find(' ')
        id2uri[line[:sp]] = line[sp+1:-1]

i = 0
with open(W2V) as f:
    for line in f:
        sp = line.find(' ')
        if ' ' in line[sp+1:-1]:
            print clean(id2uri[line[:sp]]) + line[sp:-1]
        i += 1
        # if i > 3:
        #     break
