"""

skiptir: Hyphenate Icelandic text

"""

import importlib.metadata

__author__ = "Sveinbjorn Thordarson"
__copyright__ = "(C) 2026 Sveinbjorn Thordarson"

try:
    __version__ = importlib.metadata.version("skiptir")
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    # Running from a source tree without the package being installed.
    __version__ = "unknown"

from .const import DEFAULT_HYPHENATION_CHAR
from .skiptir import hyphenate

__all__ = ["DEFAULT_HYPHENATION_CHAR", "hyphenate"]
