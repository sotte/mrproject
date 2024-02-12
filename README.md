# `mkproject` - make projects from templates

This project is [home cooked software](https://www.robinsloan.com/notes/home-cooked-app/).
But of course, you are free to use it as you wish.
You might even like it.

Features:

- Generate projects from templates: `mkproject new --template <template> <project_name>`
- Templates are normal python projects and don't use any templating language.
  That means you can actually **use/test your template while you add new features**.
- The default templates are build with a high degree of automation in mind.
- List existing templates: `mkproject list`
- That's it 🤷

## Usage

```bash
mkproject help
```

```text
usage: mkproject command

Commands:

    new             Create a new project from a template with `project_name`.
    list            List all available templates.
    help            Print usage documentation on a specific command.
```

### Usage: `mkproject new`

```bash
mkproject help new
```

```text
usage: mkproject new [-t|--template] [-n|--no-interaction] project_name

Create a new project from a template with `project_name`.

    Example usage:

        mkproject new my_new_project
        mkproject new my_new_project --template my_fancy_template

    Options:

    --template
        The name or path of the template to use.
        Use `mkproject list` to list all available templates.

    --no-interaction
        Don't ask for user input but accept defaults.
```

When calling `mkproject new`
the user is asked to specify/overwrite all variables defined in `mkproject_template.toml`,
the template project is copied to the current working directory,
every occurrence of `MKPROJECT_*` is replaced with the corresponding value
(including the folder and file names),
and that's it.
This approach is very limited (on purpose) and very simple.

### Usage: `mkproject list`

```bash
mkproject help list
```

```text
usage: mkproject list

List all available templates.
```

## Template

Currently `mkproject` comes with the following templates:

- [default](mkproject/templates/default/README.md)

### What Is A Template?

A `template` is a just a folder that with these files:

```text
mkproject_template.toml   # contains the variables that are substituted
README.md                 # README desribing the features of the template
MKPROJECT_PROJECT_NAME/   # the acual project that is copied
    ...                   # anything you want really :)
tests/                    # optional tests for your template
    ...
```

The file `mkproject_template.toml` MUST contain the following fields:

```toml
[mkproject.template.substitutions]
MKPROJECT_AUTHOR = "your name"
MKPROJECT_EMAIL = "your@email.com"
```

Some additional fields are added by `mkproject` automatically:

- `MKPROJECT_CURRENT_YEAR` - the current year

The fields MUST start with `MKPROJECT_` and MUST be upper case.

### Create Your Own Template

First, read the section above.
Then, you can create your own template by putting it in the `templates` folder under:
`~/.local/share/mkproject/templates/`.

```text
~/.local/share/mkproject/templates/
    my_template/
        README.md
        mkproject_template.toml
        MKPROJECT_PROJECT_NAME/
            ...
        tests/
            ...
```

## Why `mkproject`?

There are many project template generators out there,
and many of them are great and more feature rich than this one.

But I want to have a **simple** one
where I can **actually use/test the project template as I add new features**.
This is achieved by not using any templating language, but reserved keywords.
