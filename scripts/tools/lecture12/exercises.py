# -*- coding: utf-8 -*-
"""Lecture 12's exercises: the Chapter 1 revision.

No new exercises. Each one is taken, with its answer and model answer, from
the exercises of the lecture that taught its lesson (lectureN/_teacher/
exercises.json, which must be present: `python scripts/vault.py open`
restores them on a fresh clone), renumbered, and its source line given the
lesson it belongs to.
"""
import io, json

N = 12
# (lesson, lecture, exercise number there) -- class work first, then the
# homework lesson by lesson; the order here is the order on the sheets
PICK = [
    ("1-1", 2, 9), ("1-2", 3, 9), ("1-3", 3, 22), ("1-4", 4, 6),                      # class work
    ("1-1", 2, 5), ("1-1", 2, 8), ("1-1", 2, 10), ("1-1", 2, 12),
    ("1-2", 3, 1), ("1-2", 3, 13), ("1-2", 3, 14), ("1-2", 3, 11),
    ("1-3", 3, 20), ("1-3", 3, 21), ("1-3", 4, 24), ("1-3", 3, 23),
    ("1-4", 4, 3), ("1-4", 4, 5), ("1-4", 4, 13), ("1-4", 4, 14),
]
TITLE = "Ready for Chapter 1?"

src = {}
E, A, MODEL = [], {}, {}
for k, (lesson, lec, n) in enumerate(PICK, 1):
    if lec not in src:
        src[lec] = json.load(open("lecture%d/_teacher/exercises.json" % lec, encoding="utf-8"))
    d = src[lec]
    ex = next(e for p in d["SHEET"]["parts"] for e in p["exercises"] if e["n"] == n)
    ex = dict(ex, n=k, src="Lesson %s · %s" % (lesson, ex.get("src") or "lecture %d" % lec))
    E.append(ex)
    A[str(k)] = d["ANSWERS"][str(n)]
    MODEL[str(k)] = d["MODEL"][str(n)]

DATA = {"SHEET": {"lecture": N, "title": TITLE, "parts": [{"exercises": E}]}, "ANSWERS": A, "MODEL": MODEL}
assert [x["n"] for x in E] == list(range(1, len(PICK) + 1))
assert all(x["type"] in ("truefalse", "match", "table", "category", "fill", "short", "extended") for x in E)
io.open("lecture%d/_teacher/exercises.json" % N, "w", encoding="utf-8", newline="\n").write(
    json.dumps(DATA, ensure_ascii=False, indent=1) + "\n")
print("exercises:", len(E))
