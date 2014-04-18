#!/usr/bin/env python
import sys
import random

class Graph:
  def __init__(self, peer_names, n=2):
    self._caps = {}
    self._flows = {}
    self._reviewers = set()
    self._reviewees = set()
    self.num_of_peers = n
    for name in peer_names:
      reviewer = 'reviewer_' + name
      reviewee = 'reviewee_' + name
      self._reviewers.add(reviewer)
      self._reviewees.add(reviewee)

      self.set_capacity('source', reviewer, n)
      self.set_flow('source', reviewer, 0)
      self.set_flow(reviewer, 'source', 0)

      self.set_capacity(reviewee, 'target', n)
      self.set_flow(reviewee, 'target', 0)
      self.set_flow('target', reviewee, 0)

    for reviewer in self._reviewers:
      for reviewee in self._reviewees:
        if reviewer != reviewee:
          self.set_capacity(reviewer, reviewee, 1)
          self.set_flow(reviewer, reviewee, 0)
          self.set_flow(reviewee, reviewer, 0)

  def get_role(self, v):
    return v.split('_')[0]

  def get_name(self, v):
    return v.split('_')[1]

  def swap_role(self, v):
    role = 'reviewee' if self.get_role(v) == 'reviewer' else 'reviewer'
    return role + '_' + self.get_name(v)

  def get_neighbors(self, v):
    nbs = set()
    if v == 'source':
      nbs = set(self._reviewers)
    if v == 'target':
      nbs = set(self._reviewees)
    if self.get_role(v) == 'reviewer' and v in self._reviewers:
      nbs = self._reviewees.difference([self.swap_role(v)]) | set(['source'])
    if self.get_role(v) == 'reviewee' and v in self._reviewees:
      nbs = self._reviewers.difference([self.swap_role(v)]) | set(['target'])

    nbs = list(nbs)
    random.shuffle(nbs)
    return nbs

  def get_residual_capacity(self, u, v):
    return self.get_capacity(u, v) - self.get_flow(u, v)

  def get_capacity(self, u, v):
    key = u + '_' + v
    if self._caps.has_key(key): return self._caps[u + '_' + v]
    else: return 0

  def set_capacity(self, u, v, c):
    self._caps[u + '_' + v] = int(c)

  def get_flow(self, u, v):
    key = u + '_' + v
    if self._flows.has_key(key): return self._flows[u + '_' + v]
    else: return 0

  def set_flow(self, u, v, f):
    self._flows[u + '_' + v] = int(f)

  def incr_flow(self, u, v, delta):
    self.set_flow(u, v, self.get_flow(u, v) + delta)

  def find_path(self, s, t, sofar = []):
    if s == t: return sofar
    for u in self.get_neighbors(s):
      r = self.get_residual_capacity(s, u)
      if r > 0 and (s, u) not in sofar:
        res = self.find_path(u, t, sofar + [(s, u)])
        if res != None: return res

  def ford_fulkerson_max_flow(self, s = 'source', t = 'target'):
    path = self.find_path(s, t)
    while path != None:
      residuals = [self.get_residual_capacity(u, v) for u, v in path]
      delta = min(residuals)
      for u, v in path:
        self.incr_flow(u, v, delta)
        self.incr_flow(v, u, -delta)
        path = self.find_path(s, t)

    return sum(g.get_flow('source', u) for u in g.get_neighbors('source'))

  def get_need_to_review_map(self):
    res = {}
    for x in self._reviewers:
      res[self.get_name(x)] = set()

    for x in self._reviewers:
      for y in self._reviewees:
        if self.get_flow(x, y) > 0:
          res[self.get_name(x)].add(self.get_name(y))

    return sorted(res.items())

  def get_reviewed_by_map(self):
    res = {}
    for x in self._reviewees:
      res[self.get_name(x)] = set()

    for x in self._reviewers:
      for y in self._reviewees:
        if self.get_flow(x, y) > 0:
          res[self.get_name(y)].add(self.get_name(x))

    return sorted(res.items())

def read_stdin():
  return [line.strip() for line in sys.stdin]

def read_file(fname):
  return [line.strip() for line in open(fname)]

def print_header(a, b):
  print "# %18s%20s" % (a, b)

def print_map(m):
  for k, v in m:
    l = list(v)
    l.insert(0, k)
    print ''.join(map(lambda x: '%20s', l)) % tuple(l)

def print_to_review_map(g):
  m = g.get_need_to_review_map()
  print_header('ID', 'NEED_TO_REVIEW({0})'.format(g.num_of_peers))
  print_map(m)

def print_reviewed_by_map(g):
  m = g.get_reviewed_by_map()
  print_header('ID', 'REVIEWED_BY({0})'.format(g.num_of_peers))
  print_map(m)

def print_all(g):
  print_to_review_map(g)
  print ''
  print_reviewed_by_map(g)

def print_help_msg():
  print '''
Usage: cross_review.py [file] [N] [OPTIONS]
  Given a list of peers, randomly assign reviewers to each peer.

  file
    The file name of list of ids. Use '-' to read file from stdin.

  N
    Number of reviewers. Default is 2.

  -a or --all
    Print both --to-review and --reviewed-by. By default, -a is
    enabled.

  -t or --to-review
    For each reviewer, print the list of ids to be reviewed.

  -b or --reviewed-by
    For each reviewee, print the list of ids by whom he/she
    is reviewed.

  -h or --help
    Print this help message.
'''

if __name__ == '__main__':
  argc = len(sys.argv)

  if len(sys.argv) == 0:
    print_help_msg()
    sys.exit(1)

  if len(sys.argv) > 1:
    fname = sys.argv[1]
    peers = read_file(fname) if fname != '-' else read_stdin()
    sys.argv.pop(1)
  else:
    peers = read_stdin()

  if len(sys.argv) > 1:
    n = int(sys.argv[1])
    sys.argv.pop(1)
  else:
    n = 2

  opt = sys.argv[1] if len(sys.argv) > 1 else ''

  if opt == '--help' or opt == '-h' or n < 1:
    print_help_msg()
    sys.exit(1)

  g = Graph(peers, n)
  max_flow = g.ford_fulkerson_max_flow()
  assert(max_flow == len(peers)*n)

  if opt == '--to-review' or opt == '-t':
    print_to_review_map(g)
  elif opt == '--reviewed-by' or opt == '-b':
    print_reviewed_by_map(g)
  elif opt == '--all' or opt == '-a' or opt == '':
    print_all(g)
  else:
    print_help_msg()

  print '# max_flow: ', max_flow, ' num_of_peers: ', len(peers),\
      ' num_of_reviewers_per_peer: ', n

  sys.exit(0)
