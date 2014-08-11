from pymongo import MongoClient
import fileinput

client = MongoClient('mongodb://ethan:ethan@candidate.35.mongolayer.com:10095/app27963874')

db = client['app27963874']

bigrams = db['grams']

def data_stream():
  for i,line in enumerate(fileinput.input()):
    v,o,count = line.split("\t")
    count = int(count)
    readable = "{} {} ({})".format(v,o,count)
    yield {"verb": v, "object": o, "count": count, "show":readable}

bigrams.insert(data_stream())
