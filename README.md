pytourney
=========

version 0.0.1

Python library for general tournament administration and scheduling.


Installation
------------

```bash
$ pip install git+git://github.com/SzieberthAdam/pytourney.git
```

Usage
-----

The following session calculates the 32th head-to-head tie-breaker test case of [Quilici](https://www.quickscores.com/Orgs/Head-To-Head_Tie-Breaker.pdf):

```python
>>> import pytourney
>>> results =[{"a":3,"b":1},{"a":4,"c":2},{"b":1,"d":0},{"c":2,"d":1},{"d":3,"e":1},{"c":2,"e":0}]
>>> pytourney.tie.hth.calculate(results)
{'a': 1, 'b': 2, 'c': 2, 'd': 3, 'e': 4}
```