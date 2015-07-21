#!/bin/sh
# note that the order of *.f90 files matters
gfortran -fcheck=all fortran_mod.f90 run_from_fortran.f90 -o fout
