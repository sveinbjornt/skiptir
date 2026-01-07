[![license](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![release](https://shields.io/github/v/release/sveinbjornt/skiptir?display_name=tag)](https://github.com/sveinbjornt/skiptir/releases)
[![PyPI](https://img.shields.io/pypi/v/skiptir)](https://pypi.org/project/skiptir/)
[![build](https://github.com/sveinbjornt/skiptir/actions/workflows/python-app.yml/badge.svg)](https://github.com/sveinbjornt/skiptir/actions)

# skiptir

`skiptir` is a Python package to hyphenate Icelandic text.
Requires Python 3.9 or later.

## Installation

You can install `skiptir` via `pip`:

```bash
pip install skiptir
```

## Usage

```python
from skiptir import hyphenate

hyphenate("Þetta er íslensk setning.", hyphen="-")
'Þetta er ís-lensk setn-ing.'
```

Command line tool usage:

```bash
skiptir [--mode MODE] [--hyphen HYPHEN]
```

The tool reads text from standard input and prints the
hyphenated result to standard output, e.g.:

```bash
echo "Þetta er íslensk setning." | skiptir --hyphen "-"
Þetta er ís-lensk setn-ing.
```

MODE is `pattern` by default, which means using Pyphen
with the latest Icelandic hyphenation patterns.
Other modes are not supported yet.

HYPHEN refers to a custom hyphenation character, e.g. `·` or `-`.
By default, `skiptir` uses the invisible soft hyphen character (`U+00AD`).

## Version History

* 1.0.0 (2026-01-07): Initial package release.

## License

(c) Copyright 2026 [Sveinbjörn Þórðarson](mailto:sveinbjorn@sveinbjorn.org)  
(c) Copyright 2020 [Kristján Rúnarsson](mailto:krunars@gmail.com)

The program files are licensed under the Apache License, Version 2.0
(the "License"); you may not use the files except in compliance with
the License or with another license under which they are also licensed
according to this file or another written declaration by the author.
[You may obtain a copy of the License here](https://www.apache.org/licenses/LICENSE-2.0).

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Acknowledgements

The basic funcionality in this package is based on work by Kristján
Rúnarsson, who originally developed it under the auspices of the
Icelandic Government's Language Technology Program (2016-2019).

The package includes a modified version of the Pyphen library by
Wilbert Berendsen and Guillaume Ayoub, which is licensed under the
GNU LGPL 2.1 or later. See the file `src/skiptir/pyphen/COPYING.LGPL`
for details.
