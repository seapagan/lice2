"""Tests for the command line interface."""

from io import StringIO

from pyperclip import PyperclipException
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from lice2.core import app

runner = CliRunner()


def test_cli_list_licenses(mocker: MockerFixture) -> None:
    """Test the CLI list_licenses option."""
    mock_list_licenses = mocker.patch("lice2.core.list_licenses")
    result = runner.invoke(app, ["--licenses"])

    assert result.exit_code == 0
    mock_list_licenses.assert_called_once()


def test_cli_list_languages(mocker: MockerFixture) -> None:
    """Test the CLI list_licenses option."""
    mock_list_languages = mocker.patch("lice2.core.list_languages")
    result = runner.invoke(app, ["--languages"])

    assert result.exit_code == 0
    mock_list_languages.assert_called_once()


def test_cli_generate_header(mocker: MockerFixture) -> None:
    """Test the CLI generate header option."""
    mock_generate_header = mocker.patch("lice2.core.generate_header")

    result = runner.invoke(app, ["--header"])

    assert result.exit_code == 0
    mock_generate_header.assert_called_once()


def test_cli_list_vars(mocker: MockerFixture) -> None:
    """Test the CLI list_vars option."""
    mock_list_vars = mocker.patch("lice2.core.list_vars")

    result = runner.invoke(app, ["--vars"])

    assert result.exit_code == 0
    mock_list_vars.assert_called_once()


def test_cli_template_path(mocker: MockerFixture) -> None:
    """Test the CLI template_path option."""
    mock_template_path = mocker.patch("lice2.core.load_file_template")
    mock_template_path.return_value = StringIO("Mocked template content")

    result = runner.invoke(app, ["--template", "template.txt"])

    assert result.exit_code == 0
    mock_template_path.assert_called_once_with("template.txt")


def test_cli_write_to_file_with_extension(mocker: MockerFixture) -> None:
    """Test the CLI write to file option with an extension."""
    mock_open = mocker.mock_open()
    mocker.patch("pathlib.Path.open", mock_open)

    result = runner.invoke(app, ["--file", "output.py"])

    assert result.exit_code == 0
    mock_open.assert_called_with(mode="w")
    mock_open().write.assert_called_once()
    mock_open().close.assert_called()


def test_cli_write_to_file_without_extension(mocker: MockerFixture) -> None:
    """Test the CLI write to file option without extension.

    This test needs improving so we can test the output file name is generated
    correctly.
    """
    mock_open = mocker.mock_open()
    mocker.patch("pathlib.Path.open", mock_open)

    result = runner.invoke(app, ["--file", "output"])

    assert result.exit_code == 0
    mock_open.assert_called_with(mode="w")
    mock_open().write.assert_called_once()
    mock_open().close.assert_called()


def test_cli_write_to_clipboard(mocker: MockerFixture) -> None:
    """Test the CLI write to clipboard option."""
    mock_clipboard = mocker.patch("pyperclip.copy")

    result = runner.invoke(app, ["--clipboard"])

    assert result.exit_code == 0
    mock_clipboard.assert_called_once()


def test_cli_write_to_clipboard_error(mocker: MockerFixture) -> None:
    """Test the CLI write to clipboard option with an error."""
    mocker.patch("pyperclip.copy", side_effect=PyperclipException)

    result = runner.invoke(app, ["--clipboard"])

    assert result.exit_code == 2  # noqa: PLR2004
    assert "Error copying to clipboard" in result.output
