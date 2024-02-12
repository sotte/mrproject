# `default` template of `mkproject`

A simple template for [`mkproject`](https://github.com/sotte/mkproject)
with (hopefully) reasonable defaults.

Features:

- python 3.10 project using [poetry](https://python-poetry.org/)
- run tasks with [poethepoet](https://github.com/nat-n/poethepoet)
  - test with [pytest](https://docs.pytest.org/)
  - format with [ruff](https://github.com/astral-sh/ruff)
  - lint with  [ruff](https://github.com/astral-sh/ruff)
  - type check with [pyright](https://github.com/microsoft/pyright)
  - docs with [mkdocs](https://www.mkdocs.org/) and [mkdocstrings](https://mkdocstrings.github.io)
- [`pre-commit`](https://pre-commit.com/) configuration (including many of the above tasks)
- MIT license
