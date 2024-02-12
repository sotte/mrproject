from pathlib import Path

from mkproject.utils import get_console, list_templates, user_template_dir


def list() -> None:
    """List all available templates."""
    console = get_console()

    default_templates, user_templates = list_templates()

    def print_template_entry(template: Path) -> None:
        console.print(f" - '{template.name}' ({template})")

    console.print("mkproject templates:")
    for template in default_templates:
        print_template_entry(template)

    console.print(f"User templates: ({user_template_dir()})")
    if user_templates:
        for template in user_templates:
            print_template_entry(template)
    else:
        console.print(" - No user templates found.")
