#!/usr/bin/env python
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")

VECFILE, LANG = sys.argv[1:3]

def clean(string):
    string = string.replace("http://dbpedia.org/ontology/", "dbo_")
    string = string.replace("http://dbpedia.org/property/", "dbp_")
    string = string.replace("http://dbpedia.org/resource/", "dbr_en_")
    string = string.replace("http://" + LANG + ".dbpedia.org/property/", "dbp_" + LANG + "_")
    string = string.replace("http://" + LANG + ".dbpedia.org/resource/", "dbr_" + LANG + "_")
    string = re.sub(r'\W+', '', string)
    string = string.lower()
    return string

i = 0
with open(VECFILE) as f:
    for line in f:
        sp = line.find(' ')
        if ' ' in line[sp+1:-1]:
            print clean(line[:sp]) + line[sp:-1]
        i += 1