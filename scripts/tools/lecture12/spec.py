# -*- coding: utf-8 -*-
import io, os
N = 12
TITLE = "Ready for Chapter 1?"
ACCENT = "#8A2B2B"
BOOK = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "booklet.py"), encoding="utf-8").read()
DOC = '''Generate Lecture 12's printed material: the Chapter 1 revision.

    python scripts/build_lecture12.py

Writes:
    lecture12/handout/index.html            revision booklet: two pages a lesson + class work
    lecture12/homework/index.html           revision exercises, lesson by lesson
    lecture12/_teacher/answer-key.html      key to the class work and homework
    lecture12/_teacher/model-answers.html   the students' model answers

Content comes from lecture12/_teacher/exercises.json, which lives under
_teacher/ on purpose: Jekyll does not serve underscore-prefixed paths, and
this script is itself unpublished (scripts/ is excluded in _config.yml).

Unit 1, lessons 1-1 to 1-4. Nothing new: the booklet reads
tools/lecture12/data.py (the book's key takeaways and key terms, the exam
traps, each lesson's exam question and marking points), and every exercise
is taken, with its answers, from the lecture that taught its lesson
(tools/lecture12/exercises.py).

Derived from build_lecture5.py: the same helpers, homework, key and model
answer code, with this lecture's constants, booklet and page plans. Every
printed document is one section.sheet per A4 page; the page lists below are
checked by rendering each sheet on its own.'''
HW = '''HW_SECTIONS = [
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
'''
KEY = '''KEY_PAGES = [
    ('class', IN_CLASS),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [5, 6, 7, 8]), ('hw', [9, 10, 11, 12]), ('hw', [13, 14, 15, 16]),
    ('hw', [17, 18]), ('hw', [19, 20]),
]
'''
MODEL = '''MODEL_PAGES = [
    ('class', [1]), ('class', [2]), ('class', [3, 4]),
    ('hw', [5, 6, 7]), ('hw', [8]), ('hw', [9, 10, 11]), ('hw', [12]),
    ('hw', [13, 14, 15]), ('hw', [16]), ('hw', [17, 18, 19]), ('hw', [20]),
]
'''
REVISE = """        head = ('<h2>What to revise</h2><div class="summary">'
                '<p>Go lesson by lesson: the key takeaway, then every key term word for word, then the exam traps. 1-1: the '
                'five stages in order and the five social changes; 1-2: the four nested layers; 1-3: what AI is good at and '
                'where it needs a human; 1-4: algorithmic bias and the four principles.</p>'
                '<p class="ar">راجع درس درس: الفكرة الأساسية، وبعدين كل مصطلح بالنص، وبعدين فخاخ الامتحان.</p></div>')"""

# the booklet puts each term's Arabic under its English, inside the table cell
PATCHES = [
    ("EXTRA_CSS = '''\n", "EXTRA_CSS = '''\n.tdar{font-size:9pt;color:var(--soft);margin-top:.6mm}\n"),
]
