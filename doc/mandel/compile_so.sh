#!/bin/sh
# Compiles various shared libraries.

gfortran -c -fPIC mandel.f90 -o mandel.o
# c-wrap in two forms
gfortran -shared -fPIC mandel.o mandel_wrap.f90 -o libmandel.so
gfortran -shared -fPIC mandel.o mandel_wrap_colmajor.f90 -o libmandel_colmajor.so
# c-wrap with openMP
gfortran -fopenmp -c -fPIC mandel.f90 -o mandel_openMP.o
gfortran -fopenmp -shared -fPIC mandel_openMP.o mandel_wrap.f90 -o libmandel_openMP.so
gfortran -fopenmp -shared -fPIC mandel_openMP.o mandel_wrap_colmajor.f90 -o libmandel_colmajor_openMP.so

# compile the c-runner using above shared lib
gfortran -L. -lmandel run_mandel_from_c.c -o cout_so
gfortran -L. -lmandel_openMP run_mandel_from_c.c -o cout_openmp_so

# compile the Fortran runner using a shared lib
gfortran -shared -fPIC mandel.f90 -o libmandel_fortran.so
gfortran -L. -lmandel_fortran run_mandel_from_fortran.f90 -o fout_so

# compile fortran directly to a shared lib
#gfortran -shared -fPIC mandel.f90 -o libmandel_f90.so
gfortran          -shared -fPIC mandel_wrap_f90.f90 mandel.o        -o libmandel_f90.so
gfortran -fopenmp -shared -fPIC mandel_wrap_f90.f90 mandel_openMP.o -o libmandel_f90_openMP.so
