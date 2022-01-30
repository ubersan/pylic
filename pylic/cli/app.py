import sys

# pylic -> global help
# pylic --help | -h -> global help

# pylic version
# pylic version --help | -h -> help of version command

# pylic check
# pylic check --help | -h -> help of check command

# pylic list
# pylic list --help | -h -> help of list command

# pylic no match -> error string "no command found"

COMMANDS = ["check", "list", "version"]
OPTIONS = {"--help": "help", "-h": "help"}


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def app(args: list[str]) -> None:
    if len(args) == 0:
        print("global help")
        exit(1)

    commands = list(filter(lambda arg: not (arg.startswith("--") or arg.startswith("-")), sys.argv))
    if len(commands) > 1:
        print("too many arguments")
        exit(1)

    command = "pylic"
    if len(commands) > 0:
        command = commands[0]
        if command not in COMMANDS:
            print("command", command, "is not availabe")
            exit(1)

    options_list = list(filter(lambda arg: arg.startswith("--") or arg.startswith("-"), sys.argv))
    options = set()
    for option_candidate in options_list:
        option = OPTIONS.get(option_candidate)
        if option is None:
            print("option", option_candidate, "does not exist")
            exit(1)
        options.add(option)

    print(bcolors.OKBLUE, bcolors.UNDERLINE, "running", command, "with options", options, "\033[0m")
    exit(0)


def main() -> None:
    sys.argv.pop(0)
    app(sys.argv)


if __name__ == "__main__":
    main()
