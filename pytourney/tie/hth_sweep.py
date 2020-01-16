def hth(results):
  """
  Does the head-to-head ordering.

  It works identical to the NFL Head-to-head sweep which is
  applied to break a tie for the wild-card team. Basically it is
  applicable only if one club has defeated each of the others or
  if one club has lost to each of the others.

  results attribute should be an iterable of dictionaries of
  names/players as keys and scores as values. A dictionary
  should contain the scores of the *tied* players in a given
  match. Note that only the results of the tied members involved
  should be passed to this function, not the whole tournament.

  Return a dictionary with names/players as keys, and HTH
  scores as values.
  """
  # first, collect the players
  players = {player for result in results for player in result}
  if not players:
    return {}
  elif len(players) == 1:
    return {next(iter(players)): -1}
  players = tuple(sorted(players))
  # prepare the H2H value matrix
  h2hval = {
      player1: {
          player2: 0
          for player2 in players if player2 != player1
      }
      for player1 in players
  }
  for result in results:
    if len(result) <= 1:  # no opponent
      continue
    elif 2 < len(result):
      raise NotImplementedError()
    ((p1, v1), (p2, v2)) = result.items()
    if v1 == v2:
      continue
    elif v1 < v2:
      p1, p2, v1, v2 = p2, p1, v2, v1  # switch sides so p1 wins
    h2hval[p1][p2] += 1
    h2hval[p2][p1] -= 1
  superior, inferior = None, None
  for p1, d in h2hval.items():
    if superior and inferior:
      break
    values = set(d.values())
    if not superior and all((0 < x) for x in values):
      superior = p1
      continue
    if not inferior and all((x < 0) for x in values):
      inferior = p1
      continue
  if superior and inferior:
    result = {player: 2 for player in players}
    result[superior] = 1
    if 2 < len(result):
      result[inferior] = 3
    return result
  elif superior:
    result = {player: 2 for player in players}
    result[superior] = 1
    return result
  elif inferior:
    result = {player: 1 for player in players}
    result[inferior] = 2
    return result
  else:
    return {player: 0 for player in players}



calculate = hth
