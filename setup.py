#from distutils.core import setup
#from Cython.Build import cythonize
#from distutils.extension import Extension
from distutils.core import setup, Extension

#'''C_module = Extension('crypto-g.libcipher',
#                     sources = ['crypto-g/cipher.c'],
#                     libraries=[])'''

#cython_modules = cythonize([Extension("gcipher", ["crypto-g1/gcipher.pyx"],
#                                      libraries=['cipher'],
#                                      #include_dirs=[ 'crypto-g' ],
#                                      #library_dirs=[ 'crypto-g' ],
#                                      ),
#        ])

##modules = [C_module, cython_modules[0]]
#modules = [cython_modules[0]]
##cython_modules.append(C_module)

setup(name='crypto_chaotic',
      version='0.1.0',
      author='Abhishek Bajpai',
      author_email='abbajpai@barc.gov.in',
      packages=['crypto_chaotic'],
      #ext_modules = modules,
      #ext_modules = cythonize("PyPci/*.pyx"),
      scripts=[ ],
      url=' ',
      license='LICENSE.txt',
      description='Useful stuff.',
      long_description=open('README.txt').read(),
      #install_requires=[    ],
      )
