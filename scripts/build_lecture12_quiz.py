# -*- coding: utf-8 -*-
"""Write Lecture 12's quiz -- the Chapter 1 revision exam -- into
lecture12/quiz/index.html.

    python scripts/build_lecture12_quiz.py && python scripts/protect_answers.py 12

The second command is required: this writes plaintext a: indices, and
protect_answers turns them into fingerprints before publishing.

No new questions. Every one is taken from the quizzes of lectures 3 and 4, as
written and checked there -- same wording, options, explanation and book
source -- and regrouped by lesson, so the result screen says which lesson to
read again. PICK sets how many come from each lesson and the mix of
difficulty (1 easy, 2 medium, 3 hard); where a lesson's pool is short in a
band, the nearest band makes up the number. Questions are taken in their
original order within a band, so a rebuild always picks the same ones.
"""
import io, re, importlib.util


def bank(n):
    spec = importlib.util.spec_from_file_location("bank%d" % n, "scripts/build_lecture%d_quiz.py" % n)
    q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
    return [tuple(x) + ((),) * (8 - len(x)) for x in q.Q]      # lecture 3 has no glosses


def pick(pool, want):
    """want = {band: count}; fill a short band from the nearest one."""
    out, left = [], list(pool)
    for band, k in sorted(want.items()):
        got = [x for x in left if x[1] == band][:k]
        out += got
        left = [x for x in left if x not in got]
        short = k - len(got)
        for near in sorted({1, 2, 3} - {band}, key=lambda b: abs(b - band)):
            if not short:
                break
            more = [x for x in left if x[1] == near][:short]
            out += more; short -= len(more)
            left = [x for x in left if x not in more]
    return sorted(out, key=lambda x: x[1])


SECTIONS = [
    "1-1 · IT development and society",
    "1-2 · How AI works",
    "1-3 · AI in daily life and industry",
    "1-4 · Ethical issues with AI",
]

L3, L4 = bank(3), bank(4)
REVIEW = [x for x in L4 if x[0] == 0]          # lecture 4's Unit 1 review, sorted by the lesson its source names
POOLS = {
    0: [x for x in L3 if x[0] == 1] + [x for x in REVIEW if x[6].startswith("Lesson 1-1")],
    1: [x for x in L3 if x[0] in (2, 3)] + [x for x in REVIEW if x[6].startswith("Lesson 1-2")],
    2: [x for x in L3 if x[0] == 4] + [x for x in REVIEW if x[6].startswith("Lesson 1-3")],
    3: [x for x in L4 if x[0] in (1, 2, 3, 4)],
}
PICK = {s: {1: 2, 2: 4, 3: 2} for s in POOLS}

# (section, difficulty, question, code, options, answer index, why, src, glosses)
Q, _seen = [], set()
for s in sorted(POOLS):
    pool = [x for x in POOLS[s] if x[2] not in _seen]
    for x in pick(pool, PICK[s]):
        _seen.add(x[2])
        Q.append((s, x[1], x[2], "", list(x[3]), x[4], x[5], x[6], [list(g) for g in x[7]]))


def js_str(t):
    return '"' + t.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


CODE_CSS = ('  .qcode{background:#16233F;color:#E6EDF3;font-family:"JetBrains Mono",ui-monospace,monospace;'
            'font-size:15px;line-height:1.6;border-radius:10px;padding:12px 14px;margin:-6px 0 18px;'
            'white-space:pre;overflow-x:auto;text-align:left;direction:ltr;font-variant-ligatures:none}\n'
            '  .review-card .qcode{font-size:13px;margin:4px 0 8px}')


def add_code_box(page):
    """Show q.c, when a question has one, as a code box under the question
    and in the review of wrong answers. textContent, never innerHTML."""
    if 'id="qcode"' in page:
        return page
    for a, b in [
        ('<div class="q" id="question"></div>',
         '<div class="q" id="question"></div>\n    <pre class="qcode" id="qcode" hidden></pre>'),
        ('  $("question").textContent = q.q;\n',
         '  $("question").textContent = q.q;\n  $("qcode").textContent = q.c || "";\n  $("qcode").hidden = !q.c;\n'),
        ("      question: q.q,\n", '      question: q.q,\n      code: q.c || "",\n'),
        ('      card.appendChild(el("h4", "", item.question));\n',
         '      card.appendChild(el("h4", "", item.question));\n'
         '      if(item.code) card.appendChild(el("pre", "qcode", item.code));\n'),
        ("  .q{font-size:19px;font-weight:600;line-height:1.4;margin-bottom:18px}",
         "  .q{font-size:19px;font-weight:600;line-height:1.4;margin-bottom:18px}\n" + CODE_CSS),
    ]:
        assert page.count(a) == 1, a
        page = page.replace(a, b, 1)
    return page


if __name__ == "__main__":
    from collections import Counter
    for s, d, q, c, o, a, why, src, v in Q:
        assert 0 <= s < len(SECTIONS), q
        assert d in (1, 2, 3), q
        assert 0 <= a < len(o), q
        assert len(o) == 4, "four options: " + q
        assert len(o) == len(set(o)), "repeated option: " + q
        assert why.strip() and src.strip(), q
        hay = (q + " " + " ".join(o)).lower()
        for en, ar in v:
            assert en.lower() in hay, "gloss not on screen: %r in %r" % (en, q)
    assert len({x[2] for x in Q}) == len(Q), "duplicate question text (the page tells questions apart by it)"
    print("sections:", dict(sorted(Counter(x[0] for x in Q).items())))
    print("difficulty:", dict(sorted(Counter(x[1] for x in Q).items())))

    secs = "[\n" + ",\n".join("  " + js_str(x) for x in SECTIONS) + "\n];"
    rows = []
    for s, d, q, c, o, a, why, src, v in Q:
        gl = (",v:[%s]" % ",".join("[%s,%s]" % (js_str(en), js_str(ar)) for en, ar in v)) if v else ""
        code = (",c:%s" % js_str(c)) if c else ""
        rows.append("  {s:%d,d:%d,q:%s%s,o:[%s],a:%d,why:%s,src:%s%s}"
                    % (s, d, js_str(q), code, ",".join(js_str(x) for x in o), a,
                       js_str(why), js_str(src), gl))
    qs = "[\n" + ",\n".join(rows) + "\n];"

    p = "lecture12/quiz/index.html"
    page = io.open(p, encoding="utf-8").read()
    page = add_code_box(page)
    page = re.sub(r"const SECTIONS = \[.*?\n\];", lambda m: "const SECTIONS = " + secs,
                  page, count=1, flags=re.DOTALL)
    page = re.sub(r"const QUESTIONS = \[.*?\n\];", lambda m: "const QUESTIONS = " + qs,
                  page, count=1, flags=re.DOTALL)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    print("written: %d questions" % len(Q))
