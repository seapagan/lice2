"""Initialize the application."""

__version__ = "0.7"


def main() -> None:
    """Call the main application code.

    This is the legacy code, I'll probably refactor it later out of the init.
    """
    from src.core import main

    main()
