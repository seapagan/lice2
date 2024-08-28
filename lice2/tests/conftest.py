"""Setup the test configuration for the lice2 tests."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pyfakefs.fake_filesystem import FakeFilesystem

TEMPLATE_FILE = """This is a template file.
{{ organization }} is the organization.
{{ project }} is the project.
{{ year }} is the year.
"""


@pytest.fixture(autouse=True)
def fake_config(fs: FakeFilesystem) -> FakeFilesystem:
    """Fixture to setup the fake filesystem for the tests.

    This stops any tests interacting with the real filesystem.
    """
    # 'fs' is the fake filesystem object
    fs.create_file(
        Path.home() / ".config/lice/lice.toml",
        contents="default_license = 'mit'\norganization = 'Awesome Co.'",
    )

    fs.create_file(Path.home() / "template.txt", contents=TEMPLATE_FILE)

    # copy over the license templates so we can use them in the tests
    fs.add_real_directory(Path(__file__).parent.parent / "templates")
    return fs


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
        "clipboard": False,
        "legacy": False,
        "list_vars": False,
        "list_licenses": False,
        "list_languages": False,
    }
    return SimpleNamespace(**args_base)
