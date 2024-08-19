# lice

Lice generates license files. No more hunting down licenses from other projects.

## Changes from the original 'Lice' project

> [!NOTE]
> This project is forked from the original
> [lice](https://github.com/licenses/lice) project which seems to have been
> abandoned and is not compatible with Python 3.12.
>
> I have created a new project rather than issue a PR because the changes are
> quite large, and no-one is merging PR's on the original project. Otherwise,
> the Git history is identical to the original.

This version fixes the compatibility issue and updates the tooling :

- It now uses [Poetry](https://python-poetry.org/) for dependency management
- The code has been modernized and cleaned up, all type-hinting has been
added
- It passes strict linting with the latest 'Ruff'
- GitHub actions set up for `Dependabot` and `Dependency Review`

In addition, future plans are to

- Convert from 'argparse' to 'Typer' for CLI handling.
- Update the existing test suite to full coverage, its at about 39% right now.
- Integrate with 'codacy' for code-quality and test coverage checks.

> [!IMPORTANT]
> This library is now only compatible with Python 3.9 and above. If you wish to
> use an older version, use the original 'lice' package.

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

## Overview

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

```console
    usage: lice [-h] [-o ORGANIZATION] [-p PROJECT] [-t TEMPLATE_PATH] [-y YEAR]
                [--vars] [license]

    positional arguments:
      license               the license to generate, one of: agpl3, apache, bsd2,
                            bsd3, cddl, cc0, epl, gpl2, gpl3, lgpl, mit, mpl

    optional arguments:
      -h, --help            show this help message and exit
      -o ORGANIZATION, --org ORGANIZATION
                            organization, defaults to .gitconfig or
                            os.environ["USER"]
      -p PROJECT, --proj PROJECT
                            name of project, defaults to name of current directory
      -t TEMPLATE_PATH, --template TEMPLATE_PATH
                            path to license template file
      -y YEAR, --year YEAR  copyright year
      -l LANGUAGE, --language LANGUAGE
                            format output for language source file, one of: js, f,
                            css, c, m, java, py, cc, h, html, lua, erl, rb, sh,
                            f90, hpp, cpp, pl, txt [default is not formatted (txt)]
      -f OFILE, --file OFILE Name of the output source file (with -l, extension can be omitted)
      --vars                list template variables for specified license
```

## Changelog

See the [CHANGELOG.md](CHANGELOG.md) file for details for this fork, and the
[OLD_CHANGELOG.md](OLD_CHANGELOG.md) file for the original project.
