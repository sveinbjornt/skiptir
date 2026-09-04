# Icelandic hyphenation pattern dictionaries

These are Hunspell-format hyphenation pattern files (`hyph_*.dic`) for
Icelandic, produced by [Kristján Rúnarsson](https://github.com/krunars) under
the auspices of the Icelandic Government's
[Language Technology Program](https://clarin.is/media/uploads/mlt-en.pdf)
(2018-2022), and redistributed here with the rest of `skiptir`.

| File | Contents |
| --- | --- |
| `hyph_is_2020_alpha2_extra.dic` | 2020 patterns, extended. **Used by default.** |
| `hyph_is_2020_alpha.dic` | 2020 patterns, earlier alpha revision. |
| `hyph_is_1985_corrected.dic` | Patterns for the 1985 orthographic rules, corrected. |
| `hyph_is_1985_unchanged_list.dic` | Patterns for the 1985 rules, uncorrected. |
| `hyph_is_JPind_1988.dic` | Patterns by Jón Þ. Þórhallsson (1988). |
| `hyph_is.dic` | Generic fallback, resolved for the bare `is` language code. |

Only `hyph_is_2020_alpha2_extra` is selected by `skiptir` (see
`DEFAULT_DICTIONARY` in `src/skiptir/const.py`). The others are retained
because they document successive states of Icelandic hyphenation practice and
are useful for comparison; they add roughly 470 KB to the installed package.

Note that every file declares `LEFTHYPHENMIN 1` and `RIGHTHYPHENMIN 2`. Pyphen
skips those directives when parsing, so `skiptir` passes the same values
explicitly (`DEFAULT_LEFT_MIN` / `DEFAULT_RIGHT_MIN` in `src/skiptir/const.py`).
They match Icelandic orthography as set out in Ritreglur: a single-letter first
part is permitted (`ó-lán`, `á-stríða`, `í-hlut-un`), but a single letter must
never be carried over to the next line, so `karf-a` is wrong.
