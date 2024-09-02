# Future Ideas for the project

<!-- - All improvements and ideas I have had so far have been implemented in the -->
<!--   project. I'm always open to new ideas and improvements, so if you have any -->
<!--   suggestions, please let me know. -->
- add a GUI for the license generation (use Textual for this). This would be
  accessed through a CLI option or a config file setting.
- add an option to list licenses that have a header available. Maybe this could
  be done with a `--list-headers` option or `--headers --list`.
- add a 'human readable' value to the internal LICENSES list so we can display
  the license name in a more human readable format. This would be especially
  useful for the `--licenses` option and the API. The issue is that this
  variable is dynamically generated from the license files, so having a human
  readable value would be difficult to maintain.
