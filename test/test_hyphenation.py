#!/usr/bin/env python3
"""
Tests for skiptir's Icelandic hyphenation.

The reference files (input.txt/output.txt) are a whole-text regression
snapshot, not an independently verified gold standard. Correctness claims
belong in the explicit unit tests below, which have hand-written expectations.
"""

import io
import re
import subprocess
import sys
from pathlib import Path

import pytest

from skiptir import DEFAULT_HYPHENATION_CHAR, hyphenate
from skiptir.cli import main as cli_main

TEST_DIR = Path(__file__).parent

# Cases where the bundled 2020 patterns disagree with the older hand-corrected
# reference list this fixture originally came from. Both are foreign proper
# nouns, and neither is fixable by tuning the minimum syllable lengths:
#   Kambodíu   -> "Kam-bó-d-íu"   (reference: "Kam-bó-díu")
#   khmeranna  -> "khm-er-anna"   (reference: "kh-mer-anna")
# They are kept in the fixture deliberately; deleting awkward input to make the
# suite pass is how the punctuation bug went unnoticed in the first place.


def test_hyphenation_against_reference():
    """Full-text regression check against the reference input/output files."""
    input_text = (TEST_DIR / "input.txt").read_text(encoding="utf-8")
    expected_output = (TEST_DIR / "output.txt").read_text(encoding="utf-8")

    # Hyphenate using a regular hyphen (not soft hyphen) to match reference output
    assert hyphenate(input_text, hyphen_character="-") == expected_output


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Surrounding punctuation must not reach the hyphenator, where it would
        # count towards the minimum syllable lengths.
        ('"segja"', '"segja"'),
        ("tala.", "tala."),
        ("sinni,", "sinni,"),
        ("(íslensk)", "(ís-lensk)"),
        ("„borgaralegir", "„borg-ara-leg-ir"),
        ("óvinir“,", "óvin-ir“,"),
        # A single-character first syllable is not acceptable in Icelandic.
        ("óvinir", "óvin-ir"),
        ("íbúa", "íbúa"),
        ("óhemjumargs", "óhemju-margs"),
        # Ordinary compounds still hyphenate.
        ("ríkisstjórnarinnar", "rík-is-stjórn-ar-inn-ar"),
        ("íslensk", "ís-lensk"),
        ("stjórnartíð", "stjórn-ar-tíð"),
        # Digits, short words and empty input are left alone.
        ("1998", "1998"),
        ("3.000.000", "3.000.000"),
        ("og", "og"),
        ("", ""),
    ],
)
def test_word_hyphenation(text, expected):
    assert hyphenate(text, hyphen_character="-") == expected


def test_whitespace_is_preserved_exactly():
    text = "  Þetta\ter\n\níslensk   setning.  \n"
    result = hyphenate(text, hyphen_character="-")
    assert re.sub(r"-", "", result) == text
    assert result == "  Þetta\ter\n\nís-lensk   setn-ing.  \n"


def test_default_hyphen_is_soft_hyphen():
    result = hyphenate("íslensk")
    assert result == "ís" + DEFAULT_HYPHENATION_CHAR + "lensk"
    assert DEFAULT_HYPHENATION_CHAR == "\u00ad"


def test_hyphenation_is_idempotent():
    """Re-hyphenating already hyphenated text must not insert a second set."""
    once = hyphenate("Þetta er íslensk setning.")
    assert hyphenate(once) == once

    # Pre-existing soft hyphens are stripped even when a visible hyphen is used.
    assert hyphenate("ís\u00adlensk", hyphen_character="-") == "ís-lensk"


def test_no_hyphen_adjacent_to_punctuation():
    """Invariant: a break is never offered next to a non-word character.

    This is the regression guard for the bug that produced '"-segj-a' and
    'tal-a.' -- it holds over the whole reference text, not just the cases
    that happen to be enumerated above.
    """
    text = (TEST_DIR / "input.txt").read_text(encoding="utf-8")
    result = hyphenate(text, hyphen_character="\u00ad")

    for match in re.finditer("\u00ad", result):
        before = result[match.start() - 1]
        after = result[match.end()]
        assert before.isalnum(), f"hyphen after {before!r} in {result[match.start()-12:match.end()+12]!r}"
        assert after.isalnum(), f"hyphen before {after!r} in {result[match.start()-12:match.end()+12]!r}"


def run_cli(monkeypatch, capsys, argv, stdin_text="Þetta er íslensk setning."):
    """Invoke the CLI entry point in-process and return (exit code, stdout, stderr)."""
    monkeypatch.setattr(sys, "argv", ["skiptir", *argv])
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin_text))
    try:
        code = cli_main()
    except SystemExit as e:  # --help, --version and argparse errors
        code = e.code
    captured = capsys.readouterr()
    return code, captured.out, captured.err


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["--hyphen", "-"], "Þetta er ís-lensk setn-ing."),
        ([], "Þetta er ís\u00adlensk setn\u00ading."),
    ],
)
def test_cli_hyphenates_stdin(monkeypatch, capsys, argv, expected):
    code, out, _ = run_cli(monkeypatch, capsys, argv)
    assert code == 0
    assert out == expected


def test_cli_reports_version(monkeypatch, capsys):
    code, out, _ = run_cli(monkeypatch, capsys, ["--version"])
    assert code == 0
    assert out.startswith("skiptir ")


def test_unknown_argument_is_rejected(monkeypatch, capsys):
    """--mode was removed in 2.0.0 and must not be silently accepted."""
    code, _, err = run_cli(monkeypatch, capsys, ["--mode", "pattern"])
    assert code != 0
    assert "unrecognized arguments" in err


def test_cli_reports_invalid_utf8_cleanly(monkeypatch, capsys):
    class UndecodableStdin:
        def read(self):
            raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")

    monkeypatch.setattr(sys, "argv", ["skiptir"])
    monkeypatch.setattr(sys, "stdin", UndecodableStdin())
    with pytest.raises(SystemExit) as excinfo:
        cli_main()
    assert excinfo.value.code == 1
    err = capsys.readouterr().err
    assert "not valid UTF-8" in err
    assert "Traceback" not in err


def test_cli_entry_point_end_to_end():
    """Smoke test that the installed module actually runs as a program."""
    result = subprocess.run(
        [sys.executable, "-m", "skiptir.cli", "--hyphen", "-"],
        input="Þetta er íslensk setning.",
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "Þetta er ís-lensk setn-ing."
