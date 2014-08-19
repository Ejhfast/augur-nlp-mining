import fileinput
from collections import defaultdict
import operator
import os
import shutil
import random
import numpy as np
from sklearn.cluster import DBSCAN


by_story = defaultdict(set)
by_tag = defaultdict(set)

for line in fileinput.input():
  items = line.split(",")
  for chapter in items[1].split():
    by_story[chapter] = by_story[chapter].union(set(items[4].split()))
  for tag in items[4].split():
    by_tag[tag] = by_tag[tag].union(set(items[1].split()))

tag_counts = { tag:len(s) for tag,s in by_tag.iteritems() }
sorted_tags = sorted(tag_counts.iteritems(), key=operator.itemgetter(1), reverse=True)

def sample(seq,n):
  to_lst = list(seq)
  ids = random.sample(xrange(len(to_lst)),n)
  return [to_lst[i] for i in ids]

filtered_keys = [k for k,v in tag_counts.iteritems() if v > 1000]
#tag_keys = {k:i for i,k in enumerate(filtered_keys)}

eps = 2 # max distance for nodes to be considered in same neighborhood
min_samples = 1 # min nodes around a core

adj_matrix = []
for key in filtered_keys:
  edges = [0] * len(filtered_keys)
  for i2,key2 in enumerate(filtered_keys):
    intersect = len(by_tag[key].intersection(by_tag[key2]))
    edges[i2] = 1.0 / (intersect + 1)
    print(key,key2,edges[i2])
  adj_matrix.append(np.asarray(edges))
  print(edges)

cluster = DBSCAN(eps=eps,min_samples=min_samples).fit(np.asarray(adj_matrix))
labels = cluster.labels_

groups = defaultdict(list)
for idx, group in enumerate(labels):
  groups[group].append(filtered_keys[idx])

for k,v in groups.iteritems():
  print(k)
  for n in v: print("\t{}").format(n)

# genres = ["romance","action"]
#
# for genre in genres:
#   chapters = sample(by_tag[genre],2000)
#   path = "../files/{}".format(genre)
#   os.mkdir(path)
#   for chapter in chapters:
#     src = "../files/source_text/{}".format(chapter)
#     dst = path + "/{}".format(chapter)
#     shutil.copyfile(src,dst)
#     print("Copying {} to {}".format(src,dst))

# count = 0
# for k,v in by_story.iteritems():
#   count += 1
# print(count)
# for tag,c in sorted_tags:
#   print("{}\t{}".format(tag,c))
