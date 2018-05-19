all: clean

pypi:
	python setup.py sdist upload -r pypi

clean:
	rm -rf build dist opencli.egg-info
