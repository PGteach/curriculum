# -*- coding: utf-8 -*-
import io, os
N = 6
TITLE = "What if one wall falls?"
ACCENT = "#B5531C"
BOOK = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "booklet.py"), encoding="utf-8").read()
DOC = '''Generate Lecture 6's printed material.

    python scripts/build_lecture6.py

Writes:
    lecture6/handout/index.html            student booklet: lesson 2-2 + class work
    lecture6/homework/index.html           take-home exercises
    lecture6/_teacher/answer-key.html      key to the class work and homework
    lecture6/_teacher/model-answers.html   the students' model answers

Content comes from lecture6/_teacher/exercises.json, which lives under
_teacher/ on purpose: Jekyll does not serve underscore-prefixed paths, and
this script is itself unpublished (scripts/ is excluded in _config.yml).

Everything is lesson 2-2, Network Security Design: the English textbook
pp. 41-47, the Arabic textbook pp. 38-43 where it goes further, and the
ministry's assessment book for the lesson. Every exercise names its source.

Derived from build_lecture5.py: the same helpers, homework, key and model
answer code, with this lecture's constants, booklet and page plans. Every
printed document is one section.sheet per A4 page; the page lists below are
checked by rendering each sheet on its own.'''
HW = '''HW_SECTIONS = [
    ("Part 1 &middot; Firewall, VPN and DMZ",
     "الجزء الأول — جدار الحماية والـ VPN والمنطقة المعزولة",
     # the first sheet also carries the masthead and the intro box
     [[5], [6, 8], [12, 13]]),
    ("Part 2 &middot; Defense in depth and zero trust",
     "الجزء التاني — الدفاع في العمق ونهج انعدام الثقة",
     [[9, 10], [11], [7, 14], [15, 18]]),
    ("Part 3 &middot; Apply it",
     "الجزء التالت — طبّق",
     [[16, 17]]),
    ("Challenge &middot; optional",
     "تحدي — اختياري",
     [[19, 20]]),
]
'''
KEY = '''KEY_PAGES = [
    ('class', IN_CLASS),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [5, 6, 8]), ('hw', [12, 13, 9]), ('hw', [10, 11, 7]),
    ('hw', [14, 15]), ('hw', [18, 16]), ('hw', [17, 19, 20]),
]
'''
MODEL = '''MODEL_PAGES = [
    ('class', [1]), ('class', [2, 3, 4]),
    ('hw', [5, 6, 8]), ('hw', [12, 13, 9]), ('hw', [10, 11, 7]),
    ('hw', [14, 15, 18]), ('hw', [16, 17, 19, 20]),
]
'''
REVISE = """        head = ('<h2>What to revise</h2><div class="summary">'
                '<p>Learn the five terms word for word first &mdash; firewall, VPN, DMZ, defense in depth, zero trust '
                '&mdash; then the four layers with the measure in each, and why a DMZ protects the internal network. '
                'Then the perimeter: what it was, and why cloud and remote work blurred it.</p>'
                '<p class="ar">احفظ الخمس مصطلحات بالتعريف الأول، وبعدين الطبقات الأربعة وإجراء كل طبقة، وليه المنطقة '
                'المعزولة بتحمي الشبكة الداخلية، وبعدين المحيط الأمني وليه بقى مش كفاية.</p></div>')"""
