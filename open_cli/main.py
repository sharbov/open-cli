import os
import logging
import argparse

import cli
import formatter

HISTORY_PATH = os.path.join(os.path.expanduser("~"), ".open-cli")


def main():
    """Open-CLI entry point."""
    args_parser = argparse.ArgumentParser(description='Open-CLI.')
    args_parser.add_argument('source', type=str, help='Open API spec source')
    args_parser.add_argument('-v', '--verbose', action='store_true', help='If set, set log level to debug')
    args_parser.add_argument('-t', '--history', type=str, default=HISTORY_PATH, help='history file path')
    args_parser.add_argument('-c', '--command', type=str, help='command to execute', required=False)
    args_parser.add_argument('-f', '--format', type=str,
                             choices=formatter.FORMATTERS.keys(), default=formatter.JSON,
                             help='Set the CLI output format')
    args_parser.add_argument('--header', nargs='+', default=[],
                             help='requests headers, usage: --header x-header-1:val-1 x-header-2:val2')

    args = args_parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.ERROR)

    open_cli = cli.OpenCLI(
        source=args.source,
        history_path=args.history,
        output_format=args.format,
        headers=args.header,
    )

    if args.command:
        return open_cli.execute(command=args.command)

    open_cli.run_loop()


if __name__ == '__main__':
    main()
