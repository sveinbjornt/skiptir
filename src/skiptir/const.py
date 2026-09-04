"""

skiptir: Hyphenate Icelandic text

Constants used in skiptir.

"""

DEFAULT_HYPHENATION_CHAR = "\u00ad"  # soft hyphen

# Hyphenation dictionary used by default.
DEFAULT_DICTIONARY = "is_2020_alpha2_extra"

# Minimum length of the first and last part of a hyphenated word. Icelandic
# orthography (Ritreglur, Árni Magnússon Institute for Icelandic Studies)
# explicitly permits a single-letter first part -- the official examples include
# "ó-lán", "á-stríða" and "í-hlut-un" -- but forbids carrying a single letter
# over to the next line, so "karf-a" is wrong. Hence 1 and 2, matching the
# LEFTHYPHENMIN/RIGHTHYPHENMIN directives declared by the bundled dictionaries
# (which Pyphen itself ignores).
DEFAULT_LEFT_MIN = 1
DEFAULT_RIGHT_MIN = 2
