"""CLI entry for mrproject."""

import appeal

from mrproject import list, new


def main():
    """Entrypoint."""
    app = appeal.Appeal()
    app.command()(new.new)
    app.command()(list.list)
    app.main()


if __name__ == "__main__":
    main()
