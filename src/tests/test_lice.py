import os
from io import StringIO

import src
from src.core import (
    LICENSES,
    clean_path,
    extract_vars,
    generate_license,
    load_file_template,
    load_package_template,
)

TEMPLATE_PATH = os.path.dirname(src.__file__)


def test_paths():
    assert clean_path(".") == os.getcwd()
    assert clean_path("$HOME") == os.environ["HOME"]
    assert clean_path("~") == os.environ["HOME"]


def test_file_template():
    for license in LICENSES:
        path = os.path.join(TEMPLATE_PATH, "template-%s.txt" % license)
        with open(path) as infile:
            content = infile.read()
            assert content == load_file_template(path).getvalue()


def test_package_template():
    for license in LICENSES:
        path = os.path.join(TEMPLATE_PATH, "template-%s.txt" % license)
        with open(path) as infile:
            assert infile.read() == load_package_template(license).getvalue()


def test_extract_vars():
    template = StringIO()
    for license in LICENSES:
        template.write("Oh hey, {{ this }} is a {{ template }} test.")
        var_list = extract_vars(template)
        assert var_list == ["template", "this"]


def test_license():
    context = {"year": "1981", "project": "lice", "organization": "Awesome Co."}

    for license in LICENSES:
        template = load_package_template(license)
        content = template.getvalue()

        content = content.replace("{{ year }}", context["year"])
        content = content.replace("{{ project }}", context["project"])
        content = content.replace("{{ organization }}", context["organization"])

        assert content == generate_license(template, context).getvalue()
        template.close()  # discard memory


def test_license_header():
    context = {"year": "1981", "project": "lice", "organization": "Awesome Co."}

    for license in LICENSES:
        try:
            template = load_package_template(license, header=True)
            content = template.getvalue()

            content = content.replace("{{ year }}", context["year"])
            content = content.replace("{{ project }}", context["project"])
            content = content.replace("{{ organization }}", context["organization"])

            assert content == generate_license(template, context).getvalue()
            template.close()  # discard memory

        except IOError:
            pass  # it's okay to not find templates
