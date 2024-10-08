"""Define constants for the LICE2 package."""

import re

from lice2 import resource_listdir

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
# "comment_name":['string', 'string', 'string']
# where the first string open multiline comment, second string comment every
# license's line and the last string close multiline comment,
# associate your language and source file suffix with your new comment type
# how explained above.
# EXAMPLE:
# LANG_CMT = {"c":['/*', '*', '*/']}  # noqa: ERA001
# LANGS = {"cpp":"c"}  # noqa: ERA001
# (for more examples see LANG_CMT and langs dicts below)

LANGS = {
    "ada": "ada",
    "adb": "ada",
    "ads": "ada",
    "agda": "haskell",
    "bash": "unix",
    "c": "c",
    "cc": "c",
    "clj": "lisp",
    "cpp": "c",
    "cs": "c",
    "css": "c",
    "dart": "c",
    "el": "lisp",
    "erl": "erlang",
    "f": "fortran",
    "f90": "fortran90",
    "go": "c",
    "h": "c",
    "hpp": "c",
    "hs": "haskell",
    "html": "html",
    "idr": "haskell",
    "java": "java",
    "js": "c",
    "kt": "java",
    "lisp": "lisp",
    "lua": "lua",
    "m": "c",
    "md": "html",
    "ml": "ml",
    "php": "c",
    "pl": "perl",
    "ps": "powershell",
    "py": "unix",
    "rb": "ruby",
    "r": "unix",
    "rs": "rust",
    "scala": "java",
    "scm": "lisp",
    "sh": "unix",
    "sql": "c",
    "swift": "c",
    "toml": "unix",
    "ts": "c",
    "txt": "text",
    "v": "c",
    "vhdl": "ada",
    "xml": "html",
    "yaml": "unix",
}

LANG_CMT = {
    "ada": ["", "--", ""],
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
    "rust": ["", "//", ""],
    "text": ["", "", ""],
    "unix": ["", "#", ""],
}

LICENSES: list[str] = []
for file in sorted(resource_listdir(__name__, "templates")):
    match = re.match(r"template-([a-z0-9_]+).txt", file)
    if match:
        LICENSES.append(match.groups()[0])
