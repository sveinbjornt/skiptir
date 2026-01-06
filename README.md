[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Release](https://shields.io/github/v/release/sveinbjornt/skiptir?display_name=tag)](https://github.com/sveinbjornt/skiptir/releases)
[![PyPI](https://img.shields.io/pypi/v/skiptir)](https://pypi.org/project/skiptir/)
[![Build](https://github.com/sveinbjornt/skiptir/actions/workflows/python-app.yml/badge.svg)](https://github.com/sveinbjornt/skiptir/actions)

# skiptir

`skiptir` is a Python package to hyphenate Icelandic text.
Requires Python 3.9 or later.

## Installation

You can install `skiptir` via pip:

```bash
pip install skiptir
```

## Usage

```python
TBD
```

Command line tool usage:

```bash
skiptir [--mode MODE] [--hyphen HYPHEN]
```

The tool reads text from standard input and prints the
hyphenated result to standard output.

MODE is 'pattern' by default, which means using Pyphen
with the latest Icelandic hyphenation patterns.
Other modes are not supported yet.

HYPHEN refers to a custom hyphenation character, e.g. · or -.
By default, the program uses the soft hyphen character (U+00AD).

## Version History

TBD

## License

TBD
