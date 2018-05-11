import logging
import argparse

from open_cli import cli


def main():
    """Open-CLI entry point."""
    args_parser = argparse.ArgumentParser(description='Open-CLI.')
    args_parser.add_argument('source', type=str, help='Open API spec source')
    args_parser.add_argument('-v', '--verbose', action='store_true', help='If set, set log level to debug')
    args_parser.add_argument('-t', '--history', type=str, default='history.txt', help='history file path')
    args_parser.add_argument('-c', '--command', type=str, help='command to execute', required=False)
    args_parser.add_argument('-f', '--format', type=str, choices=['raw', 'table'], default='raw',
                             help='Set the CLI output format')

    args = args_parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    open_cli = cli.OpenCLI(
        source=args.source,
        history_path=args.history,
        output_format=args.format
    )

    if args.command:
        return open_cli.execute(command=args.command)

    open_cli.run_loop()


if __name__ == '__main__':
    main()
