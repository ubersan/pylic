import sys

from pylic.cli.console_reader import ConsoleReader


def main() -> None:
    sys.argv.pop(0)

    console_reader = ConsoleReader()
    tokens = console_reader.tokenize_input(sys.argv)
    program = console_reader.parse_tokens(tokens)
    print("program", program)
    program.command.handle(program.args)


if __name__ == "__main__":
    main()
