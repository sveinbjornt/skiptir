"""

skiptir: Hyphenate Icelandic text

Main hyphenation functionality.

"""

import re

from .const import (
    DEFAULT_DICTIONARY,
    DEFAULT_HYPHENATION_CHAR,
    DEFAULT_LEFT_MIN,
    DEFAULT_RIGHT_MIN,
)
from .pyphen import Pyphen

SOFT_HYPHEN = "\u00ad"

# A "word" is a maximal run of word characters (letters and digits). Matching
# these directly leaves every other character -- whitespace, punctuation,
# quotation marks -- untouched in the output, and keeps punctuation out of the
# hyphenator, where it would count towards the minimum syllable lengths and
# produce breaks such as '"-segj-a' or 'tal-a.'.
_WORD_RE = re.compile(r"\w+")

# The hyphenator is created on first use rather than at import time, so that
# importing skiptir does not pay for parsing the hyphenation dictionary.
# Races are harmless: Pyphen caches parsed dictionaries internally, so a
# redundant instance costs an object, not a second parse.
hyphenator = None


def _get_hyphenator() -> Pyphen:
    global hyphenator
    if hyphenator is None:
        hyphenator = Pyphen(
            lang=DEFAULT_DICTIONARY, left=DEFAULT_LEFT_MIN, right=DEFAULT_RIGHT_MIN
        )
    return hyphenator


# Hyphenates a string of text, preserving whitespace and punctuation intact.
# The hyphen character to be used can be specified (soft hyphen, U+00AD, by default).
def hyphenate(
    input_text: str,
    hyphen_character: str = DEFAULT_HYPHENATION_CHAR,
) -> str:
    hyph = _get_hyphenator()

    # Remove any pre-existing soft hyphens so that hyphenating already
    # hyphenated text is idempotent rather than inserting a second set.
    clean_input_text = input_text.replace(SOFT_HYPHEN, "")

    def hyphenate_word(match: "re.Match[str]") -> str:
        return hyph.inserted(match.group(), hyphen=hyphen_character)  # type: ignore[no-any-return]

    return _WORD_RE.sub(hyphenate_word, clean_input_text)
