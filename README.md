OpenCLI
=========
Generate a command line interface based on OpenAPI Specification.

From the OpenAPI Specification project:

> The goal of The OpenAPI Specification is to define a standard, language-agnostic interface to REST APIs which allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection.

Demo
----

![Alt Text](https://github.com/sharbov/open-cli/blob/master/demo.gif)

Installation
------------
To install OpenCLI, simply:

    pip install opencli

Usage
-----

To start a CLI session run:

    open-cli <swagger-spec-url>

e.g:

    open-cli http://petstore.swagger.io/v2/swagger.json

For more options run:

    open-cli -h

Credits
-------
This project relies on Yelps [bravado](https://github.com/Yelp/bravado) project & on Jonathan Slenders [python-prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit).
