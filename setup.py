## python setup.py build_ext --inplace

from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

setup(
  name = 'BLS 2015',
  ext_modules = cythonize('_maximal.pyx'),
  include_dirs = [np.get_include()]
)