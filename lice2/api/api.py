"""This defines an API that other Python code can use to interact with LICE2."""

from lice2.constants import LANGS, LICENSES


class Lice:
    """List or Generate a License from many supported licenses."""

    def __init__(self, organization: str, project: str) -> None:
        """Initialize the Lice object.

        Args:
            organization: The name of the organization that owns the project.
            project: The name of the project.

        Note that not all licenses will use the 'project' field.

        Example:
        >>> lice = Lice(organization="Awesome Co.", project="my_project")
        """
        self.organization = organization
        self.project = project

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
