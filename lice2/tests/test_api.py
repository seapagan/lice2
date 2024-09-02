"""Test suite for the programmatic API of lice2."""

import pytest

from lice2.api import Lice
from lice2.api.exceptions import (
    HeaderNotFoundError,
    InvalidYearError,
    LanguageNotFoundError,
    LicenseNotFoundError,
)
from lice2.constants import LANGS, LICENSES
from lice2.helpers import get_local_year


class TestAPI:
    """A test class for the API."""

    def test_lice_instance(self, lice: Lice) -> None:
        """Test that the Lice instance is created correctly."""
        assert isinstance(lice, Lice)
        assert lice.organization == "Awesome Co."
        assert lice.project == "my_project"

    def test_lice_instance_no_args(self) -> None:
        """Test that creating a Lice instance with no args fails."""
        with pytest.raises(
            TypeError, match="missing 2 required positional arguments"
        ):
            Lice()  # type: ignore[call-arg]

    def test_lice_instance_invalid_year(self) -> None:
        """Test that creating a Lice instance with an invalid year fails."""
        with pytest.raises(InvalidYearError) as exc_info:
            Lice(organization="Awesome Co.", project="my_project", year="202")

        assert "'202' is not a valid year" in str(exc_info.value)

    def test_lice_instance_very_bad_year(self) -> None:
        """Test that creating a Lice instance with a very bad year fails.

        This is basically anything that cannot be converted to an integer.
        """
        with pytest.raises(InvalidYearError) as exc_info:
            Lice(organization="Awesome Co.", project="my_project", year="bad1")

        assert "'bad1' is not a valid year" in str(exc_info.value)

    def test_lice_instance_integer_year(self) -> None:
        """Test that creating a Lice instance with an integer year works."""
        lice = Lice(organization="Awesome Co.", project="my_project", year=1314)
        assert lice.year == "1314"

    def test_license_not_found_error_no_arg(self) -> None:
        """Test that raising LicenseNotFoundError without an argument fails."""
        with pytest.raises(TypeError):
            raise LicenseNotFoundError  # type: ignore[call-arg]

    def test_language_not_found_error_no_arg(self) -> None:
        """Test that raising LanguageNotFoundError without an argument fails."""
        with pytest.raises(TypeError):
            raise LanguageNotFoundError  # type: ignore[call-arg]

    def test_header_not_found_error_no_arg(self) -> None:
        """Test that raising HeaderNotFoundError without an argument fails."""
        with pytest.raises(TypeError):
            raise HeaderNotFoundError  # type: ignore[call-arg]

    def test_invalid_year_error_no_arg(self) -> None:
        """Test that raising InvalidYearError without an argument fails."""
        with pytest.raises(TypeError):
            raise InvalidYearError  # type: ignore[call-arg]

    def test_invalid_year_error(self) -> None:
        """Test that InvalidYearError is raised correctly."""
        bad_year = "202"
        with pytest.raises(InvalidYearError) as exc_info:
            raise InvalidYearError(bad_year)
        assert "Year '202' is not a valid year" in str(exc_info.value)
        assert exc_info.value.year == bad_year

    def test_license_not_found_error(self) -> None:
        """Test that LicenseNotFoundError is raised correctly."""
        bad_license = "unknown_license"
        with pytest.raises(LicenseNotFoundError) as exc_info:
            raise LicenseNotFoundError(bad_license)
        assert str(exc_info.value) == "License 'unknown_license' is unknown."
        assert exc_info.value.license_name == "unknown_license"

    def test_language_not_found_error(self) -> None:
        """Test that LanguageNotFoundError is raised correctly."""
        bad_language = "unknown_language"
        with pytest.raises(LanguageNotFoundError) as exc_info:
            raise LanguageNotFoundError(bad_language)
        assert str(exc_info.value) == "Language 'unknown_language' is unknown."
        assert exc_info.value.language_name == "unknown_language"

    def test_header_not_found_error(self) -> None:
        """Test that HeaderNotFoundError is raised correctly."""
        license_name = "unknown_license"
        with pytest.raises(HeaderNotFoundError) as exc_info:
            raise HeaderNotFoundError(license_name)
        assert (
            str(exc_info.value)
            == "License 'unknown_license' does not have any headers."
        )
        assert exc_info.value.license_name == "unknown_license"

    def test_get_licenses(self, lice: Lice) -> None:
        """Test that get_licenses returns a list of licenses."""
        licenses = lice.get_licenses()
        assert isinstance(licenses, list)
        assert len(licenses) == len(LICENSES)
        assert all(isinstance(license_name, str) for license_name in licenses)

    def test_get_languages(self, lice: Lice) -> None:
        """Test that get_languages returns a list of languages."""
        languages = lice.get_languages()
        assert isinstance(languages, list)
        assert len(languages) == len(LANGS.keys())
        assert all(isinstance(language, str) for language in languages)

    def test_get_license(self, lice: Lice) -> None:
        """Test we can get a standard license.

        We'll use the AFL3 license as it uses all 3 context vars.
        """
        license_txt = lice.get_license("afl3")

        this_year = get_local_year()

        assert "Academic Free License" in license_txt
        assert "Awesome Co." in license_txt
        assert "my_project" in license_txt
        assert str(this_year) in license_txt

    def test_get_license_unknown(self, lice: Lice) -> None:
        """Test that get_license raises an exception for unknown licenses."""
        with pytest.raises(LicenseNotFoundError) as exc_info:
            lice.get_license("unknown_license")
        assert str(exc_info.value) == "License 'unknown_license' is unknown."
        assert exc_info.value.license_name == "unknown_license"

    def test_get_license_language(self, lice: Lice) -> None:
        """Test we can get a license for a specific language."""
        license_txt = lice.get_license("mit", language="py")

        assert "The MIT License (MIT)" in license_txt
        for line in license_txt.splitlines():
            assert line.startswith("#")

    def test_get_license_language_unknown(self, lice: Lice) -> None:
        """Test that get_license raises an exception for unknown languages."""
        with pytest.raises(LanguageNotFoundError) as exc_info:
            lice.get_license("mit", language="unknown_language")
        assert str(exc_info.value) == "Language 'unknown_language' is unknown."
        assert exc_info.value.language_name == "unknown_language"

    def test_get_license_header(self, lice: Lice) -> None:
        """Test we can get a license header."""
        header = lice.get_header("gpl3")

        assert "This program is free software:" in header
        assert "GNU General Public License" in header

    def test_get_license_header_language(self, lice: Lice) -> None:
        """Test we can get a license header for a specific language."""
        header = lice.get_header("gpl3", language="py")

        assert "This program is free software:" in header
        assert "GNU General Public License" in header
        for line in header.splitlines():
            assert line.startswith("#")

    def test_get_license_header_not_exists(self, lice: Lice) -> None:
        """Test that get_license_header raises an exception for no header."""
        with pytest.raises(HeaderNotFoundError) as exc_info:
            lice.get_header("mit")
        assert str(exc_info.value) == "License 'mit' does not have any headers."
        assert exc_info.value.license_name == "mit"

    def test_get_license_header_language_unknown(self, lice: Lice) -> None:
        """Test get_license_header raises an exception for unknown languages."""
        with pytest.raises(LanguageNotFoundError) as exc_info:
            lice.get_header("gpl3", language="unknown_language")
        assert str(exc_info.value) == "Language 'unknown_language' is unknown."
        assert exc_info.value.language_name == "unknown_language"
