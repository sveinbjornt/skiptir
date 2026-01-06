"""

skiptir: Hyphenate Icelandic text

"""

import importlib.metadata

__author__ = "Sveinbjorn Thordarson"
__copyright__ = "(C) 2026 Sveinbjorn Thordarson"
__version__ = importlib.metadata.version("skiptir")

from .const import DEFAULT_HYPHENATION_CHAR, DEFAULT_HYPHENATION_MODE
from .skiptir import hyphenate

__all__ = ["hyphenate", "DEFAULT_HYPHENATION_CHAR", "DEFAULT_HYPHENATION_MODE"]
