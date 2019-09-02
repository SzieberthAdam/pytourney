import collections
import itertools

import networkx as nx


def results_graph(results):
  G = nx.MultiDiGraph()
  for result in results:
    names = tuple(result.keys())
    if len(names) == 1:
      G.add_node(names[0])
      continue
    combs = itertools.combinations(names, 2)
    for name1, name2 in combs:
      G.add_node(name1)
      G.add_node(name2)
      score1 = result[name1]
      score2 = result[name2]
      if score2 < score1:
        G.add_edge(name1, name2, **result)
      elif score1 < score2:
        G.add_edge(name2, name1, **result)
      else:
        G.add_edge(name1, name2, **result)
        G.add_edge(name2, name1, **result)
  return G


def simplified_graph(G):
  G = G.copy()
  C = collections.Counter(e[:2] for e in G.edges)
  while True:
    count = 0
    for edge, count in C.most_common():
      if count <= 1:
        break
      name1, name2 = edge
      reverse_edge = (name2, name1)
      reverse_count = C[reverse_edge]
      discard_count = min(reverse_count, count - 1)
      for _ in range(discard_count):
        G.remove_edge(*edge)
        G.remove_edge(*reverse_edge)
      del C[edge]
      del C[reverse_edge]
    if count <= 1:
      break
  return G


def paths(simplified_results_graph, cutoff=None):
  Grs = simplified_results_graph
  result = set()
  gen = nx.all_pairs_shortest_path(Grs, cutoff=cutoff)
  for name1, lengths in gen:
    names2 = set(lengths.keys()) - {name1}
    for name2 in names2:
      result.add((name1, name2))
  return result


def hth(results, cutoff=None):
  Gr = results_graph(results)
  nodes = set(Gr.nodes())
  Grs = simplified_graph(Gr)
  P = paths(Grs, cutoff=cutoff)
  nodegroups = [frozenset((node,)) for node in nodes]
  join_or_reorder = True
  while join_or_reorder:
    for group1, group2 in itertools.combinations(nodegroups, 2):
      relation = 0
      group1index = nodegroups.index(group1)
      for node1, node2 in itertools.product(group1, group2):
        join_or_reorder = False
        from1to2 = ((node1, node2) in P)
        from2to1 = ((node2, node1) in P)
        if from1to2 == from2to1:
          join_or_reorder = True
        elif from1to2:
          if relation == 0:
            relation = 12
          if relation != 12:
            join_or_reorder = True
        elif from2to1:
          if relation == 0:
            relation = 21
          if relation != 21:
            join_or_reorder = True
        if join_or_reorder:
          nodegroups.remove(group1)
          nodegroups.remove(group2)
          nodegroups.insert(group1index, group1 | group2)
          break
      else:
        if relation == 21:
          nodegroups.remove(group2)
          nodegroups.insert(group1index, group2)
          join_or_reorder = True
          break
      if join_or_reorder:
        break
  d = {}
  if len(nodegroups) == 1:
    hth_val = 0
    for node in nodegroups[0]:
      d[node] = hth_val
  else:
    for hth_val, group in enumerate(nodegroups, 1):
      for node in group:
        d[node] = hth_val
  return d


calculate = hth
