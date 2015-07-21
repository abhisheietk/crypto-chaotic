from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
npy_include_dir = numpy.get_include()

ext_modules = [Extension("fort_wrap", ["py_fortran_mod_wrap.pyx"], include_dirs = [npy_include_dir],
               libraries=["gfortran"], extra_objects=["fortran_mod.o", "fortran_mod_wrap.o"])]

setup(name = 'Fortran wrapping',
      cmdclass = {'build_ext': build_ext},
      ext_modules = ext_modules)
