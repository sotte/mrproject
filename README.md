# `mrproject` - make projects from templates

This project is [home cooked software](https://www.robinsloan.com/notes/home-cooked-app/).
But of course, you are free to use it as you wish.
You might even like it.

Features:

- Generate projects from templates: `mrproject new --template <template> <project_name>`
- Templates are normal python projects and don't use any templating language.
  That means you can actually **use/test your template while you add new features**.
- The default templates are build with a high degree of automation in mind.
- List existing templates: `mrproject list`
- That's it 🤷

## Usage

```bash
mrproject help
```

```text
usage: mrproject command

Commands:

    new             Create a new project from a template with `project_name`.
    list            List all available templates.
    help            Print usage documentation on a specific command.
```

### Usage: `mrproject new`

```bash
mrproject help new
```

```text
usage: mrproject new [-t|--template] [-n|--no-interaction] project_name

Create a new project from a template with `project_name`.

    Example usage:

        mrproject new my_new_project
        mrproject new my_new_project --template my_fancy_template

    Options:

    --template
        The name or path of the template to use.
        Use `mrproject list` to list all available templates.

    --no-interaction
        Don't ask for user input but accept defaults.
```

When calling `mrproject new`
the user is asked to specify/overwrite all variables defined in `mrproject_template.toml`,
the template project is copied to the current working directory,
every occurrence of `MRPROJECT_*` is replaced with the corresponding value
(including the folder and file names),
and that's it.
This approach is very limited (on purpose) and very simple.

### Usage: `mrproject list`

```bash
mrproject help list
```

```text
usage: mrproject list

List all available templates.
```

## Template

Currently `mrproject` comes with the following templates:

- [default](mrproject/templates/default/README.md)

### What Is A Template?

A `template` is a just a folder that with these files:

```text
mrproject_template.toml   # contains the variables that are substituted
README.md                 # README desribing the features of the template
MRPROJECT_PROJECT_NAME/   # the acual project that is copied
    ...                   # anything you want really :)
tests/                    # optional tests for your template
    ...
```

The file `mrproject_template.toml` MUST contain the following fields:

```toml
[mrproject.template.substitutions]
MRPROJECT_AUTHOR = "your name"
MRPROJECT_EMAIL = "your@email.com"
```

Some additional fields are added by `mrproject` automatically:

- `MRPROJECT_CURRENT_YEAR` - the current year

The fields MUST start with `MRPROJECT_` and MUST be upper case.

### Create Your Own Template

First, read the section above.
Then, you can create your own template by putting it in the `templates` folder under:
`~/.local/share/mrproject/templates/`.

```text
~/.local/share/mrproject/templates/
    my_template/
        README.md
        mrproject_template.toml
        MRPROJECT_PROJECT_NAME/
            ...
        tests/
            ...
```

## Why `mrproject`?

There are many project template generators out there,
and many of them are great and more feature rich than this one.

But I want to have a **simple** one
where I can **actually use/test the project template as I add new features**.
This is achieved by not using any templating language, but reserved keywords.
