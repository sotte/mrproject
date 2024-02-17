"""General utility functions."""


def hello_world(name: str = "World") -> str:
    """Return a hello world string.

    Args:
        name: The name to say hello to.

    Returns:
        The greeting string.

    Examples:
        >>> hello_world()
        'Hello World!'
    """
    return f"Hello {name}!"
