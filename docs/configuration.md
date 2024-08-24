# Configuration

There is an optional configuration file that can be used to customize some of
the application defaults. This is a TOML file that should be named `config.toml`
and placed in the `lice` subdirectory of the appliciable configuration directory
for your operating system. Generally this is `$HOME/.config/` on all operating
systems.

So for example, on a Linux or Mac system, the configuration file would be
located at `$HOME/.config/lice/config.toml`.

The TOML file should look like this:

```toml
[lice]
default_license = "mit"
organization = "Your Organization"
```

Currently there are only two options that can be set:

- `default_license` - This is the default license that will be used if no
  license is specified on the command line.
- `organization` - This is the organization name that will be used in the
  license by default. If this is set, it will not try to get the organization
  name from `git config` or the `$USER` environment variable.
