from pymongo import MongoClient
import fileinput

client = MongoClient('mongodb://ethan:ethan@candidate.35.mongolayer.com:10095/app27963874')

db = client['app27963874']

bigrams = db['bigrams']
data = []

gd = {}
with open("../analytics/re-custom.tsv","r") as f:
  for line in f:
    v,o,count = [x.rstrip() for x in line.split("\t")]
    gd["\t".join([v,o])] = int(count)

def data_stream():
  for i,line in enumerate(fileinput.input()):
    p1,p2,count = [x.rstrip() for x in line.split("\t")]
    v1, o1 = p1.split(" ")
    v2, o2 = p2.split(" ")
    readable = "{} {} =({})=> {} {}".format(v1,o1,count,v2,o2)
    count = int(count)
    yield {"v1": v1, "o1": o1, "v2": v2, "o2": o2, "count": count, "g1_count":gd["\t".join([v1,o1])], "g2_count":gd["\t".join([v2,o2])]}

#for l in data_stream(): print l
bigrams.insert(data_stream())
