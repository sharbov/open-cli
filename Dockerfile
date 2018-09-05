FROM python:3.6 AS build

# Set build work directory
WORKDIR /open-cli/

# Install build requirements
RUN pip install pbr==1.8.0

# Copy config files into the build container
COPY .git /open-cli/.git
COPY LICENSE /open-cli/LICENSE
COPY setup.py /open-cli/setup.py
COPY setup.cfg /open-cli/setup.cfg
COPY README.md /open-cli/README.md
COPY requirements.txt /open-cli/requirements.txt

# Copy package code into the build container
COPY open_cli/*.py /open-cli/open_cli/

# Build the package and set its name
RUN python setup.py sdist && mv dist/opencli*.tar.gz dist/opencli.tar.gz

# -----------------------------------------------------------------------

FROM python:3.6-alpine AS release

# Set entrypoint
ENTRYPOINT ["open-cli"]

# Copy & install package requirements
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy & install packge
COPY --from=build /open-cli/dist/opencli.tar.gz /opencli.tar.gz
RUN pip install --no-cache --no-deps /opencli.tar.gz
