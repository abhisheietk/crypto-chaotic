#!/usr/bin/bash

INSTALLDIR=/home/admin/usr/local
IPYTHON=${INSTALLDIR}/bin/ipython
export LD_LIBRARY_PATH=${INSTALLDIR}/lib:${LD_LIBRARY_PATH}
export LD_INCLUDE_PATH=${INSTALLDIR}/include:${LD_INCLUDE_PATH}
export PATH=${INSTALLDIR}/bin:${PATH}
insmod pciDriver/src/driver/pciDriver.ko
${IPYTHON} notebook --port 8889 --no-browser
rmmod pciDriver
