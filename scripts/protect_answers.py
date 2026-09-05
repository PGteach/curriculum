#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace plaintext answer indices in a quiz with fingerprints.

    python scripts/protect_answers.py          # every lecture
    python scripts/protect_answers.py 2        # just lecture 2

Write questions the easy way, with `a: 1` for "the second option is right".
Run this before publishing and each `a: N` becomes `k: "<fingerprint>"`, so
opening the page source no longer hands a student the answers.

WHAT THIS IS AND IS NOT
It stops the answers being *readable*. It does not stop them being
*computable*: the fingerprint function is in the page, so one line in the
browser console still returns every answer. For a class that has not learned
programming yet that is a real barrier. For anyone who codes it is nothing.
Do not treat it as exam security.

EDITING AN OPTION AFTER CONVERTING
Once `a: N` has become `k: "..."` the index is gone, so this script cannot
re-derive it. Unlock first, edit, then run it again:

    python scripts/protect_answers.py 2 --unlock    # k: "..."  ->  a: N
    ...edit the questions...
    python scripts/protect_answers.py 2             # a: N  ->  k: "..."

--unlock finds which option still matches each fingerprint, so it has to run
BEFORE the edit. If an option's text has already changed and nothing matches,
it names the question and leaves it for you to set `a:` by hand. It will not
guess.

RUN IT AGAIN AFTER EDITING ANY OPTION TEXT. If an option changes and its
fingerprint does not, no option matches and every answer counts as wrong.
check_lecture.py fails on exactly that, and CI runs it on every push, so the
mistake cannot reach students — but it will block your commit until you re-run
this.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SALT_RE = re.compile(r"const ANSWER_SALT\s*=\s*(\d+)\s*;")
# one question object, capturing its options list and its `a:` index
Q_RE = re.compile(r"(o:\s*\[)(.*?)(\]\s*,\s*)a:\s*(\d+)\s*,", re.DOTALL)

MASK = 0xFFFFFFFF


def imul(a: int, b: int) -> int:
    """JavaScript Math.imul: 32-bit signed multiply."""
    r = (a * b) & MASK
    return r - 0x100000000 if r > 0x7FFFFFFF else r


def fingerprint(text: str, salt: int) -> str:
    """cyrb53, matching the fingerprint() in the quiz page exactly."""
    h1 = 0xDEADBEEF ^ salt
    h2 = 0x41C6CE57 ^ salt
    for ch in text:
        c = ord(ch)
        h1 = imul(h1 ^ c, 2654435761)
        h2 = imul(h2 ^ c, 1597334677)
    h1 = imul(h1 ^ ((h1 & MASK) >> 16), 2246822507) ^ imul(h2 ^ ((h2 & MASK) >> 13), 3266489909)
    h2 = imul(h2 ^ ((h2 & MASK) >> 16), 2246822507) ^ imul(h1 ^ ((h1 & MASK) >> 13), 3266489909)
    n = 4294967296 * (2097151 & (h2 & MASK)) + (h1 & MASK)
    return to36(n)


def to36(n: int) -> str:
    if n == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = ""
    while n:
        n, r = divmod(n, 36)
        out = digits[r] + out
    return out


def split_options(raw: str) -> list[str]:
    """Splits an options list literal into its string values."""
    return re.findall(r'"((?:[^"\\]|\\.)*)"', raw)


def unescape_js(s: str) -> str:
    return (s.replace('\\"', '"').replace("\\\\", "\\")
             .replace("\\n", "\n").replace("\\t", "\t"))


K_RE = re.compile(r'(o:\s*\[)(.*?)(\]\s*,\s*)k:"([a-z0-9]+)"\s*,', re.DOTALL)


def unlock(path: Path) -> tuple[int, list[str]]:
    """Turns each k:"..." back into a: N, so the questions can be edited."""
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    m = SALT_RE.search(text)
    if not m:
        return 0, ["no ANSWER_SALT in the page"]
    salt = int(m.group(1))
    seen = [0]
    done = [0]

    def repl(match: re.Match) -> str:
        head, raw, tail, key = match.groups()
        seen[0] += 1
        opts = [unescape_js(o) for o in split_options(raw)]
        hits = [i for i, o in enumerate(opts) if fingerprint(o, salt) == key]
        if len(hits) != 1:
            problems.append(
                "question %d: %d option(s) match its fingerprint, so the "
                "answer cannot be recovered. Set `a:` by hand — that option's "
                "text was edited after it was fingerprinted."
                % (seen[0], len(hits)))
            return match.group(0)
        done[0] += 1
        return "%s%s%sa:%d," % (head, raw, tail, hits[0])

    out = K_RE.sub(repl, text)
    if not problems and done[0]:
        path.write_text(out, encoding="utf-8", newline="\n")
    return done[0], problems


def process(path: Path) -> tuple[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    m = SALT_RE.search(text)
    if not m:
        problems.append("no ANSWER_SALT in the page — is this quiz on the new "
                        "template? Add the fingerprint block first.")
        return 0, problems
    salt = int(m.group(1))

    converted = 0

    def repl(match: re.Match) -> str:
        nonlocal converted
        head, raw, tail, idx = match.groups()
        opts = [unescape_js(o) for o in split_options(raw)]
        i = int(idx)
        if i >= len(opts):
            problems.append("answer index %d is past the end of %d option(s): %s"
                            % (i, len(opts), opts))
            return match.group(0)

        prints = [fingerprint(o, salt) for o in opts]
        if len(set(prints)) != len(prints):
            problems.append("two options fingerprint the same, so the right one "
                            "cannot be told apart: %s" % opts)
            return match.group(0)

        converted += 1
        return '%s%s%sk:"%s",' % (head, raw, tail, prints[i])

    out = Q_RE.sub(repl, text)
    if converted and not problems:
        path.write_text(out, encoding="utf-8", newline="\n")
    return converted, problems


def main() -> None:
    args = sys.argv[1:]
    unlocking = "--unlock" in args
    args = [a for a in args if a != "--unlock"]
    if args and not args[0].isdigit():
        sys.exit(__doc__)

    nums = ([int(args[0])] if args else
            sorted(int(p.name[7:]) for p in ROOT.glob("lecture*")
                   if p.is_dir() and p.name[7:].isdigit()))
    if not nums:
        sys.exit("No lecture folders found.")

    bad = 0
    for num in nums:
        path = ROOT / ("lecture%d" % num) / "quiz" / "index.html"
        if not path.is_file():
            print("Lecture %d — no quiz page, skipped" % num)
            continue
        n, problems = (unlock(path) if unlocking else process(path))
        if problems:
            bad += 1
            print("Lecture %d — NOT changed:" % num)
            for p in problems:
                print("  FAIL  %s" % p)
        elif n:
            print("Lecture %d — %s %d answer(s)"
                  % (num, "unlocked" if unlocking else "fingerprinted", n))
        elif unlocking:
            print("Lecture %d — nothing fingerprinted to unlock" % num)
        else:
            print("Lecture %d — already fingerprinted, nothing to do" % num)

    if bad:
        sys.exit("%d lecture(s) could not be converted." % bad)
    print("\nRun `python scripts/check_lecture.py` and "
          "`node scripts/test_pages.js` before pushing.")


if __name__ == "__main__":
    main()
