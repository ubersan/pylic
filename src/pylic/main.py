import typer

from pylic.__version__ import version as __version
from pylic.config import read_config
from pylic.license_checker import LicenseChecker
from pylic.licenses import read_all_installed_licenses_metadata

app = typer.Typer(no_args_is_help=True)


@app.command(help="Checks all installed licenses against the configuaration provided in [tool.pylic].")
def check(
    quiet: bool = typer.Option(False, "--quiet", help="Only show warnings and errors."),
    allow_extra_packages: bool = typer.Option(
        False, "--allow-extra-packages", help="Allow to list extra unsafe packages."
    ),
    allow_extra_licenses: bool = typer.Option(False, "--allow-extra-licenses", help="Allow extra safe licenses."),
) -> None:
    config = read_config()
    installed_licenses = read_all_installed_licenses_metadata()
    checker = LicenseChecker(config, installed_licenses)

    unnecessary_safe_licenses = checker.get_unnecessary_safe_licenses()
    unnecessary_unlicensed_packages = checker.get_unnecessary_unlicensed_packages()
    unnecessary_ignore_packages = checker.get_unnecessary_ignore_packages()
    bad_unlicensed_packages = checker.get_bad_unlicensed_packages()
    missing_unlicensed_packages = checker.get_missing_unlicensed_packages()
    unsafe_licenses = checker.get_unsafe_licenses()

    if any(
        [
            unnecessary_safe_licenses,
            unnecessary_unlicensed_packages,
            unnecessary_ignore_packages,
            bad_unlicensed_packages,
            missing_unlicensed_packages,
            unsafe_licenses.found,
        ]
    ):
        if len(unnecessary_safe_licenses) > 0:
            print("Unnecessary safe licenses listed which are not used by any installed package:")
            for unnecessary_safe_license in unnecessary_safe_licenses:
                print(f"  {unnecessary_safe_license}")

        if len(unnecessary_unlicensed_packages) > 0:
            print("Unsafe packages listed which are not installed:")
            for unnecessary_unsafe_package in unnecessary_unlicensed_packages:
                print(f"  {unnecessary_unsafe_package}")

        if len(unnecessary_ignore_packages) > 0:
            print("Ignore packages listed which are not installed:")
            for unnecessary_ignore_package in unnecessary_ignore_packages:
                print(f"  {unnecessary_ignore_package}")

        if len(bad_unlicensed_packages) > 0:
            print("Found unsafe packages with a known license. Instead allow these licenses explicitly:")
            for bad_package in bad_unlicensed_packages:
                print(f"  {bad_package['package']} ({bad_package['version']}): {bad_package['license']}")

        if len(missing_unlicensed_packages) > 0:
            print("Found unsafe packages:")
            for missing_unsafe_package in missing_unlicensed_packages:
                print(f"  {missing_unsafe_package['package']} ({missing_unsafe_package['version']})")

        if len(unsafe_licenses.found) > 0:
            print("Found unsafe licenses:")
            for bad_license in unsafe_licenses.found:
                print(f"  {bad_license['package']} ({bad_license['version']}): {bad_license['license']}")

        if not all(
            [unnecessary_ignore_packages, bad_unlicensed_packages, missing_unlicensed_packages, unsafe_licenses.found]
        ):
            extra_packages_declared_and_allowed = len(unnecessary_unlicensed_packages) > 0 and allow_extra_packages
            extra_licenses_declared_and_allowed = len(unnecessary_safe_licenses) > 0 and allow_extra_licenses
            if (
                (not unnecessary_safe_licenses and extra_packages_declared_and_allowed)
                or (not unnecessary_unlicensed_packages and extra_licenses_declared_and_allowed)
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


@app.command(help="Lists all installed packages and their corresponding license.")
def list() -> None:
    installed_licenses = read_all_installed_licenses_metadata()
    unsorted = {
        installed["package"]: {"version": installed["version"], "license": installed["license"]}
        for installed in installed_licenses
    }
    for package, rest in sorted(unsorted.items(), key=lambda k: k[0].lower()):  # type:ignore
        print(f"{package} ({rest['version']}): {rest['license']}")


@app.command(help="Prints the version of pylic.")
def version() -> None:
    print(__version)


if __name__ == "__main__":
    app()
