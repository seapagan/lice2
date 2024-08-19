"""Main core of the application."""

from __future__ import annotations

import sys
from pathlib import Path

from lice2.cli import get_args
from lice2.constants import DEFAULT_LICENSE
from lice2.helpers import (
    format_license,
    generate_header,
    generate_license,
    get_context,
    get_lang,
    get_suffix,
    list_languages,
    list_licences,
    list_vars,
    load_file_template,
    load_package_template,
)


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
        list_licences()

    # list available source formatting languages
    if args.list_languages:
        list_languages()

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
