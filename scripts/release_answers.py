#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish the students' model answers for the lectures the teacher has
released, and only those.

    python scripts/release_answers.py

The model answers are built into lectureN/_teacher/model-answers.html, which
Jekyll does not serve. This copies a released lecture's file to
lectureN/answers/index.html, which it does serve, and the dashboard links to
it. A lecture not on the list has no public copy: if one exists from an
earlier release, it is removed.

The list is scripts/answers-released.json. A lecture goes on it once its
homework has been collected, so the answers cannot be copied the night
before it is due. scripts/ is not published, so the list itself is not
public either.
"""
import io, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIST = ROOT / "scripts" / "answers-released.json"

released = set(json.loads(LIST.read_text(encoding="utf-8"))["released"])
for folder in sorted(ROOT.glob("lecture*")):
    try:
        n = int(folder.name[len("lecture"):])
    except ValueError:
        continue
    src = folder / "_teacher" / "model-answers.html"
    dst = folder / "answers" / "index.html"
    if n in released:
        assert src.is_file(), "lecture %d is released but has no model answers" % n
        dst.parent.mkdir(exist_ok=True)
        shutil.copyfile(src, dst)
        print("lecture %d  published   %s" % (n, dst.relative_to(ROOT)))
    elif dst.parent.is_dir():
        shutil.rmtree(dst.parent)
        print("lecture %d  withdrawn   (not on the released list)" % n)
    elif src.is_file():
        print("lecture %d  held back" % n)
