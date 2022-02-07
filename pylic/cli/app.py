import sys

from pylic.cli.commands.check import CheckCommand
from pylic.cli.commands.help import HelpCommand
from pylic.cli.commands.list import ListCommand
from pylic.cli.commands.version import VersionCommand
from pylic.cli.console_reader import ConsoleReader


def main() -> None:
    sys.argv.pop(0)

    console_reader = ConsoleReader(commands=[CheckCommand(), ListCommand(), HelpCommand(), VersionCommand()])
    program = console_reader.get_program(sys.argv)
    program.command.handle(program.options)


if __name__ == "__main__":
    main()
