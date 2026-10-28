#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish the students' model answers, and the chapter exam papers, that
the teacher has released, and only those.

    python scripts/release_answers.py

The model answers are built into lectureN/_teacher/model-answers.html, which
Jekyll does not serve. This copies a released lecture's file to
lectureN/answers/index.html, which it does serve, and the dashboard links to
it. A lecture not on the list has no public copy: if one exists from an
earlier release, it is removed. The chapter exam papers work the same way,
from EXAMS below (the paper only; the marking scheme is never published).

The list is scripts/answers-released.json:
    "released"  lecture numbers whose model answers are public
    "exams"     chapter numbers whose exam paper is public
A lecture goes on it once its homework has been collected, so the answers
cannot be copied the night before it is due; an exam once it has been sat.

The dashboard changes the same list, and the same public copies, straight
on GitHub (it signs in with the teacher's own GitHub key). After using it,
`git pull` before building anything here, or this script will put back
what the dashboard took down.
"""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIST = ROOT / "scripts" / "answers-released.json"

# chapter -> (the paper in _teacher, where a released copy is served)
EXAMS = {
    1: ("lecture4/_teacher/chapter1-exam.html", "lecture4/chapter1-exam/index.html"),
    2: ("lecture7/_teacher/chapter2-exam.html", "lecture7/chapter2-exam/index.html"),
}


def model_paths(n):
    return ("lecture%d/_teacher/model-answers.html" % n, "lecture%d/answers/index.html" % n)


def publish(src, dst, on, what):
    src, dst = ROOT / src, ROOT / dst
    if on:
        assert src.is_file(), "%s is released but %s is missing" % (what, src)
        dst.parent.mkdir(exist_ok=True)
        shutil.copyfile(src, dst)
        print("%-20s published   %s" % (what, dst.relative_to(ROOT).as_posix()))
    elif dst.parent.is_dir():
        shutil.rmtree(dst.parent)
        print("%-20s withdrawn   (not on the released list)" % what)
    elif src.is_file():
        print("%-20s held back" % what)


def main():
    state = json.loads(LIST.read_text(encoding="utf-8"))
    released, exams = set(state.get("released", [])), set(state.get("exams", []))
    for folder in sorted(ROOT.glob("lecture*")):
        try:
            n = int(folder.name[len("lecture"):])
        except ValueError:
            continue
        publish(*model_paths(n), n in released, "lecture %d answers" % n)
    for ch, (src, dst) in sorted(EXAMS.items()):
        publish(src, dst, ch in exams, "chapter %d exam" % ch)


if __name__ == "__main__":
    main()
