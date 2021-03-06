'''
Distance functions between Samples.  That is, Pandas Series.

A distance function d(m, n) takes as input two samples, and outputs a mathematical "distance".
'''
import itertools

import numpy as np
import pandas as pd
from scipy.spatial import distance as scipy_distance




# helper functions
def jaccard_index(a, b):
  # get set of all keys whose values are nonzero
  a_set = set(a[a != 0].keys())
  b_set = set(b[b != 0].keys())
  numerator = len(a_set & b_set)
  denominator = len(a_set | b_set)
  return numerator / denominator

def weighted_jaccard_index(a, b):
  ''' For each key k, we take min(a[k], b[k]), and sum those up.  That's the numerator.  The denominator is the same except is uses max instead of min.'''
  # NOTE: This takes about 30 times longer to run than jaccard_index
  # numerator
  min_ = pd.DataFrame({'a': a, 'b': b}).fillna(0).apply(min, axis=1)
  numerator = min_.sum()
  # denominator
  max_ = pd.DataFrame({'a': a, 'b': b}).fillna(0).apply(max, axis=1)
  denominator = max_.sum()
  # return
  return numerator / denominator



# distance functions
def l2(a, b):
  '''
  The standard Euclidean distance.
  '''
  dist = np.sqrt((a.subtract(b, fill_value=0)**2).sum())
  return dist

# l1 is arguably the best because it is a good norm AND computationally efficient.
def lp(p):
  ''' Given `p`, a real number >= 1, output the `lp` distance function. '''
  if p < 1:
    raise ValueError(f'p={p} illegal. in order for lp to be a distance function, we must have p >=1')
  def dist_func(a, b):
    dist = (np.abs(a.subtract(b, fill_value=0))**p).sum()**(1/p)
    return dist
  # Give the distance function a more helpful user-friendly name
  dist_func.__name__ = f'L{p}'
  return dist_func

def linfty(a, b):
  ''' The l-infinity distance, coming from the L-infinity norm. '''
  dist = np.abs(a.subtract(b, fill_value=0)).max()
  return dist

def jaccard(a, b):
  return 1 - jaccard_index(a, b)

def weighted_jaccard(a, b):
  return 1 - weighted_jaccard_index(a, b)

def jensen_shannon(a, b):
    ''' We use scipy's jensenshannon distance function (which includes normalizing a and b into unit vectors as a preprocessing step) with a base 2 logorithm in the Kullback-Leibler divergence. '''
    # use a kluge to fill in 0 values where missing
    a_filled_sorted = a.add(b, fill_value=0).subtract(b, fill_value=0).sort_index()
    b_filled_sorted = b.add(a, fill_value=0).subtract(a, fill_value=0).sort_index()
    # apply scipy metric
    return scipy_distance.jensenshannon(a_filled_sorted, b_filled_sorted, 2.0)



# meta distance functions
def get_distance_ladder(vectors, dist_func, max_gap):
  '''
  Given a list of vectors, a distance function, and a maximum gap, compute for each vector v_i its distance from the following vector v_i+1, from v_i+2, and so forth up to v_i+max_gap.
  '''
  vectors_dists = []
  for i in range(len(vectors)):
    vector_dists = []
    for gap in range(1, max_gap + 1):
      if i + gap < len(vectors):
        dist = dist_func(vectors[i], vectors[i + gap])
      else:
        dist = None
      vector_dists.append(dist)
    vectors_dists.append(vector_dists)
  return vectors_dists

def get_pairwise_distances(vectors, dist_func):
  ''' Given a set of vectors, get the distance between each unordered pair of vectors. '''
  vector_pairs = itertools.combinations(vectors, 2)
  distances = [dist_func(a, b) for a,b in vector_pairs]
  return distances
