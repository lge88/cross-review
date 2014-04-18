#!/usr/bin/env python
import sys
from cross_review import *

def generate_hist(num_of_ids = 40, N = 2, indx = 0, num_of_tests = 1000):
  ids = [str(i) for i in range(num_of_ids)]
  bins = [0 for i in range(num_of_ids)]
  ten_percent = int(num_of_tests/10)

  yield (0.0, bins)
  for i in range(num_of_tests):
    g = Graph(ids, N)
    g.ford_fulkerson_max_flow()
    m = g.get_need_to_review_map()

    reviewees = m[indx][1]
    for reviewee in reviewees:
      bins[int(reviewee)] += 1

    if (i + 1) % ten_percent == 0:
      yield (100.0 * (i+1) / num_of_tests, bins)

if __name__ == '__main__':
  for percent, bins in generate_hist():
    print '# %2.1f%%' % percent

  print '\n'.join(map(str, bins))
