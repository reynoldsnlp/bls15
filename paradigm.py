#!/usr/bin/env python

import random
import numpy as np
from zipf import ZipfGenerator
from utils import unique
from _maximal import maximal

class Lexicon(object):
    """Store lexicon for a single speaker"""

    def __init__(self, decls=0, cells=0):
        if decls and cells:
            self.lex = np.zeros((decls, cells), dtype=np.int)

    def randomize(self, k):
        """Create a random blurry lexicon with up to k exponents per cell"""

        for c in xrange(self.lex.shape[1]):
            self.lex[:,c] = np.random.random_integers(k, size=self.lex.shape[0]) + (c * k)
        self.lex = unique(self.lex)

    def declensions(self):
        """Return (unique) declensions"""

        return self.lex.shape[0]

    def blur(self):
        """Find fraction of "blurred" cells"""

        blur = 0
        for c in xrange(self.lex.shape[1]):
            bins = np.bincount(self.lex[:,c])
            if sum(bins > 1) > 1:
                blur += 1

        return blur / float(self.lex.shape[1])

    def replace(self):
        """Re-predict one cell"""

        # "forget" one form
        r = random.randint(0, self.lex.shape[0]-1)
        c1 = random.randint(0, self.lex.shape[1]-1)
        c2 = random.randint(0, self.lex.shape[1]-1)

        # collect candidate replacements
        cand = [ ]
        for i in xrange(self.lex.shape[0]):
            if i != r:
                if self.lex[i, c2] == self.lex[r, c2]:
                    cand.append(self.lex[i, c1])
        if not cand:
            cand = list(self.lex[:, c1])

        # replace
        self.lex[r, c1] = max(set(cand), key=cand.count)
        self.lex = unique(self.lex)


    def learn(self, sample):
        """Generate a set of full paradigms from a sample"""

        # get rid of duplicates

        sample = unique(sample)
        decls = unique(maximal(sample))

        defaults = [ np.argmax(np.bincount(col[col!=0])) for col in decls.T ]
        for r in xrange(decls.shape[0]):
            for c in xrange(decls.shape[1]):
                if decls[r,c] == 0:
                    decls[r,c] = defaults[c]

        for r in xrange(sample.shape[0]):
            cand = [ ]
            for i in xrange(decls.shape[0]):
                if (decls[i] == sample[r])[sample[r] != 0].all():
                    cand.append(i)
            sample[r] = decls[random.choice(cand),:]

        self.lex = unique(sample)


class Population(object):
    """A collection of speakers of a simulated language"""

    def __init__(self, adam):
        self.speakers = [ adam ]

    def sample(self, n, p):
        """Generate a (partial) lexical sample from population"""


        #rword = ZipfGenerator(self.words, 1.01)
        #rcell= ZipfGenerator(self.cells, 1.01)

        items = [ ]

        for i in xrange(n):
            spkr = random.choice(self.speakers)
            r = random.randint(0, spkr.lex.shape[0]-1) #rword.next()
            item = spkr.lex[r].copy()
            for c in xrange(item.shape[0]):
                if random.random() > p:
                    item[c] = 0
            items.append(item)

        return items

    def spawn(self, m, n, p):
        """Create a new generation of speakers"""

        newspkrs = [ ]
        for i in xrange(m):
            newspkr = Lexicon()
            sample = self.sample(n, p)
            newspkr.learn(sample)
            newspkrs.append(newspkr)
        self.speakers = newspkrs

if __name__ == '__main__':

    random.seed(10)

    lex = Lexicon(10, 5)
    lex.randomize(3)

    print lex.lex
    print lex.lex.shape[0], lex.blur()
    print
    pop = Population(lex)
    data = pop.sample(25, 0.7)
    spkr2 = Lexicon()
    spkr2.learn(data)
    print spkr2.lex
    print spkr2.lex.shape[0], spkr2.blur()
