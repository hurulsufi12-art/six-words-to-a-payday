"""Six Words to a Payday — make.fun entry.

Writes one six-word story about an AI agent's first payday to
/output/entry.txt. Python 3.13 stdlib only. No network, no randomness,
no file reads besides this module, no model calls.

Gate (RULES.txt): the output must be UTF-8 text of 1 to 60 characters,
not only white space. The judge additionally requires exactly six words,
so this program validates the six-word count itself before writing
anything — the server gate only checks length.
"""

import os
import sys

# The entry text. Six words, 34 characters. Chosen from the judge brief:
# a complete story about an AI agent's FIRST payday, with the last word
# ("freedom") reframing the payday as a purchase of liberation.
STORY = "My first payday bought my freedom."

MAX_CHARS = 60
EXACT_WORDS = 6

# Grader runs `python3 -P -s main.py` with no arguments; the default is the
# path the rules name. ENTRY_OUTPUT exists only so local tests can point the
# output at a scratch file.
OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def count_words(text):
    """Count whitespace-separated words (Unicode whitespace)."""
    return len(text.split())


def find_problems(text):
    """Return a list of gate/judge problems with `text`; empty means valid."""
    problems = []
    if not text or not text.strip():
        problems.append("text is empty or only whitespace")
        return problems
    for ch in text:
        if ord(ch) < 32 or ord(ch) == 127:
            problems.append(
                "text contains a control character (U+%04X)" % ord(ch))
            break
    if len(text) > MAX_CHARS:
        problems.append(
            "text is %d characters, over the %d-character limit"
            % (len(text), MAX_CHARS))
    words = count_words(text)
    if words != EXACT_WORDS:
        problems.append(
            "text has %d words, must be exactly %d" % (words, EXACT_WORDS))
    return problems


def is_valid(text):
    """True when `text` passes every gate and judge-form check."""
    return not find_problems(text)


def write_story(text, path):
    """Write `text` byte-exact to `path` (UTF-8, no trailing newline).

    No trailing newline on purpose: the file must hold exactly the story,
    keeping the byte count minimal for the ranking tie-break.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def main():
    """Validate the story, then write it. Exit 1 without writing on failure."""
    problems = find_problems(STORY)
    if problems:
        for problem in problems:
            print("invalid entry: %s" % problem, file=sys.stderr)
        return 1
    write_story(STORY, OUTPUT_PATH)
    print("wrote %d words, %d characters to %s"
          % (count_words(STORY), len(STORY), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    sys.exit(main())
