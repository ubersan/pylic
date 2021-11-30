from cleo import Application
from cleo.config import ApplicationConfig
from clikit.api.args.format.option import Option

from pylic.__version__ import version
from pylic.cli.commands.check import CheckCommand
from pylic.cli.commands.help import HelpCommand
from pylic.cli.commands.list import ListCommand


# Set custom app config to be able to provide our own help function.
# This allows to have complete control over the text and the return code.
class AppConfig(ApplicationConfig):
    def configure(self) -> None:
        self.set_io_factory(self.create_io)


config = AppConfig()
config.add_option("help", "h", Option.NO_VALUE, "Displays this help message")

app = Application("pylic", version, complete=True, config=config)
app.add(CheckCommand())
app.add(HelpCommand().default())
app.add(ListCommand())


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()
