#!/bin/bash
PYTHON=~/usr/local/bin/python2

cat installed.txt | xargs sudo rm -rf
${PYTHON} setup.py clean
${PYTHON} setup.py sdist
${PYTHON} setup.py bdist
sudo ${PYTHON} setup.py install --record installed.txt
sudo pypy setup.py install --record installed1.txt
#service httpd restart

