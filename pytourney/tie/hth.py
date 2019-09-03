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


def hth(results, paths_cutoff=None):
  """
  Does the head-to-head ordering.

  It works identical to the QuickScores HTH algorithm which is
  published by Tim Quilici and uses logical deduction to
  determine the head-to-head order.

  results attribute should be an iterable of dictionaries of
  players as keys and scores as values.

  paths_cutoff attribute is optional and sets the depth to stop
  the search for paths.
  """
  Gr = results_graph(results)
  nodes = set(Gr.nodes())
  if len(nodes) == 1:
    return {next(iter(nodes)): 0}
        # a single node will get reported as not strongly
        # connected (0 replaces Quilici's "--" in the output)
  Grs = simplified_graph(Gr)
  paths_Grs = paths(Grs, cutoff=paths_cutoff)
  nodegroups = [frozenset((node,)) for node in nodes]
      # initially each node has its own group; they may merge
      # later
  strongly_connected = True
      # will matter only if only a single group will remain at
      # the end; I assume disconnection and will set it later if
      # true; its value controls whether 0 or 1 HTH values will
      # be applied to the nodes
  join = True
      # this variable controls the next loop; basically if the
      # nodegroups were joined then it will enforce another
      # pass if there are multiple nodegroups remained
  transposed = None
      # this stores the recetly transposed group pairs;
      # transposition is a major change in the nodegroups and
      # implies another group ordering pass; the transposed
      # groups can get skipped if unchanged though
  while (join or transposed) and 1 < len(nodegroups):
    group_combinations = itertools.combinations(nodegroups, 2)
    for group_pair in group_combinations:
      if transposed == group_pair:
          # skip the checking of the recently transposed groups
        transposed = None
        join = False
        continue
      group1, group2 = group_pair
      relation = None
          # relation stores the previous direction of nodes of
          # the two groups; if not consistent over all of
          # the node pairs then the two groups will be joined;
          # set as None as the order of the two groups is
          # unknown yet
      group1index = nodegroups.index(group1)
          # the index of the first group is stored; this value
          # will be used for join and transposition of groups
      nodepairs = itertools.product(group1, group2)
      for node1, node2 in nodepairs:
          # for all nodepairs of all group combinations...
        join = False
            # no change in the group structure yet
        from1to2 = ((node1, node2) in paths_Grs)
        from2to1 = ((node2, node1) in paths_Grs)
        if not (from1to2 and from2to1):
          strongly_connected = False
        if from1to2 and from2to1:
            # two-way path: the two nodes should be weighted
            # equally; groups will be joined
          join = True
        elif not from1to2 and not from2to1:
            # no path: the two nodes should be weighted equally;
            # groups will be joined
          join = True
        elif from1to2:
            # node2 (group2) is dominant; if it used to be
            # differently then join groups
          if not relation:  # set initial value
            relation = 12
          elif relation != 12:
            join = True
        elif from2to1:
            # similarly, node1 (group1) is dominant
          if not relation:
            relation = 21
          elif relation != 21:
            join = True
        if join:
            # join takes place here; remove the two groups from
            # the nodegroups list and add their union to the
            # place of the first group; as this was a major
            # change in the nodegroups I have to start another
            # group ordering pass; this break only exists from
            # the inner loop but the join will be
            # checked there too to indicate the next pass
          nodegroups.remove(group1)
          nodegroups.remove(group2)
          nodegroups.insert(group1index, group1 | group2)
          break
      else:
          # the two groups were checked; no joins were necessary
        if relation == 21:
            # transposition takes place here; remove the second
            # group and place it before the first one then store
            # the new pair in the transposed variable
          nodegroups.remove(group2)
          nodegroups.insert(group1index, group2)
          transposed = (group2, group1)
          break
        else:
          transposed = None
      if join or transposed:
        break  # pass the break to the outer loop
  # the nodegroups list is done at this point and I only have
  # to transform it to a dictionary with names as keys and HTH
  # values as values; I do that by allocating an increasing
  # number (HTH value) to the groups (starting with 1) and all
  # nodes in a groups gets that number in the result dictionary;
  # if there is however a single nodegroup then its nodes get
  # 0 or 1 for being disconnected or strongly connected,
  # respectively
  d = {}
  if len(nodegroups) == 1:
    hth_val = (1 if strongly_connected else 0)
    for node in nodegroups[0]:
      d[node] = hth_val
  else:
    for hth_val, group in enumerate(nodegroups, 1):
      for node in group:
        d[node] = hth_val
  return d


calculate = hth
