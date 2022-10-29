#!/usr/bin/env python

from collections import deque
import numpy as np
from numpy import array
from _maximal import maximal

def merge(items):
    """Merge paradigms"""

    if items:
        result = items[0].copy()
        for item in items[1:]:
            for c in xrange(len(result)):
                if item[c] != 0:
                    if result[c] == 0:
                        result[c] = item[c]
                    elif result[c] != item[c]:
                        return None
        return result
    else:
        return True


def _subset(X, Y):
    """Check to see if the paradigm Y is a subset of the paradigm X"""

    sub = True
    for c in xrange(len(X)):
        if Y[c] != 0:
            if X[c] == 0 or X[c] != Y[c]:
                return False
    return True


def _maximal(items):
    """Find the best ways that paradigms can be merged via Malouf's (2007) BFS-RL algorithm"""

    result = [ ]
    N = len(items)
    Q = deque([(np.ones(len(items), dtype=np.bool), -1, False)])

    while Q:
        (S, k, leftmost) = Q.popleft()
        merged = merge([items[i] for i in xrange(N) if S[i]])
        #print merged, [items[i] for i in xrange(N) if S[i]]
        if merged != None:
            # found a consistent paradigm, but is it maximal?
            if not any(subset(R, merged) for R in result):
                # yes, it is
                result.append(merged)
        else:
            # not consistent, so we have to try removing words from the set
            L = S.copy()
            L[(k+1):] = False
            consistent = merge([items[i] for i in xrange(N) if L[i]])
            if leftmost or consistent != None:
                leftmost = True
                for i in xrange(k+1, N):
                    S1 = S.copy()
                    S1[i] = False
                    Q.append((S1, i, leftmost))
                    leftmost = False

    return result



if __name__ == '__main__':

### python -m cProfile -s tottime maximal.py | head -20


    a = np.array([0,0,0,11,0,0])
    b = array([np.array([0,0,4,11,0,0]), np.array([0,0,5,11,0,0])])
    print maximal(b)

    b = array([array([1, 4, 0, 0, 0, 0]), array([ 3,  6,  0,  0, 15,  0]), array([ 0,  6,  7,  0,  0, 17]),
         array([ 2,  5,  7, 11, 13, 16]), array([ 1,  4,  0, 11, 15, 17]), array([ 0,  0,  0, 11,  0,  0]),
         array([ 3,  5,  7, 11, 14, 17]), array([ 0,  0,  8,  0,  0, 17]), array([ 1,  6,  0,  0,  0, 18]),
         array([ 3,  6,  7,  0, 15, 17]), array([ 3,  0,  8, 11,  0, 18]), array([ 1,  0,  0,  0,  0, 17]),
         array([ 2,  6,  0,  0, 14,  0]), array([ 1,  5,  7, 11,  0,  0]), array([ 1,  0,  8,  0, 13,  0]),
         array([ 1,  6,  0, 11,  0,  0]), array([ 0,  4,  0,  0, 14,  0]), array([ 0,  6,  0,  0, 13, 18]),
         array([ 0,  4,  7, 11,  0, 16]), array([ 2,  0,  8,  0, 13, 16]), array([ 3,  0,  9,  0,  0, 17]),
         array([ 3,  4,  9,  0, 15, 16]), array([ 2,  0,  0,  0,  0, 18]), array([ 0,  6,  7,  0, 15,  0]),
         array([ 2,  5,  0,  0, 15, 18]), array([ 0,  0,  7,  0, 15, 17]), array([0, 4, 0, 0, 0, 0]),
         array([ 0,  4,  0,  0, 14,  0]), array([2, 6, 0, 0, 0, 0]), array([ 0,  0,  0,  0,  0, 17]),
         array([ 1,  0,  7,  0, 13, 16]), array([ 0,  0,  9,  0, 14, 17]), array([ 0,  0,  8,  0,  0, 17]),
         array([ 3,  5,  0,  0, 14, 17]), array([ 0,  5,  0,  0,  0, 17]), array([ 0,  4,  7,  0,  0, 18]),
         array([ 0,  0,  9,  0, 15,  0]), array([ 2,  5,  7,  0, 14,  0]), array([ 0,  4,  7, 11,  0, 18]),
         array([ 0,  0,  0,  0, 15, 17]), array([ 1,  6,  0, 11, 13, 18]), array([ 0,  0,  0,  0,  0, 16])])
    print maximal(b)



    # b = [array([1, 4, 0, 0, 0, 0]), array([ 3,  6,  0,  0, 15,  0]), array([ 0,  6,  7,  0,  0, 17]),
    #      array([ 2,  5,  7, 11, 13, 16]), array([ 1,  4,  0, 11, 15, 17]), array([ 0,  0,  0, 11,  0,  0]),
    #      array([ 3,  5,  7, 11, 14, 17]), array([ 0,  0,  8,  0,  0, 17]), array([ 1,  6,  0,  0,  0, 18]),
    #      array([ 3,  6,  7,  0, 15, 17]), array([ 3,  0,  8, 11,  0, 18]), array([ 1,  0,  0,  0,  0, 17]),
    #      array([ 2,  6,  0,  0, 14,  0]), array([ 1,  5,  7, 11,  0,  0]), array([ 1,  0,  8,  0, 13,  0]),
    #      array([ 1,  6,  0, 11,  0,  0]), array([ 0,  4,  0,  0, 14,  0]), array([ 0,  6,  0,  0, 13, 18]),
    #      array([ 0,  4,  7, 11,  0, 16]), array([ 2,  0,  8,  0, 13, 16]), array([ 3,  0,  9,  0,  0, 17]),
    #      array([ 3,  4,  9,  0, 15, 16]), array([ 2,  0,  0,  0,  0, 18]), array([ 0,  6,  7,  0, 15,  0]),
    #      array([ 2,  5,  0,  0, 15, 18]), array([ 0,  0,  7,  0, 15, 17]), array([0, 4, 0, 0, 0, 0]),
    #      array([ 0,  4,  0,  0, 14,  0]), array([2, 6, 0, 0, 0, 0]), array([ 0,  0,  0,  0,  0, 17]),
    #      array([ 1,  0,  7,  0, 13, 16]), array([ 0,  0,  9,  0, 14, 17]), array([ 0,  0,  8,  0,  0, 17]),
    #      array([ 3,  5,  0,  0, 14, 17]), array([ 0,  5,  0,  0,  0, 17]), array([ 0,  4,  7,  0,  0, 18]),
    #      array([ 0,  0,  9,  0, 15,  0]), array([ 2,  5,  7,  0, 14,  0]), array([ 0,  4,  7, 11,  0, 18]),
    #      array([ 0,  0,  0,  0, 15, 17]), array([ 1,  6,  0, 11, 13, 18]), array([ 0,  0,  0,  0,  0, 16]),
    #      array([0, 4, 0, 0, 0, 0]), array([ 1,  6,  7, 11,  0,  0]), array([2, 0, 8, 0, 0, 0]),
    #      array([ 0,  5,  7,  0, 14, 17]), array([3, 6, 9, 0, 0, 0]), array([ 1,  0,  9,  0, 14, 18]),
    #      array([ 3,  0,  8,  0,  0, 18]), array([ 0,  0,  0,  0,  0, 17]), array([ 1,  0,  0,  0,  0, 17]),
    #      array([ 2,  0,  0, 11,  0, 17]), array([0, 5, 0, 0, 0, 0]), array([ 0,  4,  0,  0, 15,  0]),
    #      array([ 0,  4,  0,  0, 13, 16]), array([ 0,  0,  8,  0,  0, 17]), array([ 0,  0,  0,  0,  0, 16]),
    #      array([ 0,  0,  0,  0, 15, 18]), array([ 3,  4,  7,  0, 14,  0])]
    # print maximal(b)
