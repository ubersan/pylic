[private]
default:
    @just --list

check:
    uv run ruff format --diff --quiet .
    uv run ruff check --quiet .
    uv run ty check .
    uv run python -m pylic check --quiet

fix:
    uv run ruff format .
    uv run ruff check --fix .

test:
    uv run pytest
