import collections
import itertools

import networkx as nx


def hth_graph(results):
  """
  Creates a head-to-head graph.

  results attribute should be an iterable of dictionaries of
  names/players as keys and scores as values. A dictionary
  should contain the scores of the players in a given
  match.

  Return a directed multigraph in which nodes represent
  names/teams/players and edges represent wins. Draws are
  handled with two wins vica versa. There is no python graph
  library yet which supports mixed multigraphs so this is the
  best I can do here.
  """
  G = nx.MultiDiGraph()
  for result in results:
    names = tuple(result.keys())
    if len(names) == 1:
      G.add_node(names[0])
      continue
    combs = itertools.combinations(names, 2)
    for name1, name2 in combs:
      score1 = result[name1]
      score2 = result[name2]
      if score2 < score1:
        G.add_edge(name1, name2, **result)
            # nodes are automatically added if required
      elif score1 < score2:
        G.add_edge(name2, name1, **result)
      else:  # draws are represented with two edges
        G.add_edge(name1, name2, **result)
        G.add_edge(name2, name1, **result)
  return G


def simplified_hth_graph(G):
  """
  Creates a simplified head-to-head graph.

  G attribute should be a normal head-to-head graph.

  The simplified graph has no more than a single edge between
  two nodes. Technically if the two nodes are in a draw relation
  then there are two win edges between them vica versa.

  The remained edges reflect the dominance relations of the node
  pairs.
  """
  H = G.__class__()
  H.add_nodes_from(G)
  C = collections.Counter(e[:2] for e in G.edges)
      # edge key ignored hence e[:2]
  while True:  # simplify multi edges
    count = 0
    for (name1, name2), count in C.most_common():
      if count <= 1:
        break
      reverse_count = C[(name2, name1)]  # reverse_count < count
      if reverse_count < count:
        H.add_edge(name1, name2)
      elif reverse_count == count:
        H.add_edge(name1, name2)
        H.add_edge(name2, name1)
      else:  # should never reached because of C.most_common()
        raise NotImplementedError("unexpected count relation")
      del C[(name1, name2)]
      del C[(name2, name1)]
    if count <= 1:
      break
  for (name1, name2) in C:  # add the remaining single edges
    H.add_edge(name1, name2)
  return H


def paths(simplified_hth_graph, cutoff=None):
  """
  Generates a set of paths of the graph.

  cutoff attribute is optional and sets the depth to stop the
  search for paths.
  """
  H = simplified_hth_graph
  result = set()
  gen = nx.all_pairs_shortest_path(H, cutoff=cutoff)
  for name1, lengths in gen:
    names2 = set(lengths.keys()) - {name1}
        # lengths always contain the node itself but I do want
        # the other nodes which is reached from this node
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
  names/players as keys and scores as values. A dictionary
  should contain the scores of the *tied* players in a given
  match. Note that only the results of the tied members involved
  should be passed to this function, not the whole tournament.

  paths_cutoff attribute is optional and sets the depth to stop
  the search for paths.

  Return a dictionary with names/players as keys, and HTH
  scores as values.
  """
  # Technical note:
  # First I generate a simplified graph from which I get all
  # paths. Then I define all nodes as separate groups of nodes:
  # initially every node has its own group and no ordering is
  # made. These groups will be merged and transposed based on
  # their relations. At the end, every node pairs in a given two
  # groups should be connected in the same way: either all nodes
  # of group-1 should dominate all nodes of group-2 or the other
  # way around. The dominant group should be ahead of the other
  # in the list of groups. If there is no path or path exists to
  # both directions between two nodes then the respective groups
  # should be merged. The groups should be also merged if their
  # paths are inconsistent. At the end, the dictionary is made
  # of the final list of groups.
  Gr = hth_graph(results)
  nodes = set(Gr.nodes())
  if len(nodes) == 1:
    return {next(iter(nodes)): -1}
        # a single node will get reported specifically as -1
        # to support text formatting like replacing it with
        # empty string in reports;
        # note that 0 replaces Quilici's "--" in the output
  H = simplified_hth_graph(Gr)
  paths_H = paths(H, cutoff=paths_cutoff)
  nodegroups = [frozenset((node,)) for node in nodes]
      # initially each node has its own group; they may merge
      # later
  strongly_connected = True
      # will matter only if only a single group will remain at
      # the end; I assume disconnection and will set it later if
      # true; its value controls whether 0 or 1 HTH values will
      # be applied to the nodes
  merge = True
      # this variable controls the next loop; basically if the
      # nodegroups were merged then it will enforce another
      # pass if there are multiple nodegroups remained
  transposed = None
      # this stores the recetly transposed group pairs;
      # transposition is a major change in the nodegroups and
      # implies another group ordering pass; the transposed
      # groups can get skipped if unchanged though
  while (merge or transposed) and 1 < len(nodegroups):
    group_combinations = itertools.combinations(nodegroups, 2)
    for group_pair in group_combinations:
      if transposed == group_pair:
          # skip the checking of the recently transposed groups
        transposed = None
        merge = False
        continue
      group1, group2 = group_pair
      relation = None
          # relation stores the previous direction of nodes of
          # the two groups; if not consistent over all of
          # the node pairs then the two groups will be merged;
          # set as None as the order of the two groups is
          # unknown yet
      group1index = nodegroups.index(group1)
          # the index of the first group is stored; this value
          # will be used for merge and transposition of groups
      nodepairs = itertools.product(group1, group2)
      for node1, node2 in nodepairs:
          # for all nodepairs of all group combinations...
        merge = False
            # no change in the group structure yet
        from1to2 = ((node1, node2) in paths_H)
        from2to1 = ((node2, node1) in paths_H)
        if not (from1to2 and from2to1):
          strongly_connected = False
        if from1to2 and from2to1:
            # two-way path: the two nodes should be weighted
            # equally; groups will be merged
          merge = True
        elif not from1to2 and not from2to1:
            # no path: the two nodes should be weighted equally;
            # groups will be merged
          merge = True
        elif from1to2:
            # node2 (group2) is dominant; if it used to be
            # differently then merge groups
          if not relation:  # set initial value
            relation = 12
          elif relation != 12:
            merge = True
        elif from2to1:
            # similarly, node1 (group1) is dominant
          if not relation:
            relation = 21
          elif relation != 21:
            merge = True
        if merge:
            # merge takes place here; remove the two groups from
            # the nodegroups list and add their union to the
            # place of the first group; as this was a major
            # change in the nodegroups I have to start another
            # group ordering pass; this break only exists from
            # the inner loop but the merge will be
            # checked there too to indicate the next pass
          nodegroups.remove(group1)
          nodegroups.remove(group2)
          nodegroups.insert(group1index, group1 | group2)
          break
      else:
          # the two groups were checked; no merges were necessary
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
      if merge or transposed:
        break  # pass the break to the outer loop
  # the nodegroups list is done at this point and I only have
  # to transform it to a dictionary with names as keys and HTH
  # values as values; I do that by allocating an increasing
  # number (HTH value) to the groups (starting with 1) and all
  # nodes in a group gets that number in the result dictionary;
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
