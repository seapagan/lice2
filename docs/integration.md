# Integrating 'Lice2' in your own project

## Overview

Starting version `0.12.0`, you can use `Lice2` as an API in your own project to
generate licenses. Here is an example:

```python
from lice2.api import Lice

lice = Lice(organization="Awesome Organization", project="Awesome Project")
license_text = lice.get_license("mit")
print(license_text)
```

This will generate the MIT license text with the organization and project name
replaced with the values you provided, using the current year as the default.

## Construct a Lice object

To use `lice2` in your own project, you first need to construct a `Lice` object.

```python
from lice2.api import Lice

lice = Lice(organization="Awesome Organization", project="Awesome Project")
```

This is the minimum required to construct a `Lice` object. The organization and
project name are required to generate a license. If you don't provide them, the
class will raise a `TypeError`.

You can also pass a year to the constructor if you want to use a different year
for any reason (can be useful for testing). This can be an integer or a string.

```python
from lice2.api import Lice

lice = Lice(
  organization="Awesome Organization",
  project="Awesome Project",
  year="2022"
)
```

## Methods

There are several other methods available in the API. These are called on the
`Lice` object you created.

### `get_license`

This method generates a license text based on the license name you provide. The
license name must be a valid (existing) license name. You can get a list of
valid license names using the `get_licenses` method.

```python
license_text = lice.get_license("mit")
print(license_text)
```

```pre
The MIT License (MIT)
Copyright (c) 2024 Grant Ramsay

Permission is hereby granted, free of charge, to any person obtaining a copy
...
```

If you provide an invalid license name, the method will raise a
`lice2.exceptions.LicenseNotFoundError` exception.

You can pass an optional `language` argument to the method to generate the
license text as a commented block in the specified language. This can be useful
for generating license headers in source code files. You can get a list of valid
languages using the `get_languages` method. Note that the value passed should be
the **file extension** of the language (ie 'py' for Python, 'js' for JavaScript
etc) exactly as you would from the CLI.

```python
license_text = lice.get_license("mit", language="py")
print(license_text)
```

```pre
# The MIT License (MIT)
# Copyright (c) 2024 Grant Ramsay
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
...
```

If you provide an invalid language name, the method will raise a
`lice2.exceptions.LanguageNotFoundError` exception.

### `get_header`

Return the header of the given license. This is a stripped-down version of the
license text that is suitable for use as a header in source code files.

If the language is specified, the header will be formatted as a commented block
for that language. If not, the header will be returned as a plain text block.

Note: Not all licenses have headers, if the license does not have a header, this
method will raise a `lice2.exceptions.HeaderNotFoundError` exception.

```python
header_text = lice.get_header("gpl3")
print(header_text)
```

```pre
lice2
Copyright (C) 2024  Grant Ramsay

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
...
```

As with the `get_license` method, you can pass an optional `language` argument
to the method to generate the header as a commented block in the specified
language.

```python
header_text = lice.get_header("gpl3", language="py")
print(header_text)
```

```pre
# lice2
# Copyright (C) 2024  Grant Ramsay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
...
```

### `get_licenses`

This method returns a Python `list` of valid license names that can be used with
the other methods. Uesful for generating a list of licenses to display to the
user.

!!! info
    This method will probably be upgraded in the future to return a 'Human
    Readable' item also.

```python
licenses = lice.get_licenses()
print(licenses)
```

```pre
['agpl3', 'apache', 'bsd2', 'bsd3', 'cc0', 'epl', 'gpl2', 'gpl3', ...]
```

### `get_languages`

This method returns a Python `list` of valid language names that can be used with
the other methods. Note that these are the standard **file extensions** for the
languages.

```python
languages = lice.get_languages()
print(languages)
```

```pre
['c', 'cpp', 'css', 'html', 'java', 'js', 'json', 'lua', 'py', ...]
```

## Exceptions

There are several exceptions that can be raised by the API methods. These are
all subclasses of `lice2.exceptions.LiceError`, and should be caught and
handled.

They can be imported from the `lice2.exceptions` module.

```python
from lice2.exceptions import LicenseNotFoundError
```

You can get the offending attribute value by appending it to the `value`
attribute of the exception object. For example, to get the license name that was
invalid, you would access the `<exception>.value.license_name`:

```python
try:
  license_text = lice.get_license("invalid")
except LicenseNotFoundError as exc:
  print(f"Invalid license name: {exc.value.license_name}")
```

### `LicenseNotFoundError`

Raised when the license name provided to the `get_license` method is not a valid
license name.

### `LanguageNotFoundError`

Raised when the language name provided to the `get_license` method is not a
valid language name.

### `HeaderNotFoundError`

Raised when the specified license does not have a header available.

### `InvalidYearError`

Raised when the year provided to the `Lice` constructor is not a valid year, ie
it is longer than 4 characters or cannot be converted to an integer.
