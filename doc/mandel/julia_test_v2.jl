"""
Does the same as julia_test.jl but written slightly more fancy.
"""
nn = 10000
ni = 3000
# nn = 10
# ni = 11
re = linspace(-2.1,1,nn)
im = linspace(-1.3,1.3,ni)
itermax = 50
escape = 2.0
result = zeros(Cint, nn, ni)-5
resultT = result'


#showme(res) = show(res)
showme(res) = 1

libs = ["libmandel", "libmandel_colmajor",  "libmandel_f90"]
fns = ["c_calc_num_iter", "f_calc_num_iter", "f90_calc_num_iter"]
results = {resultT, result, result}

for openMP in [true]  # running for both [true, false] does not load
                      # other libraries in the second loop.
    println("openMP ", openMP)
    for (lib, fn, res) in zip(libs, fns, results)
        if lib[end]!='0'
            case1 = true
        else
            case1 = false
        end
        if openMP
            lib = lib*"_openMP"
        end
        println(lib)
        if case1
            @eval @time ccall(($fn, $lib), Void,
                              (Cint, Ptr{Cdouble}, Cint, Ptr{Cdouble}, Cint, Cdouble, Ptr{Cint}),
                              nn, re, ni, im, itermax, escape, $res)
        else
            @eval @time ccall(($fn, $lib), Void,
                              (Ptr{Cint}, Ptr{Cdouble}, Ptr{Cint}, Ptr{Cdouble}, Ptr{Cint}, Ptr{Cdouble}, Ptr{Cint}),
                              &nn, re, &ni, im, &itermax, &escape, $res)
        end
        showme(res)
    end
end
