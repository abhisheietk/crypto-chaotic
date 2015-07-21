#!/bin/sh

gcc -c run_from_c.c
gfortran -fcheck=all -c fortran_mod.f90 fortran_mod_wrap.f90

gfortran -fcheck=all fortran_mod.o fortran_mod_wrap.o run_from_c.o -o cout

