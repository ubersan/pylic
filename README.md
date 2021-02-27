# pylic - A Python license checker

Reads the pyproject.toml file and checks all installed licenses recursively.

## Example Configuration

```pyproject.toml
[tool.pylic]
allowed_licenses = [
    'MIT',
    'BSD'
]
whitelisted_packages = [
    "examplePyPackage"
]
```

## Development

Required tools:
- GitHub cli (https://github.com/cli/cli)
