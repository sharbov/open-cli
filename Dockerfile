FROM python:3.6-alpine

COPY dist/opencli.tar.gz /opencli.tar.gz

RUN pip install --no-cache /opencli.tar.gz

ENTRYPOINT ["open-cli"]
