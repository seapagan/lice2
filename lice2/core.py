"""Main core of the application."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Annotated, Optional

import typer
from rich.markup import escape  # noqa: TCH002

from lice2.config import check_default_license, settings
from lice2.constants import LANGS, LICENSES  # noqa: TCH001
from lice2.helpers import (
    format_license,
    generate_header,
    generate_license,
    get_context,
    get_lang,
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
def main(  # noqa: PLR0912, PLR0913
    license_name: Annotated[
        str,
        typer.Argument(
            help=f"The license to generate, one of: {', '.join(LICENSES)}",
            callback=validate_license,
            metavar="[license]",
        ),
    ] = check_default_license(),
    header: Annotated[
        bool,
        typer.Option(
            "--header", help="Generate source file header for specified license"
        ),
    ] = False,
    organization: Annotated[
        str,
        typer.Option(
            "--org",
            "-o",
            help='Organization, defaults to .gitconfig or os.environ["USER"]',
        ),
    ] = guess_organization(),
    project: Annotated[
        str,
        typer.Option(
            "--proj",
            "-p",
            help="Name of project, defaults to name of current directory",
        ),
    ] = Path.cwd().name,
    template_path: Annotated[
        Optional[str],
        typer.Option(
            "--template",
            "-t",
            help="Path to license template file",
        ),
    ] = None,
    year: Annotated[
        Optional[str],
        typer.Option(
            "--year", "-y", help="Copyright year", callback=validate_year
        ),
    ] = "%i" % datetime.now().date().year,  # noqa: DTZ005
    language: Annotated[
        Optional[str],
        typer.Option(
            "--language",
            "-l",
            help=(
                "Format output for language source file, one of: "
                f"{', '.join(LANGS.keys())} "
                f"[dim]{escape('[default: txt]')}[/dim]"
            ),
            show_default=False,
        ),
    ] = None,
    ofile: Annotated[
        Optional[str],
        typer.Option(
            "--file",
            "-f",
            help=(
                "Name of the output source file (with -l, "
                "extension can be ommitted)"
            ),
        ),
    ] = "stdout",
    clipboard: Annotated[
        bool,
        typer.Option(
            "--clipboard",
            "-c",
            help="Copy the generated license to the clipboard",
        ),
    ] = False,
    show_vars: Annotated[
        Optional[bool],
        typer.Option(
            "--vars",
            help="List template variables for specified license",
        ),
    ] = None,
    show_licenses: Annotated[
        bool,
        typer.Option(
            "--licenses",
            help="List available license templates and their parameters",
        ),
    ] = False,
    show_languages: Annotated[
        bool,
        typer.Option(
            "--languages",
            help="List available source code formatting languages",
        ),
    ] = False,
    legacy: Annotated[
        bool,
        typer.Option(
            "--legacy",
            help="Use legacy method to generate license",
        ),
    ] = False,
) -> None:
    """Generate a license file.

    Can generate a license file, a source file header, or list available
    licenses, template variables, and source code formatting.
    """
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

    # list available licenses and their template variables
    if args.list_licenses:
        list_licenses()

    # list available source formatting languages
    if args.list_languages:
        list_languages()

    # language
    lang = get_lang(args)

    # generate header if requested
    if header:
        generate_header(args, lang)

    # list template vars if requested
    if args.list_vars:
        list_vars(args, license_name)

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
            try:
                import pyperclip

                pyperclip.copy(out.getvalue())
                typer.secho(
                    "License text copied to clipboard",
                    fg=typer.colors.BRIGHT_GREEN,
                )
            except pyperclip.PyperclipException as exc:
                typer.secho(
                    f"Error copying to clipboard: {exc}",
                    fg=typer.colors.BRIGHT_RED,
                )
                raise typer.Exit(2) from None

    out.close()  # free content memory (paranoic memory stuff)


if __name__ == "__main__":
    app()  # pragma: no cover
