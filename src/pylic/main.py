import typer

from pylic.__version__ import version as __version
from pylic.config import read_config
from pylic.license_checker import LicenseChecker
from pylic.licenses import read_all_installed_licenses_metadata

app = typer.Typer(no_args_is_help=True)


@app.command()
def check(quiet: bool = False, allow_extra_packages: bool = False, allow_extra_licenses: bool = False) -> None:
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
            print("Unnecessary safe licenses listed which are not used by any installed package:")
            for unnecessary_safe_license in unnecessary_safe_licenses:
                print(f"  {unnecessary_safe_license}")

        if len(unnecessary_unsafe_packages) > 0:
            print("Unsafe packages listed which are not installed:")
            for unnecessary_unsafe_package in unnecessary_unsafe_packages:
                print(f"  {unnecessary_unsafe_package}")

        if len(unnecessary_ignore_packages) > 0:
            print("Ignore packages listed which are not installed:")
            for unnecessary_ignore_package in unnecessary_ignore_packages:
                print(f"  {unnecessary_ignore_package}")

        if len(bad_unsafe_packages) > 0:
            print("Found unsafe packages with a known license. Instead allow these licenses explicitly:")
            for bad_package in bad_unsafe_packages:
                print(f"  {bad_package['package']} ({bad_package['version']}): {bad_package['license']}")

        if len(missing_unsafe_packages) > 0:
            print("Found unsafe packages:")
            for missing_unsafe_package in missing_unsafe_packages:
                print(f"  {missing_unsafe_package['package']} ({missing_unsafe_package['version']})")

        if len(unsafe_licenses.found) > 0:
            print("Found unsafe licenses:")
            for bad_license in unsafe_licenses.found:
                print(f"  {bad_license['package']} ({bad_license['version']}): {bad_license['license']}")

        if not all([unnecessary_ignore_packages, bad_unsafe_packages, missing_unsafe_packages, unsafe_licenses.found]):
            extra_packages_declared_and_allowed = len(unnecessary_unsafe_packages) > 0 and allow_extra_packages
            extra_licenses_declared_and_allowed = len(unnecessary_safe_licenses) > 0 and allow_extra_licenses
            if (
                (not unnecessary_safe_licenses and extra_packages_declared_and_allowed)
                or (not unnecessary_unsafe_packages and extra_licenses_declared_and_allowed)
                or (extra_licenses_declared_and_allowed and extra_packages_declared_and_allowed)
            ):
                print("✨ All licenses ok ✨")
                raise typer.Exit(0)

        raise typer.Exit(1)

    if len(unsafe_licenses.ignored) > 0:
        print("Ignored packages with unsafe licenses:")
        for bad_license in unsafe_licenses.ignored:
            print(f"  {bad_license['package']} ({bad_license['version']}): {bad_license['license']}")

    if not quiet:
        print("✨ All licenses ok ✨")


@app.command()
def list() -> None:
    print("list")


@app.command()
def version() -> None:
    print(__version)


if __name__ == "__main__":
    app()
