#!/bin/sh
# Compiles the cython shared lib

# make the *.o files
gfortran -fPIC -c mandel.f90 mandel_wrap.f90 
gfortran -fopenmp -fPIC -c mandel.f90 -o mandel_openMP.o
 
# make the cython stuff
python setup.py build_ext --inplace 
rm pymandel.c  # this is needed otherwise import does not work
python setup_openmp.py build_ext --inplace 


