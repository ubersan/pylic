# pylic - Python license checker [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/sandrochuber/pylic/blob/main/LICENSE) [![PyPI version](https://badge.fury.io/py/pylic.svg)](https://badge.fury.io/py/pylic/) [![Codecov](https://codecov.io/gh/sandrochuber/pylic//branch/main/graph/badge.svg)](https://codecov.io/gh/sandrochuber/pylic/)

Reads the pyproject.toml file and checks all installed licenses recursively.

Principles:
- Every license has to be allowed explicitly (case-insensitive comparison).
- All packages without license are considered unsafe and have to be listed as such.

## Example Configuration

```pyproject.toml
[tool.pylic]
safe_licenses = [
    'MIT',
    'BSD'
]
unsafe_packages = [
    "unlicensedPackage"
]
```

## Docker

You can also use `pylic` with docker. There is already a pre-built image available:

```bash
docker pull docker.pkg.github.com/sandrochuber/pylic/pylic:latest
docker run --volume ${PWD}/pyproject.toml:/pyproject.toml docker.pkg.github.com/sandrochuber/pylic/pylic:latest
```

## Development

Required tools:
- Poetry (https://python-poetry.org/)
- GitHub cli (https://github.com/cli/cli)

Creating a new release is as simple as:
- Update `version` in the pyproject.toml file.
- `poetry run task release vx.x.x`.
