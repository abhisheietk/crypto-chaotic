#!/bin/bash

cat installed.txt | xargs sudo rm -rf
python2 setup.py clean
python2 setup.py sdist
python2 setup.py bdist
sudo python2 setup.py install --record installed.txt
sudo pypy setup.py install --record installed1.txt
#service httpd restart

