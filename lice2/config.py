"""Setup configuration for lice2."""

from rich.console import Console
from rich.panel import Panel
from simple_toml_settings import TOMLSettings

from lice2.constants import LICENSES


class Settings(TOMLSettings):
    """Settings for lice2."""

    default_license: str = "bsd3"
    organization: str = ""
    legacy: bool = False
    clipboard: bool = False


def check_default_license() -> str:
    """Check the default license is in the list of available licenses.

    Return the default license if it is in the list, otherwise return "bsd3".
    This is only used to ensure that the configuration file does not have an
    invalid default license hence crashing the application, and will be called
    automatically by 'Typer'
    """
    if settings.default_license not in LICENSES:
        console = Console(width=80)
        error_text = (
            f"[red]Invalid default license '[b]{settings.default_license}"
            "'[/b] in the configuration file, falling back to '[b]bsd3[/b]', "
            "unless specified otherwise on the command line.\n\nCheck that [b]"
            f"{settings.get_settings_folder()/settings.settings_file_name}[/b]'"
            " has a valid value for [b]'default_license'[/b]."
        )
        panel = Panel(
            error_text,
            title="[b]Error[/b]",
            title_align="left",
            expand=False,
            style="red",
        )

        console.print()
        console.print(panel)
        settings.default_license = "bsd3"
    return settings.default_license


settings = Settings.get_instance(
    "lice",
    xdg_config=True,
    auto_create=False,
    allow_missing_file=True,
    schema_version="1",
)
