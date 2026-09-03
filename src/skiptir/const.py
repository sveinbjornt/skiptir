"""

skiptir: Hyphenate Icelandic text

Constants used in skiptir.

"""

DEFAULT_HYPHENATION_CHAR = "\u00ad"  # soft hyphen

# Hyphenation dictionary used by default. The bundled dictionaries all declare
# LEFTHYPHENMIN 1, but a single-character first syllable (e.g. "ó-vinir") is not
# acceptable in Icelandic typography, so we require two.
DEFAULT_DICTIONARY = "is_2020_alpha2_extra"
DEFAULT_LEFT_MIN = 2
DEFAULT_RIGHT_MIN = 2
