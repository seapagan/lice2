"""Main core of the application."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, Optional

import typer
from rich import print as rprint
from rich.markup import escape

from lice2 import __version__
from lice2.config import check_default_license, settings
from lice2.constants import LANGS, LICENSES
from lice2.helpers import (
    copy_to_clipboard,
    format_license,
    generate_header,
    generate_license,
    get_context,
    get_lang,
    get_local_year,
    get_metadata,
    get_suffix,
    guess_organization,
    list_languages,
    list_licenses,
    list_vars,
    load_file_template,
    load_package_template,
    validate_license,
    validate_year,
)

app = typer.Typer(rich_markup_mode="rich")


@app.command(
    help=(
        "Generates a license template with context variables, and "
        "optionally write this to a file."
    ),
    context_settings={"help_option_names": ["-h", "--help"]},
)
def main(  # noqa: PLR0913
    license_name: str = typer.Argument(
        default=check_default_license(),
        help=f"The license to generate, one of: {', '.join(LICENSES)}",
        callback=validate_license,
        metavar="[license]",
    ),
    organization: str = typer.Option(
        guess_organization(),
        "--org",
        "-o",
        help='Organization, defaults to .gitconfig or os.environ["USER"]',
    ),
    project: str = typer.Option(
        Path.cwd().name,
        "--proj",
        "-p",
        help="Name of project, defaults to name of current directory",
    ),
    template_path: Optional[str] = typer.Option(
        None,
        "--template",
        "-t",
        help="Path to license template file",
    ),
    year: Optional[str] = typer.Option(
        get_local_year(),
        "--year",
        "-y",
        help="Copyright year",
        callback=validate_year,
    ),
    language: Optional[str] = typer.Option(
        None,
        "--language",
        "-l",
        help=(
            "Format output for language source file, one of: "
            f"{', '.join(LANGS.keys())} "
            f"[dim]{escape('[default: txt]')}[/dim]"
        ),
        show_default=False,
    ),
    ofile: Optional[str] = typer.Option(
        "stdout",
        "--file",
        "-f",
        help=(
            "Name of the output source file (with -l, extension can be omitted)"
        ),
    ),
    *,
    header: bool = typer.Option(
        False,
        "--header",
        help="Generate source file header for specified license",
    ),
    clipboard: bool = typer.Option(
        False,
        "--clipboard",
        "-c",
        help="Copy the generated license to the clipboard",
    ),
    show_vars: Optional[bool] = typer.Option(
        None,
        "--vars",
        help="List template variables for specified license",
    ),
    show_licenses: bool = typer.Option(
        False,
        "--licenses",
        help="List available license templates and their parameters",
    ),
    show_languages: bool = typer.Option(
        False,
        "--languages",
        help="List available source code formatting languages",
    ),
    legacy: bool = typer.Option(
        False,
        "--legacy",
        help="Use legacy method to generate license",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        is_eager=True,
        help="Show version info",
    ),
    metadata: bool = typer.Option(
        False,
        "--metadata",
        help=(
            "Output a JSON string listing all available licenses and "
            "languages This allows easy integration into other tools."
        ),
    ),
) -> None:
    """Generate a license file.

    Can generate a license file, a source file header, or list available
    licenses, template variables, and source code formatting.
    """
    # deal with the '--version' flag first
    if version:
        rprint(
            "\n[green]Lice2 - Generate license files for your projects."
            f"\n[/green]Version: {__version__} "
            "\u00a9 2013-2024\n"
        )
        raise typer.Exit(0)

    # get the args into a dict to avoid refactoring all the code...
    args_base: dict[str, str | bool | None] = {
        "license": license_name,
        "header": header,
        "organization": organization,
        "project": project,
        "template_path": template_path,
        "year": year,
        "language": language,
        "ofile": ofile,
        "clipboard": clipboard or settings.clipboard,
        "legacy": legacy or settings.legacy,
        "list_vars": show_vars,
        "list_licenses": show_licenses,
        "list_languages": show_languages,
    }
    # convert to SimpleNamespace, so we can use dot notation
    args = SimpleNamespace(**args_base)

    # get the language if set
    lang = get_lang(args)

    actions: list[tuple[bool, Callable[..., None], list[Any]]] = [
        (metadata, get_metadata, [args]),
        (args.list_licenses, list_licenses, []),
        (args.list_languages, list_languages, []),
        (header, generate_header, [args, lang]),
        (args.list_vars, list_vars, [args, license_name]),
    ]

    # Iterate through the list and call the utility functions based on the
    # conditions. All the utility functions exit the program after execution.
    # This saves us from having to write a lot of if-else statements.
    for condition, func, func_args in actions:
        if condition:
            func(*func_args)

    # create context
    if args.template_path:
        template = load_file_template(args.template_path)
    else:
        template = load_package_template(license_name)

    content = generate_license(template, get_context(args))

    if args.ofile != "stdout":
        ext = get_suffix(args.ofile)
        if ext:
            output = args.ofile
            out = format_license(
                content, ext, legacy=args.legacy
            )  # format license by file suffix
        else:
            output = f"{args.ofile}.{lang}" if lang else args.ofile
            out = format_license(content, lang, legacy=args.legacy)

        out.seek(0)
        with Path(output).open(mode="w") as f:
            f.write(out.getvalue())
    else:
        out = format_license(content, lang, legacy=args.legacy)
        out.seek(0)
        if not args.clipboard:
            sys.stdout.write(out.getvalue())
        else:
            copy_to_clipboard(out)

    out.close()


if __name__ == "__main__":
    app()  # pragma: no cover
