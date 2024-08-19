"""Define the command-line interface for the `lice` package."""

import argparse
import re
from datetime import datetime
from pathlib import Path

from lice2.constants import LANGS, LICENSES
from lice2.helpers import guess_organization


def get_args() -> argparse.Namespace:
    """Set up the arg parsing and return it."""

    def valid_year(string: str) -> str:
        if not re.match(r"^\d{4}$", string):
            message = "Must be a four-digit year"
            raise argparse.ArgumentTypeError(message)
        return string

    parser = argparse.ArgumentParser(description="Generate a license")

    parser.add_argument(
        "license",
        metavar="license",
        nargs="?",
        choices=LICENSES,
        help=f"the license to generate, one of: {', '.join(LICENSES)}",
    )
    parser.add_argument(
        "--header",
        dest="header",
        action="store_true",
        help="generate source file header for specified license",
    )
    parser.add_argument(
        "-o",
        "--org",
        dest="organization",
        default=guess_organization(),
        help='organization, defaults to .gitconfig or os.environ["USER"]',
    )
    parser.add_argument(
        "-p",
        "--proj",
        dest="project",
        default=Path.cwd().name,
        help="name of project, defaults to name of current directory",
    )
    parser.add_argument(
        "-t",
        "--template",
        dest="template_path",
        help="path to license template file",
    )
    parser.add_argument(
        "-y",
        "--year",
        dest="year",
        type=valid_year,
        default="%i" % datetime.now().date().year,  # noqa: DTZ005
        help="copyright year",
    )
    parser.add_argument(
        "-l",
        "--language",
        dest="language",
        help="format output for language source file, one of: "
        f"{', '.join(LANGS.keys())} [default is not formatted (txt)]",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="ofile",
        default="stdout",
        help="Name of the output source file (with -l, "
        "extension can be ommitted)",
    )
    parser.add_argument(
        "--vars",
        dest="list_vars",
        action="store_true",
        help="list template variables for specified license",
    )
    parser.add_argument(
        "--licenses",
        dest="list_licenses",
        action="store_true",
        help="list available license templates and their parameters",
    )
    parser.add_argument(
        "--languages",
        dest="list_languages",
        action="store_true",
        help="list available source code formatting languages",
    )

    return parser.parse_args()
