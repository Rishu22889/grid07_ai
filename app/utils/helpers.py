# Helper functions
# app/utils/helpers.py

import json
import textwrap
from typing import Any
 
 
def print_section(title: str) -> None:
    """Print a prominently formatted section header."""
    bar = "═" * (len(title) + 4)
    print(f"\n╔{bar}╗")
    print(f"║  {title}  ║")
    print(f"╚{bar}╝\n")
 
 
def print_table_row(*cols: str, widths: tuple[int, ...] = (12, 22, 10, 7)) -> None:
    """Print a simple fixed-width table row."""
    padded = []
    for i, col in enumerate(cols):
        w = widths[i] if i < len(widths) else 12
        padded.append(str(col).ljust(w))
    print("  " + " ".join(padded))
 
 
def pretty_json(obj: Any) -> str:
    """Return a pretty-printed JSON string for any serialisable object."""
    return json.dumps(obj, indent=2, ensure_ascii=False)
 
 
def wrap_text(text: str, width: int = 80, indent: str = "  ") -> str:
    """Wrap text to a given width with a leading indent."""
    return textwrap.fill(text, width=width, initial_indent=indent, subsequent_indent=indent)
 
 
def truncate(text: str, max_len: int = 280) -> str:
    """Hard-truncate text to max_len characters."""
    return text if len(text) <= max_len else text[: max_len - 1] + "…"
 