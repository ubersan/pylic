import sys

from pylic.cli.commands.check import CheckCommand
from pylic.cli.commands.help import HelpCommand
from pylic.cli.commands.list import ListCommand
from pylic.cli.commands.version import VersionCommand
from pylic.cli.console_reader import ConsoleReader


def main() -> None:
    sys.argv.pop(0)

    program = ConsoleReader(
        commands=[
            CheckCommand(),
            ListCommand(),
            HelpCommand(),
            VersionCommand(),
        ]
    ).get_program(sys.argv)

    status_code = program.command.handle(program.options)
    exit(status_code)


if __name__ == "__main__":
    main()
