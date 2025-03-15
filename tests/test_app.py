from typer.testing import CliRunner

from pylic.__version__ import version
from pylic.main import app

runner = CliRunner()


def test_no_command_prints_error_message() -> None:
    result = runner.invoke(app)
    assert result.exit_code == 2
    assert "Usage:" in result.stdout
    assert "pylic [OPTIONS] COMMAND [ARGS]..." in result.stdout
    assert "Try" in result.stdout
    assert "for help." in result.stdout


def test_help_option_prints_help_message() -> None:
    result = runner.invoke(app, "--help")
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "pylic [OPTIONS] COMMAND [ARGS]..." in result.stdout
    assert "Commands" in result.stdout


def test_successful_check_prints_all_licenses_ok() -> None:
    result = runner.invoke(app, "check")
    assert result.exit_code == 0
    assert "✨ All licenses ok ✨" in result.stdout


def test_successful_list_prints_all_installed_packages_and_licenses() -> None:
    result = runner.invoke(app, "list")
    assert result.exit_code == 0
    assert "click" in result.stdout
    assert "mypy" in result.stdout
    assert "toml" in result.stdout
    assert "MIT License" in result.stdout
    assert "BSD License" in result.stdout


def test_version_command_prints_version() -> None:
    result = runner.invoke(app, "version")
    assert result.exit_code == 0
    assert f"{version}\n" == result.stdout
