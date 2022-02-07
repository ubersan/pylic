from pylic.__version__ import version

LABEL = "\033[96m"
SUCCESS = "\033[92m"
WARNING = "\033[93m"
ERROR = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END_STYLE = "\033[0m"


def label(text: str) -> str:
    return f"{LABEL}{text}{END_STYLE}"


def header(text: str) -> str:
    return f"{BOLD}{text}{END_STYLE}"


def print_global_help() -> None:
    print(f"Pylic version {label(version)}\n")
    print(f'{header("USAGE")}')
    print(f"  {UNDERLINE}pylic{END_STYLE} [-h] [-V] <command>\n")
    print(f'{header("ARGUMENTS")}')
    print(f"  {LABEL}<command>{END_STYLE}\t\tThe command to execute\n")
    print(f'{header("GLOBAL OPTIONS")}')
    print(f"  {LABEL}-h{END_STYLE} (--help)\t\tDisplay this or a commands help message")
    print(f"  {LABEL}-V{END_STYLE} (--version)\tDisplay this application version\n")
    print(f'{header("AVAILABLE COMMANDS")}')
    print(f"  {LABEL}check{END_STYLE}\t\t\tChecks all installed licenses")
    print(f"  {LABEL}list{END_STYLE}\t\t\tLists all installed packages and their corresponding license\n")


def print_too_many_arguments() -> None:
    print(f"{ERROR}{BOLD}Too many arguments.{END_STYLE}")


def print_no_such_command(command: str) -> None:
    print(f'{ERROR}{BOLD}The command "{command}" is not available.{END_STYLE}')


def print_no_such_option(option: str) -> None:
    print(f'{ERROR}{BOLD}The option "{option}" is not available.{END_STYLE}')


def print_all_licenses_ok() -> None:
    print(f"{SUCCESS}All licenses ok{END_STYLE}")
