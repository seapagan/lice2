"""Main core of the application."""

from __future__ import annotations

import argparse
import getpass
import os
import re
import subprocess
import sys
from contextlib import closing
from datetime import datetime
from importlib import resources
from io import StringIO
from pathlib import Path
from typing import IO, Union

try:
    from pkg_resources import resource_listdir, resource_stream  # type: ignore
except ImportError:
    import importlib.resources

    def resource_stream(
        package_or_requirement: resources.Package, resource_name: str
    ) -> IO[bytes]:
        """Emulate the 'resource_stream' method."""
        ref = importlib.resources.files(package_or_requirement).joinpath(
            resource_name
        )
        return ref.open("rb")

    def resource_listdir(
        package_or_requirement: resources.Package, resource_name: str
    ) -> list[str]:
        """Emulate the 'resource_listdir' method."""
        resource_qualname = f"{package_or_requirement}".rstrip(".")
        return [
            r.name
            for r in importlib.resources.files(resource_qualname)
            .joinpath(resource_name)
            .iterdir()
        ]


LICENSES: list[str] = []
for file in sorted(resource_listdir(__name__, "templates")):
    match = re.match(r"template-([a-z0-9_]+).txt", file)
    if match:
        LICENSES.append(match.groups()[0])

DEFAULT_LICENSE = "bsd3"

# To extend language formatting sopport with a new language, add an item in
# LANGS dict:
# "language_suffix":"comment_name"
# where "language_suffix" is the suffix of your language and "comment_name" is
# one of the comment types supported and listed in LANG_CMT:
# text : no comment
# c    : /* * */
# unix : #
# lua  : --- --

# if you want add a new comment type just add an item to LANG_CMT:
# "comment_name":[u'string', u'string', u'string']
# where the first string open multiline comment, second string comment every
# license's line and the last string close multiline comment,
# associate your language and source file suffix with your new comment type
# how explained above.
# EXAMPLE:
# LANG_CMT = {"c":[u'/*', u'*', u'*/']}  # noqa: ERA001
# LANGS = {"cpp":"c"}  # noqa: ERA001
# (for more examples see LANG_CMT and langs dicts below)
# NOTE: unicode (u) in comment strings is required.


LANGS = {
    "agda": "haskell",
    "c": "c",
    "cc": "c",
    "clj": "lisp",
    "cpp": "c",
    "css": "c",
    "el": "lisp",
    "erl": "erlang",
    "f": "fortran",
    "f90": "fortran90",
    "h": "c",
    "hpp": "c",
    "hs": "haskell",
    "html": "html",
    "idr": "haskell",
    "java": "java",
    "js": "c",
    "lisp": "lisp",
    "lua": "lua",
    "m": "c",
    "ml": "ml",
    "php": "c",
    "pl": "perl",
    "py": "unix",
    "ps": "powershell",
    "rb": "ruby",
    "scm": "lisp",
    "sh": "unix",
    "txt": "text",
    "rs": "rust",
}

LANG_CMT = {
    "c": ["/*", " *", " */"],
    "erlang": ["%%", "%", "%%"],
    "fortran": ["C", "C", "C"],
    "fortran90": ["!*", "!*", "!*"],
    "haskell": ["{-", "", "-}"],
    "html": ["<!--", "", "-->"],
    "java": ["/**", " *", " */"],
    "lisp": ["", ";;", ""],
    "lua": ["--[[", "", "--]]"],
    "ml": ["(*", "", "*)"],
    "perl": ["=item", "", "=cut"],
    "powershell": ["<#", "#", "#>"],
    "ruby": ["=begin", "", "=end"],
    "text": ["", "", ""],
    "unix": ["", "#", ""],
    "rust": ["", "//" ""],
}


def clean_path(p: str) -> str:
    """Clean a path.

    Expand user and environment variables anensuring absolute path.
    """
    expanded = os.path.expandvars(Path(p).expanduser())
    return str(Path(expanded).resolve())


def get_context(args: argparse.Namespace) -> dict[str, str]:
    """Return the context vars from the provided args."""
    return {
        "year": args.year,
        "organization": args.organization,
        "project": args.project,
    }


def guess_organization() -> str:
    """Guess the organization from `git config`.

    If that can't be found, fall back to $USER environment variable.
    """
    try:
        stdout = subprocess.check_output("git config --get user.name".split())  # noqa: S603
        org = stdout.strip().decode("UTF-8")
    except subprocess.CalledProcessError:
        org = getpass.getuser()
    return org


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


def load_package_template(
    license_name: str, *, header: bool = False
) -> StringIO:
    """Load license template distributed with package."""
    content = StringIO()
    filename = "template-%s-header.txt" if header else "template-%s.txt"
    with resource_stream(
        __name__, f"templates/{filename % license_name}"
    ) as licfile:
        for line in licfile:
            content.write(line.decode("utf-8"))  # write utf-8 string
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
    """
    out = StringIO()
    content = template.getvalue()
    for key in extract_vars(template):
        if key not in context:
            message = f"{key} is missing from the template context"
            raise ValueError(message)
        content = content.replace(f"{{{{ {key} }}}}", context[key])
    template.close()  # free template memory (when is garbage collected?)
    out.write(content)
    return out


def format_license(template: StringIO, lang: str) -> StringIO:
    """Format the StringIO template object for specified lang string.

    Return StringIO object formatted
    """
    if not lang:
        lang = "txt"

    out = StringIO()

    with closing(template):
        template.seek(0)  # from the start of the buffer
        out.write(LANG_CMT[LANGS[lang]][0] + "\n")
        for line in template:
            out.write(LANG_CMT[LANGS[lang]][1] + " ")
            out.write(line)
        out.write(LANG_CMT[LANGS[lang]][2] + "\n")

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


def list_vars(args: argparse.Namespace, license_name: str) -> None:
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

    sys.exit(0)


def generate_header(
    args: argparse.Namespace, license_name: str, lang: str
) -> None:
    """Generate a file header for the given license and language."""
    if args.template_path:
        template = load_file_template(args.template_path)
    else:
        try:
            template = load_package_template(license_name, header=True)
        except OSError:
            sys.stderr.write(
                "Sorry, no source headers are available for "
                f"{args.license}.\n"
            )
            sys.exit(1)

    content = generate_license(template, get_context(args))
    out = format_license(content, lang)
    out.seek(0)
    sys.stdout.write(out.getvalue())
    out.close()  # free content memory (paranoic memory stuff)
    sys.exit(0)


def get_lang(args: argparse.Namespace) -> str:
    """Check the specified language is supported."""
    lang: str = args.language
    if lang and lang not in LANGS:
        sys.stderr.write(
            "I do not know about a language ending with "
            f"extension {lang}.\n"
            "Please send a pull request adding this language to\n"
            "https://github.com/seapagan/lice2. Thanks!\n"
        )
        sys.exit(1)
    return lang


def main() -> None:
    """Main program loop."""
    args = get_args()

    # do license stuff
    license_name = args.license or DEFAULT_LICENSE

    # language
    lang = get_lang(args)

    # generate header if requested
    if args.header:
        generate_header(args, license_name, lang)

    # list template vars if requested
    if args.list_vars:
        list_vars(args, license_name)

    # list available licenses and their template variables
    if args.list_licenses:
        for license_name in LICENSES:
            template = load_package_template(license_name)
            var_list = extract_vars(template)
            sys.stdout.write(
                "{} : {}\n".format(license_name, ", ".join(var_list))
            )
        sys.exit(0)

    # list available source formatting languages
    if args.list_languages:
        for lang in sorted(LANGS.keys()):
            sys.stdout.write(f"{lang}\n")
        sys.exit(0)

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
            out = format_license(content, ext)  # format license by file suffix
        else:
            output = f"{args.ofile}.{lang}" if lang else args.ofile
            out = format_license(content, lang)

        out.seek(0)
        with Path(output).open(mode="w") as f:
            f.write(out.getvalue())
        f.close()
    else:
        out = format_license(content, lang)
        out.seek(0)
        sys.stdout.write(out.getvalue())
    out.close()  # free content memory (paranoic memory stuff)


if __name__ == "__main__":
    main()