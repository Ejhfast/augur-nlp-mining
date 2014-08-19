from pymongo import MongoClient
import fileinput
import sys
from stream_util import *

client = MongoClient('mongodb://ethan:ethan@candidate.35.mongolayer.com:10095/app27963874')

db = client['app27963874']

title = sys.argv[1].split(".")[0]
collection = db[title]

def data_stream():
  relations = title.split("-")
  header = relations + ["pmi","count"] + [r+"_scale" for r in relations] + [r+"_count" for r in relations]
  floats = [float for r in relations]
  funcs = [(lambda x:x.split(" ")[0]) for r in relations] + [float,float] + floats + floats
  with open(sys.argv[1],"r") as f:
    for i,line in enumerate(f):
      if(i==0):
        None #header
      else:
        items = [x.rstrip() for x in line.split("\t\t")]
        h = {header[i]:funcs[i](items[i]) for i in range(len(items))}
        yield h
#data_stream()
#for l in data_stream(): print l
groups = grouper(1000,data_stream())
for g in groups:
  collection.insert(g)
#collection.insert(data_stream())
