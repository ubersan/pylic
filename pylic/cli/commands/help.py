from cleo import Command

from pylic.__version__ import version


class HelpCommand(Command):
    name = "help"
    description = "Displays this help message"

    def handle(self) -> int:
        self.line(f"Pylic version <comment>{version}</>\n")
        self.line("<b>USAGE</>")
        self.line("  <u>pylic</> <command>\n")
        self.line("<b>ARGUMENTS</>")
        self.line("  <comment><command></>\tThe command to execute\n")
        self.line("<b>AVAILABLE COMMANDS</>")
        for command in self.application.commands:
            if command.name == "completions":
                continue

            self.line(f"  <comment>{command.name}</>\t\t{command.config.description}")

        return 1
