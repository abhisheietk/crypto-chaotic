# This wraps the mandel_wrap.f90 with cython to produce a python
# callable function.
import numpy as np
 
# this defines the external function's interface.  Note that the out
# needs to be defined as 'int *out' and not 'int **out'.
# // http://eli.thegreenplace.net/2010/04/06/pointers-vs-arrays-in-c-part-2d/
# The same holds for Julia and Matlab but not cffi.
cdef extern:
    void c_calc_num_iter(int nre, double *re, int nim, double *im,
                        int itermax, double escape, int *out)

def calc_num_iter(double[::1] re not None,
                   double[::1] im not None,
                     int itermax=20, double escape=2.):
    cdef int nre, nim
    nre = len(re)
    nim = len(im)
    # initialize the output array with cython so python manages the
    # memory:
    out = np.empty((nre, nim), dtype=np.int32)
    cdef int [:,::1] res = out
    
    c_calc_num_iter(nre, &re[0], nim, &im[0],
                     itermax, escape, &res[0,0])
    return out
