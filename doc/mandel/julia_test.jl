""" 
Illustrates how ccall can be used to call the various shared libs from
Julia.

Note: the pointer which points to the results array is defined as
Ptr{Cint} and not Ptr{Ptr{Cint}}.  The same needs to be done in Cython
as well but not in cffi.
"""

nn = 1000
ni = 1100;
re = linspace(-2.1,1,nn)
im = linspace(-1.3,1.3,ni)
itermax = 20
escape = 2.0
result = zeros(Cint, nn, ni)
resultT = result'

openMP = false

#showme(res) = show(res)
showme(res) = 1

# call the same shared lib as wrapped for c (in mandel_wrap.f90)
@time ccall((:c_calc_num_iter, "libmandel"), Void,
            (Cint, Ptr{Cdouble}, Cint, Ptr{Cdouble}, Cint, Cdouble, Ptr{Cint}),
            nn, re, ni, im, itermax, escape, resultT)
showme(resultT)
            
# call a shared lib which does not do the transposing of above  (in mandel_wrap_colmajor.f90)
@time ccall((:f_calc_num_iter, "libmandel_colmajor"), Void,
                (Cint, Ptr{Cdouble}, Cint, Ptr{Cdouble}, Cint, Cdouble, Ptr{Cint}),
                nn, re, ni, im, itermax, escape, result)
showme(result)
# call a shared lib which is direct Fortran without using the iso_c_bindings  (in mandel_wrap_f90.f90)
@time ccall((:f90_calc_num_iter, "libmandel_f90"), Void,
                (Ptr{Cint}, Ptr{Cdouble}, Ptr{Cint}, Ptr{Cdouble}, Ptr{Cint}, Ptr{Cdouble}, Ptr{Cint}),
                &nn, re, &ni, im, &itermax, &escape, result)
showme(result)
