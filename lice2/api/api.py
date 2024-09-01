"""This defines an API that other Python code can use to interact with LICE2."""

from __future__ import annotations

from lice2.api.exceptions import (
    HeaderNotFoundError,
    InvalidYearError,
    LanguageNotFoundError,
    LicenseNotFoundError,
)
from lice2.constants import LANGS, LICENSES
from lice2.helpers import (
    format_license,
    generate_license,
    get_local_year,
    load_package_template,
)


class Lice:
    """List or Generate a License from many supported licenses."""

    def __init__(
        self,
        organization: str,
        project: str,
        year: str | int = get_local_year(),
    ) -> None:
        """Initialize the Lice object.

        Args:
            organization: The name of the organization that owns the project.
            project: The name of the project.
            year: The year to use in the license. Defaults to the current year.
                (can be a string or an integer)

        Note that not all licenses will use the 'project' field.

        Example:
        >>> lice = Lice(organization="Awesome Co.", project="my_project")
        """
        self.organization = organization
        self.project = project

        try:
            # make sure the year can be a valid integer
            _ = int(year)
        except ValueError:
            raise InvalidYearError(year) from None

        self.year = str(year)
        if len(self.year) != 4:  # noqa: PLR2004
            raise InvalidYearError(year) from None

    def get_licenses(self) -> list[str]:
        """Return a list of all licenses in the system.

        This returns a list of strings, where each string is the name of a
        license that can then be used to generate or retrieve the text of that
        license.

        Example:
            >>> lice = Lice(organization="Awesome Co.", project="my_project")
            >>> lice.get_licenses()
            ['apache', 'bsd2', 'bsd3', 'gpl2', 'gpl3', ...]
        """
        return LICENSES

    def get_languages(self) -> list[str]:
        """Return a list of all supported languages.

        This returns a list of strings, where each string is the name of a
        language EXTENSION that can be used to generate a license in that
        language format.

        Example:
            >>> lice = Lice(organization="Awesome Co.", project="my_project")
            >>> lice.get_languages()
            ['py', 'js', 'c', 'cpp', 'java', 'rs', 'rb', 'sh', 'html', ...]
        """
        return list(LANGS.keys())

    def get_license(self, license_name: str, language: str = "") -> str:
        """Return the text of the given license.

        Args:
            license_name: The name of the license to retrieve.
            language: [OPTIONAL] If set, comment the license for that language.

        Examples:
            >>> lice = Lice(organization="Awesome Co.", project="my_project")
            >>> licence_txt = Lice.get_license("mit")
        """
        args = {
            "year": self.year,
            "organization": self.organization,
            "project": self.project,
        }
        try:
            template = load_package_template(license_name)
        except FileNotFoundError:
            raise LicenseNotFoundError(license_name) from None

        content = generate_license(template, args)

        try:
            out = format_license(content, language)
        except KeyError:
            raise LanguageNotFoundError(language) from None
        return out.getvalue()

    def get_header(self, license_name: str, language: str = "") -> str:
        """Return the header of the given license suitable for source files.

        If the language is specified, the header will be formatted as a
        commented block for that language. If not, the header will be returned
        as a plain text block.

        Note: Not all licenses have headers, if the license does not have a
        header, this method will raise a HeaderNotFoundError.

        Args:
            license_name: The name of the license to retrieve.
            language: The language to format the header for.

        Example:
            >>> lice = Lice(organization="Awesome Co.", project="my_project")
            >>> header_txt = Lice.get_header("mit", "py")
        """
        args = {
            "year": self.year,
            "organization": self.organization,
            "project": self.project,
        }
        try:
            template = load_package_template(license_name, header=True)
        except FileNotFoundError:
            raise HeaderNotFoundError(license_name) from None

        content = generate_license(template, args)

        try:
            out = format_license(content, language)
        except KeyError:
            raise LanguageNotFoundError(language) from None
        return out.getvalue()
