"""Package initialisation."""

from importlib import resources
from typing import IO

try:
    from pkg_resources import resource_listdir, resource_stream  # type: ignore
except ImportError:

    def resource_stream(
        package_or_requirement: resources.Package, resource_name: str
    ) -> IO[bytes]:
        """Emulate the 'resource_stream' method."""
        ref = resources.files(package_or_requirement).joinpath(resource_name)
        return ref.open("rb")

    def resource_listdir(
        package_or_requirement: resources.Package, resource_name: str
    ) -> list[str]:
        """Emulate the 'resource_listdir' method."""
        resource_qualname = f"{package_or_requirement}".rstrip(".")
        return [
            r.name
            for r in resources.files(resource_qualname)
            .joinpath(resource_name)
            .iterdir()
        ]


__version__ = "0.8.0"

__all__ = ["resource_listdir", "resource_stream"]
