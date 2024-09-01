"""Define custom exceptions for the API."""

from __future__ import annotations


class LiceError(Exception):
    """Base class for all exceptions in the Lice API."""


class LicenseNotFoundError(LiceError):
    """Raised when a license is not found in the database."""

    def __init__(self, license_name: str) -> None:
        """Initialize the LicenseNotFoundError exception.

        Args:
            license_name: The name of the license that was not found.
        """
        self.license_name = license_name
        super().__init__(f"License '{self.license_name}' is unknown.")


class LanguageNotFoundError(LiceError):
    """Raised when a language is not found in the database."""

    def __init__(self, language_name: str) -> None:
        """Initialize the LanguageNotFoundError exception.

        Args:
            language_name: The name of the language that was not found.
        """
        self.language_name = language_name
        super().__init__(f"Language '{self.language_name}' is unknown.")


class HeaderNotFoundError(LiceError):
    """Raised when a header is not found for the supplied license."""

    def __init__(self, license_name: str) -> None:
        """Initialize the NoHeaderFoundError exception.

        Args:
            license_name: The name of the license without a header.
        """
        self.license_name = license_name
        super().__init__(
            f"License '{self.license_name}' does not have any headers."
        )


class InvalidYearError(LiceError):
    """Raised when an invalid year is supplied."""

    def __init__(self, year: str | int) -> None:
        """Initialize the InvalidYearError exception.

        Args:
            year: The year that was not valid.
        """
        self.year = year
        super().__init__(
            f"Year '{self.year}' is not a valid year (must be 4 digits)."
        )
