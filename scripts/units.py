# -*- coding: utf-8 -*-
"""Where the page sets live, for every script that walks them.

    lectureN/              Lecture N            the lessons, numbered in order
    revision/chapterN/     Chapter N Revision   a chapter's revision, kept apart
                                                so it does not take a lecture
                                                number

Both hold the same pages (slides, quiz, handout, homework, _teacher). A page
says which set it belongs to in its LECTURE CONFIG: LECTURE_NUM is N, and a
revision page adds PAGE_PATH ("revision/chapter1") and PAGE_LABEL ("Chapter 1
Revision"), which its quiz link, QR code and recorded results are built from.

On the command line a set is named "12" (lecture 12) or "r1" (Chapter 1
Revision); "revision/chapter1" works too.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Unit:
    def __init__(self, kind: str, num: int):
        self.kind, self.num = kind, num
        if kind == "lecture":
            self.rel, self.label, self.tag = "lecture%d" % num, "Lecture %d" % num, "L%d" % num
        else:
            self.rel, self.label, self.tag = "revision/chapter%d" % num, "Chapter %d Revision" % num, "R%d" % num
        self.dir = ROOT / self.rel

    @property
    def revision(self) -> bool:
        return self.kind == "revision"

    def __repr__(self):
        return self.label


def lectures() -> list:
    return sorted((Unit("lecture", int(p.name[7:])) for p in ROOT.glob("lecture*")
                   if p.is_dir() and p.name[7:].isdigit()), key=lambda u: u.num)


def revisions() -> list:
    return sorted((Unit("revision", int(p.name[7:])) for p in (ROOT / "revision").glob("chapter*")
                   if p.is_dir() and p.name[7:].isdigit()), key=lambda u: u.num)


def all_units() -> list:
    return lectures() + revisions()


def find(arg: str) -> Unit | None:
    """'12' -> Lecture 12; 'r1', 'revision1' or 'revision/chapter1' -> Chapter 1 Revision."""
    a = arg.strip().strip("/").lower()
    if a.isdigit():
        return Unit("lecture", int(a))
    m = re.fullmatch(r"(?:r|revision|revision/chapter)(\d+)", a)
    return Unit("revision", int(m.group(1))) if m else None
