from pathlib import Path

import pytest

from mrproject.new import new


@pytest.fixture()
def dummy_project(with_tmp_path):
    new("dummy", template="default", no_interaction=True)
    return with_tmp_path


EXPECTED_FILES = [
    "dummy/.gitignore",
    "dummy/.pre-commit-config.yaml",
    "dummy/LICENSE",
    "dummy/dummy/__init__.py",
    "dummy/dummy/py.typed",
    "dummy/dummy/utils.py",
    "dummy/README.md",
    "dummy/docs/api/utils.md",
    "dummy/docs/index.md",
    "dummy/mkdocs.yml",
    "dummy/pyproject.toml",
    "dummy/tests/test_utils.py",
]


@pytest.mark.parametrize("expected_file", EXPECTED_FILES)
def test_new_create_expected_file(expected_file, dummy_project):
    assert Path(expected_file).is_file()


def test_new_creates_no_unexpected_files(dummy_project):
    path_of_project = dummy_project
    existing_files = [
        f.relative_to(path_of_project)
        for f in path_of_project.rglob("*")
        if f.is_file()
    ]
    assert len(existing_files) == len(EXPECTED_FILES)
