#!/usr/bin/env python3
"""

skiptir: Hyphenate Icelandic text

Command line interface.

"""

from . import __version__ as program_version


def main():
    """Hyphenates text from standard input and prints the result
    to standard output."""

    import argparse
    import sys

    from .const import DEFAULT_HYPHENATION_CHAR
    from .skiptir import hyphenate

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--hyphen",
        default=DEFAULT_HYPHENATION_CHAR,
        help="Hyphen character to use (default: soft hyphen, U+00AD)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=program_version,
        help="Show program version and exit",
    )
    args = parser.parse_args()

    input_text = sys.stdin.read()
    print(hyphenate(input_text, hyphen_character=args.hyphen), end="")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
