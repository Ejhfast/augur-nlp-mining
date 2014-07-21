from collections import defaultdict
import json
import fileinput
import sys
import operator
import re

def node_type(node): return node.split(" ")[-1]
def node_name(node): return " ".join(node.split(" ")[:-1])

def tsv_to_dict(iter):
  threshold = 10
  graph = defaultdict(list)
  inverse_graph = defaultdict(list)
  for line in iter:
    left,right,count = [x.rstrip() for x in line.split("\t")]
    if(int(count) > threshold):
        graph[left].append((right,int(count)))
        inverse_graph[right].append((left,int(count)))
  return (graph, inverse_graph)

def best_n(lst, n, f):
  sort_lst = sorted(lst, key=f)
  return sort_lst[:n]

def avg_weight(lst):
  if(len(lst) == 0): return 1
  sum = reduce(operator.add, lst)
  return float(sum)/len(lst)

def create_projection(graph, inverse_graph):
  o_n, v_n = 1, 1
  nodes = set([])
  edges = []
  basic_weight = lambda x: x[1] * -1
  edge_control = lambda x: float(x[1] * -1)/(avg_weight([y[1] for y in inverse_graph[x[0]]]))
  for v,es in graph.iteritems():
    d_n = o_n if node_type(v)=="O" else v_n
    for node in best_n(es, d_n, edge_control):
      nodes.add(node[0])
      nodes.add(v)
      edges.append([v,node[0],node[1]])
  order = list(nodes)
  order_tags = {n:i for i,n in enumerate(order)}
  node_list = [{"name":node_name(n), "type":node_type(n)} for n in order]
  edge_list =[{"source": order_tags[x[0]], "target": order_tags[x[1]], "value": float(x[2])/10} for x in edges]
  json_dict = {"nodes":node_list, "links":edge_list}
  print json.dumps(json_dict)

g_v, g_o = tsv_to_dict(fileinput.input())
create_projection(g_v,g_o)
