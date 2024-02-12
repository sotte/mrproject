# Contributing

You want to contribute? Great!

Here are some things you should know:

- Please read this document and create an issue if something is unclear
  or you have a question.
- Please create an issue before you start working on a feature.
- Please make sure that all checks pass before you create a PR.
  You can run the checks locally with `poe chores`.
- Please update the `CHANGELOG.md`.

## Dev setup

```bash
# Bootstrap the project
python3.11 -m venv venv
poetry shell
poetry install
pre-commit install

# Make sure the project works
poe chores

# Check available tasks
poe
```
