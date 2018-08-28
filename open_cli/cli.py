#!/usr/bin/python3
"""Open-CLI."""
import os
import logging
import warnings

from bravado.client import SwaggerClient

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

import parser
import completer
import formatter

# Suppress bravado warnings
warnings.filterwarnings("ignore")


class OpenCLI:
    """CLI processor."""

    def __init__(self, source, history_path, output_format="raw", headers=None):
        """Initialize the CLI processor."""
        self.history_path = history_path
        self.output_format = output_format

        self.logger = logging.getLogger("open-cli")
        self.logger.debug("Creating a python client based on %s, headers: %s", source, headers)

        headers = self._parse_headers(headers)

        # Handle non-url sources
        if os.path.exists(source):
            source = "file://" + source

        self.client = SwaggerClient.from_url(
            source,
            request_headers=headers,
            config={
                'use_models': False,
                'validate_responses': False,
                'validate_swagger_spec': False,
            }
        )

        # Get the CLI prompt name from the spec title
        self.name = self.client.swagger_spec.spec_dict["info"].get("title", u"Open-CLI")

        # Initialize a command parser based on the client
        self.command_parser = parser.CommandParser(client=self.client)

    def run_loop(self):
        """Run the CLI loop."""
        history = FileHistory(self.history_path)
        command_completer = completer.CommandCompleter(client=self.client)

        while True:

            try:
                input_text = prompt(
                    u"%s $ " % self.name,
                    history=history,
                    completer=command_completer,
                    auto_suggest=AutoSuggestFromHistory(),
                )
                self.execute(command=input_text)

            except KeyboardInterrupt:
                exit("User Exited")

            except Exception as exc:
                self.logger.error(exc)

    def execute(self, command):
        """Parse and execute the given command."""
        self.logger.debug("Parsing the input text %s", command)
        operation, arguments = self.command_parser.parse(text=command)

        self.logger.debug("Invoke operation %s with arguments %s", operation, arguments)
        response = operation(**arguments).result()

        self.logger.debug("Formatting response %s", response)
        print(formatter.format_response(response, output_format=self.output_format))

    @staticmethod
    def _parse_headers(headers):
        """Parse headers list into a dictionary."""
        try:
            return dict(header.split(":") for header in headers)
        except:
            raise ValueError("Invalid headers %s" % headers)


if __name__ == '__main__':
    OpenCLI("http://petstore.swagger.io/v2/swagger.json").run_loop()
