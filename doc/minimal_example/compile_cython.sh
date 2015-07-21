#!/bin/sh

# make 
gfortran -fPIC -c fortran_mod.f90 fortran_mod_wrap.f90

# make the cython stuff
python setup.py build_ext --inplace 
