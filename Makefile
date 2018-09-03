.PHONY: all image pypi-upload

all: image

dist/opencli.tar.gz: $(shell find open_cli -name "*.py") requirements.txt README.md

	# Clean old versions
	rm -rf dist

	# Build the package
	python setup.py sdist

	# Rename the package to a constant name
	mv dist/opencli*.tar.gz dist/opencli.tar.gz

image: Dockerfile dist/opencli.tar.gz

	# Build a docker image
	docker build -t open-cli .

	# Extract version from container
	$(eval version:=$(shell docker run --entrypoint pip open-cli show opencli | awk '/Version:/ {print $$2}'))

	# Tag the image using the package version
	docker tag open-cli:latest open-cli:$(version)

pypi-upload:

	# Upload packge to pypi
	python setup.py sdist upload -r pypi

clean:

	# Delete generated files
	find -name "*.pyc" -delete
	rm -rf build dist opencli.egg-info .eggs
