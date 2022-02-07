from typing import NamedTuple

from pylic.cli.commands.check import CheckCommand
from pylic.cli.commands.command import Command
from pylic.cli.commands.help import HelpCommand
from pylic.cli.commands.list import ListCommand
from pylic.cli.commands.version import VersionCommand
from pylic.cli.console_writer import print_no_such_command, print_no_such_option, print_too_many_arguments

HELP = "help"
VERSION = "version"
CHECK = "check"
LIST = "list"

OPTION_TOKENS = {"-h": HELP, "--help": HELP, "-V": VERSION, "--version": VERSION}
COMMAND_TOKENS = {"check": CHECK, "list": LIST}

COMMANDS = {CHECK: CheckCommand(), LIST: ListCommand(), HELP: HelpCommand(), VERSION: VersionCommand()}


class Program(NamedTuple):
    command: Command
    args: list[str]


class ConsoleReader:
    def tokenize_input(self, raw_strings: list[str]) -> list[str]:
        tokens = []
        for raw in raw_strings:
            if raw.startswith("-"):
                candidate = raw[:2]  # single dash options only allow a single char
                if raw.startswith("--"):
                    candidate = raw
                option = OPTION_TOKENS.get(candidate)
                if option is None:
                    print_no_such_option(candidate)
                    exit(1)
                tokens.append(option)
                continue

            command = COMMAND_TOKENS.get(raw)
            if command is None:
                print_no_such_command(raw)
                exit(1)
            tokens.append(command)

        return tokens

    def parse_tokens(self, tokens: list[str]) -> Program:
        if len(tokens) == 0:
            return Program(COMMANDS[HELP], [])

        non_repeating_tokens = [tokens[0]]
        for token in tokens:
            if non_repeating_tokens[-1] == token:
                continue
            non_repeating_tokens.append(token)

        if sum(map(lambda _: 1, filter(lambda token: token in [CHECK, LIST], tokens))) > 1:
            print_too_many_arguments()
            exit(1)

        return Program(COMMANDS[non_repeating_tokens[0]], non_repeating_tokens[1:])
