from flask import Flask
import flask
from bson.json_util import dumps
from pymongo import MongoClient
from flask_cors import *
from relgrams import *
import json
app = Flask(__name__)


client = MongoClient('mongodb://ethan:ethan@candidate.35.mongolayer.com:10095/app27963874')
db = client['app27963874']
bigrams = db['bigrams']
grams = db['grams']
gram_index = db['gram_index']

app.config['CORS_ORIGINS'] = ['*']
app.config['CORS_HEADERS'] = ['Content-Type']

def grams_between(i,j):
  return gram_index.find({"$and":[{"index":{"$gte":i}},{"index":{"$lte":j}}]})
def just_keys(keys,d):
  o = {}
  for k in keys: o[k] = d[k]
  return o

@app.route("/edges/<v>/<o>")
@app.route("/edges/<v>/<o>/<l>")
@app.route("/edges/<v>/<o>/<l>/<nb>")
@cross_origin(headers=['Content-Type'])
def edges(v,o,l=10,nb=""):
  l = int(l)
  s = {"v1":v, "o1":o}
  if(nb == "no_blank"):
    s.update({"v2": {"$ne": "_"}, "o2": {"$ne": "_"}})
  search = [{"v1":b["v1"],
             "o1":b["o1"],
             "v2":b["v2"],
             "o2":b["o2"],
             "count":b["count"]} for b in bigrams.find(s).limit(l)]
  return json.dumps(search)

@app.route("/gram/<v>/<o>")
@cross_origin(headers=['Content-Type'])
def gram(v,o):
  s = grams.find_one({"verb":v,"object":o})
  return json.dumps({"verb":s["verb"], "object":s["object"], "count":s["count"]})

@app.route("/partial_gram/<t>/<s>")
@app.route("/partial_gram/<t>/<s>/<l>")
@cross_origin(headers=['Content-Type'])
def partial_gram(t,s,l=10):
  l=int(l)
  if(t=="verb" or t=="object"):
    search = [{"verb":b["verb"],
               "object":b["object"],
               "count":b["count"]} for b in grams.find({t:s}).limit(l)]
    return json.dumps(search)
  else:
    return json.dumps([])

@app.route("/indices/<v>/<o>")
@cross_origin(headers=['Content-Type'])
def indices(v,o):
  search = [q["index"] for q in gram_index.find({"verb":v, "object":o})]
  return json.dumps(search)

@app.route("/find_paths/<v1>/<o1>/<v2>/<o2>/<n>")
@cross_origin(headers=['Content-Type'])
def min_dist(v1,o1,v2,o2,n):
  n = int(n)
  i1 = [o["index"] for o in gram_index.find({"verb":v1, "object":o1}).limit(500)]
  i2 = [o["index"] for o in gram_index.find({"verb":v2, "object":o2}).limit(500)]
  print(len(i1),len(i2))
  dists = [(o1,o2, o2-o1) for o1 in i1 for o2 in i2 if o1 < o2]
  sort_dists = sorted(dists, key=lambda x:x[2])
  paths = [grams_between(min(x[:2]),max(x[:2])) for x in sort_dists[:n]]
  #results = [{"index_1":t[0]["index"], "index_2":t[1]["index"], "dist":t[2]} for t in sort_dists[:10]]
  return dumps([ [just_keys(["verb","object"],y) for y in x] for x in paths[:n]])

@app.route("/gram_range/<b>/<e>")
@cross_origin(headers=['Content-Type'])
def gram_range(b,e):
  query = grams_between(int(b),int(e))
  r = [{"verb":q["verb"],"object":q["object"]} for q in query]
  return json.dumps(r)

@app.route("/")
@cross_origin(headers=['Content-Type'])
def hello():
    return "Hello World!"

@app.route('/convert/<sent>')
@cross_origin(headers=['Content-Type'])
def convert_sentence(sent):
	return json.dumps(reverb_like_thing(sent));

if __name__ == "__main__":
    app.run(debug = True)
