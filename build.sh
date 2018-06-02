rm -r build
rm -r dist
rm -r gmapi.egg-info
python setup.py clean
python setup.py sdist bdist_wheel
