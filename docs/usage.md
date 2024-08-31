# Usage

## Basic Usage

At its simplest, `lice` will generate a license header for you to the standard
output. If you don't specify a license, `lice` will default to the BSD-3
license.

```console
$ lice

 Copyright (c) 2024, Grant Ramsay

 All rights reserved.

 Redistribution and use in source and binary forms, with or without modification,
 ...
```

It will fill in the current year and your name as the copyright holder.

## Specifying a License

You can specify a license as the first option. For example, to generate a MIT
license:

```console
$ lice mit

The MIT License (MIT)
Copyright (c) 2024 Grant Ramsay

Permission is hereby granted, free of charge, to any person obtaining a copy
...
```

This can be used with any of the options below. Run `lice --licenses` to see a
list of all available licenses.

## Command Line Options

`lice` has a number of command line options to customize the output. For a full
list of options, run `lice --help`.

### `--header` option

This will generate a brief license header that can be used in source files.

```console
lice --header
```

Again, you can specify a license:

```console
lice --header apache
```

!!! note
    The `--header` option is not available for all licenses. If it is not
    available, there will be a message to that effect.

### `--org` / `-o` option

This will allow you to specify an organization name to be used in the license,
and can be set in the configuration file under the `organization` key.

```console
lice -o "Awesome Co."
```

### `--proj` / `-p` option

This will allow you to specify a project name to be used in the license.

```console
lice -p "My Awesome Project"
```

!!! note
    Not all licenses support the `--proj` option. Run `lice --licences` to see
    which licenses support this option.

### `--template` / `-t` option

This will allow you to specify a custom template to be used as the license.

```console
lice -t "./path/to/template.txt"
```

### `--year` / `-y` option

This will allow you to specify a year to be used in the license. If you don't
specify a year, it will default to the current year.

```console
lice -y 2024
```

### `--language` / `-l` option

This will allow you to specify a **programming** language to be used in the
license. Specify the **extension** of the file you are creating the license for.

```console

lice -l py
```

Currently supported languages are:

agda, c, cc, clj, cpp, css, el, erl, f, f90, h, hpp, hs, html, idr, java, js,
lisp, lua, m, ml, php, pl, py, ps, rb, scm, sh, txt, rs

### `--file` / `-f` option

This will allow you to specify a file name to be used in the license, and so the
license will be written to that file instead of the standard output.

```console
lice mit -f "LICENSE.txt"
```

!!! note
    If you specify a language with the `-l` option, the extension will be
    automatically added to the file name so you don't need to include it.

### `--clipboard` / `-c` option

This will automatically copy the generated license to the clipboard.

```console
lice mit -c
```

In this case the license will not be written to the standard output.

If you are writing to a file with the `-f` option, the clipboard option will
be ignored. This is only implemented for the normal license output to the
terminal  and the `--header` option.

!!! warning
    This option may initially fail on some Linux systems, as it requires the
    `xclip` or `xsel` command to be installed. You can install one of these with
    your package manager. It should work out of the box on macOS or Windows. The
    program will give you an informative error message if it fails on how to
    install the required program.

### `--legacy` option

In the original `lice`, the licenses were generated with a leading space on each
line and extra newlines at start and end. This was considered a bug by at least
several users, so it was fixed in version `0.10.0`. However, if you want to
generate a license with the old style, you can use the `--legacy` option.

```console
lice mit --legacy
```

If you want to use the old style by default, you can set the `legacy` key in the
configuration file to `true`.

```toml
[lice]
legacy = true
```

### `--vars` option

This will list the variables that can be used in the specified license.

```console
lice --vars mit
```

### `--licenses` option

This will list all the available licenses and their parameters.

```console
lice --licenses
```

### `--languages` option

This will list all the available source code formatting languages.

```console
lice --languages
```

### `--metadata` option

This will output a JSON object containing a list of all the licenses and
languages available.

```console
lice --metadata
```

The output will have 4 keys: `licenses`, `languages`, `organization` and
`project` which another tool can use to populate a list of licenses and
languages in a GUI for example. The first two keys are simple lists of strings
that can be parsed.

Future versions will have an actual python api that can be imported in other
python projects to generate licenses from within the project.

### `--install-completion` option

This will install tab-completion for the current shell.

```console
lice --install-completion
```

### `--show-completion` option

This will show the tab-completion for the current shell, so you can copy it or
customize the installation.

```console
lice --show-completion
```

### `--help` / `-h` option

Displays help for the application and it's options.

```console
lice --help
```
