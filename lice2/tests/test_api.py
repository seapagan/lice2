"""Test suite for the programmatic API of lice2."""

import pytest

from lice2.api import Lice
from lice2.constants import LANGS, LICENSES


@pytest.fixture
def lice() -> Lice:
    """Return a Lice instance for testing."""
    return Lice(
        organization="Awesome Co.",
        project="my_project",
    )


def test_lice_instance(lice: Lice) -> None:
    """Test that the Lice instance is created correctly."""
    assert isinstance(lice, Lice)
    assert lice.organization == "Awesome Co."
    assert lice.project == "my_project"


def test_get_licenses(lice: Lice) -> None:
    """Test that get_licenses returns a list of licenses."""
    licenses = lice.get_licenses()
    assert isinstance(licenses, list)
    assert len(licenses) == len(LICENSES)
    assert all(isinstance(license_name, str) for license_name in licenses)


def test_get_languages(lice: Lice) -> None:
    """Test that get_languages returns a list of languages."""
    languages = lice.get_languages()
    assert isinstance(languages, list)
    assert len(languages) == len(LANGS.keys())
    assert all(isinstance(language, str) for language in languages)
