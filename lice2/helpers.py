"""Helper functions for LICE2."""

import getpass
import json
import os
import re
import subprocess
import sys
from contextlib import closing
from datetime import datetime
from importlib import resources
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from typing import Union

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

from lice2.config import settings
from lice2.constants import LANG_CMT, LANGS, LICENSES


def clean_path(p: str) -> str:
    """Clean a path.

    Expand user and environment variables anensuring absolute path.
    """
    expanded = os.path.expandvars(Path(p).expanduser())
    return str(Path(expanded).resolve())


def guess_organization() -> str:
    """First, try to get fom the settings file.

    If this is blank, guess the organization from `git config`.
    If that can't be found, fall back to $USER environment variable.
    """
    if settings.organization:
        return settings.organization

    try:
        stdout = subprocess.check_output(  # noqa: S603
            ["git", "config", "--get", "user.name"]  # noqa: S607
        )
        org = stdout.strip().decode("UTF-8")
    except subprocess.CalledProcessError:
        org = getpass.getuser()
    return org


def get_context(args: SimpleNamespace) -> dict[str, str]:
    """Return the context vars from the provided args."""
    return {
        "year": args.year,
        "organization": args.organization,
        "project": args.project,
    }


def get_lang(args: SimpleNamespace) -> str:
    """Check the specified language is supported."""
    lang: str = args.language
    if lang and lang not in LANGS:
        sys.stderr.write(
            "I do not know about a language ending with "
            f"extension '{lang}'.\n"
            "Please send a pull request adding this language to\n"
            "https://github.com/seapagan/lice2. Thanks!\n"
        )
        raise typer.Exit(1)
    return lang


def list_licenses() -> None:
    """List available licenses and their template variables."""
    table = Table(title="Available Licenses")
    table.add_column("License Name")
    table.add_column("Variables")
    for license_name in LICENSES:
        template = load_package_template(license_name)
        var_list = extract_vars(template)
        table.add_row(license_name, ", ".join(var_list))

    console = Console()
    console.print(table)

    raise typer.Exit(0)


def list_languages() -> None:
    """List available source code formatting languages."""
    console = Console(width=80)
    languages = sorted(LANGS.keys())
    text = Text(", ".join(languages))
    console.print(
        "The following source code formatting languages are supported:\n"
    )
    console.print(text)

    raise typer.Exit(0)


def load_file_template(path: str) -> StringIO:
    """Load template from the specified filesystem path."""
    template = StringIO()
    if not Path(path).exists():
        message = f"path does not exist: {path}"
        raise ValueError(message)
    with Path(clean_path(path)).open(mode="rb") as infile:  # opened as binary
        for line in infile:
            template.write(line.decode("utf-8"))  # ensure utf-8
    return template


def get_template_content(license_name: str, *, header: bool = False) -> str:
    """Get the content of a license template as a string.

    Args:
        license_name: Name of the license template to load
        header: If True, load the header template instead of the full license

    Returns:
        The template content as a string

    Raises:
        FileNotFoundError: If the template doesn't exist
    """
    filename = (
        f"template-{license_name}-header.txt"
        if header
        else f"template-{license_name}.txt"
    )
    package_name = __package__ or __name__.split(".")[0]
    template_file = resources.files(package_name) / "templates" / filename
    return template_file.read_text(encoding="utf-8")


def load_package_template(
    license_name: str, *, header: bool = False
) -> StringIO:
    """Load license template distributed with package.

    Args:
        license_name: Name of the license template to load
        header: If True, load the header template instead of the full license

    Returns:
        StringIO object containing the template content

    Raises:
        FileNotFoundError: If the template doesn't exist
    """
    content = StringIO()
    content.write(get_template_content(license_name, header=header))
    return content


def extract_vars(template: StringIO) -> list[str]:
    """Extract variables from template.

    Variables are enclosed in double curly braces.
    """
    keys: set[str] = set()
    for match in re.finditer(r"\{\{ (?P<key>\w+) \}\}", template.getvalue()):
        keys.add(match.groups()[0])
    return sorted(keys)


def generate_license(template: StringIO, context: dict[str, str]) -> StringIO:
    """Generate a license.

    We extract variables from the template and replace them with the
    corresponding values in the given context.

    This could be done with a template engine like 'Jinja2, but we're keeping it
    simple.
    """
    out = StringIO()
    with closing(template):
        content = template.getvalue()
        for key in extract_vars(template):
            if key not in context:
                message = f"{key} is missing from the template context"
                raise ValueError(message)
            content = content.replace(f"{{{{ {key} }}}}", context[key])
        out.write(content)
    return out


def get_comments(lang: str, *, legacy: bool) -> tuple[str, str, str]:
    """Adjust the comment strings for the given language.

    The way it was done previously, extra whitespace was added to the start of
    the comment lines if the comment was a block comment. This tries to fix
    that.
    """
    prefix, comment, postfix = LANG_CMT[LANGS[lang]]
    if legacy:
        return (
            f"{prefix}\n",
            f"{comment} ",
            f"{postfix}\n",
        )

    if comment:
        comment = f"{comment} "
    prefix = f"{prefix}\n" if prefix else ""
    postfix = f"{postfix}\n" if postfix else ""
    return prefix, comment, postfix


def format_license(
    template: StringIO, lang: str, *, legacy: bool = False
) -> StringIO:
    """Format the StringIO template object for specified lang string.

    Return StringIO object formatted
    """
    if not lang:
        lang = "txt"

    prefix, comment, postfix = get_comments(lang, legacy=legacy)

    out = StringIO()

    with closing(template):
        template.seek(0)  # from the start of the buffer
        out.write(prefix)
        for line in template:
            # ensure no extra whitespace is added for blank lines
            out.write(comment if line.strip() else comment.rstrip())
            out.write(line)
        out.write(postfix)

    return out


def get_suffix(name: str) -> Union[str, None]:
    """Check if file name have valid suffix for formatting.

    If have suffix, return it else return None.
    """
    a = name.count(".")
    if a:
        ext = name.split(".")[-1]
        if ext in LANGS:
            return ext
    return None


def list_vars(args: SimpleNamespace, license_name: str) -> None:
    """List the variables for the given template."""
    context = get_context(args)

    if args.template_path:
        template = load_file_template(args.template_path)
    else:
        template = load_package_template(license_name)

    var_list = extract_vars(template)

    if var_list:
        sys.stdout.write(
            "The %s license template contains the following variables "
            "and defaults:\n" % (args.template_path or license_name)
        )
        for v in var_list:
            if v in context:
                sys.stdout.write(f"  {v} = {context[v]}\n")
            else:
                sys.stdout.write(f"  {v}\n")
    else:
        sys.stdout.write(
            f"The {args.template_path or license_name} license template "
            "contains no variables.\n"
        )

    raise typer.Exit(0)


def generate_header(args: SimpleNamespace, lang: str) -> None:
    """Generate a file header for the given license and language."""
    if args.template_path:
        template = load_file_template(args.template_path)
    else:
        try:
            template = load_package_template(args.license, header=True)
        except OSError:
            sys.stderr.write(
                f"Sorry, no source headers are available for {args.license}.\n"
            )
            raise typer.Exit(1) from None

    with closing(template):
        content = generate_license(template, get_context(args))
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
    raise typer.Exit(0)


def validate_year(string: str) -> str:
    """Validate the year is a four-digit number."""
    if not re.match(r"^\d{4}$", string):
        message = "Must be a four-digit year"
        raise typer.BadParameter(message)
    return string


def validate_license(license_name: str) -> str:
    """Validate the license is in the list of available licenses."""
    if license_name not in LICENSES:
        message = (
            f"License '{license_name}' not found - please run 'lice "
            "--licenses' to get a list of available licenses."
        )
        raise typer.BadParameter(message)
    return license_name


def copy_to_clipboard(out: StringIO) -> None:
    """Try to copy to clipboard, exit with error if not possible."""
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


def get_metadata(args: SimpleNamespace) -> None:
    """Return metadata for the package as a JSON string."""
    licenses = LICENSES
    languages = list(LANGS.keys())
    organization = args.organization
    project = args.project

    metadata = {
        "languages": languages,
        "licenses": licenses,
        "organization": organization,
        "project": project,
    }

    sys.stdout.write(json.dumps(metadata) + "\n")

    raise typer.Exit(0)


def get_local_year() -> str:
    """Return the current year using the local timezone."""
    return f"{datetime.now().astimezone().year}"
