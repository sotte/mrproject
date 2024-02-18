from contextlib import suppress
from copy import deepcopy
from datetime import datetime
from functools import partial
from pathlib import Path

import tomli
from platformdirs import user_config_dir
from rich import print as rprint
from rich.prompt import Prompt

from mrproject.utils import ConfiguredTemplate, Template


def new(
    project_name: str, *, template: str = "default", no_interaction: bool = False
) -> None:
    """Create a new project from a template with  `project_name`.

    Example usage:

        mrproject new my_new_project
        mrproject new my_new_project --template my_fanxy_template

    Options:

    --template
        The name or path of the template to use.
        Use `mrproject list` to list all available templates.

    --no-interaction
        Don't ask for user input but accept defaults.

    """
    if not _is_valid_project_name(project_name):
        return

    _template = Template.from_name(template)
    if _template is None:
        rprint(f"ERROR: Template '{template}' not found.")
        rprint("Use one of these instead:")

        from mrproject.list import list as list_templates

        list_templates()
        return

    configured_template = _configure_template(
        _template, project_name, Path.cwd(), no_interaction=no_interaction
    )
    rprint(configured_template)

    # utils
    add_dst_file_func = partial(_add_dst_file, configured_template=configured_template)
    copy_and_substitute_func = partial(
        _copy_and_substitute, configured_template=configured_template
    )

    source_files = configured_template.template.source_files
    src_dst_files = map(add_dst_file_func, source_files)
    list(map(copy_and_substitute_func, src_dst_files))


def _configure_template(
    template: Template, project_name: str, destination: Path, no_interaction: bool
) -> ConfiguredTemplate:
    substitutions = deepcopy(template.config["mrproject"]["template"]["substitutions"])

    # overwrite default values with user config
    user_config_path = Path(user_config_dir("mrproject")) / "config.toml"
    if user_config_path.is_file():
        rprint(f"Loading user config from {user_config_path}.")
        user_config = tomli.loads(user_config_path.read_text())
        with suppress(KeyError):
            for k, v in user_config["mrproject"]["template"]["substitutions"].items():
                substitutions[k] = v

    # overwrite default values with user input
    if not no_interaction:
        rprint("Overwrite default values. Enter to keeep the default.")
        for k, v in substitutions.items():
            substitutions[k] = Prompt.ask(k, default=v)

    # set useful substitutions
    substitutions["MRPROJECT_PROJECT_NAME"] = project_name
    substitutions["MRPROJECT_CURRENT_YEAR"] = str(datetime.now().year)
    substitutions["MRPROJECT_CURRENT_MONTH"] = str(datetime.now().month)
    substitutions["MRPROJECT_CURRENT_DAY"] = str(datetime.now().day)

    return ConfiguredTemplate(
        template=template,
        project_name=project_name,
        project_dir=destination / project_name,
        substitutions=substitutions,
    )


def _add_dst_file(
    src_file: Path, configured_template: ConfiguredTemplate
) -> tuple[Path, Path]:
    """Get the destination path for a source file."""
    src_file_rel = src_file.relative_to(configured_template.template.source_dir)
    dst_file = str(configured_template.project_dir / src_file_rel)

    for k, v in configured_template.substitutions.items():
        dst_file = dst_file.replace(k, v)

    return src_file, Path(dst_file)


def _copy_and_substitute(
    src_and_dst: tuple[Path, Path], configured_template: ConfiguredTemplate
) -> None:
    src_file, dst_file = src_and_dst

    src_content = src_file.read_text()
    for k, v in configured_template.substitutions.items():
        src_content = src_content.replace(k, v)

    dst_file_relative = dst_file.relative_to(Path.cwd())
    if dst_file.is_file():
        dst_content = dst_file.read_text()
        if dst_content == src_content:
            rprint(f"- [green]Skipping[/green] '{dst_file_relative}'. Same content.")
            return
        else:
            rprint(f"- [red]Conflict[/red] '{dst_file_relative}'.")
            overwrite = Prompt.ask(
                "Overwrite?", default="n", choices=["y", "n"], show_choices=True
            )
            if overwrite == "y":
                rprint("- [green]  Overwritten[/green]")
                dst_file.write_text(src_content)
            else:
                rprint("- [orange]  Skipped.[/orange]")
    else:
        rprint(f"- [green]Creating[/green] '{dst_file_relative}'.")
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        dst_file.write_text(src_content)


def _is_valid_project_name(project_name: str) -> bool:
    allowed_chars = "abcdefghijklmnopqrstuvwxyz1234567890_"

    if project_name == "":
        rprint("ERROR: Project name cannot be empty.")
        return False

    if project_name is None:
        rprint("ERROR: Project name cannot be None.")
        return False

    if not str.isalpha(project_name[0]):
        rprint("ERROR: Project name must start with an alpha character.")
        return False

    _illegal_chars = [c for c in project_name if c not in allowed_chars]
    if len(_illegal_chars) > 0:
        rprint(
            f"ERROR: Project name can only contain '{allowed_chars}' but found '{_illegal_chars}'"
        )
        return False

    return True
