"""CLI entry for mkproject."""

import appeal

from mkproject import list, new


def main():
    """Entrypoint."""
    app = appeal.Appeal()
    app.command()(new.new)
    app.command()(list.list)
    app.main()


if __name__ == "__main__":
    main()
