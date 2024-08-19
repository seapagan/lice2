# Changelog

## Changelog from the original 'lice' project

2013-08-23 Alessandro Cresto Miseroglio <alex179ohm@gmail.com>

* core.py Unicode fixed (python 2.7 and 3.3 tested)

2013-08-23 Alessandro Cresto Miseroglio <alex179ohm@gmail.com>

* core.py File name for a source file was added.
   main (parser.add_argument [135]) -f (ofile) argument added

2013-08-22 Alessandro Cresto Miseroglio <alex179ohm@gmail.com>

* core.py (lice) Formatted output for source file programs
   was added.
      languages implemented  "lua, py, c, cc, pl, rb, sh, txt"
   load_file_template (template) If template is StringIO, unicode
    is supported in native mode (both 2.7[maibe] and 3.3)
   load_package_template (content) StringIO support added
    content.decode("utf-8") was removed
   main (parser.add_argument [133]) -l (language) argument added
   [20..24] LANGS and LANG_CMT added.

* test.py  some tests was changed (maibe become unnecessary)
   test_file_template [31] assertEqual changed in assertNotEqual
   test_package_template [39] assertEqual changed in assertNotEqual

## Release notes from the original README

**0.6**

* Add PowerShell support (thanks to `danijeljw <https://github.com/danijeljw>`_)
* Add Rust support (thanks to `alex179ohm <https://github.com/alex179ohm>`_)
* Bugfixes (thanks to `ganziqim <https://github.com/ganziqim>`_)
* Added support for Python 3.7 and 3.8, removed support for Python 3.4

Tested against Python 2.7, 3.5, 3.6, 3.7, and 3.8.

**0.5**

* Add support for SCM alias for lisp-style comments (thanks to `ejmr <https://github.com/ejmr>`_)
* Additional support for WTFPL and GPL2 licenses (thanks to `ejmr <https://github.com/ejmr>`_)
* Support for Python 3.4 and 3.5 (thanks to `ejmr <https://github.com/ejmr>`_)

**0.4**

* Use ASCII instead of Unicode for templates (thanks to `tabletcorry <https://github.com/tabletcorry>`_)
* Add Academic Free License ("AFL") v. 3.0 (thanks to `brianray <https://github.com/brianray>`_)
* Add ISC (thanks to `masklinn <https://github.com/masklinn>`_)
* Add tox support for testing (thanks to `lukaszb <https://github.com/lukaszb>`_)
* Show defaults when listing template variables

**0.3**

* Generate source file headers for some liceneses
* Discover available licenses at runtime
* Use getpass module for retrieving username
* Better unicode support for Python 3 (thanks to `astagi <https://github.com/astagi>`_)
* Add Creative Commons licenese (thanks to `rjnienaber <https://github.com/rjnienaber>`_)

**0.2**

* Add AGPL 3 license
* Add extra templates variables to GPL 2 and 3

**0.1**

* Initial release

## Generated CHANGELOG from the original project repository

**Closed Issues**

* LICENSE-2.0 ([#56](https://github.com/licenses/lice/issues/56)) by [jcarbaugh](https://github.com/jcarbaugh)
* Two bugs ([#48](https://github.com/licenses/lice/issues/48)) by [ganziqim](https://github.com/ganziqim)
* WTFPL copyright notice and source header ([#46](https://github.com/licenses/lice/issues/46)) by [ejmr](https://github.com/ejmr)
* Don't render the boilerplate in the license template. ([#44](https://github.com/licenses/lice/issues/44)) by [ejmr](https://github.com/ejmr)
* Upgrade Creative Commons License to version 4.0 ([#43](https://github.com/licenses/lice/issues/43)) by [rgaiacs](https://github.com/rgaiacs)
* Not supporting Python 3.4 ([#38](https://github.com/licenses/lice/issues/38)) by [jiegec](https://github.com/jiegec)
* Experimental support of license-templates as template source. ([#30](https://github.com/licenses/lice/issues/30)) by [ejmr](https://github.com/ejmr)
* Print list of available styles ([#29](https://github.com/licenses/lice/issues/29)) by [jcarbaugh](https://github.com/jcarbaugh)
* Infer language only on the basis of file extension ([#27](https://github.com/licenses/lice/issues/27)) by [Yonaba](https://github.com/Yonaba)
* Existing file ([#26](https://github.com/licenses/lice/issues/26)) by [ejmr](https://github.com/ejmr)
* TypeError under Python 3 ([#17](https://github.com/licenses/lice/issues/17)) by [jcarbaugh](https://github.com/jcarbaugh)
* Error thrown on "subprocess.check_output('git config --get user.name'.split())" ([#8](https://github.com/licenses/lice/issues/8)) by [jcarbaugh](https://github.com/jcarbaugh)
* Additional licenses e.g. Creative Commons, OSI-approved licenses. ([#7](https://github.com/licenses/lice/issues/7)) by [jcarbaugh](https://github.com/jcarbaugh)
* Use non-newlined license files ([#5](https://github.com/licenses/lice/issues/5)) by [jcarbaugh](https://github.com/jcarbaugh)
* In-file Apache/GNU/MPL headers ([#2](https://github.com/licenses/lice/issues/2)) by [jcarbaugh](https://github.com/jcarbaugh)
* Affero GPL ([#1](https://github.com/licenses/lice/issues/1)) by [jcarbaugh](https://github.com/jcarbaugh)

**Merged Pull Requests**

* Add PowerShell language ([#53](https://github.com/licenses/lice/pull/53)) by [danijeljw](https://github.com/danijeljw)
* Add rust programming language ([#52](https://github.com/licenses/lice/pull/52)) by [alex179ohm](https://github.com/alex179ohm)
* Fix: issue #48 ([#49](https://github.com/licenses/lice/pull/49)) by [ganziqim](https://github.com/ganziqim)
* [Feature] Add `scm` as an acceptable value for `--language` ([#45](https://github.com/licenses/lice/pull/45)) by [ejmr](https://github.com/ejmr)
* Pep8 check ([#42](https://github.com/licenses/lice/pull/42)) by [lord63](https://github.com/lord63)
* Add --licenses flag to list all licenses/vars ([#37](https://github.com/licenses/lice/pull/37)) by [relrod](https://github.com/relrod)
* More languages ([#36](https://github.com/licenses/lice/pull/36)) by [relrod](https://github.com/relrod)
* Fixed launch-time error ([#35](https://github.com/licenses/lice/pull/35)) by [smcquay](https://github.com/smcquay)
* Ignore .tox dir ([#34](https://github.com/licenses/lice/pull/34)) by [bsdlp](https://github.com/bsdlp)
* Removed default txt file extension ([#33](https://github.com/licenses/lice/pull/33)) by [alex179ohm](https://github.com/alex179ohm)
* Incorporating license-templates package support ([#32](https://github.com/licenses/lice/pull/32)) by [ghost](https://github.com/ghost)
* Resume ([#25](https://github.com/licenses/lice/pull/25)) by [alex179ohm](https://github.com/alex179ohm)
* Docs updated ([#24](https://github.com/licenses/lice/pull/24)) by [alex179ohm](https://github.com/alex179ohm)
* Tests fixed ([#23](https://github.com/licenses/lice/pull/23)) by [alex179ohm](https://github.com/alex179ohm)
* Langs ([#22](https://github.com/licenses/lice/pull/22)) by [alex179ohm](https://github.com/alex179ohm)
* Added source file languages output format and file output redirect ([#21](https://github.com/licenses/lice/pull/21)) by [alex179ohm](https://github.com/alex179ohm)
* Fixes to template-cc0. ([#20](https://github.com/licenses/lice/pull/20)) by [ghost](https://github.com/ghost)
* Fix runtime error when running with python 3 ([#19](https://github.com/licenses/lice/pull/19)) by [ISF](https://github.com/ISF)
* Added tox and updated setup.py ([#18](https://github.com/licenses/lice/pull/18)) by [lukaszb](https://github.com/lukaszb)
* ISC license ([#16](https://github.com/licenses/lice/pull/16)) by [masklinn](https://github.com/masklinn)
* AFL v. 3.0 ([#15](https://github.com/licenses/lice/pull/15)) by [brianray](https://github.com/brianray)
* Replace unicode license text with ASCII ([#14](https://github.com/licenses/lice/pull/14)) by [tabletcorry](https://github.com/tabletcorry)
* Added Creative Commons licences. ([#13](https://github.com/licenses/lice/pull/13)) by [rjnienaber](https://github.com/rjnienaber)
* Added python3 compatibility ([#12](https://github.com/licenses/lice/pull/12)) by [astagi](https://github.com/astagi)
* Added the zlib License ([#11](https://github.com/licenses/lice/pull/11)) by [astagi](https://github.com/astagi)
* Added the WTFPL License ([#10](https://github.com/licenses/lice/pull/10)) by [aaronbassett](https://github.com/aaronbassett)
* Failure on Windows when getting default user ([#6](https://github.com/licenses/lice/pull/6)) by [rjnienaber](https://github.com/rjnienaber)
* Previously discussed changes ([#3](https://github.com/licenses/lice/pull/3)) by [JNRowe](https://github.com/JNRowe)

---
*This changelog was generated using [github-changelog-md](http://changelog.seapagan.net/) by [Seapagan](https://github.com/seapagan)*
