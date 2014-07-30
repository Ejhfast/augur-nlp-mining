from pymongo import MongoClient
import fileinput

client = MongoClient('mongodb://ethan:ethan@candidate.35.mongolayer.com:10095/app27963874')

db = client['app27963874']

bigrams = db['grams']

for i,line in enumerate(fileinput.input()):
  if(i % 100 == 0): print(i)
  parts = line.split("\t")
  v = parts[0]
  o = parts[1]
  count = int(parts[3])
  if(count > 2):
    bigrams.insert({"verb": v, "object": o, "count": count})
