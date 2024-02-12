from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path

import tomli
from platformdirs import user_data_dir
from rich.console import Console


@dataclass(frozen=True)
class Template:
    """A raw template for a project."""

    name: str
    dir: Path
    source_dir: Path
    config: dict

    @classmethod
    def from_name(cls, name: str) -> Template | None:
        template_path = user_template_dir() / name
        if cls._is_valid(template_path):
            return cls(
                name,
                template_path,
                template_path / "MKPROJECT_PROJECT_NAME",
                config=tomli.loads(
                    (template_path / "mkproject_template.toml").read_text()
                ),
            )

        template_path = default_template_dir() / name
        if cls._is_valid(template_path):
            return cls(
                name,
                template_path,
                template_path / "MKPROJECT_PROJECT_NAME",
                config=tomli.loads(
                    (template_path / "mkproject_template.toml").read_text()
                ),
            )

        return None

    @staticmethod
    def _is_valid(path: Path) -> bool:
        return (
            path.is_dir()
            and (path / "mkproject_template.toml").is_file()
            and (path / "MKPROJECT_PROJECT_NAME").is_dir()
        )

    @property
    def source_files(self) -> list[Path]:
        def in_blocklist(path: Path) -> bool:
            # Use git logic to ignore files.
            # echo "foo.pyc" | git check-ignore --stdin --no-index
            path_str = str(path)
            return (
                ".pytest_cache" in path_str
                or ".ruff_cache" in path_str
                or ".venv" in path_str
                or "poetry.lock" in path_str
                or path_str.endswith(".pyc")
            )

        src_files = self.source_dir.glob("**/*")
        src_files = [f for f in src_files if f.is_file()]
        src_files = [f for f in src_files if not in_blocklist(f)]
        src_files = sorted(src_files)
        return src_files


@dataclass(frozen=True)
class ConfiguredTemplate:
    template: Template

    project_name: str  # corresponds to MKPROJECT_PROJECT_NAME
    project_dir: Path
    substitutions: dict


@cache
def get_console() -> Console:
    """Return a rich console object."""
    return Console()


@cache
def user_template_dir() -> Path:
    """Return the path to the user's template directory."""
    return Path(user_data_dir("mkproject"))


@cache
def default_template_dir() -> Path:
    """Return the path to the default template directory."""
    return Path(__file__).parent / "templates"


def list_templates() -> tuple[list[Path], list[Path]]:
    default_templates = list(default_template_dir().iterdir())

    user_templates = user_template_dir()
    if user_templates.is_dir():
        user_templates = list(user_templates.iterdir())
    else:
        user_templates = []

    return default_templates, user_templates


def get_template(template_name: str) -> Template | None:
    """Get the path to the template directory."""
    # user_template = user_template_dir() / template_name
    return Template.from_name(template_name)
