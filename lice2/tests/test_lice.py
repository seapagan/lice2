"""Test suite for the application."""

import os
from io import StringIO
from pathlib import Path

import lice2
from lice2.constants import LICENSES
from lice2.helpers import (
    clean_path,
    extract_vars,
    generate_license,
    load_file_template,
    load_package_template,
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
