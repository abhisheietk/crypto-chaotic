#!/bin/sh
# Compiles the Fortran executables

# note that the order of *.f90 files matters

gfortran -c mandel.f90 -o  mandel.o
gfortran -c run_mandel_from_fortran.f90
gfortran mandel.o run_mandel_from_fortran.o -o fout

# with openMP
gfortran -fopenmp -c mandel.f90 -o  mandel_openMP.o
gfortran -fopenmp mandel_openMP.o run_mandel_from_fortran.o -o fout_openMP
