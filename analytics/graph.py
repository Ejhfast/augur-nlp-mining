from collections import defaultdict
import json
import fileinput
import sys
import operator
import re

def node_type(node):
  a, b = node.split(" ")
  if(a == "_" and b != "_"):
    return "O"
  elif(a != "_" and b == "_"):
    return "V"
  else:
    return "OV"
def node_name(node): return node#" ".join(node.split(" ")[:-1])

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
  o_n, v_n = 1,1
  nodes = set([])
  edges = []
  basic_weight = lambda x: x[1] * -1
  edge_control = lambda x: float(x[1] * -1)/(len(inverse_graph[x[0]])**3)
  new_graph = defaultdict(list)
  for v,es in graph.iteritems():
    d_n = o_n if node_type(v)=="O" else v_n
    for node in best_n(es, d_n, edge_control):
      nodes.add(node[0])
      nodes.add(v)
      edges.append([v,node[0],node[1]])
      new_graph[v].append([node[0],node[1]])
  return nodes, edges, new_graph

def print_json(nodes, edges):
  order = list(nodes)
  order_tags = {n:i for i,n in enumerate(order)}
  node_list = [{"name":node_name(n), "type":node_type(n)} for n in order]
  edge_list =[{"source": order_tags[x[0]], "target": order_tags[x[1]], "value": float(x[2])/1} for x in edges]
  json_dict = {"nodes":node_list, "links":edge_list}
  print json.dumps(json_dict)

def print_matrix(nodes, graph):
  order = list(nodes)
  order_tags = {n:i for i,n in enumerate(order)}
  matrix = []
  for node,e_lst in graph.iteritems():
    new_edges = [0] * len(order)
    for edge in e_lst: # SO inefficient...
      new_edges[order_tags[edge[0]]] = 1
    new_edges[order_tags[node]] = 0 # Not connected to self...
    matrix.append(new_edges)
  print("\t".join(order))
  for row in matrix:
    print("\t".join([str(x) for x in row]))


g_v, g_o = tsv_to_dict(fileinput.input())
n, e, g = create_projection(g_v,g_o)
print_json(n,e)
