"""Test suite for the application."""

import io
import os
import subprocess
from io import StringIO
from pathlib import Path
from types import SimpleNamespace

import pytest
import typer
from pyperclip import PyperclipException
from pytest_mock import MockerFixture

import lice2
from lice2.config import check_default_license
from lice2.constants import LANGS, LICENSES
from lice2.helpers import (
    clean_path,
    extract_vars,
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
from lice2.tests.conftest import TEMPLATE_FILE

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


def test_validate_license() -> None:
    """Test the 'validate_license' function."""
    assert validate_license("mit") == "mit"

    with pytest.raises(typer.BadParameter) as exc:
        validate_license("bad")

    assert "License 'bad' not found" in exc.value.message


def test_list_vars_mit(
    args: SimpleNamespace, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test the 'list_vars' function for a function with context vars."""
    with pytest.raises(typer.Exit) as exc:
        list_vars(args, "mit")

    captured = capsys.readouterr()

    assert exc.value.exit_code == 0
    assert (
        "The mit license template contains the following variables and "
        "defaults:" in captured.out
    )
    assert "year" in captured.out
    assert "organization" in captured.out


def test_list_vars_gpl3(
    args: SimpleNamespace, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test the 'list_vars' function for license with NO context vars."""
    with pytest.raises(typer.Exit) as exc:
        list_vars(args, "gpl3")

    captured = capsys.readouterr()

    assert exc.value.exit_code == 0
    assert "The gpl3 license template contains no variables" in captured.out


def test_list_vars_not_in_context(
    args: SimpleNamespace,
    capsys: pytest.CaptureFixture[str],
    mocker: MockerFixture,
) -> None:
    """Test the 'list_vars' function with a variable NOT in the context.

    In this case, we should see the name but not the value.
    """
    mock_context = mocker.patch("lice2.helpers.get_context")
    mock_context.return_value = {"year": "2024"}
    with pytest.raises(typer.Exit) as exc:
        list_vars(args, "mit")

    captured = capsys.readouterr()

    assert exc.value.exit_code == 0
    assert (
        "The mit license template contains the following variables and "
        "defaults:" in captured.out
    )
    assert "year" in captured.out
    assert "2024" in captured.out
    assert "organization" in captured.out
    # this was removed from context when we mocked it
    assert "Awesome Co." not in captured.out


def test_list_vars_from_template(
    args: SimpleNamespace, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test the 'list_vars' function with a template path."""
    args.template_path = Path.home() / "template.txt"

    with pytest.raises(typer.Exit) as exc:
        list_vars(args, "mit")

    captured = capsys.readouterr()

    assert exc.value.exit_code == 0
    assert (
        f"The {args.template_path} license template contains the following "
        "variables and defaults:" in captured.out
    )
    assert "year" in captured.out
    assert "2024" in captured.out
    assert "organization" in captured.out
    assert "Awesome Co." in captured.out


def test_generate_header_none(
    args: SimpleNamespace, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test the 'generate_header' function."""
    with pytest.raises(typer.Exit) as exc:
        generate_header(args, "py")

    captured = capsys.readouterr()

    assert exc.value.exit_code == 1
    assert "Sorry, no source headers are available for mit." in captured.err


def test_generate_header_exists(
    args: SimpleNamespace, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test the 'generate_header' function."""
    args.license = "apache"

    with pytest.raises(typer.Exit) as exc:
        generate_header(args, "py")

    captured = capsys.readouterr()

    assert exc.value.exit_code == 0

    assert "# Copyright 2024 Awesome Co." in captured.out
    assert "# Licensed under the Apache License, Version 2.0" in captured.out


def test_generate_header_from_template(
    args: SimpleNamespace, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test the 'generate_header' function."""
    args.template_path = Path.home() / "template.txt"

    with pytest.raises(typer.Exit) as exc:
        generate_header(args, "py")

    captured = capsys.readouterr()

    assert exc.value.exit_code == 0

    assert "# This is a template file." in captured.out

    assert "# Awesome Co. is the organization." in captured.out
    assert "# my_project is the project." in captured.out
    assert "# 2024 is the year." in captured.out


def test_generate_header_to_clipboard(
    args: SimpleNamespace, mocker: MockerFixture
) -> None:
    """Test the 'generate_header' function with clipboard=True."""
    args.license = "apache"
    args.clipboard = True

    mock_pyperclip = mocker.patch("pyperclip.copy")

    with pytest.raises(typer.Exit) as exc:
        generate_header(args, "py")

    assert exc.value.exit_code == 0
    mock_pyperclip.assert_called_once()


def test_generate_header_to_clipboard_fail(
    args: SimpleNamespace,
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test the 'generate_header' function with pyperclip exeception."""
    args.license = "apache"
    args.clipboard = True

    mocker.patch("pyperclip.copy", side_effect=PyperclipException)

    with pytest.raises(typer.Exit) as exc:
        generate_header(args, "py")

    assert exc.value.exit_code == 2  # noqa: PLR2004

    captured = capsys.readouterr()
    assert "Error copying to clipboard" in captured.out


def test_generate_license_missing_context(mocker: MockerFixture) -> None:
    """Test the 'generate_license' function with missing context."""
    # Mock the input template StringIO
    mock_template = io.StringIO(
        "la la la {{ year }} la la la {{ organization }} la more"
    )

    # Mock StringIO for the output to avoid writing to an actual file
    mock_out = mocker.patch("io.StringIO", autospec=True)
    mock_out_instance = mock_out.return_value

    with pytest.raises(ValueError, match="missing from the template context"):
        generate_license(mock_template, {"year": "2024"})

    mock_out_instance.write.assert_not_called()


def test_format_license_no_lang_legacy(fake_config) -> None:
    """Test the 'format_license' function with no lang and legacy=True."""
    content = StringIO(TEMPLATE_FILE)
    result = format_license(content, "", legacy=True)

    # Adjust the TEMPLATE_FILE to match the expected output with a leading space
    # on each line and leading/post <CR>. This extra space is added when the
    # '--legacy' flag is used, to maintain compatibility with the original lice
    # if required.
    adjusted_template = (
        "\n"
        + ("\n".join(" " + line for line in TEMPLATE_FILE.splitlines()) + "\n")
        + "\n"
    )

    assert result.getvalue() == adjusted_template


def test_format_license_no_lang() -> None:
    """Test the 'format_license' function."""
    content = StringIO(TEMPLATE_FILE)
    result = format_license(content, "")

    assert result.getvalue() == TEMPLATE_FILE


def test_format_license_empty_lines() -> None:
    """Test the 'format_license' function with empty lines."""
    content = StringIO("\n\nThis is a test.\n")
    result = format_license(content, "py")

    expected = "#\n#\n# This is a test.\n"

    assert result.getvalue() == expected


def test_load_file_template_path_not_found() -> None:
    """Test the 'load_file_template' function with a bad path."""
    with pytest.raises(ValueError, match="path does not exist"):
        load_file_template("bad/path/to/template.txt")


def test_guess_organization_from_config(mocker: MockerFixture) -> None:
    """Test the 'guess_organization' function.

    Testing when the organization is read from the config file.
    """
    mocker.patch("lice2.helpers.settings.organization", "Awesome Co.")
    result = guess_organization()
    assert result == "Awesome Co."


def test_guess_organization_from_git(mocker: MockerFixture) -> None:
    """Test the 'guess_organization' function.

    Testing when the organization is read from git.
    """
    # Mock the settings.organization to be None or empty
    mocker.patch("lice2.helpers.settings", organization=None)

    # Mock subprocess.check_output to return a specific git user.name
    mock_subprocess = mocker.patch("subprocess.check_output")
    mock_subprocess.return_value = b"Mocked Git User"

    # Call the function under test
    result = guess_organization()

    # Assert that the function returns the git user.name
    assert result == "Mocked Git User"


def test_guess_organization_from_user(mocker: MockerFixture) -> None:
    """Test the 'guess_organization' function.

    Testing when the organization is read from the $USER environment variable.
    """
    # Mock the settings.organization to be None or empty
    mocker.patch("lice2.helpers.settings", organization=None)

    # Mock subprocess.check_output to raise a CalledProcessError
    mock_subprocess = mocker.patch("subprocess.check_output")
    mock_subprocess.side_effect = subprocess.CalledProcessError(
        1, "git config --get user.name"
    )

    # Mock getpass.getuser to return a specific username
    mock_getuser = mocker.patch("getpass.getuser")
    mock_getuser.return_value = "Mocked User"

    # Call the function under test
    result = guess_organization()

    # Assert that the function falls back to the username
    assert result == "Mocked User"


def test_bad_default_license(
    mocker: MockerFixture, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test when the config file has a bad default license.

    It should return bsd3 instead, and not raise an exception.
    It should also print a warning message.
    """
    mocker.patch("lice2.config.settings", default_license="bad")

    result = check_default_license()

    captured = capsys.readouterr()

    assert result == "bsd3"

    assert (
        "Invalid default license 'bad' in the configuration file"
        in captured.out
    )
