# Compiles the cython code.
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
npy_include_dir = numpy.get_include()

ext_modules = [Extension("mandel", ["pymandel.pyx"], include_dirs = [npy_include_dir],
               libraries=["gfortran"], extra_objects=["mandel.o", "mandel_wrap.o"])]

# ext_modules = [Extension("mandel", ["pymandel.pyx"], include_dirs = [npy_include_dir],
#                          extra_compile_args=['-fopenmp'],
#                          extra_link_args=['-fopenmp'],
#                          libraries=["gfortran"], extra_objects=["mandel_openMP.o", "mandel_wrap.o"])]

# other libraries which may need to be included for fortran:
# "quadmath", "m", ...
# To figure out which other ones are needed, run the last gcc command
# python setup.py build_ext --inplace spits out but replace "gcc" with
# (1) gcc -v and (2) gfortran -v and see what the difference are.
# (Note (2) should compile it such that the fortran function is found)

setup(name = 'Mandelbrot fractals',
      cmdclass = {'build_ext': build_ext},
      ext_modules = ext_modules)
