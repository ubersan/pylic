from importlib.metadata import Distribution
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from pylic.__version__ import version
from pylic.config import Config
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


def test_successful_check_prints_all_licenses_ok_with_classifier(mocker: MockerFixture) -> None:
    given_distributions(
        mocker,
        [
            MagicMock(
                Distribution, metadata={"Classifier": "License :: MIT License", "Name": "pylic", "Version": "1.2.3"}
            )
        ],
    )
    given_config(mocker, Config(safe_licenses=["MIT License"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 0
    assert "✨ All licenses ok ✨" in result.stdout


def test_successful_check_prints_all_licenses_ok_with_license(mocker: MockerFixture) -> None:
    given_distributions(
        mocker, [MagicMock(Distribution, metadata={"License": "MIT License", "Name": "pylic", "Version": "1.2.3"})]
    )
    given_config(mocker, Config(safe_licenses=["MIT License"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 0
    assert "✨ All licenses ok ✨" in result.stdout


def test_successful_check_prints_all_licenses_ok_with_license_expression(mocker: MockerFixture) -> None:
    given_distributions(
        mocker,
        [MagicMock(Distribution, metadata={"License-Expression": "MIT License", "Name": "pylic", "Version": "1.2.3"})],
    )
    given_config(mocker, Config(safe_licenses=["MIT License"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 0
    assert "✨ All licenses ok ✨" in result.stdout


def test_successful_check_prints_all_licenses_ok_with_spdx_license_expression(mocker: MockerFixture) -> None:
    given_distributions(
        mocker,
        [
            MagicMock(
                Distribution,
                metadata={"License-Expression": "0BSD or miT or apache-2.0", "Name": "pylic", "Version": "1.2.3"},
            )
        ],
    )
    given_config(mocker, Config(safe_licenses=["MIT", "0BSD", "Apache-2.0"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 0
    assert "✨ All licenses ok ✨" in result.stdout


def test_quiet_flag(mocker: MockerFixture) -> None:
    given_distributions(
        mocker,
        [MagicMock(Distribution, metadata={"License-Expression": "MIT License", "Name": "pylic", "Version": "1.2.3"})],
    )
    given_config(mocker, Config(safe_licenses=["MIT License"]))
    result = runner.invoke(app, ["check", "--quiet"])
    assert result.exit_code == 0
    assert "✨ All licenses ok ✨" not in result.stdout


def test_unnecessary_safe_license_is_correctly_detected(mocker: MockerFixture) -> None:
    given_distributions(
        mocker, [MagicMock(Distribution, metadata={"License": "MIT License", "Name": "pylic", "Version": "1.2.3"})]
    )
    given_config(mocker, Config(safe_licenses=["MIT License", "MIT License2"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 1
    assert "Safe licenses listed which are not used by any installed package:" in result.stdout
    assert "MIT License2" in result.stdout
    assert "✨ All licenses ok ✨" not in result.stdout


def test_unnecessary_unsafe_package_is_correctly_detected(mocker: MockerFixture) -> None:
    given_distributions(
        mocker, [MagicMock(Distribution, metadata={"License": "MIT License", "Name": "pylic", "Version": "1.2.3"})]
    )
    given_config(mocker, Config(safe_licenses=["MIT License"], unsafe_packages=["pylic2"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 1
    assert "Unsafe packages listed which are not installed:" in result.stdout
    assert "pylic2" in result.stdout
    assert "✨ All licenses ok ✨" not in result.stdout


def test_unsafe_package_with_safe_license_is_correctly_detected(mocker: MockerFixture) -> None:
    given_distributions(
        mocker,
        [
            MagicMock(Distribution, metadata={"License": "MIT License", "Name": "pylic1", "Version": "1.2.3"}),
            MagicMock(Distribution, metadata={"License": "MIT License2", "Name": "pylic2", "Version": "1.2.2"}),
        ],
    )
    given_config(mocker, Config(safe_licenses=["MIT License", "MIT License2"], unsafe_packages=["pylic2"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 1
    assert "Unsafe packages listed that have a safe license:" in result.stdout
    assert "pylic2" in result.stdout
    assert "pylic1" not in result.stdout
    assert "✨ All licenses ok ✨" not in result.stdout


def test_package_with_unsafe_licenses_are_correctly_detected(mocker: MockerFixture) -> None:
    given_distributions(
        mocker,
        [
            MagicMock(Distribution, metadata={"License": "MIT License", "Name": "pylic1", "Version": "1.2.3"}),
            MagicMock(Distribution, metadata={"License": "MIT License2", "Name": "pylic2", "Version": "1.2.2"}),
        ],
    )
    given_config(mocker, Config(safe_licenses=["MIT License"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 1
    assert "Found installed packages with unsafe licenses:" in result.stdout
    assert "pylic2 (1.2.2): MIT License2" in result.stdout
    assert "pylic1" not in result.stdout
    assert "✨ All licenses ok ✨" not in result.stdout


@pytest.mark.parametrize("operator", ["AND", "OR"])
def test_check_fails_for_spdx_expression_with_unsafe_license(mocker: MockerFixture, operator: str) -> None:
    given_distributions(
        mocker,
        [
            MagicMock(
                Distribution,
                metadata={
                    "License-Expression": f"Apache-2.0 {operator} GPL-3.0-only",
                    "Name": "pkg",
                    "Version": "1.0.0",
                },
            )
        ],
    )
    given_config(mocker, Config(safe_licenses=["Apache-2.0"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 1
    assert "Found installed packages with unsafe licenses:" in result.stdout
    assert "pkg (1.0.0): Apache-2.0,GPL-3.0-only" in result.stdout
    assert "✨ All licenses ok ✨" not in result.stdout


@pytest.mark.parametrize("license_metadata", [{}, {"License": "unknown"}, {"License": "UNKNOWN"}])
def test_packages_with_unknown_license_are_correctly_detected(
    mocker: MockerFixture, license_metadata: dict[str, str]
) -> None:
    given_distributions(
        mocker,
        [
            MagicMock(Distribution, metadata={"Name": "pylic1", "Version": "1.2.3", **license_metadata}),
            MagicMock(Distribution, metadata={"License": "MIT License2", "Name": "pylic2", "Version": "1.2.2"}),
        ],
    )
    given_config(mocker, Config(safe_licenses=["MIT License2"]))
    result = runner.invoke(app, "check")
    assert result.exit_code == 1
    assert "Found packages with unknown license, mark them as unsafe:" in result.stdout
    assert "Found installed packages with unsafe licenses:" not in result.stdout
    assert "pylic1 (1.2.3)" in result.stdout
    assert "pylic2" not in result.stdout
    assert "✨ All licenses ok ✨" not in result.stdout


def test_successful_list_prints_all_installed_packages_and_licenses(mocker: MockerFixture) -> None:
    given_distributions(
        mocker,
        [
            MagicMock(
                Distribution, metadata={"License-Expression": "MIT License1", "Name": "pylic1", "Version": "1.2.1"}
            ),
            MagicMock(
                Distribution, metadata={"License-Expression": "MIT License2", "Name": "pylic2", "Version": "1.2.2"}
            ),
            MagicMock(
                Distribution, metadata={"License-Expression": "MIT License3", "Name": "pylic3", "Version": "1.2.3"}
            ),
            MagicMock(
                Distribution, metadata={"License-Expression": "MIT License4", "Name": "pylic4", "Version": "1.2.4"}
            ),
        ],
    )
    result = runner.invoke(app, "list")
    assert result.exit_code == 0
    assert "pylic1 (1.2.1): MIT License1" in result.stdout
    assert "pylic2 (1.2.2): MIT License2" in result.stdout
    assert "pylic3 (1.2.3): MIT License3" in result.stdout
    assert "pylic4 (1.2.4): MIT License4" in result.stdout


def test_successful_list_prints_all_licenses_ok_with_spdx_license_expression(mocker: MockerFixture) -> None:
    given_distributions(
        mocker,
        [
            MagicMock(
                Distribution,
                metadata={"License-Expression": "0BSD or miT or apache-2.0", "Name": "pylic", "Version": "1.2.3"},
            )
        ],
    )
    given_config(mocker, Config(safe_licenses=["MIT", "0BSD", "Apache-2.0"]))
    result = runner.invoke(app, "list")
    assert result.exit_code == 0
    assert "pylic (1.2.3): 0BSD,Apache-2.0,MIT" in result.stdout


def test_version_command_prints_version() -> None:
    result = runner.invoke(app, "version")
    assert result.exit_code == 0
    assert f"{version}\n" == result.stdout


def given_distributions(mocker: MockerFixture, distributions: list[Distribution]) -> None:
    mocker.patch("pylic.licenses.distributions", return_value=distributions)


def given_config(mocker: MockerFixture, config: Config) -> None:
    mocker.patch("pylic.main.read_config", return_value=config)
