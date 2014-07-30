from pymongo import MongoClient
import fileinput

client = MongoClient('mongodb://ethan:ethan@candidate.35.mongolayer.com:10095/app27963874')

db = client['app27963874']

bigrams = db['bigrams']

for i,line in enumerate(fileinput.input()):
  if(i % 100 == 0): print(i)
  parts = line.split("\t")
  v1 = parts[0]
  o1 = parts[1]
  v2 = parts[3]
  o2 = parts[4]
  count = int(parts[6])
  if(count > 2):
    bigrams.insert({"v1": v1, "o1": o1, "v2": v2, "o2": o2, "count": count})
