# -*- coding: utf-8 -*-
import io, os
N = 9
TITLE = "What happens when you click?"
ACCENT = "#7D5A1E"
BOOK = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "booklet.py"), encoding="utf-8").read()
DOC = '''Generate Lecture 9's printed material.

    python scripts/build_lecture9.py

Writes:
    lecture9/handout/index.html            student booklet: lesson 3-1 + Qureo 31 + class work
    lecture9/homework/index.html           take-home exercises
    lecture9/_teacher/answer-key.html      key to the class work and homework
    lecture9/_teacher/model-answers.html   the students' model answers

Content comes from lecture9/_teacher/exercises.json, which lives under
_teacher/ on purpose: Jekyll does not serve underscore-prefixed paths, and
this script is itself unpublished (scripts/ is excluded in _config.yml).

Lesson 3-1, The Overall Structure of Web Applications: the English textbook
pp. 56-61, the Arabic textbook's lesson 3-1 where it goes further, and the
ministry's assessment book for the lesson. Then Qureo chapter 31, Functions
(4). Every exercise names its source. An exercise may carry `code`, printed
as a code box under its source line (the PATCHES in tools/lecture9/spec.py).

Derived from build_lecture5.py: the same helpers, homework, key and model
answer code, with this lecture's constants, booklet and page plans. Every
printed document is one section.sheet per A4 page; the page lists below are
checked by rendering each sheet on its own.'''
HW = '''HW_SECTIONS = [
    ("Part 1 &middot; Web applications and the three tiers",
     "الجزء الأول — تطبيقات الويب والطبقات التلاتة",
     # the first sheet also carries the masthead and the intro box
     [[5], [6, 7], [8], [9], [10, 11]]),
    ("Part 2 &middot; How the tiers cooperate",
     "الجزء التاني — إزاي الطبقات بتتعاون",
     [[12], [13, 14], [15]]),
    ("Part 3 &middot; Apply it",
     "الجزء التالت — طبّق",
     [[16], [17]]),
    ("Part 4 &middot; On the platform: Functions (4)",
     "الجزء الرابع — على المنصة: الدوال (4)",
     [[18], [19]]),
    ("Challenge &middot; optional",
     "تحدي — اختياري",
     [[20]]),
]
'''
KEY = '''KEY_PAGES = [
    ('class', [1, 2]), ('class', [3, 4]),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [5, 6, 7, 8]), ('hw', [9, 10, 11]), ('hw', [12, 13]),
    ('hw', [14, 15]), ('hw', [16, 17]), ('hw', [18, 19, 20]),
]
'''
MODEL = '''MODEL_PAGES = [
    ('class', [1]), ('class', [2, 3]), ('class', [4]),
    ('hw', [5, 6]), ('hw', [7, 8]), ('hw', [9, 10, 11]), ('hw', [12, 13]),
    ('hw', [14, 15, 16]), ('hw', [17, 18]), ('hw', [19, 20]),
]
'''
REVISE = """        head = ('<h2>What to revise</h2><div class="summary">'
                '<p>Learn what a web application is, then the three tiers by their roles: the frontend shows and collects, '
                'the backend decides and processes, the database stores and retrieves. Then the six steps of a search, '
                'and which tier does each job on a video site, a social network and a shop. On the platform: a function '
                'takes arguments and gives back a return value.</p>'
                '<p class="ar">احفظ تعريف تطبيق الويب، والطبقات التلاتة بأدوارها، وخطوات البحث الست، وكل طبقة بتعمل إيه في '
                'موقع الفيديو والتواصل والتسوق. وعلى المنصة: الدالة بتاخد وسائط وترجّع قيمة.</p></div>')"""

# what lecture 5's print code cannot do yet: an exercise's code, printed as a
# box under its source line -- on the sheet, in the key and in the model answers
CODE_CSS = (".code{font-family:'JetBrains Mono',monospace;font-size:9pt;line-height:1.5;background:#F4F6F8;"
            "border:1px solid var(--line);border-radius:2mm;padding:2.5mm 3.5mm;margin:1.5mm 0 2.5mm 9.5mm;"
            "white-space:pre;font-variant-ligatures:none}"
            ".sheet>.code,.summary .code{margin-left:0}\n")
PATCHES = [
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
