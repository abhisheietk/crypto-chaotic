#!/usr/bin/python
# Tests the Cython in Python
import numpy as np
import pylab as plt
import mandel as md
import time
import mandel_openMP as md_omp
nn = 1000
ni = 1100;
re = np.linspace(-2.1,1,nn)
im = np.linspace(-1.3,1.3,ni)

st = time.time()
md.calc_num_iter(re, im, itermax=20, escape=2.) # calling Fortran
st = time.time() - st
print(st)

#out1 = md.calc_num_iter(re, im, itermax=20, escape=2.) # calling Fortran

#out2 = md_omp.calc_num_iter(re, im, itermax=20, escape=2.) # calling Fortran

# plt.imshow(out.T, extent=(re[0],re[-1],im[0],im[-1]))
# plt.show()
