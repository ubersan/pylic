from cleo import Application

from pylic.cli.commands.check import CheckCommand
from pylic.cli.commands.list import ListCommand
from pylic.toml import version

app = Application(name="pylic", version=version, complete=True)
app.add(ListCommand())
app.add(CheckCommand())


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()
