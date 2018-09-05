.PHONY: all image pypi-upload

all: image

dist/opencli.tar.gz: $(shell find open_cli -name "*.py") requirements.txt README.md

	# Clean old versions
	rm -rf dist

	# Build the package
	python setup.py sdist

	# Rename the package to a constant name
	mv dist/opencli*.tar.gz dist/opencli.tar.gz

image:

	# Build a docker image
	docker build -t open-cli .

pypi-upload:

	# Upload packge to pypi
	python setup.py sdist upload -r pypi

clean:

	# Delete generated files
	find -name "*.pyc" -delete
	rm -rf build dist opencli.egg-info .eggs
