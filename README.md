# pylic - Python license checker [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/sandrochuber/pylic/blob/main/LICENSE) [![PyPI version](https://badge.fury.io/py/pylic.svg)](https://badge.fury.io/py/pylic/) [![Codecov](https://codecov.io/gh/ubersan/pylic//branch/main/graph/badge.svg)](https://codecov.io/gh/ubersan/pylic/)

Reads pylic configuration in `pyproject.toml` and checks licenses of installed packages recursively.

Principles:
- Every license has to be allowed explicitly (case-insensitive comparison).
- All installed packages without a license are considered unsafe and have to be listed as such.

> Only installed packages are checked for licenses. Packages/dependencies listed in `pyproject.toml` are ignored.

## Installation

```sh
pip install pylic
```

## Configuration

`pylic` needs be run in the directory where your `pyproject.toml` file is located. You can configure
- `safe_licenses`: All licenses you consider safe for usage. The string comparison is case-insensitive.
- `unsafe_packages`: If you rely on a package that does not come with a license you have to explicitly list it as such.
- `ignore_packages`: Packages that will not be reported as unsafe even if they use a license not listed as safe. This is useful in case an existing projects want to start integrating `pylic`, but are still using unsafe licenses. This enables first to ignore these packages temporarely, while they're being replaced, second to already validate newly added or updated packages against the safe license set and third to integrate `pylic` frictionless into CI/CD from the get go.

```toml
[tool.pylic]
safe_licenses = [
    "Apache Software License",
    "Apache License 2.0",
    "MIT License",
    "Python Software Foundation License",
    "Mozilla Public License 2.0 (MPL 2.0)",
]
unsafe_packages = [
    "unlicensedPackage",
]
ignore_packages = [
    "ignoredPackage",
]
```

## Commands

`pylic` provides the following commands (also see `pylic help`):
- `check`: Checks all installed licenses.
- `list`: Lists all installed packages and their corresponding license.

## Usage Example

Create a venv to start with a clean ground and activate it

```sh
python -m venv .venv
source .venv/bin/activate
```

Install `pylic` and create an empty `pyproject.toml`

```sh
pip install pylic
touch pyproject.toml
```

Install all your dependencies

```sh
pip install <packageA> <packageB>
```

Run pylic

```sh
pylic check
```

The output will be similar to

```sh
Found unsafe packages:
  pkg_resources (0.0.0)
Found unsafe licenses:
  pip (18.1): MIT License
  zipp (3.4.1): MIT License
  toml (0.10.2): MIT License
  pylic (1.2.0): MIT License
  setuptools (40.8.0): MIT License
  typing-extensions (3.7.4.3): Python Software Foundation License
  importlib-metadata (3.9.0): Apache Software License
```

The return code of `pylic` is in this case non-zero due to unsafe licenses. This allows usage of pylic in CI.

```sh
echo $? # prints 1
```

As these licenses and packages are all ok we can configure `pylic` accordingly

```sh
cat <<EOT >> pyproject.toml
[tool.pylic]
safe_licenses = ["Apache Software License", "MIT License", "Python Software Foundation License"]
unsafe_packages = ["pkg_resources"]
EOT
```

After rerunning `pylic check` the output now reveals a successful validation

```sh
✨ All licenses ok ✨
```

Also the return code now signals that all is good

```sh
echo $? # prints 0
```

Use `pylic list` to list all installed packages and their corresponding licenses.

## Advanced Usage

In cases where the safe licenses or unsafe packages are centrally managed keeping the configuration in perfect sync to the installed packages might be too cumbersome or even impossible. To support these use cases the `check` command provides the two options (see also `check --help`) `--allow-extra-safe-licenses` and `--allow-extra-unused-packages`. These options only affect the returned status code and will keep all corresponding printed warnings unchanged.

## Development

Required tools:
- Poetry (https://python-poetry.org/)

Run `poetry install` to install all necessary dependencies. Checkout the `[tool.taskipy.tasks]` (see [taskipy](https://github.com/illBeRoy/taskipy)) section in the `pyproject.toml` file for utility tasks. You can run these with `poetry run task <task>`.

Creating a new release is as simple as:
- Update `version` in the pyproject.toml and the `__version__.py` file.
- `poetry run task release`.
