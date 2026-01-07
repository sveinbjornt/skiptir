"""

skiptir: Hyphenate Icelandic text

Main hyphenation functionality.

"""

from typing import Optional

import re
from .pyphen import Pyphen

from .const import DEFAULT_HYPHENATION_CHAR, DEFAULT_HYPHENATION_MODE


# prepare the Pyphen hyphenator object
# (includes loading hyphenation dictionary from file)
hyphenator = Pyphen(lang="is_2020_alpha2_extra", left=1, right=2)


# Hyphenates a string of text, preserving its whitespace intact.
# The hyphenation mode can be specified as well as the particular
# hyphen character to be used (soft hyphen, U+00AD, by default).
def hyphenate(
    input_text: str,
    hyphenation_mode: Optional[str] = DEFAULT_HYPHENATION_MODE,
    hyphen_character: str = DEFAULT_HYPHENATION_CHAR,
):
    if hyphenation_mode is None:
        hyphenation_mode = DEFAULT_HYPHENATION_MODE
    if hyphenation_mode is not DEFAULT_HYPHENATION_MODE:
        raise Exception(f"Unsupported hyphenation mode: {hyphenation_mode}")

    output_text = ""

    # list for separated words and strings of whitespace from the input
    # guaranteed to return the first string as '' or whitespace
    words_and_whitespace: list[str] = re.split(r"(\S+)", input_text)

    # corresponding list for the hyphenated output
    hyphenated_words_and_whitespace: list[str] = []
    # first string will be whitespace (or an empty string)
    is_space = True

    for item in words_and_whitespace:
        if is_space:
            # add the spaces directly to the output
            hyphenated_words_and_whitespace.append(item)
            # the next item will not be whitespace
            is_space = False
        else:  # i.e. if it's a word
            # hyphenate the word (note that the hyphen is a soft hyphen (U+00AD))
            hyphenated_words_and_whitespace.append(
                hyphenator.inserted(item, hyphen=hyphen_character)  # type: ignore
            )
            # the next item will be whitespace
            is_space = True

    output_text = "".join(hyphenated_words_and_whitespace)

    return output_text
