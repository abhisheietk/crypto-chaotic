#!/bin/sh
# Compiles the C executable

gcc -c run_mandel_from_c.c
gfortran -c mandel.f90 mandel_wrap.f90
gfortran mandel.o mandel_wrap.o run_mandel_from_c.o  -o cout

gfortran -fopenmp -c mandel.f90 -o mandel_openMP.o
gfortran -fopenmp mandel_openMP.o mandel_wrap.o run_mandel_from_c.o -o cout_openmp

# note that when running above command with gcc it needs to specify the additional library 'm':
#gcc -lm mandel.o mandel_wrap.o run_mandel_from_c.o  -o cout
