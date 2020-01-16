import unittest

import pytourney

class TestQuiliciHTHSweep(unittest.TestCase):
  test_cases = {
      1: {
        "results": [
            {"A": 0},
            {"B": 0},
        ],
        "hth": {"A": 0, "B": 0},
      },
      2: {
        "results": [
            {"A": 3, "B": 0},
        ],
        "hth": {"A": 1, "B": 2},
      },
      3: {
        "results": [
            {"A": 3, "B": 3},
        ],
        "hth": {"A": 0, "B": 0},
      },
      4: {
        "results": [
            {"A": 0},
            {"B": 0},
            {"C": 12},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      5: {
        "results": [
            {"A": 1, "C": 0},
            {"B": 3},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      6: {
        "results": [
            {"A": 1, "B": 0},
            {"B": 3, "C": 2},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      7: {
        "results": [
            {"A": 1, "C": 0},
            {"B": 3, "C": 2},
        ],
        "hth": {"A": 1, "B": 1, "C": 2},
      },
      8: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 3, "C": 2},
        ],
        "hth": {"A": 1, "B": 2, "C": 2},
      },
      9: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 3, "C": 2},
            {"B": 2, "C": 1},
        ],
        "hth": {"A": 1, "B": 2, "C": 3},
      },
      10: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 3, "C": 2},
            {"B": 2, "C": 2},
        ],
        "hth": {"A": 1, "B": 2, "C": 2},
      },
      11: {
        "results": [
            {"A": 1, "B": 1},
            {"A": 3, "C": 2},
            {"B": 2, "C": 1},
        ],
        "hth": {"A": 1, "B": 1, "C": 2},
      },
      12: {
        "results": [
            {"A": 10, "B": 1},
            {"B": 2, "C": 2},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      13: {
        "results": [
            {"A": 1, "B": 1},
            {"B": 2, "C": 2},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      14: {
        "results": [
            {"A": 1, "B": 1},
            {"A": 4, "C": 2},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      15: {
        "results": [
            {"A": 2, "B": 1},
            {"B": 4, "C": 2},
            {"C": 4, "A": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      16: {
        "results": [
            {"A": 2, "B": 1},
            {"B": 4, "C": 2},
            {"B": 1, "C": 0},
            {"C": 4, "A": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      17: {
        "results": [
            {"A": 1},
            {"B": 2},
            {"C": 3},
            {"D": 4},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      18: {
        "results": [
            {"A": 1, "C": 0},
            {"B": 2, "D": 1},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      19: {
        "results": [
            {"A": 1, "C": 0},
            {"B": 2, "C": 1},
            {"B": 3, "D": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      20: {
        "results": [
            {"A": 1, "B": 1},
            {"B": 2, "D": 1},
            {"C": 0, "D": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      21: {
        "results": [
            {"A": 2, "B": 1},
            {"C": 2, "A": 1},
            {"B": 2, "D": 0},
            {"D": 1, "C": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      22: {
        "results": [
            {"A": 2, "B": 1},
            {"B": 2, "C": 1},
            {"C": 2, "D": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      23: {
        "results": [
            {"A": 2, "B": 1},
            {"A": 2, "C": 1},
            {"B": 2, "D": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      24: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 2, "C": 1},
            {"B": 1, "D": 0},
            {"C": 1, "D": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      25: {
        "results": [
            {"A": 1, "B": 0},
            {"B": 2, "D": 1},
            {"C": 1, "D": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      26: {
        "results": [
            {"A": 1, "C": 0},
            {"B": 2, "C": 1},
            {"C": 1, "D": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      27: {
        "results": [
            {"A": 1, "B": 0},
            {"B": 2, "C": 1},
            {"D": 1, "B": 0},
            {"C": 1, "D": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      28: {
        "results": [
            {"A": 1, "C": 0},
            {"B": 2, "C": 1},
            {"C": 1, "D": 0},
            {"C": 1, "E": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0},
      },
      29: {
        "results": [
            {"A": 1, "B": 0},
            {"B": 2, "C": 1},
            {"C": 1, "A": 0},
            {"C": 1, "D": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0},
      },
      30: {
        "results": [
            {"A": 1, "C": 0},
            {"B": 2, "C": 2},
            {"D": 1, "C": 1},
            {"C": 1, "E": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0},
      },
      31: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 1, "C": 0},
            {"B": 1, "D": 0},
            {"C": 1, "E": 0},
            {"D": 1, "E": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0},
      },
      32: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 1, "C": 0},
            {"B": 1, "D": 0},
            {"C": 1, "D": 0},
            {"C": 1, "E": 0},
            {"D": 1, "E": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0},
      },
      33: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 1, "C": 0},
            {"B": 1, "C": 0},
            {"B": 1, "D": 0},
            {"C": 1, "E": 0},
            {"D": 1, "E": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0},
      },
      34: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 1, "C": 0},
            {"B": 1, "D": 0},
            {"C": 1, "D": 0},
            {"D": 1, "E": 0},
            {"D": 1, "F": 0},
            {"E": 1, "G": 0},
            {"F": 1, "G": 0},
        ],
        "hth": {
            "A": 0, "B": 0, "C": 0, "D": 0,
            "E": 0, "F": 0, "G": 0
        },
      },
  }

for _n, _d in TestQuiliciHTHSweep.test_cases.items():
  _test_method = lambda self, _d=_d: self.assertEqual(
      pytourney.tie.hth_sweep.calculate(_d["results"]),
      _d["hth"],
  )
  _test_method.__name__ = f'test_quilici_{_n:0>2}'
  setattr(
      TestQuiliciHTHSweep,
      _test_method.__name__,
      _test_method,
  )
del _n, _d, _test_method


class TestSzieberthAdamHTHSweep(unittest.TestCase):
  test_cases = {
      1: {
        "results": [
            {"A": 0},
        ],
        "hth": {"A": -1},
            # A single node should be reported differently
      },
      2: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 0, "B": 0},
            {"B": 0, "C": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      3: {
        "results": [
            {"A": 1, "B": 0},
            {"A": 1, "B": 0},
            {"A": 0, "B": 1},
            {"B": 1, "C": 0},
            {"B": 0, "C": 1},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
      4: {
        "results": [
            {"A": 1, "B": 0},
            {"B": 0, "C": 0},
            {"C": 1, "A": 0},
        ],
        "hth": {"A": 0, "B": 0, "C": 0},
      },
  }

for _n, _d in TestSzieberthAdamHTHSweep.test_cases.items():
  _test_method = lambda self, _d=_d: self.assertEqual(
      pytourney.tie.hth_sweep.calculate(_d["results"]),
      _d["hth"],
  )
  _test_method.__name__ = f'test_szieberth_{_n:0>2}'
  setattr(
      TestSzieberthAdamHTHSweep,
      _test_method.__name__,
      _test_method,
  )
del _n, _d, _test_method



if __name__ == '__main__':
    unittest.main()
