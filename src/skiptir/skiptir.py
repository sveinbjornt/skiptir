"""

skiptir: Hyphenate Icelandic text

Main hyphenation functionality.

"""

import re
from .pyphen import Pyphen

from .const import DEFAULT_HYPHENATION_CHAR


hyphenator = None


# Hyphenates a string of text, preserving its whitespace intact.
# Hyphen character to be used can be specified (soft hyphen, U+00AD, by default).
def hyphenate(
    input_text: str,
    hyphen_character: str = DEFAULT_HYPHENATION_CHAR,
    hyphenation_mode: str = "",
) -> str:
    # Lazy-load the hyphenator object, so that it is only created when needed.
    global hyphenator
    if not hyphenator:
        hyphenator = Pyphen(lang="is_2020_alpha2_extra", left=1, right=2)

    output_text = ""

    clean_input_text = input_text.replace("\u00ad", "")  # remove any existing soft hyphens

    # list for separated words and strings of whitespace from the input
    # guaranteed to return the first string as '' or whitespace
    words_and_whitespace: list[str] = re.split(r"(\S+)", clean_input_text)

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
