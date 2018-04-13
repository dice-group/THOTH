#!/usr/bin/env python
import sys
import re

filename = sys.argv[1]
path = sys.argv[2]
SRC = sys.argv[3]
TGT = sys.argv[4]

reload(sys)
sys.setdefaultencoding("utf-8")

def clean(string):
    string = string.replace("http://dbpedia.org/ontology/", "dbo_")
    string = string.replace("http://dbpedia.org/property/", "dbp_")
    string = string.replace("http://" + SRC + ".dbpedia.org/property/", "dbp_" + SRC + "_")
    string = string.replace("http://" + SRC + ".dbpedia.org/resource/", "dbr_" + SRC + "_")
    string = string.replace("http://" + TGT + ".dbpedia.org/property/", "dbp_" + TGT + "_")
    string = string.replace("http://" + TGT + ".dbpedia.org/resource/", "dbr_" + TGT + "_")
    string = re.sub(r'\W+', '', string)
    return string

with open(filename) as f:
    with open(path + "/orig." + SRC, "w") as f_src:
        with open(path + "/orig." + TGT, "w") as f_tgt:
            for line in f:
                line = line[:-1].split('\t')
                if line[0] == "\"s1\"":
                    continue
                src_l = list()
                tgt_l = list()
                for i in range(3):
                    src_l.append(clean(line[i][1:-1]))
                    tgt_l.append(clean(line[i + 3][1:-1]))
                f_src.write(" ".join(src_l) + "\n")
                f_tgt.write(" ".join(tgt_l) + "\n")
