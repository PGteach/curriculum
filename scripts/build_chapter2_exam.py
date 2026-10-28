#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print the Chapter 2 exam and its marking scheme.

    python scripts/tools/chapter2_exam_data.py     # the questions -> JSON
    python scripts/build_chapter2_exam.py           # JSON -> the two papers

Writes:
    lecture7/_teacher/chapter2-exam.html       the paper, to print
    lecture7/_teacher/chapter2-exam-key.html   its marking scheme

Both live under _teacher/: neither has a public URL. The teacher prints the
paper and hands it out in the room, as with the Chapter 1 exam.

Unit 2, lessons 2-1 to 2-3. Every item is from the textbook's own questions
or the ministry's assessment book, and says which; check() refuses an item
without one. The shape is the Chapter 1 exam's, scaled to three lessons:
24 MCQ (8 per lesson, six of each letter, no letter three times running,
easy to hard) and 6 written answers (two per lesson, marks rising), where
each written answer's mark points add up to its marks.

The page shell, the cover, the question layout and the answer grid are the
Chapter 1 exam's own functions in build_lecture4.py, imported here, so the
two papers look and print alike.
"""
import importlib.util, io, json, re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("b4", ROOT / "scripts" / "build_lecture4.py")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)                       # its main is guarded

EXAM = json.loads((ROOT / "lecture7/_teacher/chapter2-exam.json").read_text(encoding="utf-8"))
B.EXAM = EXAM                                    # the borrowed functions read this
ACCENT = "#4F55B8"                               # lecture 7's, which closes Unit 2
LESSONS = ("2-1", "2-2", "2-3")


def check():
    mcq, essay = EXAM["mcq"], EXAM["essay"]
    assert len(mcq) == 24, len(mcq)
    for q in mcq:
        assert len(q["o"]) == 4 and len(set(q["o"])) == 4, q["q"]
    letters = [q["pos"] for q in mcq]
    counts = {L: letters.count(L) for L in B.LETTERS}
    assert set(counts.values()) == {6}, "answer letters not balanced: %s" % counts
    for k in range(len(letters) - 2):
        assert len(set(letters[k:k + 3])) > 1, "three %s in a row at Q%d" % (letters[k], k + 1)
    levels = [q["level"] for q in mcq]
    assert levels == sorted(levels), "MCQ not ordered easy to hard"
    for L in LESSONS:
        assert sum(q["lesson"] == L for q in mcq) == 8, "lesson %s needs 8 MCQ" % L
        assert sum(e["lesson"] == L for e in essay) == 2, "lesson %s needs 2 written answers" % L
    marks = [e["marks"] for e in essay]
    assert marks == sorted(marks), "written answers not ordered easy to hard"
    for e in essay:
        assert len(e["points"]) == e["marks"], "points %d != marks %d: %s" % (len(e["points"]), e["marks"], e["q"][:40])
    # the teacher's rule: every item is from the book or the ministry, and says so
    for item in mcq + essay:
        assert item.get("src", "").startswith(("Book p.", "Ministry assessments")), (
            "item without a curriculum source: %s" % item["q"][:60])
    return len(mcq), sum(marks)


# which questions go on which printed page -- checked by rendering each sheet
# on its own and counting one A4 page
PAGES = [
    ("A", [0, 1, 2, 3, 4]),          # page 1 carries the cover
    ("A", [5, 6, 7, 8, 9, 10, 11]),
    ("A", [12, 13, 14, 15, 16, 17]),
    ("A", [18, 19, 20, 21, 22, 23]),
    ("B", [0, 1, 2]),
    ("B", [3, 4]),
    ("B", [5]),
]


def shell():
    head, tail = B.shell()
    # the template's own config still names lecture 4; this paper belongs to
    # lecture 7, which closes Unit 2
    tail = (tail.replace("const LECTURE_NUM   = 4;", "const LECTURE_NUM   = 7;")
                .replace('const LECTURE_TITLE = "%s";' % B.TITLE, 'const LECTURE_TITLE = "When something goes wrong";'))
    assert "const LECTURE_NUM   = 7;" in tail
    return head.replace(B.ACCENT, ACCENT), tail.replace(B.ACCENT, ACCENT)


def paper(head, tail):
    total = check()
    pages, seen_sec, seen_lvl = [], set(), set()
    for sec, idx in PAGES:
        b = []
        if not pages:
            b.append(B.exam_head_block(total))
        if sec not in seen_sec:
            if sec == "A":
                b.append('<div class="examsec"><h2>Section A &middot; Multiple choice</h2>'
                         '<span class="tot">%d marks &middot; 1 mark each</span></div>' % total[0])
            else:
                b.append('<div class="examsec"><h2>Section B &middot; Written answers</h2>'
                         '<span class="tot">%d marks</span></div>' % total[1])
            seen_sec.add(sec)
        for i in idx:
            if sec == "A":
                lv = EXAM["mcq"][i]["level"]
                if lv not in seen_lvl:
                    L = EXAM["levels"][lv]
                    b.append('<div class="lvl">' + esc(L["name"]) + '<span class="ar">'
                             + esc(L["nameAr"]) + '</span></div>')
                    seen_lvl.add(lv)
                b.append(B.mcq_html(i + 1, EXAM["mcq"][i]))
            else:
                b.append(B.essay_html(len(EXAM["mcq"]) + i + 1, EXAM["essay"][i]))
        if sec == "B" and idx[-1] == len(EXAM["essay"]) - 1:
            b.append('<p style="text-align:center;margin-top:4mm;font-weight:600">End of the exam</p>')
        pages.append(B.page(''.join(b)))
    return head + ''.join(pages) + tail


def key(head, tail):
    total = check()
    rows = []
    for i, q in enumerate(EXAM["mcq"]):
        o, k = B.placed(q)
        rows.append('<tr><td>%d</td><td class="let">%s</td><td>%s</td><td>%s</td></tr>'
                    % (i + 1, B.LETTERS[k], esc(o[k]), esc(q["lesson"] + " — " + q["src"])))

    def grid(rs):
        return ('<table class="answergrid"><tr><th style="width:8mm">Q</th><th>Ans</th>'
                '<th>Correct option</th><th style="width:34%">Source</th></tr>' + ''.join(rs) + '</table>')
    first = (B.page(masthead(total) + '<div class="keygroup">Section A &mdash; answers (1 mark each)</div>'
                    + grid(rows[:12]))
             + B.page('<div class="keygroup">Section A &mdash; answers, continued</div>' + grid(rows[12:])))
    blocks = []
    for i, e in enumerate(EXAM["essay"]):
        n = len(EXAM["mcq"]) + i + 1
        blocks.append('<div class="ex"><div class="exhead"><span class="exn">' + str(n) + '</span>'
                      '<span class="exq">' + esc(e["q"]) + '</span></div>'
                      '<div class="src">' + esc(e["lesson"] + " — " + e["src"]) + '</div>'
                      '<div class="key"><div class="marks">[' + str(e["marks"]) + ' marks]</div>'
                      '<p><b>Model answer.</b> ' + esc(e["model"]) + '</p>'
                      '<p><b>Award a mark for each:</b></p><ul>'
                      + ''.join('<li>' + esc(x) + '</li>' for x in e["points"]) + '</ul></div></div>')
    rest = (B.page('<div class="keygroup">Section B &mdash; marking scheme</div>' + ''.join(blocks[0:3]))
            + B.page(''.join(blocks[3:5]))
            + B.page(blocks[5]
                     + '<div class="summary"><p><b>Total: %d marks.</b> Section A %d, Section B %d. '
                       'Accept any wording that carries the point; the book&#8217;s words are not required, '
                       'the idea is.</p><p class="ar">اقبل أي صياغة فيها الفكرة؛ مش لازم كلام الكتاب بالحرف.</p></div>'
                     % (total[0] + total[1], total[0], total[1])))
    return head + first + rest + tail


def masthead(total):
    return ('<div class="brand">Programming &amp; Artificial Intelligence &middot; Grade 11</div>'
            '<h1>' + esc(EXAM["title"]) + ' &mdash; Marking scheme</h1>'
            '<div class="docsub">' + esc(EXAM["unit"]) + ' &middot; ' + esc(EXAM["lessons"])
            + ' &middot; %d marks</div>' % (total[0] + total[1]) + B.teacher_warn())


if __name__ == "__main__":
    head, tail = shell()
    name = EXAM["title"] + " — %s"
    for path, html, title in [
            (ROOT / "lecture7/_teacher/chapter2-exam.html", paper(head, tail), name % EXAM["unit"]),
            (ROOT / "lecture7/_teacher/chapter2-exam-key.html", key(head, tail), name % "Marking scheme")]:
        html = B.name(html, title)
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        assert not re.search(r"\{[%{]", html), "Liquid delimiter in " + path.name
        io.open(path, "w", encoding="utf-8", newline="\n").write(html)
        print("%-42s %6d bytes, %2d sheets" % (path.relative_to(ROOT), len(html),
                                               html.count('<section class="sheet')))
