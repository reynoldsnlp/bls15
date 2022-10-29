#!/usr/bin/env python

import random
from paradigm import Lexicon, Population

random.seed(10)

adam = Lexicon(25, 6)
adam.randomize(3)

pop = Population(adam)
print pop.speakers[0].lex.shape[0]



for i in xrange(100):
    pop.spawn(10, 25, 0.5)
    d = [s.lex.shape[0] for s in pop.speakers]
    print d, sum(d)/float(len(d))
    d = [s.blur() for s in pop.speakers]
    print d, sum(d)/float(len(d))
    print
