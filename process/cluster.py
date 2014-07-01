import fileinput
from collections import defaultdict
import numpy as np
from sets import Set
from sklearn.cluster import DBSCAN

eps = 2 # max distance for nodes to be considered in same neighborhood
min_samples = 2 # min nodes around a core

connec = defaultdict(list)
uniq_nodes = Set([])

for line in fileinput.input():
  first, second, count = line.split('\t')
  connec[first].append(second)
  for el in [first, second]: uniq_nodes.add(el)

node_map = { node:idx for idx, node in enumerate(uniq_nodes) }

adj_matrix = []
for k,v in connec.iteritems():
  edges = [0] * len(uniq_nodes)
  edges[node_map[k]] = 1 # Connected to self?
  for n in v: edges[node_map[n]] = 1
  adj_matrix.append(np.asarray(edges))

cluster = DBSCAN(eps=eps,min_samples=min_samples).fit(np.asarray(adj_matrix))
labels = cluster.labels_

print labels
