import numpy as np
 
# this defines the external function's interface.  Why the out needs
# to be defined as 'int *out' and not 'int **out' I do not know...
cdef extern:
    void fort_fun_wrap(int a_int, int na_vec, double *a_vec,
                       int nia_array, int nja_array, double *a_array,
                       double *out)

def fortran_fun(int a_int,
                double[::1] vec not None,
                double[:,::1] arr not None):
    cdef int nv, ni, nj
    nv = len(vec)
    ni = arr.shape[0]
    nj = arr.shape[1]
    # initialize the output array with cython so python manages the
    # memory:
    out = np.empty((nv, ni), dtype=np.double)
    cdef double [:,::1] res = out
    
    fort_fun_wrap(a_int, nv, &vec[0],
                  ni, nj, &arr[0,0],
                  &res[0,0])
    return out
