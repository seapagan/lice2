"""Test suite for the application."""

import os
from io import StringIO
from pathlib import Path
from types import SimpleNamespace

import pytest
import typer

import lice2
from lice2.constants import LANGS, LICENSES
from lice2.helpers import (
    clean_path,
    extract_vars,
    generate_license,
    get_context,
    get_lang,
    get_suffix,
    list_languages,
    list_licenses,
    load_file_template,
    load_package_template,
    validate_year,
)

TEMPLATE_PATH = Path(lice2.__file__).parent / "templates"


def test_paths() -> None:
    """Test the 'clean_path' function."""
    assert clean_path(".") == str(Path.cwd())
    assert clean_path("$HOME") == os.environ["HOME"]
    assert clean_path("~") == os.environ["HOME"]


def test_file_template() -> None:
    """Test we can load templates properly."""
    for license_name in LICENSES:
        path = TEMPLATE_PATH / (f"template-{license_name}.txt")
        with path.open() as infile:
            content = infile.read()
            assert content == load_file_template(str(path)).getvalue()


def test_package_template() -> None:
    """Test the 'load_package_template' function."""
    for license_name in LICENSES:
        path = TEMPLATE_PATH / (f"template-{license_name}.txt")
        with path.open() as infile:
            assert (
                infile.read() == load_package_template(license_name).getvalue()
            )


def test_extract_vars() -> None:
    """Test the 'extract_vars' function."""
    template = StringIO()
    for _ in LICENSES:
        template.write("Oh hey, {{ this }} is a {{ template }} test.")
        var_list = extract_vars(template)
        assert var_list == ["template", "this"]


def test_generate_license() -> None:
    """Test the 'generate_license' function."""
    context = {"year": "1981", "project": "lice", "organization": "Awesome Co."}

    for license_name in LICENSES:
        template = load_package_template(license_name)
        content = template.getvalue()

        content = content.replace("{{ year }}", context["year"])
        content = content.replace("{{ project }}", context["project"])
        content = content.replace("{{ organization }}", context["organization"])

        assert content == generate_license(template, context).getvalue()
        template.close()  # discard memory


def test_license_header() -> None:
    """Test the license header is correct."""
    context = {"year": "1981", "project": "lice", "organization": "Awesome Co."}

    try:
        for license_name in LICENSES:
            template = load_package_template(license_name, header=True)
            content = template.getvalue()

            content = content.replace("{{ year }}", context["year"])
            content = content.replace("{{ project }}", context["project"])
            content = content.replace(
                "{{ organization }}", context["organization"]
            )

            assert content == generate_license(template, context).getvalue()
            template.close()  # discard memory

    except OSError:
        pass  # it's okay to not find templates


def test_get_context() -> None:
    """Test the 'get_context' function."""
    context_dict = {
        "year": "2024",
        "project": "lice",
        "organization": "Awesome Co.",
    }
    fake_context = SimpleNamespace(**context_dict)

    context = get_context(fake_context)
    assert context["year"] == "2024"
    assert context["project"] == "lice"
    assert context["organization"] == "Awesome Co."


def test_get_lang(args: SimpleNamespace) -> None:
    """Test the 'get_lang' function."""
    args.language = "py"
    result = get_lang(args)

    assert result == "py"


def test_get_bad_lang(
    args: SimpleNamespace, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test the 'get_lang' function with a bad language spec."""
    args.language = "bad"
    with pytest.raises(typer.Exit) as exc:
        get_lang(args)

    captured = capsys.readouterr()

    assert exc.value.exit_code == 1
    assert (
        "I do not know about a language ending with extension 'bad'."
        in captured.err
    )


def test_list_languages(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the 'list_languages' function."""
    with pytest.raises(typer.Exit) as exc:
        list_languages()

    captured = capsys.readouterr()

    assert exc.value.exit_code == 0
    assert (
        "The following source code formatting languages are supported:"
        in captured.out
    )
    for lang in LANGS:
        assert lang in captured.out


def test_list_licenses(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the 'list_licenses' function."""
    with pytest.raises(typer.Exit) as exc:
        list_licenses()

    captured = capsys.readouterr()

    assert exc.value.exit_code == 0
    assert "Available Licenses" in captured.out
    for license_name in LICENSES:
        assert license_name in captured.out
        template = load_package_template(license_name)
        var_list = extract_vars(template)
        for var in var_list:
            assert var in captured.out


def test_get_suffix() -> None:
    """Test the 'get_suffix' function."""
    assert get_suffix("file.py") == "py"
    assert get_suffix("file") is None
    assert get_suffix("file.") is None
    assert get_suffix("file.unknown") is None


def test_validate_year() -> None:
    """Test the 'validate_year' function."""
    assert validate_year("2024") == "2024"

    with pytest.raises(typer.BadParameter) as exc1:
        validate_year("12345")

    with pytest.raises(typer.BadParameter) as exc2:
        validate_year("123")

    assert "Must be a four-digit year" in exc1.value.message
    assert "Must be a four-digit year" in exc2.value.message
