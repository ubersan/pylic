from typing import List

from pylic.cli.commands.command import Command, TargetsToToken
from pylic.cli.console_writer import BLUE, BOLD, END_STYLE, LABEL, UNDERLINE, WARNING, console_writer
from pylic.license_checker import LicenseChecker
from pylic.licenses import read_all_installed_licenses_metadata
from pylic.toml import read_config


class CheckCommand(Command):
    targets_to_token = TargetsToToken(targets=["check"], token="check")
    option_targets_to_token = [
        TargetsToToken(targets=["--allow-extra-unused-packages", "-p"], token="allow_extra_packages"),
        TargetsToToken(targets=["--allow-extra-safe-licenses", "-l"], token="allow_extra_licenses"),
        TargetsToToken(targets=["--help", "-h"], token="help"),
    ]

    def handle(self, options: List[str]) -> int:
        if "help" in options:
            self._show_help()
            return 1

        config = read_config()
        installed_licenses = read_all_installed_licenses_metadata()
        checker = LicenseChecker(config, installed_licenses)

        unnecessary_safe_licenses = checker.get_unnecessary_safe_licenses()
        unnecessary_unsafe_packages = checker.get_unnecessary_unsafe_packages()
        unnecessary_ignore_packages = checker.get_unnecessary_ignore_packages()
        bad_unsafe_packages = checker.get_bad_unsafe_packages()
        missing_unsafe_packages = checker.get_missing_unsafe_packages()
        unsafe_licenses = checker.get_unsafe_licenses()

        if any(
            [
                unnecessary_safe_licenses,
                unnecessary_unsafe_packages,
                unnecessary_ignore_packages,
                bad_unsafe_packages,
                missing_unsafe_packages,
                unsafe_licenses.found,
            ]
        ):
            if len(unnecessary_safe_licenses) > 0:
                console_writer.line("Unnecessary safe licenses listed which are not used by any installed package:")
                for unnecessary_safe_license in unnecessary_safe_licenses:
                    console_writer.line(f"  {WARNING}{unnecessary_safe_license}{END_STYLE}")

            if len(unnecessary_unsafe_packages) > 0:
                console_writer.line("Unsafe packages listed which are not installed:")
                for unnecessary_unsafe_package in unnecessary_unsafe_packages:
                    console_writer.line(f"  {WARNING}{unnecessary_unsafe_package}{END_STYLE}")

            if len(unnecessary_ignore_packages) > 0:
                console_writer.line("Ignore packages listed which are not installed:")
                for unnecessary_ignore_package in unnecessary_ignore_packages:
                    console_writer.line(f"  {WARNING}{unnecessary_ignore_package}{END_STYLE}")

            if len(bad_unsafe_packages) > 0:
                console_writer.line("Found unsafe packages with a known license. Instead allow these licenses explicitly:")
                for bad_package in bad_unsafe_packages:
                    console_writer.line(
                        (
                            f"  {WARNING}{bad_package['package']}{END_STYLE} {LABEL}({bad_package['version']}{END_STYLE}): "
                            f"{BLUE}{bad_package['license']}{END_STYLE}"
                        )
                    )

            if len(missing_unsafe_packages) > 0:
                console_writer.line("Found unsafe packages:")
                for missing_unsafe_package in missing_unsafe_packages:
                    console_writer.line(
                        (
                            f"  {WARNING}{missing_unsafe_package['package']}{END_STYLE} "
                            f"{LABEL}({missing_unsafe_package['version']}){END_STYLE}"
                        )
                    )

            if len(unsafe_licenses.found) > 0:
                console_writer.line("Found unsafe licenses:")
                for bad_license in unsafe_licenses.found:
                    console_writer.line(
                        (
                            f"  {BLUE}{bad_license['package']}{END_STYLE} {LABEL}({bad_license['version']}){END_STYLE}: "
                            f"{WARNING}{bad_license['license']}{END_STYLE}"
                        )
                    )

            if not all([unnecessary_ignore_packages, bad_unsafe_packages, missing_unsafe_packages, unsafe_licenses.found]):
                extra_packages_declared_and_allowed = len(unnecessary_unsafe_packages) > 0 and "allow_extra_packages" in options
                extra_licenses_declared_and_allowed = len(unnecessary_safe_licenses) > 0 and "allow_extra_licenses" in options
                if (
                    (not unnecessary_safe_licenses and extra_packages_declared_and_allowed)
                    or (not unnecessary_unsafe_packages and extra_licenses_declared_and_allowed)
                    or (extra_licenses_declared_and_allowed and extra_packages_declared_and_allowed)
                ):
                    console_writer.write_all_licenses_ok()
                    return 0

            return 1

        if len(unsafe_licenses.ignored) > 0:
            console_writer.line("Ignored packages with unsafe licenses:")
            for bad_license in unsafe_licenses.ignored:
                console_writer.line(
                    (
                        f"  {BLUE}{bad_license['package']}{END_STYLE} {LABEL}({bad_license['version']}){END_STYLE}: "
                        f"{WARNING}{bad_license['license']}{END_STYLE}"
                    )
                )

        console_writer.write_all_licenses_ok()
        return 0

    def _show_help(self) -> None:
        console_writer.line(f"{BOLD}USAGE{END_STYLE}")
        console_writer.line(f"  {UNDERLINE}pylic{END_STYLE} {UNDERLINE}check{END_STYLE} [-h] [-l] [-p]\n")
        console_writer.line(f"{BOLD}OPTIONS{END_STYLE}")
        console_writer.line(f"  {LABEL}-h{END_STYLE} (--help)\t\t\t\tDisplay this help message")
        console_writer.line(f"  {LABEL}-l{END_STYLE} (--allow-extra-safe-licenses)\tAllow to list extra safe licenses")
        console_writer.line(f"  {LABEL}-p{END_STYLE} (--allow-extra-unused-packages)\tAllow to list extra unused packages\n")
        console_writer.line(f"{BOLD}DESCRIPTION{END_STYLE}")
        console_writer.line("  Checks all installed licenses against the configuaration provided in the [tool.pylic]")
        console_writer.line("  section of the pyproject.toml file.\n")
        console_writer.line(f"    - {BOLD}safe_licenses{END_STYLE}: Licenses considered to be valid.")
        console_writer.line(f"    - {BOLD}unsafe_packages{END_STYLE}: Packages without a license yet to be considered valid.")
        console_writer.line(f"    - {BOLD}ignore_packages{END_STYLE}: Packages that are not considered at all.")
