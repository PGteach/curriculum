# -*- coding: utf-8 -*-
import io, os
N = 11
TITLE = "What is a web page made of?"
ACCENT = "#7A3B69"
BOOK = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "booklet.py"), encoding="utf-8").read()
DOC = '''Generate Lecture 11's printed material.

    python scripts/build_lecture11.py

Writes:
    lecture11/handout/index.html            student booklet: lesson 3-3 + Qureo 34-36 + class work
    lecture11/homework/index.html           take-home exercises
    lecture11/_teacher/answer-key.html      key to the class work and homework
    lecture11/_teacher/model-answers.html   the students' model answers

Content comes from lecture11/_teacher/exercises.json, which lives under
_teacher/ on purpose: Jekyll does not serve underscore-prefixed paths, and
this script is itself unpublished (scripts/ is excluded in _config.yml).

Lesson 3-3, Fundamentals of Frontend Technology: the English textbook pp.
68-74, the Arabic textbook's lesson 3-3 where it goes further, and the
ministry's assessment book for the lesson. Then Qureo chapters 34 HTML (2),
35 CSS (2) and 36 (review of 34-35). A longer lecture: six class exercises,
not four (the IN_CLASS patch below). Every exercise names its source. An
exercise may carry `code`, printed as a code box (the PATCHES below).

Derived from build_lecture5.py: the same helpers, homework, key and model
answer code, with this lecture's constants, booklet and page plans. Every
printed document is one section.sheet per A4 page; the page lists below are
checked by rendering each sheet on its own.'''
HW = '''HW_SECTIONS = [
    ("Part 1 &middot; HTML, CSS, JavaScript and semantic HTML",
     "الجزء الأول — HTML و CSS و JavaScript و HTML الدلالي",
     # the first sheet also carries the masthead and the intro box
     [[7], [8], [9], [10], [11], [12, 13]]),
    ("Part 2 &middot; Explain it",
     "الجزء التاني — اشرح",
     [[14], [15, 16], [17]]),
    ("Part 3 &middot; Apply it",
     "الجزء التالت — طبّق",
     [[18], [19]]),
    ("Part 4 &middot; On the platform: HTML (2) and CSS (2)",
     "الجزء الرابع — على المنصة: HTML (2) و CSS (2)",
     [[20], [21], [22]]),
    ("Challenge &middot; optional",
     "تحدي — اختياري",
     [[23], [24]]),
]
'''
KEY = '''KEY_PAGES = [
    ('class', [1, 2, 3]), ('class', [4, 5, 6]),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [7, 8, 9, 10]), ('hw', [11, 12, 13]), ('hw', [14, 15]),
    ('hw', [16, 17, 18]), ('hw', [19, 20, 21]), ('hw', [22, 23, 24]),
]
'''
MODEL = '''MODEL_PAGES = [
    ('class', [1, 2]), ('class', [3, 4]), ('class', [5, 6]),
    ('hw', [7, 8, 9]), ('hw', [10, 11]), ('hw', [12, 13]), ('hw', [14, 15]),
    ('hw', [16, 17, 18]), ('hw', [19, 20, 21]), ('hw', [22, 23]), ('hw', [24]),
]
'''
REVISE = """        head = ('<h2>What to revise</h2><div class="summary">'
                '<p>Learn the three roles first: HTML structure, CSS appearance, JavaScript behavior. Then semantic HTML '
                '(header, nav, main, footer) and its two benefits, responsive design and mobile-first, and what a framework '
                'is, with React, Vue and Next.js. On the platform: div and span, input and button, and CSS as selector, '
                'property and value &mdash; color, background-color, padding, border-radius, border.</p>'
                '<p class="ar">احفظ الأدوار التلاتة الأول، وبعدين HTML الدلالي وفايدتيه، والتصميم المتجاوب والأولوية للجوال، '
                'ويعني إيه إطار عمل. وعلى المنصة: div و span و input و button، و CSS: محدِّد وخاصية وقيمة.</p></div>')"""

# what lecture 5's print code cannot do yet: an exercise's code, printed as a
# box under its source line -- on the sheet, in the key and in the model
# answers -- and six class exercises instead of four
CODE_CSS = (".code{font-family:'JetBrains Mono',monospace;font-size:9pt;line-height:1.5;background:#F4F6F8;"
            "border:1px solid var(--line);border-radius:2mm;padding:2.5mm 3.5mm;margin:1.5mm 0 2.5mm 9.5mm;"
            "white-space:pre;font-variant-ligatures:none}"
            ".sheet>.code,.summary .code,.fcrow .code{margin-left:0}"
            ".fcrow{display:flex;gap:6mm;align-items:flex-start;margin:2mm 0 3mm}.fcrow>div{flex:1;min-width:0}"
            ".key li,.key .mq-a{white-space:pre-line}\n")
PATCHES = [
    ("IN_CLASS = [1, 2, 3, 4]", "IN_CLASS = [1, 2, 3, 4, 5, 6]"),
    ("def shell():",
     "def code_block(x):\n"
     "    return ('<div class=\"code\">' + esc(x['code']) + '</div>') if x.get('code') else ''\n\n\n"
     "def shell():"),
    ("+ '</p><div class=\"src\">' + esc(x['src']) + '</div>' + body + '</div>')",
     "+ '</p><div class=\"src\">' + esc(x['src']) + '</div>' + code_block(x) + body + '</div>')"),
    ("'<div class=\"src\">' + esc(EX[n]['src']) + '</div>'\n                     '<div class=\"key\">' + answer_html(n)",
     "'<div class=\"src\">' + esc(EX[n]['src']) + '</div>' + code_block(EX[n])\n                     + '<div class=\"key\">' + answer_html(n)"),
    ("'<span class=\"exq\">' + esc(EX[n]['prompt']) + '</span></div>'\n                     '<div class=\"key\">' + rows",
     "'<span class=\"exq\">' + esc(EX[n]['prompt']) + '</span></div>' + code_block(EX[n])\n                     + '<div class=\"key\">' + rows"),
    ("EXTRA_CSS = '''\n", "EXTRA_CSS = '''\n" + CODE_CSS),
]
