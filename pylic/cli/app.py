import sys

from pylic.cli.output import print_all_licenses_ok, print_command_not_available, print_global_help, print_too_many_arguments

# pylic -> global help
# pylic --help | -h -> global help

# pylic check
# pylic check --help | -h -> help of check command

# pylic list
# pylic list --help | -h -> help of list command

# pylic no match -> error string "no command found"

COMMANDS = ["check", "list"]
OPTIONS = {"--help": "help", "-h": "help"}


def app(args: list[str]) -> None:
    if len(args) == 0:
        print_global_help()
        exit(1)

    commands = list(filter(lambda arg: not (arg.startswith("--") or arg.startswith("-")), sys.argv))
    if len(commands) > 1:
        print_too_many_arguments()
        exit(1)

    command = "pylic"
    if len(commands) > 0:
        command = commands[0]
        if command not in COMMANDS:
            print_command_not_available(command)
            exit(1)

    options_list = list(filter(lambda arg: arg.startswith("--") or arg.startswith("-"), sys.argv))
    options = set()
    for option_candidate in options_list:
        option = OPTIONS.get(option_candidate)
        if option is None:
            print("option", option_candidate, "does not exist")
            exit(1)
        options.add(option)

    print_all_licenses_ok()
    exit(0)


def main() -> None:
    sys.argv.pop(0)
    app(sys.argv)


if __name__ == "__main__":
    main()
