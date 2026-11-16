# -*- coding: utf-8 -*-
import io, os
N = 10
TITLE = "How do they talk?"
ACCENT = "#5E6B1F"
BOOK = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "booklet.py"), encoding="utf-8").read()
DOC = '''Generate Lecture 10's printed material.

    python scripts/build_lecture10.py

Writes:
    lecture10/handout/index.html            student booklet: lesson 3-2 + Qureo 32-33 + class work
    lecture10/homework/index.html           take-home exercises
    lecture10/_teacher/answer-key.html      key to the class work and homework
    lecture10/_teacher/model-answers.html   the students' model answers

Content comes from lecture10/_teacher/exercises.json, which lives under
_teacher/ on purpose: Jekyll does not serve underscore-prefixed paths, and
this script is itself unpublished (scripts/ is excluded in _config.yml).

Lesson 3-2, Web Application Communication Methods: the English textbook
pp. 62-67, the Arabic textbook's lesson 3-2 where it goes further, and the
ministry's assessment book for the lesson. Then Qureo chapters 32
(Flowchart) and 33 (review of 31-32). Every exercise names its source. An
exercise may carry `code`, printed as a code box, or `svg`, a flowchart
from the deck (the PATCHES in tools/lecture10/spec.py).

Derived from build_lecture5.py: the same helpers, homework, key and model
answer code, with this lecture's constants, booklet and page plans. Every
printed document is one section.sheet per A4 page; the page lists below are
checked by rendering each sheet on its own.'''
HW = '''HW_SECTIONS = [
    ("Part 1 &middot; Client, server, HTTP and HTTPS",
     "الجزء الأول — العميل والخادم و HTTP و HTTPS",
     # the first sheet also carries the masthead and the intro box
     [[5], [6], [7], [8], [9], [10, 11]]),
    ("Part 2 &middot; Requests, responses and APIs",
     "الجزء التاني — الطلبات والاستجابات وواجهات البرمجة",
     [[12], [13, 14], [15]]),
    ("Part 3 &middot; Apply it",
     "الجزء التالت — طبّق",
     [[16], [17]]),
    ("Part 4 &middot; On the platform: Flowchart",
     "الجزء الرابع — على المنصة: المخطط الانسيابي",
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
                '<p>Learn the client and the server first, then HTTP and HTTPS and why HTTPS is safer. Then GET and POST with '
                'an example of each, the status codes 200, 404 and 500, and what an API and JSON are. On the platform: the '
                'four flowchart symbols, and how a diamond becomes an if ... else.</p>'
                '<p class="ar">احفظ العميل والخادم، و HTTP و HTTPS وليه HTTPS أأمن، و GET و POST بمثال لكل واحد، ورموز الحالة '
                '200 و 404 و 500، ويعني إيه API و JSON. وعلى المنصة: أشكال المخطط الانسيابي الأربعة، وإزاي المعين بيبقى if ... else.</p></div>')"""

# what lecture 5's print code cannot do yet: an exercise's code, printed as a
# box under its source line, and a flowchart from the deck -- on the sheet,
# in the key and in the model answers
CODE_CSS = (".code{font-family:'JetBrains Mono',monospace;font-size:9pt;line-height:1.5;background:#F4F6F8;"
            "border:1px solid var(--line);border-radius:2mm;padding:2.5mm 3.5mm;margin:1.5mm 0 2.5mm 9.5mm;"
            "white-space:pre;font-variant-ligatures:none}"
            ".sheet>.code,.summary .code,.fcrow .code{margin-left:0}"
            ".fcx svg{width:62mm;height:auto;display:block}.ex .fcx{margin:1mm 0 2mm 9.5mm}"
            ".fcrow{display:flex;gap:6mm;align-items:flex-start;margin:2mm 0 3mm}.fcrow>div{flex:1;min-width:0}\n")
PATCHES = [
    ("def shell():",
     "def code_block(x):\n"
     "    return ((('<div class=\"code\">' + esc(x['code']) + '</div>') if x.get('code') else '')\n"
     "            + (('<div class=\"fcx\">' + x['svg'] + '</div>') if x.get('svg') else ''))\n\n\n"
     "def shell():"),
    ("+ '</p><div class=\"src\">' + esc(x['src']) + '</div>' + body + '</div>')",
     "+ '</p><div class=\"src\">' + esc(x['src']) + '</div>' + code_block(x) + body + '</div>')"),
    ("'<div class=\"src\">' + esc(EX[n]['src']) + '</div>'\n                     '<div class=\"key\">' + answer_html(n)",
     "'<div class=\"src\">' + esc(EX[n]['src']) + '</div>' + code_block(EX[n])\n                     + '<div class=\"key\">' + answer_html(n)"),
    ("'<span class=\"exq\">' + esc(EX[n]['prompt']) + '</span></div>'\n                     '<div class=\"key\">' + rows",
     "'<span class=\"exq\">' + esc(EX[n]['prompt']) + '</span></div>' + code_block(EX[n])\n                     + '<div class=\"key\">' + rows"),
    ("EXTRA_CSS = '''\n", "EXTRA_CSS = '''\n" + CODE_CSS),
]
