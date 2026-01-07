#!/usr/bin/env python3
"""
Test hyphenation patterns against a hand-corrected standard hyphenation list.
Adapted from a script by Kristján Rúnarsson (krunars@gmail.com).
"""

from pathlib import Path

from skiptir import hyphenate


def test_hyphenation_against_reference():
    """Test hyphenation by comparing against reference input/output files."""
    test_dir = Path(__file__).parent
    input_file = test_dir / "input.txt"
    output_file = test_dir / "output.txt"

    # Read input text
    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    # Read expected output
    with open(output_file, "r", encoding="utf-8") as f:
        expected_output = f.read()

    # Hyphenate using regular hyphen (not soft hyphen) to match reference output
    actual_output = hyphenate(input_text, hyphen_character="-")

    # Compare results
    assert actual_output == expected_output, "Hyphenation output does not match expected output"
