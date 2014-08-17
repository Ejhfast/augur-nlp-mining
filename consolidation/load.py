from pymongo import MongoClient
import fileinput
import sys

client = MongoClient('mongodb://ethan:ethan@candidate.35.mongolayer.com:10095/app27963874')

db = client['app27963874']

bigrams = db['bigrams']
data = []

gd = {}


def data_stream():
  relations = sys.argv[1].split(".")[0].split("-")
  header = relations + ["pmi","count"] + [r+"_scale" for r in relations] + [r+"_count" for r in relations]
  floats = [float for r in relations]
  funcs = [str for r in relations] + [float,float] + floats + floats
  with open(sys.argv[1],"r") as f:
    for i,line in enumerate(f):
      if(i==0):
        None #header
      else:
        items = [x.rstrip() for x in line.split("\t\t")]
        hsh = {header[i]:funcs[i](items[i]) for i in range(len(items))}
        print(hsh)

data_stream()
#for l in data_stream(): print l
#bigrams.insert(data_stream())
