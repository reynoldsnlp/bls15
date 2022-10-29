#!/usr/bin/env python

## simple LSA 2010-style simulation

import random
from paradigm import Lexicon

random.seed(10)

blur = [ ]
decl = [ ]
for i in xrange(500):

    spkr = Lexicon(100, 6)
    spkr.randomize(3)
    for i in xrange(750):
        spkr.replace()




    decl.append(spkr.lex.shape[0])
    blur.append(spkr.blur())
    print i,decl[-1],blur[-1]
#    if decl[-1] < 10:
#        print spkr.lex

#print sum(decl) / float(len(decl))
#print sum(blur) / float(len(blur))