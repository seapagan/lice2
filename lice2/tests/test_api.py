"""Test suite for the programmatic API of lice2."""

import pytest

from lice2.api import Lice
from lice2.api.exceptions import (
    HeaderNotFoundError,
    LanguageNotFoundError,
    LicenseNotFoundError,
)
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


def test_license_not_found_error_no_arg() -> None:
    """Test that raising LicenseNotFoundError without an argument fails."""
    with pytest.raises(TypeError):
        raise LicenseNotFoundError  # type: ignore[call-arg]


def test_language_not_found_error_no_arg() -> None:
    """Test that raising LanguageNotFoundError without an argument fails."""
    with pytest.raises(TypeError):
        raise LanguageNotFoundError  # type: ignore[call-arg]


def test_header_not_found_error_no_arg() -> None:
    """Test that raising HeaderNotFoundError without an argument fails."""
    with pytest.raises(TypeError):
        raise HeaderNotFoundError  # type: ignore[call-arg]


def test_license_not_found_error() -> None:
    """Test that LicenseNotFoundError is raised correctly."""
    bad_license = "unknown_license"
    with pytest.raises(LicenseNotFoundError) as exc_info:
        raise LicenseNotFoundError(bad_license)
    assert str(exc_info.value) == "License 'unknown_license' is unknown."
    assert exc_info.value.license_name == "unknown_license"


def test_language_not_found_error() -> None:
    """Test that LanguageNotFoundError is raised correctly."""
    bad_language = "unknown_language"
    with pytest.raises(LanguageNotFoundError) as exc_info:
        raise LanguageNotFoundError(bad_language)
    assert str(exc_info.value) == "Language 'unknown_language' is unknown."
    assert exc_info.value.language_name == "unknown_language"


def test_header_not_found_error() -> None:
    """Test that HeaderNotFoundError is raised correctly."""
    license_name = "unknown_license"
    with pytest.raises(HeaderNotFoundError) as exc_info:
        raise HeaderNotFoundError(license_name)
    assert (
        str(exc_info.value)
        == "License 'unknown_license' does not have any headers."
    )
    assert exc_info.value.license_name == "unknown_license"


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
