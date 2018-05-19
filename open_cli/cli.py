#!/usr/bin/python3
"""Open-CLI."""
import logging
import warnings

from bravado.client import SwaggerClient

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from open_cli import parser
from open_cli import completer
from open_cli import formatter

# Suppress bravado warnings
warnings.filterwarnings("ignore")


class OpenCLI:
    """CLI processor."""

    def __init__(self, source, history_path="history.txt", output_format="raw"):
        """Initialize the CLI processor."""
        self.history_path = history_path
        self.output_format = output_format

        self.logger = logging.getLogger("open-cli")
        self.logger.debug("Creating a python client based on %s", source)
        self.client = SwaggerClient.from_url(
            source,
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
                    self.name + " $ ",
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


if __name__ == '__main__':
    OpenCLI("http://petstore.swagger.io/v2/swagger.json").run_loop()
