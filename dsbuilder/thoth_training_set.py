#!/usr/bin/env python
import urllib2, urllib, httplib, json
import sys
import re

reload(sys)
sys.setdefaultencoding("utf-8")

SRC, TGT, OUTPUT_PATH = sys.argv[1:4]
FILENAME = 'dataset_{}2{}.tsv'.format(SRC, TGT)

MAX_OFFSET = 100000
ENDPOINT = "http://porque.cs.upb.de:3030/mapping-sample/sparql"
GRAPH = ""

def sparql_query(query):
    param = dict()
    param["default-graph-uri"] = GRAPH
    param["query"] = query
    param["format"] = "JSON"
    # param["CXML_redir_for_subjs"] = "121"
    # param["CXML_redir_for_hrefs"] = ""
    param["timeout"] = "0" # really important to avoid partial results
    # param["debug"] = "on"
    try:
        resp = urllib2.urlopen(ENDPOINT + "?" + urllib.urlencode(param))
        j = resp.read()
        resp.close()
    except (urllib2.HTTPError, httplib.BadStatusLine):
        print("*** Query error. Empty result set. ***")
        j = '{ "results": { "bindings": [] } }'
    sys.stdout.flush()
    return json.loads(j)

def clean(string):
    string = string.replace("http://dbpedia.org/ontology/", "dbo_")
    string = string.replace("http://dbpedia.org/property/", "dbp_")
    string = string.replace("http://dbpedia.org/resource/", "dbr_en_")
    string = string.replace("http://" + SRC + ".dbpedia.org/property/", "dbp_" + SRC + "_")
    string = string.replace("http://" + SRC + ".dbpedia.org/resource/", "dbr_" + SRC + "_")
    string = string.replace("http://" + TGT + ".dbpedia.org/property/", "dbp_" + TGT + "_")
    string = string.replace("http://" + TGT + ".dbpedia.org/resource/", "dbr_" + TGT + "_")
    string = re.sub(r'\W+', '', string)
    return string

# ======================================================================

# TODO if FILENAME does not exist...
offset = 0
prefix = 'PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX owl: <http://www.w3.org/2002/07/owl#> '
while True:
    query = 'SELECT ?s1 ?p1 ?o1 ?s2 ?p2 ?o2 WHERE { SELECT ?s1 ?p1 ?o1 ?s2 ?p2 ?o2 WHERE {?s1 owl:sameAs ?s2 . ?s1 ?p1 ?o1 . ?s2 ?p2 ?o2 . ?o1 owl:sameAs ?o2 . FILTER(regex(str(?s1), "http://' + ((SRC+'.') if SRC != 'en' else '') + 'dbpedia.org/resource/") && regex(str(?s2), "http://' + ((TGT+'.') if TGT != 'en' else '') + 'dbpedia.org/resource/") && ?p1 != owl:sameAs && ?p2 != owl:sameAs)} ORDER BY ?s1 ?o1 } LIMIT 100000 OFFSET ' + str(offset)
    query = prefix + query
    print(query)
    results = sparql_query(query)["results"]["bindings"]
    print("results =", len(results))
    with open(FILENAME, 'a') as f:
        for row in results:
            f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(row["s1"]["value"], row["p1"]["value"], row["o1"]["value"], row["s2"]["value"], row["p2"]["value"], row["o2"]["value"]))
    if len(results) < MAX_OFFSET:
        break
    offset += MAX_OFFSET

def keep(line, f_src, f_tgt):
    src_l = list()
    tgt_l = list()
    for i in range(3):
        src_l.append(clean(line[i]))
        tgt_l.append(clean(line[i + 3]))
    #print('src_l:', src_l)
    #print('tgt_l:', tgt_l)
    f_src.write(" ".join(src_l) + "\n")
    f_tgt.write(" ".join(tgt_l) + "\n")


prev = (None, None)
temp_set = list()
i = 0
j = 0
# count cases by issue size
cnt = dict()
with open(FILENAME) as f:
    with open(OUTPUT_PATH + "/orig." + SRC, "w") as f_src:
        with open(OUTPUT_PATH + "/orig." + TGT, "w") as f_tgt:
            for line in f:
                #print('line: ',line)
                line = line[:-1].split('\t')
                # get S-O
                key = (line[0], line[2])
                #print('key: ', key)
                #print('prev: ', prev)
                #print('temp_set: ', temp_set)
                if prev == key:
                    # group aligned triples by S-O
                    temp_set.append(line)
                else:
                    # keep or discard?
                    if temp_set:
                        size = len(temp_set)
                        if size > 1:
                            j += size
                            if size not in cnt:
                                cnt[size] = 0
                            cnt[size] += 1
                        for issue in temp_set:
                            # if size=1 or properties are the same
                            if size == 1 or issue[1] == issue[4]:
                                # keep
                                keep(issue, f_src, f_tgt)
                    temp_set = list()
                    temp_set.append(line)
                # update with previous S-O
                prev = key
                i += 1
                # if i > 30:
                #     break
                
# print analytics
print(j, "/", i)
for c in cnt:
    print('{}\t{}'.format(c,cnt[c]))

