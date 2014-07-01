import fileinput
from collections import defaultdict
import numpy as np
from sets import Set
from sklearn.cluster import DBSCAN

eps = 0.3 # max distance for nodes to be considered in same neighborhood
min_samples = 1 # min nodes around a core

connec = defaultdict(list)
uniq_nodes = Set([])

for line in fileinput.input():
  first, second, count = line.split('\t')
  connec[first].append(second)
  for el in [first, second]: uniq_nodes.add(el)

ordered_uniq = sorted(uniq_nodes) # does set change ordering?
node_map = { node:idx for idx, node in enumerate(ordered_uniq) }

adj_matrix = []
for node in ordered_uniq:
  edges = [0] * len(ordered_uniq)
  for n in connec[node]: edges[node_map[n]] = 1
  adj_matrix.append(np.asarray(edges))

cluster = DBSCAN(eps=eps,min_samples=min_samples).fit(np.asarray(adj_matrix))
labels = cluster.labels_

groups = defaultdict(list)
for idx, group in enumerate(labels):
  groups[group].append(ordered_uniq[idx])

for k,v in groups.iteritems():
  print(k)
  for n in v: print("\t{}").format(n)
