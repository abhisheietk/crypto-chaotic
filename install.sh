cat install.log | xargs rm -rf
python setup.py clean
rm -rf dist
rm -rf build
python setup.py sdist
python setup.py bdist
sudo python setup.py install --record install.log