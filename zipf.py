# http://stackoverflow.com/questions/1366984/generate-random-numbers-distributed-by-zipf

import random
import bisect 
import math 

class ZipfGenerator: 

    def __init__(self, n, alpha): 
        # Calculate Zeta values from 1 to n: 
        tmp = [1. / (math.pow(float(i), alpha)) for i in range(1, n+1)] 
        zeta = reduce(lambda sums, x: sums + [sums[-1] + x], tmp, [0]) 

        # Store the translation map: 
        self.distMap = [x / zeta[-1] for x in zeta] 

    def next(self): 
        # Take a uniform 0-1 pseudo-random value: 
        u = random.random()  

        # Translate the Zipf variable: 
        return bisect.bisect(self.distMap, u) - 1