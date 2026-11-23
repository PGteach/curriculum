# -*- coding: utf-8 -*-
"""The Chapter 2 Revision's exercises.

No new exercises. Each one is taken, with its answer and model answer, from
the exercises of the lecture that taught its lesson (lectureN/_teacher/
exercises.json, which must be present: `python scripts/vault.py open`
restores them on a fresh clone), renumbered, and its source line given the
lesson it belongs to.
"""
import io, json

K = 2          # Chapter K Revision, in revision/chapterK/
# (lesson, lecture, exercise number there) -- class work first, then the
# homework lesson by lesson; the order here is the order on the sheets
PICK = [
    ("2-1", 5, 2), ("2-1", 5, 7), ("2-2", 6, 2), ("2-3", 7, 2),                        # class work
    ("2-1", 5, 3), ("2-1", 5, 5), ("2-1", 5, 9), ("2-1", 5, 12),
    ("2-2", 6, 3), ("2-2", 6, 5), ("2-2", 6, 10), ("2-2", 6, 7),
    ("2-3", 7, 3), ("2-3", 7, 5), ("2-3", 7, 6), ("2-3", 7, 7),
    ("2-2", 6, 11), ("2-3", 7, 12), ("2-1", 5, 15), ("2-2", 6, 18),                   # mixed, from the ministry
]
TITLE = "Ready for Chapter 2?"

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

DATA = {"SHEET": {"lecture": "r%d" % K, "title": TITLE, "parts": [{"exercises": E}]}, "ANSWERS": A, "MODEL": MODEL}
assert [x["n"] for x in E] == list(range(1, len(PICK) + 1))
assert all(x["type"] in ("truefalse", "match", "table", "category", "fill", "short", "extended") for x in E)
io.open("revision/chapter%d/_teacher/exercises.json" % K, "w", encoding="utf-8", newline="\n").write(
    json.dumps(DATA, ensure_ascii=False, indent=1) + "\n")
print("exercises:", len(E))
