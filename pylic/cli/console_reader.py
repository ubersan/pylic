import re
from typing import List, NamedTuple

from pylic.cli.commands.command import Command
from pylic.cli.console_writer import console_writer


class Program(NamedTuple):
    command: Command
    options: List[str]


class ConsoleReader:
    def __init__(self, commands: List[Command]) -> None:
        self._commands = commands
        self._single_dash_option_pattern = re.compile(r"-[a-zA-Z]+")
        self._help_command = next(filter(lambda command: command.targets_to_token.token == "help", self._commands))

    def get_program(self, input: List[str]) -> Program:
        tokens = self._tokenize_input(input)
        return self._parse_tokens(tokens)

    def _tokenize_input(self, inputs: List[str]) -> List[str]:
        if len(inputs) == 0:
            return []

        sanitized_inputs: List[str] = []
        for target_candidate in inputs:
            if len(target_candidate) == 1:
                console_writer.write_invalid_input(target_candidate)
                exit(1)
            if self._single_dash_option_pattern.match(target_candidate):
                sanitized_inputs.extend([f"-{option}" for option in target_candidate[1:]])
            else:
                sanitized_inputs.append(target_candidate)

        tokens = []
        command_target = sanitized_inputs[0]
        command = next(filter(lambda command: command_target in command.targets_to_token.targets, self._commands), None)
        if command is None:
            console_writer.write_no_such_option(command_target) if command_target.startswith("-") else console_writer.write_no_such_command(
                command_target
            )
            exit(1)
        tokens.append(command.targets_to_token.token)

        if len(sanitized_inputs) > 0 and command.option_targets_to_token is not None:
            for option_target in sanitized_inputs[1:]:
                option_targets_to_token = next(
                    filter(lambda targets_to_token: option_target in targets_to_token.targets, command.option_targets_to_token),
                    None,
                )
                if option_targets_to_token is None:
                    console_writer.write_no_such_option_for_command(option_target, command.targets_to_token.token)
                    exit(1)
                tokens.append(option_targets_to_token.token)

        return tokens

    def _parse_tokens(self, tokens: List[str]) -> Program:
        if len(tokens) == 0:
            return Program(self._help_command, [])

        command = next(filter(lambda command: command.targets_to_token.token == tokens[0], self._commands))
        return Program(command, tokens[1:])
