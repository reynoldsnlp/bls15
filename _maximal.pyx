#!/usr/bin/env python
# cython: profile=True

import numpy as np
from collections import deque

cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef np.ndarray[np.int_t, ndim=1] merge(np.ndarray[np.int_t, ndim=1] S, np.ndarray[np.int_t, ndim=2] items):
    """Merge paradigms"""

    cdef unsigned int i, c
    cdef np.ndarray[np.int_t, ndim=1] result = np.zeros(items.shape[1], dtype=np.int)

    for i in range(S.shape[0]):
        if S[i]:
            #item = items[i]
            for c in range(M):
                if items[i, c] != 0:
                    if result[c] == 0:
                        result[c] = items[i, c]
                    elif result[c] != items[i, c]:
                        return None

    return result

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef bint subset(np.ndarray[np.int_t, ndim=1] X, np.ndarray[np.int_t, ndim=1] Y) except *:
    """Check to see if the paradigm Y is a subset of the paradigm X"""

    cdef unsigned int c

    for c in range(len(X)):
        if Y[c] != 0:
            if X[c] == 0 or X[c] != Y[c]:
                return False
    return True

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
def maximal(np.ndarray[np.int_t, ndim=2] items):
    """Find the best ways that paradigms can be merged via Malouf's (2007) BFS-RL algorithm"""

    cdef int k
    cdef unsigned int i


    cdef np.ndarray[np.int_t, ndim=1] S, S1, L, merged, consistent, R

    #cdef bint maximal
    #cdef bint leftmost

    result = [ ]
    cdef int N = items.shape[0]
    cdef int M = items.shape[1]
    Q = deque([(np.ones(N, dtype=np.int), -1, False)])

    while Q:
        (S, k, leftmost) = Q.popleft()
        merged = merge(S, M, items)
        #print merged, [items[i] for i in xrange(N) if S[i]]
        if merged != None:
            # found a consistent paradigm, but is it maximal?
            maximal = True
            for R in result:
                if subset(R, merged):
                    maximal = False
                    break
            if maximal:
                # yes, it is
                result.append(merged)
        else:
            # not consistent, so we have to try removing words from the set
            L = S.copy()
            L[(k+1):] = 0
            consistent = merge(L, M, items)
            if leftmost or consistent != None:
                leftmost = True
                for i in xrange(k+1, N):
                    S1 = S.copy()
                    S1[i] = 0
                    Q.append((S1, i, leftmost))
                    leftmost = False

    return result