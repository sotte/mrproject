from copy import deepcopy
from datetime import datetime
from functools import partial
from pathlib import Path

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
    return


def _configure_template(
    template: Template, project_name: str, destination: Path, no_interaction: bool
) -> ConfiguredTemplate:
    substitutions = deepcopy(template.config["mrproject"]["template"]["substitutions"])

    if not no_interaction:
        rprint("Overwrite default values. Enter to keeep the default.")
        for k, v in substitutions.items():
            substitutions[k] = Prompt.ask(k, default=v)

    substitutions["MRPROJECT_PROJECT_NAME"] = project_name
    substitutions["MRPROJECT_CURRENT_YEAR"] = str(datetime.now().year)

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
