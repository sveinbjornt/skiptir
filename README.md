[![license](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![release](https://shields.io/github/v/release/sveinbjornt/skiptir?display_name=tag)](https://github.com/sveinbjornt/skiptir/releases)
[![PyPI](https://img.shields.io/pypi/v/skiptir)](https://pypi.org/project/skiptir/)
[![build](https://github.com/sveinbjornt/skiptir/actions/workflows/python-app.yml/badge.svg)](https://github.com/sveinbjornt/skiptir/actions)

# skiptir

`skiptir` is a Python package to hyphenate **Icelandic text**.
Requires Python 3.10 or later.

## Installation

You can install `skiptir` via `pip`:

```bash
pip install skiptir
```

## Usage

```python
from skiptir import hyphenate

hyphenate("Þetta er íslensk setning.", hyphen_character="-")
'Þetta er ís-lensk setn-ing.'
```

Command line tool usage:

```bash
skiptir [--hyphen HYPHEN]
```

The tool reads text from standard input and prints the
hyphenated result to standard output, e.g.:

```bash
echo "Þetta er íslensk setning." | skiptir --hyphen "-"
Þetta er ís-lensk setn-ing.
```

The `--hyphen` flag allows you to specify a custom hyphenation character,
e.g. `·` or `-`. By default, `skiptir` uses the invisible soft hyphen
character (`U+00AD`).

Whitespace and punctuation are preserved exactly, and only runs of
letters and digits are hyphenated, so quotation marks and sentence-final
punctuation cannot produce a break next to them. Any soft hyphens already
present in the input are removed first, which makes hyphenating the same
text twice a no-op.

Break positions follow Icelandic orthography as set out in
[Ritreglur](https://ritreglur.arnastofnun.is/): the first part of a broken
word may be a single letter (`ó-lán`, `í-hlut-un`), but a single letter is
never carried over to the next line (so `karfa` is not broken as `karf-a`).

## Version History

* 2.0.0 (2026-09-04): Major refactoring and API change.
  * Removed the unused `hyphenation_mode` parameter of `hyphenate()`
    and the corresponding `--mode` command line flag. This may break code
    that uses the old API.
  * Fixed issues where punctuation could be treated as part of a word.
  * Hyphenation is now idempotent. Existing soft hyphens are stripped first.
  * The hyphenation dictionary is now lazy-loaded.
  * Added `--version` flag to CLI.
  * Invalid UTF-8 input is now handled more gracefully.
  * Now requires Python 3.10 or later.
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

The distributed package additionally contains a vendored copy of Pyphen
(see Acknowledgements), which is licensed separately. The package metadata
therefore declares the combined expression
`Apache-2.0 AND LGPL-2.1-or-later`.

## Acknowledgements

The basic functionality in this package is based on work by
[Kristján Rúnarsson](https://github.com/krunars), who originally
developed it under the auspices of the Icelandic Government's
[Language Technology Program](https://clarin.is/media/uploads/mlt-en.pdf)
(2018-2022). The bundled hyphenation pattern dictionaries in
`src/skiptir/pyphen/dictionaries/` originate from that work. See the
`README.md` in that directory for their provenance.

The package includes a modified version of the
[Pyphen](https://github.com/Kozea/Pyphen) library by
Wilbert Berendsen and Guillaume Ayoub, which is licensed under the
GNU LGPL 2.1 or later. See the file `src/skiptir/pyphen/COPYING.LGPL`
for details. Modifications made for `skiptir` are marked in the source
with a `Local modification (skiptir)` comment.
