# lice <!-- omit in toc -->

Lice generates license files. No more hunting down licenses from other projects.

- [Changes from the original 'Lice' project](#changes-from-the-original-lice-project)
- [Installation](#installation)
  - [Development Version](#development-version)
  - [Autocompletion](#autocompletion)
- [Overview](#overview)
- [I want XXXXXXXXX license in here!](#i-want-xxxxxxxxx-license-in-here)
- [Usage](#usage)
- [Config File](#config-file)
- [Changelog](#changelog)

## Changes from the original 'Lice' project

> [!NOTE]
> This project is forked from the original
> [lice](https://github.com/licenses/lice) project which seems to have been
> abandoned and is not compatible with Python 3.12.
>
> I have created a new project rather than issue a PR because the changes are
> quite large, and no-one is merging PR's on the original project. Otherwise,
> the Git history is identical to the original.

This version fixes the compatibility issue with Python 3.12, and adds some new
features:

- It now uses [Poetry](https://python-poetry.org/) for dependency management.
- Can read from a config file for default values.
- Can optionally copy the license to the clipboard automatically.
- Converted from 'argparse' to 'Typer' for CLI handling.
- Fixes the issue where extra spaces and newlines were added to the generated
  license text. This was considered a bug by at least several users, so it was
  fixed in version `0.10.0`. However, if you want to generate a license with the
  old style, you can use the `--legacy` option or set the `legacy` key in the
  configuration file to `true`.
- The code has been modernized and cleaned up, all type-hinting has been
  added.
- It passes strict linting with the latest 'Ruff' and 'mypy'.
- GitHub actions set up for linting, `Dependabot` and `Dependency Review`.

In addition, future plans can be seen in the [TODO.md](TODO.md) file.

> [!IMPORTANT]
> This appllication is now only compatible with Python 3.9 and above. If you
> wish to use an older version, use the original 'lice' package.
>
> However, I'ts the **development** dependencies that are causing the
> incompatibility, so I'll look at reducing the **Production** version in future
> releases while still requiring Python 3.9 or above for development.

## Installation

Installation is standard. If you are using [pipx](https://pipx.pypa.io/)
(recommended) install it as:

```console
pipx install lice2
```

Otherwise use `pip` as standard:

```console
pip install lice2
```

### Development Version

If you want to install the development version to try out new features before
they are release, you can do so with the following command:

```console
pipx install git+https://github.com/seapagan/lice2.git
```

or

```console
pip install git+https://github.com/seapagan/lice2.git
```

### Autocompletion

To enable autocompletion for lice options, run the following command after
installation:

```console
lice --install-completion
```

## Overview

Full usage information is available on the documentation site at
<https://seapagan.github.io/lice2>

Generate a BSD-3 license, the default:

```console
$ lice
Copyright (c) 2013, Jeremy Carbaugh

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
...
```

Generate an MIT license:

```console
$ lice mit
The MIT License (MIT)
Copyright (c) 2013 Jeremy Carbaugh

Permission is hereby granted, free of charge, to any person obtaining a copy
...
```

Generate a BSD-3 license, specifying the year and organization to be used:

```console
$ lice -y 2012 -o "Sunlight Foundation"
Copyright (c) 2012, Sunlight Foundation

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
...
```

Generate a BSD-3 license, formatted for python source file:

```console
$ lice -l py

# Copyright (c) 2012, Sunlight Foundation
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
...
```

Generate a python source file with a BSD-3 license commented in the header:

```console
$ lice -l py -f test
$ ls
test.py
$ cat test.py

# Copyright (c) 2012, Sunlight Foundation
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
...
```

Generate a source file (language detected by -f  extension):

```console
$ lice -f test.c && cat test.c
/*
 * Copyright (c) 2012, Sunlight Foundation
 *
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 ...
```

If organization is not specified, lice will first attempt to use `git config` to
find your name. If not found, it will use the value of the $USER environment
variable. If the project name is not specified, the name of the current
directory is used. Year will default to the current year.

You can see what variables are available to you for any of the licenses:

```console
$ lice --vars mit
The mit license template contains the following variables:
  year
  organization
```

## I want XXXXXXXXX license in here!

Great! Is it a license that is commonly used? If so, open an issue or, if you
are feeling generous, fork and submit a pull request.

## Usage

You can get help on the command line with `lice --help`:

```console
$ lice --help

 Usage: lice [OPTIONS] [license]

 Generates a license template with context variables, and can optionally write this to a file.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────╮
│   license_name      [license]  The license to generate, one of: afl3, agpl3, apache, bsd2, bsd3,  │
│                                cc0, cc_by, cc_by_nc, cc_by_nc_nd, cc_by_nc_sa, cc_by_nd,          │
│                                cc_by_sa, cddl, epl, gpl2, gpl3, isc, lgpl, mit, mpl, wtfpl, zlib  │
│                                [default: bsd3]                                                    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --header                            Generate source file header for specified license             │
│ --org                 -o      TEXT  Organization, defaults to .gitconfig or os.environ["USER"]    │
│                                     [default: <as above>]                                         │
│ --proj                -p      TEXT  Name of project, defaults to name of current directory        │
│                                     [default: <current folder>]                                   │
│ --template            -t      TEXT  Path to license template file [default: None]                 │
│ --year                -y      TEXT  Copyright year [default: <current year>]                      │
│ --language            -l      TEXT  Format output for language source file, one of: agda, c, cc,  │
│                                     clj, cpp, css, el, erl, f, f90, h, hpp, hs, html, idr, java,  │
│                                     js, lisp, lua, m, ml, php, pl, py, ps, rb, scm, sh, txt, rs   │
│                                     [default: txt]                                                │
│ --file                -f      TEXT  Name of the output source file (with -l, extension can be     │
│                                     ommitted)                                                     │
│                                     [default: stdout]                                             │
| --clipboard           -c            Copy the generated license to the clipboard                   |
│ --vars                              List template variables for specified license                 │
│ --licenses                          List available license templates and their parameters         │
│ --languages                         List available source code formatting languages               │
│ --install-completion                Install completion for the current shell.                     │
│ --show-completion                   Show completion for the current shell, to copy it or          │
│                                     customize the installation.                                   │
│ --help                -h            Show this message and exit.                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Config File

The app will look for a config file in `~/.config/lice/config.toml`. This file
can be used to set default values for the license and organization.

```toml
[lice]
default_license = "mit"
organization = "Grant Ramsay"
clipboard = false
```

The 'default_license' is checked at run-time, and if it is not valid then it
falls back to the BSD-3 license.

## Changelog

See the [CHANGELOG.md](CHANGELOG.md) file for details for this fork, and the
[OLD_CHANGELOG.md](OLD_CHANGELOG.md) file for the original project.
