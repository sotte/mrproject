import pytest

from mrproject.new import _is_valid_project_name


@pytest.mark.parametrize(
    "project_name",
    [
        "project",
        "project123",
        "project_123",
        "project_123_foo",
    ],
)
def test_is_valid_project_name(project_name: str):
    assert _is_valid_project_name(project_name)


@pytest.mark.parametrize(
    "project_name",
    [
        "1",
        "123",
        "DUMMY",
        "<dummy",
        "_dummy",
        "dummy-",
        "dummy/",
    ],
)
def test_is_valid_project_name_with_invalid_project_name(project_name: str):
    assert not _is_valid_project_name(project_name)
