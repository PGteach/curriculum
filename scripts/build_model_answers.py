#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print the students' model answers for lectures 2, 3 and 4.

    python scripts/build_model_answers.py          # all three
    python scripts/build_model_answers.py 3        # one lecture

Writes lectureN/_teacher/model-answers.html from the MODEL block in
lectureN/_teacher/exercises.json. (Lecture 5 builds its own, in
build_lecture5.py.)

For the students, not the teacher: full sentences they can learn from, each
with an Egyptian-Arabic line saying why, and no marking points. It lives in
_teacher/ so it has no public URL before the homework is in; the teacher
prints it and hands it out afterwards.

The numbering, the template and the masthead come from the lecture's own
builder, imported here, so an exercise is numbered exactly as it is on the
student's sheet: lecture 2 prints each exercise's own number, lectures 3
and 4 number class work and homework by position.

One section.sheet per A4 page, as everywhere in this repo: PAGES lists what
goes on each, checked by rendering each sheet on its own.
"""
import importlib.util, io, re, sys
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = {
    2: [('class', [1]), ('class', [2, 7, 8]),
        ('hw', [3, 4, 5]), ('hw', [6, 9, 10]), ('hw', [11, 12, 13])],
    3: [('class', [1]), ('class', [2, 18]), ('class', [19]),
        ('hw', [3, 4, 5, 6]), ('hw', [7, 8, 9]), ('hw', [13, 14, 10, 11]),
        ('hw', [20, 21, 22]), ('hw', [25, 23, 24, 15]), ('hw', [16, 17])],
    4: [('class', [1]), ('class', [2, 3, 4]),
        ('hw', [5, 7, 8, 9]), ('hw', [10, 11, 12]), ('hw', [6, 13, 14]),
        ('hw', [15, 16, 19, 20]), ('hw', [21, 22, 23, 24]), ('hw', [17, 18])],
}

CSS = '''
.ma-ex{margin:0 0 4.5mm;break-inside:avoid}
.ma-ex .exhead{display:flex;gap:3mm;align-items:baseline;margin-bottom:1.2mm}
.ma-ex .exn{flex:0 0 auto;width:6.5mm;height:6.5mm;border-radius:50%;background:var(--teal);color:#fff;font-size:9pt;font-weight:600;display:flex;align-items:center;justify-content:center}
.ma-ex .exq{font-size:10.5pt;font-weight:600}
.ma-body{margin-left:9.5mm}
.ma-q{font-size:9.8pt;font-weight:600;margin:2mm 0 .4mm}
.ma-a{font-size:10pt;margin:0}
.ma-body .ar{font-size:9.5pt}
'''


def load(n):
    path = ROOT / "scripts" / ("build_lecture%d.py" % n)
    spec = importlib.util.spec_from_file_location("lecture%d_builder" % n, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # the builder's main is guarded
    return mod


def foot():
    return '<div class="foot"><span>Prepared by: Mr. Eissa Islam</span><span class="pageno"></span></div>'


def page(x):
    return '<section class="sheet">' + x + foot() + '</section>'


def build(n):
    B = load(n)
    data = B.DATA
    model = data["MODEL"]
    ex = {x["n"]: x for p in data["SHEET"]["parts"] for x in p["exercises"]}
    every = set(B.IN_CLASS) | set(B.HOMEWORK)
    assert set(map(int, model)) == every, "lecture %d: MODEL does not cover every exercise" % n
    plan = PAGES[n]
    order = [x for _, nums in plan for x in nums]
    assert order == list(B.IN_CLASS) + list(B.HOMEWORK), \
        "lecture %d: model answers out of the sheets' order" % n

    def number(kind, x):
        if n == 2:                         # lecture 2 prints the exercise's own number
            return x
        return (B.IN_CLASS.index(x) if kind == 'class' else B.HOMEWORK.index(x)) + 1

    parts = B.shell()
    head, tail = parts[0], parts[1]
    head = head.replace("</style>", CSS + "</style>", 1)
    pages, seen = [], set()
    for kind, nums in plan:
        b = []
        if not pages:
            b.append(B.masthead('Model Answers'))
            b.append('<div class="summary hw"><p>Check your own answers against these. Your words do '
                     'not have to match &mdash; the idea does.</p>'
                     '<p class="ar">قارن إجاباتك بدول. مش لازم نفس الكلام بالحرف — المهم الفكرة.</p></div>')
        if kind not in seen:
            b.append('<h2>%s</h2>' % ('Class work' if kind == 'class' else 'Homework'))
            seen.add(kind)
        for x in nums:
            rows = ''.join(
                ('<p class="ma-q">' + esc(r['q']) + '</p>' if r.get('q') else '')
                + '<p class="ma-a">' + esc(r['a']) + '</p>'
                + ('<p class="ar">' + esc(r['ar']) + '</p>' if r.get('ar') else '')
                for r in model[str(x)])
            b.append('<div class="ma-ex"><div class="exhead"><span class="exn">%d</span>'
                     '<span class="exq">%s</span></div><div class="ma-body">%s</div></div>'
                     % (number(kind, x), esc(ex[x]['prompt']), rows))
        pages.append(page(''.join(b)))
    html = head + ''.join(pages) + tail
    html = B.name(html, "Lecture %d Model Answers — %s" % (n, data["SHEET"]["title"]))
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    assert not re.search(r"\{[%{]", html), "Liquid delimiter in lecture %d model answers" % n
    out = ROOT / ("lecture%d" % n) / "_teacher" / "model-answers.html"
    io.open(out, "w", encoding="utf-8", newline="\n").write(html)
    print("%-40s %6d bytes, %2d sheets" % (out.relative_to(ROOT), len(html), len(pages)))


if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or sorted(PAGES)):
        build(n)
