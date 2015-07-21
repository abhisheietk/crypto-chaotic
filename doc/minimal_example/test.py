#!/usr/bin/python
import numpy as np
import fort_wrap as fw
nn = 5
aint = 5
ve = np.array([3,4,6,78,99], dtype=np.double)
ar = np.zeros((3,4), dtype=np.double) + 3.4
ar[0,0] = -10.5
ar[1,0] = -100.5

out = fw.fortran_fun(aint, ve, ar)

print(out)
