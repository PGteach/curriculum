#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the Chapter 1 Revision's printed material.

    python scripts/build_revision1.py

Writes:
    revision/chapter1/handout/index.html     revision booklet: two pages a lesson + class work
    revision/chapter1/homework/index.html    revision exercises, lesson by lesson
    revision/chapter1/_teacher/answer-key.html     key to the class work and homework
    revision/chapter1/_teacher/model-answers.html  the students' model answers

Content comes from revision/chapter1/_teacher/exercises.json, which lives under
_teacher/ on purpose: Jekyll does not serve underscore-prefixed paths, and
this script is itself unpublished (scripts/ is excluded in _config.yml).

Unit 1, lessons 1-1 to 1-4. Nothing new: the booklet reads
tools/revision1/data.py (the book's key takeaways and key terms, the exam
traps, each lesson's exam question and marking points), and every exercise
is taken, with its answers, from the lecture that taught its lesson
(tools/revision1/exercises.py).

Derived from build_lecture5.py: the same helpers, homework, key and model
answer code, with this lecture's constants, booklet and page plans. Every
printed document is one section.sheet per A4 page; the page lists below are
checked by rendering each sheet on its own.
"""
import io, json, re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "revision" / "chapter1" / "_teacher"
DATA = json.loads((T / "exercises.json").read_text(encoding="utf-8"))
EX = {x["n"]: x for x in DATA["SHEET"]["parts"][0]["exercises"]}

TITLE = "Ready for Chapter 1?"
ACCENT = "#8A2B2B"

# Class work: the book's Worked Example and Try, all quick to mark together.
IN_CLASS = [1, 2, 3, 4]

HW_SECTIONS = [
    ("Lesson 1-1 &middot; Development of IT and social transformation",
     "الدرس 1-1 — تطور تكنولوجيا المعلومات والتحول الاجتماعي",
     # the first sheet also carries the masthead and the intro box
     [[5], [6, 7], [8]]),
    ("Lesson 1-2 &middot; How AI works",
     "الدرس 1-2 — كيف يعمل الذكاء الاصطناعي",
     [[9, 10], [11], [12]]),
    ("Lesson 1-3 &middot; AI in daily life and industry",
     "الدرس 1-3 — الذكاء الاصطناعي في الحياة اليومية والصناعة",
     [[13, 14], [15], [16]]),
    ("Lesson 1-4 &middot; Ethical issues with AI",
     "الدرس 1-4 — القضايا الأخلاقية للذكاء الاصطناعي",
     [[17], [18], [19], [20]]),
]
HOMEWORK = [n for _, _, pages in HW_SECTIONS for g in pages for n in g]

EXTRA_CSS = '''
.tdar{font-size:9pt;color:var(--soft);margin-top:.6mm}
.namebox{display:flex;gap:5mm;margin:0 0 6mm}.namebox>div{flex:1;display:flex;align-items:flex-end;gap:2mm}.namebox span{font-size:9pt;color:var(--soft);font-weight:600}.namebox i{flex:1;border-bottom:1px solid var(--rule);height:6mm}.ex{margin:0 0 5mm;break-inside:avoid}.exhead{display:flex;gap:3mm;align-items:baseline;margin-bottom:1.5mm}.exn{flex:0 0 auto;width:6.5mm;height:6.5mm;border-radius:50%;background:var(--teal);color:#fff;font-size:9pt;font-weight:600;display:flex;align-items:center;justify-content:center}.exq{font-size:10.5pt;font-weight:600}.src{font-size:8pt;color:var(--soft);font-style:italic;margin:0 0 1.5mm 9.5mm}.passage{font-size:10pt;line-height:1.8;background:#FCFCFA;border:1px solid var(--line);padding:3mm}.marks{font-size:9pt;font-weight:600;color:var(--gold);margin:2mm 0}.key{margin-left:9.5mm;font-size:10pt}.teacherwarn{background:#FBF0EE;border-left:3px solid #9C3B2E;padding:3mm}.summary.hw{background:var(--teal-pale)}.keygroup{font-size:9.5pt;color:var(--soft);font-weight:600;text-transform:uppercase;letter-spacing:.04em;margin:5mm 0 2mm}.key ul{margin-left:4mm}.key li{margin-bottom:1mm}.key .note{font-size:9.5pt;color:var(--soft);font-style:italic;margin-top:1.5mm}ol.blanks{list-style:none;margin:3mm 0 0}ol.blanks li{display:flex;align-items:flex-end;gap:3mm;margin-bottom:4.5mm}ol.blanks li b{flex:0 0 auto;font-size:10.5pt}ol.blanks .rule{flex:1;height:6mm;border-bottom:1px solid var(--rule)}.opt{display:block;margin:1.2mm 0 0 4mm}.srcinline{font-size:8pt;color:var(--soft);font-style:italic;margin-left:2mm}ol.qs li{margin-bottom:3mm}.optlead{font-size:10pt;font-weight:600;margin:2.5mm 0 1.5mm}.fields{display:flex;flex-wrap:wrap;gap:2.5mm;margin:0 0 2mm}.chip{border:1px solid var(--line);border-radius:20mm;padding:1.5mm 4mm;font-size:10pt;background:#FCFCFA}
.key .mq-q{font-size:9.8pt;font-weight:600;margin:2.2mm 0 .4mm}.key .mq-a{font-size:10pt;margin:0}.key .ar{font-size:9.5pt}
.dg{margin:3mm 0 4mm}.dg svg{display:block;width:100%;height:auto}
.principles{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin:3mm 0}
.principles .pr{border:1px solid var(--line);border-left:3px solid var(--teal);border-radius:1.5mm;padding:2.5mm 3.5mm;background:#FCFCFA}
.principles .pr h4{font-size:10.5pt;margin-bottom:1mm}.principles .pr p{font-size:9.5pt;margin:0}
'''


def slide_svg(name):
    """Read a diagram out of the deck's builder, so the booklet cannot drift
    from the picture the lesson was taught with."""
    src = (ROOT / "scripts" / "build_revision1_slides.py").read_text(encoding="utf-8")
    m = re.search(r"^%s = '''(.*?)'''" % name, src, re.DOTALL | re.MULTILINE)
    assert m, "diagram %s not found in the slide builder" % name
    return m.group(1).strip()


def revisionize(html, k):
    """A revision page builds its links and label from PAGE_PATH and
    PAGE_LABEL, not from a lecture number (see scripts/units.py)."""
    num = re.search(r"const LECTURE_NUM\s*=\s*%d;" % k, html)
    assert num, "no LECTURE_NUM = %d in the page" % k
    if "const PAGE_PATH" not in html:
        html = (html[:num.end()]
                + '\nconst PAGE_PATH     = "revision/chapter%d";   /* a revision, not a lecture */' % k
                + '\nconst PAGE_LABEL    = "Chapter %d Revision";' % k
                + html[num.end():])
    html = html.replace('"Lecture " + LECTURE_NUM', "PAGE_LABEL")
    html = html.replace('"/lecture" + LECTURE_NUM + "/', '"/" + PAGE_PATH + "/')
    assert '"Lecture " + LECTURE_NUM' not in html and '"/lecture" + LECTURE_NUM' not in html
    return html


def shell():
    t = (ROOT / "templates/handout-template.html").read_text(encoding="utf-8")
    t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    t = (t.replace("__LECTURE_NUM__", "1").replace("__TITLE_HTML__", esc(TITLE))
          .replace("__TITLE_JS__", TITLE)
          .replace("__TOPIC_HTML__", "Programming &amp; Artificial Intelligence")
          .replace("__TOPIC_JS__", "Programming & Artificial Intelligence")
          .replace("__ACCENT__", ACCENT))
    t = revisionize(t, 1)
    head = t[:t.index('<div id="pagesTop"></div>') + len('<div id="pagesTop"></div>')]
    tail = t[t.index("<script>"):]
    return head, tail


def foot():
    return '<div class="foot"><span>Prepared by: Mr. Eissa Islam</span><span class="pageno"></span></div>'


def dg(x):
    return '<div class="dg">' + x + '</div>'


def page(x):
    return '<section class="sheet">' + x + foot() + '</section>'


def masthead(sub):
    return ('<div class="brand" id="brand">Programming &amp; Artificial Intelligence</div>'
            '<h1 id="docTitle">' + esc(TITLE) + '</h1><div class="docsub">' + sub +
            ' &middot; Chapter 1 Revision</div><div class="namebox"><div><span>Name</span><i></i></div>'
            '<div><span>Class</span><i></i></div><div><span>Date</span><i></i></div></div>')


def rules(n=2):
    return ''.join('<div class="rule tight"></div>' for _ in range(n))


def mcq_inline(t):
    """Options written inline as "A: ... B: ..." read as a wall of text on
    paper. Put each on its own line."""
    parts = re.split(r'\s(?=[A-D]:\s)', esc(t))
    if len(parts) < 3:
        return esc(t)
    return parts[0] + ''.join('<span class="opt">' + x + '</span>' for x in parts[1:])


def exercise(n, num=None):
    x = EX[n]
    num = n if num is None else num
    typ = x['type']
    body = rules(3)
    if typ == 'truefalse':
        body = ('<table class="tftbl"><tr><th style="width:14%">&#10003; / &#10005;</th><th>Statement</th></tr>'
                + ''.join('<tr><td class="blank"></td><td>' + esc(a) + '</td></tr>' for a in x['statements'])
                + '</table>')
    elif typ == 'match':
        opts = ''.join('<span class="chip"><b>' + chr(65 + i) + '</b> ' + esc(a) + '</span>'
                       for i, a in enumerate(x['right']))
        body = ('<table class="matchtbl"><tr><th>Description</th><th style="width:18%">Letter</th></tr>'
                + ''.join('<tr><td>' + esc(a) + '</td><td class="blank"></td></tr>' for a in x['left'])
                + '</table><p class="optlead">Choose from:</p><div class="fields">' + opts + '</div>')
    elif typ == 'table':
        body = ('<table><tr>' + ''.join('<th>' + esc(a) + '</th>' for a in x['head']) + '</tr>'
                + ''.join('<tr>' + ''.join(
                    '<td>' + ('' if a.startswith('____') else esc(a)) + '</td>' for a in r)
                    + '</tr>' for r in x['rows']) + '</table>')
    elif typ == 'category':
        body = ('<table class="cattbl"><tr><th style="width:14%">Letter</th><th>Situation</th></tr>'
                + ''.join('<tr><td class="blank"></td><td>' + esc(a) + '</td></tr>' for a in x['items'])
                + '</table>')
    elif typ == 'fill':
        ls = [c for c in 'abcdef' if '( ' + c + ' )' in x['passage']]
        body = ('<p class="passage">' + esc(x['passage']) + '</p><ol class="blanks">'
                + ''.join('<li><b>( ' + c + ' )</b><span class="rule tight"></span></li>' for c in ls)
                + '</ol>')
    elif typ == 'short':
        qs = x.get('questions')
        body = ('<ol class="qs">' + ''.join(
            '<li>' + mcq_inline(q['q']) + rules(q.get('lines', 1)) + '</li>' for q in qs) + '</ol>'
            if qs else rules(3))
    elif typ == 'extended':
        body = '<div class="marks">[' + str(x.get('marks', 6)) + ' marks]</div>' + rules(x.get('lines', 7))
    return ('<div class="ex"><div class="exhead"><span class="exn">' + str(num) + '</span>'
            '<span class="exq">' + esc(x['prompt']) + '</span></div><p class="ar">' + esc(x['promptAr'])
            + '</p><div class="src">' + esc(x['src']) + '</div>' + body + '</div>')


def term(h, p, ar):
    return '<div class="term"><h4>' + h + '</h4><p>' + p + '</p><p class="ar">' + ar + '</p></div>'


def lastpage(kind):
    """Closing sheet, with no QR and no quiz address: the exam is taken in the
    lesson, not at home the night before with an AI to hand."""
    if kind == 'booklet':
        head = ('<h2>What to revise</h2><div class="summary">'
                '<p>Go lesson by lesson: the key takeaway, then every key term word for word, then the exam traps. 1-1: the '
                'five stages in order and the five social changes; 1-2: the four nested layers; 1-3: what AI is good at and '
                'where it needs a human; 1-4: algorithmic bias and the four principles.</p>'
                '<p class="ar">راجع درس درس: الفكرة الأساسية، وبعدين كل مصطلح بالنص، وبعدين فخاخ الامتحان.</p></div>')
    else:
        head = ('<h2>Before you hand this in</h2><div class="summary">'
                '<p>Check every answer against the booklet. Bring anything you could not work out '
                'to the next session.</p>'
                '<p class="ar">راجع كل إجابة على الكتيّب. وأي حاجة معرفتش تحلها هاتها معاك المرة الجاية.</p></div>')
    notes = '<h2>My notes</h2>' + ''.join('<div class="rule"></div>' for _ in range(8))
    exam = ('<div class="summary hw"><p><b>The exam is done in class.</b> Your teacher will show the '
            'code to scan during the lesson.</p>'
            '<p class="ar">الامتحان بيتحل في الحصة. المدرّس هيعرض الكود تمسحوه وقتها.</p></div>')
    return page(head + exam + notes)


# ------------------------------------------------------------------ booklet
def booklet(head, tail):
    """A revision booklet: three pages a lesson, in the deck's order -- the
    book's key takeaway, the lesson's picture and the exam traps; every key
    term with its meaning; the exam question, room to plan it, and its
    marking points. All of it is read from the same
    tools/lectureN/data.py the deck uses, so the two cannot drift. Then the
    class work."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "revdata", str(ROOT / "scripts" / "tools" / T.parent.name.replace("chapter", "revision") / "data.py"))
    # T is revision/chapterK/_teacher; the sources are scripts/tools/revisionK
    D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)

    p = []
    p.append(page(
        masthead('Revision Booklet')
        + '<h2>How to use this booklet</h2>'
        '<p>Three pages for each lesson. Decide each trap true or false before you read the answer; cover the meaning '
        'of each key term and say it before you look; and plan the exam question before you read its points.</p>'
        '<p class="ar">تلات صفحات لكل درس. غطّي عمود المعاني وقول التعريف قبل ما تبص، وقرّر صح ولا غلط قبل ما تقرا الإجابة، '
        'وخطّط سؤال الامتحان قبل ما تقرا النقط.</p>'
        '<h2>The unit at a glance</h2>'
        '<table><tr><th style="width:12%">Lesson</th><th>Remember</th></tr>'
        + ''.join('<tr><td class="k">%s</td><td><b>%s.</b> %s</td></tr>' % (L["id"], L["title"], L["remember"]) for L in D.LESSONS)
        + '</table>'))
    for L in D.LESSONS:
        # 1 · the big idea: the takeaway, the picture, the exam traps
        p.append(page(
            '<h2>%s &middot; %s</h2>' % (L["id"], L["title"])
            + '<div class="summary"><p><b>Remember.</b> %s</p><p class="ar">%s</p></div>' % (L["remember"], L["remember_ar"])
            + dg(slide_svg(L["svg"]))
            + '<h2>Exam traps</h2>'
            + '<table><tr><th>Statement</th><th style="width:12%">T / F</th><th style="width:34%">Why</th></tr>'
            + ''.join('<tr><td>%s</td><td><b>%s</b></td><td>%s</td></tr>' % (st, "True" if ok else "False", why)
                      for st, ok, why in L["traps"])
            + '</table>'))
        # 2 · every key term, with its meaning in English and Arabic
        p.append(page(
            '<h2>%s &middot; Key terms</h2>' % L["id"]
            + '<p>Cover the right-hand column and say each meaning before you look.</p>'
            + '<table><tr><th style="width:27%">Key term</th><th>Meaning</th></tr>'
            + ''.join('<tr><td class="k">%s</td><td>%s<div class="ar tdar">%s</div></td></tr>' % (t, d, a)
                      for t, d, a in L["terms"])
            + '</table>'))
        # 3 · the lesson's exam question, a place to plan, then the points
        ex = L["exam"]
        p.append(page(
            '<h2>%s &middot; Exam-style question &middot; %d marks</h2>' % (L["id"], ex["marks"])
            + '<p><b>%s</b></p><p class="src">%s</p>' % (ex["q"], ex["src"])
            + '<div class="summary hw"><p><b>Plan first.</b> Write your points here, then check them against the '
              'marking points below. Each point is about one mark.</p></div>'
            + rules(7)
            + '<h2>The marking points</h2>'
            + '<ol class="qs">' + ''.join('<li>%s</li>' % x for x in D.POINTS[L["id"]]) + '</ol>'))
    p.append(page('<h2>Class work</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
                  + exercise(1, 1) + exercise(2, 2)))
    p.append(page('<h2>Class work</h2><p class="ar">كمّل مع زميلك.</p>'
                  + exercise(3, 3) + exercise(4, 4)))
    return head + ''.join(p) + lastpage('booklet') + tail


# ----------------------------------------------------------------- homework
def homework(head, tail):
    p = []
    first = True
    for title, titleAr, pages in HW_SECTIONS:
        for j, group in enumerate(pages):
            intro = ''
            if first:
                intro = (masthead('Homework') + '<div class="summary hw"><p>Everything here was taught '
                         'in the session. Bring this sheet to the next class.</p>'
                         '<p class="ar">كل ده اتشرح في الحصة. هات الورقة المرة الجاية.</p></div>')
                first = False
            intro += ('<h2>' + title + '</h2><p class="ar">' + titleAr + '</p>' if j == 0
                      else '<h2>Homework</h2><p class="ar">كمّل بهدوء وراجع الكتيّب لو احتجت.</p>')
            p.append(page(intro + ''.join(exercise(n, HOMEWORK.index(n) + 1) for n in group)))
    return head + ''.join(p) + lastpage('homework') + tail


# --------------------------------------------------------------- answer key
def answer_html(n):
    a = DATA['ANSWERS'].get(str(n))
    out = []
    if isinstance(a, list):
        out.append('<ul>' + ''.join('<li>' + esc(str(x)) + '</li>' for x in a) + '</ul>')
    elif isinstance(a, dict):
        if a.get('marks'):
            out.append('<div class="marks">[' + str(a['marks']) + ' marks]</div>')
        if a.get('open'):
            out.append('<p class="note">Open response &mdash; any reasonable answer, marked on the points below.</p>')
        if a.get('model'):
            out.append('<p><b>Model answer.</b> ' + esc(a['model']) + '</p>')
        if a.get('points'):
            out.append('<p><b>The answer must cover:</b></p><ul>'
                       + ''.join('<li>' + esc(x) + '</li>' for x in a['points']) + '</ul>')
        rest = [(k, v) for k, v in a.items()
                if k not in ('note', 'src', 'marks', 'open', 'model', 'points', 'example', 'marking')]
        if rest:
            out.append('<ul>' + ''.join('<li><b>' + esc(k) + '</b> &mdash; '
                                        + esc(', '.join(v) if isinstance(v, list) else str(v)) + '</li>'
                                        for k, v in rest) + '</ul>')
        if a.get('marking'):
            out.append('<p class="note"><b>Marking.</b> ' + esc(a['marking']) + '</p>')
    elif a is not None:
        out.append('<p>' + esc(str(a)) + '</p>')
    else:
        out.append('<p class="note">Open response &mdash; mark on the points named in the question.</p>')
    return ''.join(out)


KEY_PAGES = [
    ('class', IN_CLASS),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [5, 6, 7, 8]), ('hw', [9, 10, 11, 12]), ('hw', [13, 14, 15, 16]),
    ('hw', [17, 18]), ('hw', [19, 20]),
]


def check_key_order():
    """The key must list homework in the order the student's sheet numbers
    it. Regrouping the homework once left exercise 6 -- numbered 8 on the
    sheet -- between 1 and 2 in the key, and nothing noticed."""
    hw = [n for kind, nums in KEY_PAGES if kind == 'hw' for n in nums]
    assert hw == HOMEWORK, "answer key out of homework order: %s vs %s" % (hw, HOMEWORK)
    cls = [n for kind, nums in KEY_PAGES if kind == 'class' for n in nums]
    assert cls == IN_CLASS, "answer key out of class-work order"


def teacher_warn():
    return '<div class="teacherwarn">Teacher copy &mdash; do not hand this to students.</div>'


def key(head, tail):
    check_key_order()
    pages, seen = [], set()
    for kind, nums in KEY_PAGES:
        b = []
        if not pages:
            b.append(masthead('Teacher Answer Key'))
            b.append(teacher_warn())
        if kind not in seen:
            b.append('<div class="keygroup">%s</div>' % (
                'Class work &mdash; done in the session' if kind == 'class'
                else 'Homework &mdash; separate sheet'))
            seen.add(kind)
        for n in nums:
            i = (IN_CLASS.index(n) + 1) if kind == 'class' else (HOMEWORK.index(n) + 1)
            b.append('<div class="ex"><div class="exhead"><span class="exn">' + str(i) + '</span>'
                     '<span class="exq">' + esc(EX[n]['prompt']) + '</span></div>'
                     '<div class="src">' + esc(EX[n]['src']) + '</div>'
                     '<div class="key">' + answer_html(n) + '</div></div>')
        pages.append(page(''.join(b)))
    return head + ''.join(pages) + tail


# ------------------------------------------------------------ model answers
# For the students, not the teacher: full sentences they can learn from, each
# with an Arabic line saying why -- no marking points. It lives in _teacher/
# so it has no public URL before the homework is in; the teacher prints it
# and hands it out afterwards. Numbered exactly as the student's own sheets.
MODEL_PAGES = [
    ('class', [1]), ('class', [2]), ('class', [3, 4]),
    ('hw', [5, 6, 7]), ('hw', [8]), ('hw', [9, 10, 11]), ('hw', [12]),
    ('hw', [13, 14, 15]), ('hw', [16]), ('hw', [17, 18, 19]), ('hw', [20]),
]


def model_answers(head, tail):
    order = [n for kind, nums in MODEL_PAGES for n in nums]
    assert order == IN_CLASS + HOMEWORK, "model answers out of the sheets' order"
    pages, seen = [], set()
    for kind, nums in MODEL_PAGES:
        b = []
        if not pages:
            b.append(masthead('Model Answers'))
            b.append('<div class="summary hw"><p>Check your own answers against these. Your words do '
                     'not have to match &mdash; the idea does.</p>'
                     '<p class="ar">قارن إجاباتك بدول. مش لازم نفس الكلام بالحرف — المهم الفكرة.</p></div>')
        if kind not in seen:
            b.append('<h2>%s</h2>' % ('Class work' if kind == 'class' else 'Homework'))
            seen.add(kind)
        for n in nums:
            i = (IN_CLASS.index(n) + 1) if kind == 'class' else (HOMEWORK.index(n) + 1)
            rows = ''.join(
                ('<p class="mq-q">' + esc(r['q']) + '</p>' if r.get('q') else '')
                + '<p class="mq-a">' + esc(r['a']) + '</p><p class="ar">' + esc(r['ar']) + '</p>'
                for r in DATA['MODEL'][str(n)])
            b.append('<div class="ex"><div class="exhead"><span class="exn">' + str(i) + '</span>'
                     '<span class="exq">' + esc(EX[n]['prompt']) + '</span></div>'
                     '<div class="key">' + rows + '</div></div>')
        pages.append(page(''.join(b)))
    return head + ''.join(pages) + tail


def name(html, title):
    """Give a printed document its own name. The browser saves a PDF under
    the page title, and the shared template script used to set every
    document's title to "Lecture N Handout", so homework and keys saved
    under the booklet's name. data-title on <body> is what that script now
    reads; the static <title> is set too, for before the script runs."""
    from html import escape as _e
    html = re.sub(r"<title>.*?</title>", "<title>" + _e(title) + "</title>", html, count=1)
    assert html.count("<body>") == 1, "expected one bare <body>"
    return html.replace("<body>", '<body data-title="' + _e(title, quote=True) + '">', 1)


if __name__ == "__main__":
    head, tail = shell()
    LREV = "Chapter 1 Revision %s — " + TITLE
    outs = [
        (ROOT / 'revision/chapter1/handout/index.html', booklet(head, tail), LREV % "Booklet"),
        (ROOT / 'revision/chapter1/homework/index.html', homework(head, tail), LREV % "Homework"),
        (ROOT / 'revision/chapter1/_teacher/answer-key.html', key(head, tail), LREV % "Answer Key"),
        (ROOT / 'revision/chapter1/_teacher/model-answers.html', model_answers(head, tail), LREV % "Model Answers"),
    ]
    for path, html, title in outs:
        html = name(html, title)
        # the template ships author instructions in HTML comments; not ours to publish
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        assert not re.search(r"\{[%{]", html), "Liquid delimiter in " + path.name
        with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print("%-40s %6d bytes, %2d sheets" % (path.relative_to(ROOT), len(html),
                                               html.count('<section class="sheet')))
