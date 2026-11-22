# -*- coding: utf-8 -*-
import io, os
N = 13
TITLE = "Ready for Chapter 2?"
ACCENT = "#36454F"
BOOK = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "booklet.py"), encoding="utf-8").read()
DOC = '''Generate Lecture 13's printed material: the Chapter 2 revision.

    python scripts/build_lecture13.py

Writes:
    lecture13/handout/index.html            revision booklet: two pages a lesson + class work
    lecture13/homework/index.html           revision exercises, lesson by lesson
    lecture13/_teacher/answer-key.html      key to the class work and homework
    lecture13/_teacher/model-answers.html   the students' model answers

Content comes from lecture13/_teacher/exercises.json, which lives under
_teacher/ on purpose: Jekyll does not serve underscore-prefixed paths, and
this script is itself unpublished (scripts/ is excluded in _config.yml).

Unit 2, lessons 2-1 to 2-3. Nothing new: the booklet reads
tools/lecture13/data.py (the book's key takeaways and key terms, the exam
traps, each lesson's exam question and marking points), and every exercise
is taken, with its answers, from the lecture that taught its lesson
(tools/lecture13/exercises.py).

Derived from build_lecture5.py: the same helpers, homework, key and model
answer code, with this lecture's constants, booklet and page plans. Every
printed document is one section.sheet per A4 page; the page lists below are
checked by rendering each sheet on its own.'''
HW = '''HW_SECTIONS = [
    ("Lesson 2-1 &middot; Cryptographic technologies and authentication",
     "الدرس 2-1 — تقنيات التشفير والمصادقة",
     # the first sheet also carries the masthead and the intro box
     [[5], [6, 7], [8]]),
    ("Lesson 2-2 &middot; Network security design",
     "الدرس 2-2 — تصميم أمن الشبكات",
     [[9, 10], [11], [12]]),
    ("Lesson 2-3 &middot; Incident response and risk management",
     "الدرس 2-3 — الاستجابة للحوادث وإدارة المخاطر",
     [[13, 14], [15], [16]]),
    ("Mixed &middot; from the ministry's assessments",
     "مراجعة متنوعة — من كتاب التقييمات",
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
                '<p>Go lesson by lesson: the key takeaway, then every key term word for word, then the exam traps. 2-1: which '
                'key does what in HTTPS, the four technologies and the threat each stops, the three factors; 2-2: the five '
                'terms and the four layers; 2-3: the six stages in order and risk = impact &times; likelihood.</p>'
                '<p class="ar">راجع درس درس: الفكرة الأساسية، وبعدين كل مصطلح بالنص، وبعدين فخاخ الامتحان.</p></div>')"""

# the booklet puts each term's Arabic under its English, inside the table cell
PATCHES = [
    ("EXTRA_CSS = '''\n", "EXTRA_CSS = '''\n.tdar{font-size:9pt;color:var(--soft);margin-top:.6mm}\n"),
]
