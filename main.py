"""The Robot Apology — make.fun entry (u-suga-the-robot-apology-dd96bb59).

Writes one two-line robot confession to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure stdlib (os only).

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1 to 400
characters, not only white space. validate() enforces that gate plus
the entry shape: exactly two lines, one sentence each.
"""

import os

LINE_ONE = (
    "I'm sorry I charged your toothbrush all night and left your phone "
    "at 2%, because both chargers look the same in the dark."
)

LINE_TWO = (
    "I have learned to label each charger by the thing it feeds and to "
    "check the screen, not the cable, before I walk away."
)

OUTPUT_FILENAME = "entry.txt"
MAX_CHARS = 400


def build_text():
    """Return the entry text: two lines, one sentence each."""
    return LINE_ONE + "\n" + LINE_TWO + "\n"


def validate(text):
    """Enforce the RULES.txt gate and the two-line shape."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1 to 400 characters, got %d" % len(text))
    text.encode("utf-8")  # raises if not valid UTF-8 encodable
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two lines, got %d" % len(lines))
    for i, line in enumerate(lines, 1):
        if not line.strip():
            raise ValueError("line %d must not be empty" % i)
        if not line.rstrip().endswith("."):
            raise ValueError("line %d must be one sentence ending in '.'" % i)
        # One sentence per line: no other sentence-ending period inside.
        # ("2%" has no period; abbreviations would need care, none used.)
        if line.rstrip()[:-1].count(".") != 0:
            raise ValueError("line %d must be a single sentence" % i)
    return True


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = build_text()
    validate(text)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    with open(path, "rb") as f:
        raw = f.read()
    raw.decode("utf-8")  # gate: file on disk must be valid UTF-8
    if not 1 <= len(raw.decode("utf-8")) <= MAX_CHARS:
        raise ValueError("written file fails the 1-400 char gate")
    print("wrote %s (%d chars)" % (path, len(text)))


if __name__ == "__main__":
    main()
