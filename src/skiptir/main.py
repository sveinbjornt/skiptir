#!/usr/bin/env python3
"""

skiptir: Hyphenate Icelandic text

"""


def main():
    """Hyphenates text from standard input and prints the result
    to standard output."""

    import argparse
    import sys

    from .const import DEFAULT_HYPHENATION_CHAR, DEFAULT_HYPHENATION_MODE
    from .skiptir import hyphenate

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default=DEFAULT_HYPHENATION_MODE)
    parser.add_argument("--hyphen", default=DEFAULT_HYPHENATION_CHAR)
    args = parser.parse_args()

    input_text = sys.stdin.read()
    print(hyphenate(input_text, hyphenation_mode=args.mode, hyphen_character=args.hyphen), end="")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
