from cleo import Application

from pylic.__version__ import version
from pylic.cli.commands.check import CheckCommand
from pylic.cli.commands.list import ListCommand

app = Application("pylic", version, complete=True)
app.add(ListCommand())
app.add(CheckCommand())


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()
