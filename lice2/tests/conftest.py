"""Setup the test configuration for the lice2 tests."""

from __future__ import annotations

from types import SimpleNamespace

import pytest


@pytest.fixture
def args() -> SimpleNamespace:
    """Fixture to return a default args object."""
    args_base: dict[str, str | bool | None] = {
        "license": "mit",
        "header": False,
        "organization": "Awesome Co.",
        "project": "my_project",
        "template_path": None,
        "year": "2024",
        "language": None,
        "ofile": None,
        "list_vars": False,
        "list_licenses": False,
        "list_languages": False,
    }
    return SimpleNamespace(**args_base)
