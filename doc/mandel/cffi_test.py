#!/usr/bin/python
"""
This uses the python-cffi library: http://cffi.readthedocs.org/en/release-0.8/, i.e. the
Foreign Function Interface for Python calling C code.

This is quite similar to the ccall of Julia and calllib of Matlab.
"""
from cffi import FFI
import numpy as np

ffi = FFI()
nn = 5000
ni = 1001

ffi.cdef("void c_calc_num_iter(int nre, double *re, int nim, double *im, int itermax, double escape, int out[%d][%d]);" % (nn, ni))
## using the header as in C does not work:
#ffi.cdef("""void c_calc_num_iter(int nre, double re[nre], int nim, double im[nim], int itermax, double escape, int out[nre][nim]);""")

lib = ffi.dlopen('./libmandel.so')
#lib = ffi.dlopen('./libmandel_openMP.so') # using openMP does not really work with cffi 0.7.2 ...


re = ffi.new("double[]", np.linspace(-2.1,1,nn).tolist())
im = ffi.new("double[]", np.linspace(-1.3,1.3,ni).tolist())
res = ffi.new("int[%d][%d]" % (nn, ni))


itermax = 20
escape = 2.

lib.c_calc_num_iter(nn, re, ni, im, itermax, escape, res)

ress = np.empty([nn,ni])
min_ = 0
max_ = 0
for i in range(nn):
    for j in range(ni):
        min_ = min(min_, res[i][j])
        max_ = max(min_, res[i][j])
        ress[i,j] = res[i][j]


## plot        
# import pylab as plt
# plt.imshow(ress.T)
# plt.show()


# REFS:
# http://stackoverflow.com/questions/16276268/how-to-pass-a-numpy-array-into-a-cffi-function-and-how-to-get-one-back-out
