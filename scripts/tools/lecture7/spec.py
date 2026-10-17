# -*- coding: utf-8 -*-
import io, os
N = 7
TITLE = "When something goes wrong"
ACCENT = "#4F55B8"
BOOK = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "booklet.py"), encoding="utf-8").read()
DOC = '''Generate Lecture 7's printed material.

    python scripts/build_lecture7.py

Writes:
    lecture7/handout/index.html            student booklet: lesson 2-3 + class work
    lecture7/homework/index.html           take-home exercises
    lecture7/_teacher/answer-key.html      key to the class work and homework
    lecture7/_teacher/model-answers.html   the students' model answers

Content comes from lecture7/_teacher/exercises.json, which lives under
_teacher/ on purpose: Jekyll does not serve underscore-prefixed paths, and
this script is itself unpublished (scripts/ is excluded in _config.yml).

Everything is lesson 2-3, Incident Response and Risk Management: the English
textbook pp. 48-54, the Arabic textbook pp. 44-49 where it goes further, and
the ministry's assessment book for the lesson. Every exercise names its source.

Derived from build_lecture5.py: the same helpers, homework, key and model
answer code, with this lecture's constants, booklet and page plans. Every
printed document is one section.sheet per A4 page; the page lists below are
checked by rendering each sheet on its own.'''
HW = '''HW_SECTIONS = [
    ("Part 1 &middot; Security incidents and the six stages",
     "الجزء الأول — الحوادث الأمنية والمراحل الست",
     # the first sheet also carries the masthead and the intro box
     [[5], [8, 13], [10, 14], [7]]),
    ("Part 2 &middot; Risk assessment",
     "الجزء التاني — تقييم المخاطر",
     [[6, 9], [11], [12]]),
    ("Part 3 &middot; Apply it",
     "الجزء التالت — طبّق",
     [[15, 16], [17, 18]]),
    ("Challenge &middot; optional",
     "تحدي — اختياري",
     [[19, 20]]),
]
'''
KEY = '''KEY_PAGES = [
    ('class', IN_CLASS),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [5, 8, 13]), ('hw', [10, 14, 7]), ('hw', [6, 9, 11]),
    ('hw', [12, 15, 16]), ('hw', [17, 18]), ('hw', [19, 20]),
]
'''
MODEL = '''MODEL_PAGES = [
    ('class', [1]), ('class', [2, 3, 4]),
    ('hw', [5, 8, 13]), ('hw', [10, 14, 7]), ('hw', [6, 9, 11]),
    ('hw', [12, 15, 16]), ('hw', [17, 18, 19, 20]),
]
'''
REVISE = """        head = ('<h2>What to revise</h2><div class="summary">'
                '<p>Learn the six stages in order first, with what each one does &mdash; and stage 6 by both its names. '
                'Then why containment comes before eradication, and recovery after it; the three types of incident; and '
                'risk = impact &times; likelihood, with how to rank risks by it.</p>'
                '<p class="ar">احفظ المراحل الست بالترتيب وكل مرحلة بتعمل إيه، والمرحلة السادسة باسميها. وبعدين ليه '
                'الاحتواء قبل الاستئصال، وأنواع الحوادث التلاتة، والخطر = التأثير × الاحتمالية وإزاي نرتّب بيه.</p></div>')"""
