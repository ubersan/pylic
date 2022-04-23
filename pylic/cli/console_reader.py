from typing import List, NamedTuple

from pylic.cli.commands.command import Command
from pylic.cli.console_writer import console_writer


class Program(NamedTuple):
    command: Command
    options: List[str]


class ConsoleReader:
    def __init__(self, commands: List[Command]) -> None:
        self.target_to_token = {target: command for command in commands for target in command.targets}
        self.token_to_command = {command.token: command for command in commands}
        self.help_command = next(filter(lambda command: command.token == "help", commands))

    def get_program(self, input: List[str]) -> Program:
        tokens = self._tokenize_input(input)
        return self._parse_tokens(tokens)

    def _tokenize_input(self, raw_strings: List[str]) -> List[str]:
        tokens = []
        for raw in raw_strings:
            if raw.startswith("-"):
                candidate = raw[:2]  # single dash options only allow a single char
                if raw.startswith("--"):
                    candidate = raw
                command = self.target_to_token.get(candidate)
                if command is None:
                    console_writer.write_no_such_option(candidate)
                    exit(1)
                tokens.append(command.token)
                continue

            command = self.target_to_token.get(raw)
            if command is None:
                console_writer.write_no_such_command(raw)
                exit(1)
            tokens.append(command.token)

        return tokens

    def _parse_tokens(self, tokens: List[str]) -> Program:
        if len(tokens) == 0:
            return Program(self.help_command, [])

        return Program(self.token_to_command[tokens[0]], tokens[1:])
