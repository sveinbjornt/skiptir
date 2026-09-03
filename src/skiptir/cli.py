#!/usr/bin/env python3
"""

skiptir: Hyphenate Icelandic text

Command line interface.

"""

import sys

from . import __version__ as program_version


def main() -> int:
    """Hyphenates text from standard input and prints the result
    to standard output."""

    import argparse

    from .const import DEFAULT_HYPHENATION_CHAR
    from .skiptir import hyphenate

    parser = argparse.ArgumentParser(
        prog="skiptir",
        description="Hyphenate Icelandic text read from standard input.",
    )
    parser.add_argument(
        "--hyphen",
        default=DEFAULT_HYPHENATION_CHAR,
        help="Hyphen character to use (default: soft hyphen, U+00AD)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {program_version}",
        help="Show program version and exit",
    )
    args = parser.parse_args()

    try:
        input_text = sys.stdin.read()
    except UnicodeDecodeError as e:
        parser.exit(1, f"{parser.prog}: error: input is not valid UTF-8 text: {e}\n")

    try:
        sys.stdout.write(hyphenate(input_text, hyphen_character=args.hyphen))
        sys.stdout.flush()
    except BrokenPipeError:  # pragma: no cover
        # Downstream closed the pipe (e.g. `skiptir | head`). Suppress the
        # secondary error Python prints at shutdown and exit quietly.
        sys.stderr.close()
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
