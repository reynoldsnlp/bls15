import numpy as np

def unique(items):
    """Convert list of vectors into a matrix with duplicates removes"""

    # http://stackoverflow.com/questions/16970982/find-unique-rows-in-numpy-array

    result = np.array(items)

    dtype = result.dtype.descr * result.shape[1]
    struct = result.view(dtype)
    uniq = np.unique(struct)
    uniq = uniq.view(np.int).reshape(-1, result.shape[1])

    return uniq
