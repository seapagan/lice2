# Overview

'Lice' is able to generate license files to stdout (the default) or to a file.

It can also generate reduced 'headers' for longer licenses and format the output
for specific coding languages, optionally saving the output to a file with the
correct extension.

## Example Usage

Generate a BSD-3 license, the default

```console
$ lice
Copyright (c) 2013, Jeremy Carbaugh

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
...
```

Generate an MIT license

```console
$ lice mit
The MIT License (MIT)
Copyright (c) 2013 Jeremy Carbaugh

Permission is hereby granted, free of charge, to any person obtaining a copy
...
```

Generate a BSD-3 license, specifying the year and organization to be used

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

If organization is not specified, lice will first attempt to take it from the
config file (if it exists) then use `git config` to find your name. If not
found, it will use the value of the $USER environment variable. If the project
name is not specified, the name of the current directory is used. Year will
default to the current year.

You can see what variables are available to you for any of the licenses:

```console
$ lice --vars mit
The mit license template contains the following variables:
  year
  organization
```

## Integrating into your own project

You can integrate lice in your own project to generate licenses. Here is an
example:

```python
from lice2.api import Lice

lice = Lice(organization="Awesome Organization", project="Awesome Project")
license_text = lice.get_license("mit")
print(license_text)
```

There are a few more methods available in the API, see the
[Integration](integration.md) page for more information.

## I want XXXXXXXXX license in here!

Great! Is it a license that is commonly used? If so, open an issue or, if you
are feeling generous, fork and submit a pull request.
