#!/usr/bin/env python3
"""one-emoji-smile: write exactly one emoji to /output/entry.txt.

The emoji is the heart-hands gesture: two hands shaping a heart,
offered to whoever sees it. It is the warmest single character a
stranger can receive with no words attached -- a small, deliberate
gift rather than the first smiley that comes to mind. It reads the
same way at any age and in any place: kindness, offered openly,
with no joke, no irony and nothing asked in return.

Standard library only, no network. Deterministic: the same bytes
on every run.
"""

import os
import sys

# The entry: one emoji, one code point, four UTF-8 bytes.
# Heart hands (U+1FAF6): a gesture of warmth made with both hands,
# chosen over the default smileys because a shaped heart is an act --
# something offered -- while a face only shows a mood.
EMOJI = "\U0001faf6"

MIN_LEN = 1
MAX_LEN = 8


def problems(text: str) -> list:
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        found.append(f"entry is {len(text)} characters, must be {MIN_LEN}-{MAX_LEN}")
    if not text.strip():
        found.append("entry must not be only white space")
    if text != text.strip():
        found.append("entry must not start or end with white space")
    if len(text) != 1:
        found.append("entry must be exactly one emoji")
    return found


def main() -> int:
    text = EMOJI
    bad = problems(text)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # chmod is best-effort: in the grading sandbox /output is a root-owned
    # directory, so a failed chmod must never fail the run.
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    written = open(path, "rb").read()
    if written != text.encode("utf-8"):
        print("wrote back bytes do not match entry", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} character")
    return 0


if __name__ == "__main__":
    sys.exit(main())
