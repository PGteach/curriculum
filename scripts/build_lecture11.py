#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Lecture 11's printed material.

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
checked by rendering each sheet on its own.
"""
import io, json, re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "lecture11" / "_teacher"
DATA = json.loads((T / "exercises.json").read_text(encoding="utf-8"))
EX = {x["n"]: x for x in DATA["SHEET"]["parts"][0]["exercises"]}

TITLE = "What is a web page made of?"
ACCENT = "#7A3B69"

# Class work: the book's Worked Example and Try, all quick to mark together.
IN_CLASS = [1, 2, 3, 4, 5, 6]

HW_SECTIONS = [
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
HOMEWORK = [n for _, _, pages in HW_SECTIONS for g in pages for n in g]

EXTRA_CSS = '''
.code{font-family:'JetBrains Mono',monospace;font-size:9pt;line-height:1.5;background:#F4F6F8;border:1px solid var(--line);border-radius:2mm;padding:2.5mm 3.5mm;margin:1.5mm 0 2.5mm 9.5mm;white-space:pre;font-variant-ligatures:none}.sheet>.code,.summary .code,.fcrow .code{margin-left:0}.fcrow{display:flex;gap:6mm;align-items:flex-start;margin:2mm 0 3mm}.fcrow>div{flex:1;min-width:0}.key li,.key .mq-a{white-space:pre-line}
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
    src = (ROOT / "scripts" / "build_lecture11_slides.py").read_text(encoding="utf-8")
    m = re.search(r"^%s = '''(.*?)'''" % name, src, re.DOTALL | re.MULTILINE)
    assert m, "diagram %s not found in the slide builder" % name
    return m.group(1).strip()


def code_block(x):
    return ('<div class="code">' + esc(x['code']) + '</div>') if x.get('code') else ''


def shell():
    t = (ROOT / "templates/handout-template.html").read_text(encoding="utf-8")
    t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    t = (t.replace("__LECTURE_NUM__", "11").replace("__TITLE_HTML__", esc(TITLE))
          .replace("__TITLE_JS__", TITLE)
          .replace("__TOPIC_HTML__", "Programming &amp; Artificial Intelligence")
          .replace("__TOPIC_JS__", "Programming & Artificial Intelligence")
          .replace("__ACCENT__", ACCENT))
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
            ' &middot; Lecture 11</div><div class="namebox"><div><span>Name</span><i></i></div>'
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
            + '</p><div class="src">' + esc(x['src']) + '</div>' + code_block(x) + body + '</div>')


def term(h, p, ar):
    return '<div class="term"><h4>' + h + '</h4><p>' + p + '</p><p class="ar">' + ar + '</p></div>'


def lastpage(kind):
    """Closing sheet, with no QR and no quiz address: the exam is taken in the
    lesson, not at home the night before with an AI to hand."""
    if kind == 'booklet':
        head = ('<h2>What to revise</h2><div class="summary">'
                '<p>Learn the three roles first: HTML structure, CSS appearance, JavaScript behavior. Then semantic HTML '
                '(header, nav, main, footer) and its two benefits, responsive design and mobile-first, and what a framework '
                'is, with React, Vue and Next.js. On the platform: div and span, input and button, and CSS as selector, '
                'property and value &mdash; color, background-color, padding, border-radius, border.</p>'
                '<p class="ar">احفظ الأدوار التلاتة الأول، وبعدين HTML الدلالي وفايدتيه، والتصميم المتجاوب والأولوية للجوال، '
                'ويعني إيه إطار عمل. وعلى المنصة: div و span و input و button، و CSS: محدِّد وخاصية وقيمة.</p></div>')
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
    """The booklet follows the deck slide by slide, in the same order, so what
    a student revises from is what they were taught from. The slide numbers
    in the comments are the deck's; keep them in step when either changes.
    The live demos print as tables and as the code students typed. The
    title and the exam QR have no page."""
    LAYERS, SEMANTIC = slide_svg("LAYERS"), slide_svg("SEMANTIC")

    def code(t):
        return '<div class="code">' + esc(t) + '</div>'

    p = []
    # slides 2-6: recap, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Before we start &middot; lesson 3-2</h2>'
        '<table><tr><th style="width:26%">Word</th><th>Meaning</th></tr>'
        '<tr><td class="k">Client / server</td><td>the client requests, the server responds</td></tr>'
        '<tr><td class="k">HTTP / HTTPS</td><td>the rules for the messages; HTTPS adds TLS encryption</td></tr>'
        '<tr><td class="k">GET / POST</td><td>retrieve data / send data</td></tr>'
        '<tr><td class="k">200 / 404 / 500</td><td>success / not found / server error</td></tr></table>'
        '<h2>Three technologies at work</h2>'
        '<p>Open any web page and you are seeing three technologies at work together. HTML builds the structure &mdash; the '
        'headings, paragraphs and links, like the frame of a building. CSS adds the appearance &mdash; colours, layout and '
        'fonts, like a building&#8217;s interior. JavaScript adds behavior &mdash; search boxes that respond, buttons that '
        'count, screens that update.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> How do HTML, CSS, and JavaScript work together to build a web '
        'page, and what makes a modern frontend meaningful, adaptable, and efficient to build?</p>'
        '<p class="ar">إزاي HTML و CSS و JavaScript بيشتغلوا مع بعض عشان يبنوا صفحة ويب، وإيه اللي بيخلي الواجهة الأمامية الحديثة ليها معنى وقابلة للتكيف وفعّالة؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> On a page you use often, point to one thing that is '
        'structure, one that is style, and one that reacts to you.</p>'
        '<p class="ar">اكتبوا التلاتة قبل ما تكمّلوا.</p></div>'))
    # slides 7-10: the three roles, watch the layers
    p.append(page(
        '<h2>Part 1 &middot; The roles of HTML, CSS, and JavaScript</h2>'
        + dg(LAYERS)
        + '<table><tr><th style="width:16%">Technology</th><th>Role</th><th style="width:28%">Analogy</th></tr>'
        '<tr><td class="k">HTML</td><td>Defines the structure (skeleton): headings, paragraphs, images, links</td><td>The frame of a building</td></tr>'
        '<tr><td class="k">CSS</td><td>Specifies the appearance: colours, layout, size, fonts</td><td>The interior and exterior</td></tr>'
        '<tr><td class="k">JavaScript</td><td>Adds behavior and interactivity: responds to buttons, updates part of the screen</td><td>The electrical and plumbing systems</td></tr></table>'
        '<p class="ar">والصفحة مش لازم تستخدم التلاتة: ممكن HTML لوحده، أو HTML مع CSS و JavaScript حسب اللي محتاجاه.</p>'
        '<h2>Switch on the layers</h2>'
        '<table><tr><th style="width:22%">Stage</th><th>What you see</th></tr>'
        '<tr><td class="k">HTML only</td><td>The content and its structure: a heading, a paragraph, a button. No colours; the button does nothing.</td></tr>'
        '<tr><td class="k">+ CSS</td><td>The same content with colours, spacing and a styled button. The button still does nothing.</td></tr>'
        '<tr><td class="k">+ JavaScript</td><td>Now the button responds: press it and the count goes up.</td></tr></table>'))
    # slides 10-13: your turn, true or false, match, semantic HTML defined
    p.append(page(
        '<table><tr><th>Task</th><th style="width:22%">Technology</th></tr>'
        '<tr><td>Describing the structure of headings and paragraphs</td><td>HTML</td></tr>'
        '<tr><td>Changing the colour and size of text</td><td>CSS</td></tr>'
        '<tr><td>Updating part of the screen when a button is pressed</td><td>JavaScript</td></tr>'
        '<tr><td>Placing images and links</td><td>HTML</td></tr>'
        '<tr><td>Setting the background colour of the whole page</td><td>CSS</td></tr>'
        '<tr><td>Validating what is entered into a form</td><td>JavaScript</td></tr></table>'
        '<table><tr><th>True or false?</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>HTML defines the structure (skeleton) of a web page.</td><td>True</td></tr>'
        '<tr><td>CSS adds behavior to a web page.</td><td><b>False</b> &mdash; behavior is JavaScript</td></tr>'
        '<tr><td>Responsive design adjusts the layout to different screen sizes.</td><td>True</td></tr>'
        '<tr><td>A framework means you do not write all the code from scratch.</td><td>True</td></tr></table>'
        '<h2>Part 2 &middot; Semantic HTML</h2>'
        + term('Semantic HTML', 'Describing each part of a web page with element names (tags) that show their meaning: '
               '<header> at the top, <nav> for navigation, <main> for the body, <footer> at the bottom.',
               'HTML الدلالي: استخدام عناصر بتوضح وظيفة أجزاء الصفحة.')))
    # slides 13-15: the skeleton, benefits, two ways
    p.append(page(
        dg(SEMANTIC)
        + '<table><tr><th style="width:24%">Benefit</th><th>What it means</th></tr>'
        '<tr><td class="k">Accessibility</td><td>Screen readers understand the page&#8217;s structure, so information reaches users with visual impairments more easily.</td></tr>'
        '<tr><td class="k">SEO</td><td>Search engines understand the content more easily, so it is more likely to be shown properly in results.</td></tr></table>'
        '<p class="ar">الكتاب العربي: HTML الدلالي بيساعد محركات البحث لكنه مش بيضمن ترتيب أعلى، والوصول محتاج ممارسات تانية كمان.</p>'
        '<div class="fcrow"><div><b>Plain boxes</b>'
        + code('<div>Science Club</div>\n<div>Home | Events</div>\n<div>Robot day ...</div>\n<div>© 2026</div>')
        + '</div><div><b>Semantic HTML</b>'
        + code('<header>Science Club</header>\n<nav>Home | Events</nav>\n<main>Robot day ...</main>\n<footer>© 2026</footer>')
        + '</div></div>'))
    # slides 16-18: which element, responsive design, mobile first
    p.append(page(
        '<table><tr><th style="width:24%">Element</th><th>Used for</th></tr>'
        '<tr><td class="k">&lt;header&gt;</td><td>the top of the page</td></tr>'
        '<tr><td class="k">&lt;nav&gt;</td><td>navigating between the parts of the site</td></tr>'
        '<tr><td class="k">&lt;main&gt;</td><td>the main content</td></tr>'
        '<tr><td class="k">&lt;footer&gt;</td><td>the bottom of the page</td></tr></table>'
        '<p>&lt;E-mail&gt; is <b>not</b> an element &mdash; the assessment book asks for the odd one out.</p>'
        '<h2>Part 3 &middot; Responsive design</h2>'
        + term('Responsive design', 'A design concept in which the layout is automatically adjusted to different screen sizes '
               'such as PCs, smartphones and tablets. One page, easy to view on any device.',
               'التصميم المتجاوب: التخطيط بيتظبط تلقائيًا حسب حجم الشاشة.')
        + '<table><tr><th style="width:20%">Screen</th><th>The same three boxes</th></tr>'
        '<tr><td class="k">Phone</td><td>one column: the boxes stack</td></tr>'
        '<tr><td class="k">Tablet</td><td>two side by side, the third below</td></tr>'
        '<tr><td class="k">PC</td><td>all three in one row</td></tr></table>'
        '<p><b>Mobile-first:</b> many people use the web on their phones, so developers think about small screens from the '
        'very start of the design.</p>'))
    # slides 19-20: frameworks, exam warning
    p.append(page(
        '<h2>Frameworks</h2>'
        + term('Framework', 'A structure that provides common functions and components in advance, to make web application '
               'development more efficient &mdash; you do not write everything from scratch.',
               'إطار العمل: وظايف ومكونات جاهزة عشان التطوير يبقى أكفأ.')
        + '<table><tr><th style="width:16%">Name</th><th>What to know</th></tr>'
        '<tr><td class="k">React</td><td>From Meta. Updates only part of the screen; a JavaScript library for interfaces built from reusable components.</td></tr>'
        '<tr><td class="k">Vue</td><td>A simple structure; build step by step from small features.</td></tr>'
        '<tr><td class="k">Next.js</td><td>Built on React; adds routing and faster ways to show pages.</td></tr></table>'
        '<table><tr><th>Looks right, but is false</th><th style="width:36%">Why</th></tr>'
        '<tr><td>Semantic HTML necessarily makes a page display faster.</td><td>Its benefits are accessibility and SEO.</td></tr>'
        '<tr><td>A framework is a language for defining the structure of a page.</td><td>That is HTML.</td></tr>'
        '<tr><td>Responsive design means the page works only on computers.</td><td>It adapts to every screen.</td></tr></table>'))
    # slides 20-25: exam warning, exam-style, engineer, new context, takeaway, unit 3
    p.append(page(
        '<div class="summary"><p><b>Exam-style question &middot; 6 marks.</b> Explain how HTML, CSS, and JavaScript each '
        'contribute to a library page that lists books, is styled, and filters the results as the user types. Refer to: '
        'structure, appearance, behavior.</p></div>'
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A student club wants a page that lists its events, uses the club&#8217;s colours, and has '
        'a button showing how many have signed up. Which technology does each? One change for phones, one semantic choice '
        'for a screen reader. Separate the three or not &mdash; two reasons.</p>'
        '<p class="ar">تلميح: HTML بيحمل المحتوى، CSS بينسّقه، JavaScript بيخليه يتفاعل ويتحدّث.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A news site must look good on phones and be found easily by search engines. One '
        'responsive-design choice and one semantic-HTML choice, and what each improves.</p></div>'
        '<h2>Key takeaway &middot; lesson 3-3</h2><div class="summary">'
        '<p>HTML structures, CSS styles, JavaScript behaves &mdash; and semantic HTML, responsive design and frameworks make a '
        'modern frontend meaningful, adaptable and efficient.</p></div>'
        '<table><tr><th style="width:12%">Unit 3</th><th>What to know</th></tr>'
        '<tr><td class="k">3-1</td><td>Frontend, backend, database &mdash; three tiers cooperating</td></tr>'
        '<tr><td class="k">3-2</td><td>Client and server, HTTP/HTTPS, GET/POST, status codes, API and JSON</td></tr>'
        '<tr><td class="k">3-3</td><td>HTML, CSS, JavaScript; semantic HTML, responsive design, frameworks</td></tr></table>'))
    # slides 26-32: Qureo 34, HTML (2)
    p.append(page(
        '<h2>Part 4 &middot; On the platform: HTML (2) (Qureo chapter 34)</h2>'
        '<p>An <b>element</b> is an opening tag, the content, and a closing tag.</p>'
        + code('<h1>Science Club</h1>\n<p>We build robots every Thursday.</p>\n<a href="events.html">See the events</a>')
        + '<table><tr><th style="width:24%">Tag</th><th>Makes</th></tr>'
        '<tr><td class="k">&lt;h1&gt;</td><td>a big heading</td></tr>'
        '<tr><td class="k">&lt;p&gt;</td><td>a paragraph</td></tr>'
        '<tr><td class="k">&lt;a href="..."&gt;</td><td>a link to another page</td></tr></table>'
        '<h2>Specifying ranges: div and span</h2>'
        + code('<div class="card">\n  <h3>Robot day</h3>\n  <p>Thursday, 2 pm</p>\n</div>\n\n<p>Bring your <span class="hot">own laptop</span>.</p>')
        + '<table><tr><th style="width:24%">Tag</th><th>Marks</th></tr>'
        '<tr><td class="k">&lt;div&gt;</td><td>a block: a box that holds several elements</td></tr>'
        '<tr><td class="k">&lt;span&gt;</td><td>a range inside a line of text</td></tr></table>'
        '<h2>Input fields and buttons</h2>'
        + code('<input type="text" placeholder="Your name">\n<button>Sign up</button>')
        + '<p><b>placeholder</b> shows a grey hint until the user types. &lt;input&gt; has no closing tag; &lt;button&gt; does.</p>'))
    # slides 33-39: Qureo 35, CSS (2)
    p.append(page(
        '<h2>Part 5 &middot; On the platform: CSS (2) (Qureo chapter 35)</h2>'
        + code('button {\n  color: white;\n  background-color: green;\n}')
        + '<table><tr><th style="width:20%">Part</th><th style="width:30%">In the example</th><th>It says</th></tr>'
        '<tr><td class="k">selector</td><td>button</td><td><b>which</b> part to change</td></tr>'
        '<tr><td class="k">property</td><td>background-color</td><td><b>what</b> to change</td></tr>'
        '<tr><td class="k">value</td><td>green</td><td><b>how</b> to change it</td></tr></table>'
        '<p>A class selector starts with a dot: <b>.big { ... }</b> styles every element with class="big".</p>'
        '<h2>Decorating a button, adding borders</h2>'
        + code('button {\n  background-color: #2D7A4B;\n  color: white;\n  font-size: 20px;\n  padding: 12px 28px;\n  border-radius: 30px;\n  border: 3px solid black;\n}')
        + '<table><tr><th style="width:28%">Property</th><th>Changes</th></tr>'
        '<tr><td class="k">background-color</td><td>the colour behind the text</td></tr>'
        '<tr><td class="k">color</td><td>the colour of the text</td></tr>'
        '<tr><td class="k">font-size</td><td>the size of the text</td></tr>'
        '<tr><td class="k">padding</td><td>the space inside, around the text</td></tr>'
        '<tr><td class="k">border-radius</td><td>how round the corners are</td></tr>'
        '<tr><td class="k">border</td><td>the line around it: width, style (solid, dashed, dotted), colour</td></tr></table>'))
    # slides 40-43: Qureo 36, review, what we learned
    p.append(page(
        '<h2>Part 6 &middot; Review of chapters 34-35 (Qureo chapter 36)</h2>'
        '<p>A sign-up card that puts them together:</p>'
        + code('<div class="card">\n  <h2>Science Club</h2>\n  <p>Join us on <span class="hot">Thursday</span>!</p>\n'
               '  <input type="text" placeholder="Your name">\n  <button>Sign up</button>\n</div>\n\n<style>\n'
               '  .card {\n    border: 3px solid #7A3B69;\n    border-radius: 12px;\n    padding: 16px;\n  }\n</style>')
        + '<table><tr><th>Quick-fire</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>The tag for a text box</td><td>&lt;input&gt;</td></tr>'
        '<tr><td>The tag that marks a range inside a sentence</td><td>&lt;span&gt;</td></tr>'
        '<tr><td>In p { color: blue; }, the property</td><td>color</td></tr>'
        '<tr><td>The property that adds space inside a button</td><td>padding</td></tr>'
        '<tr><td>Making the button count sign-ups</td><td>JavaScript</td></tr></table>'
        '<h2>What we learned</h2><div class="summary">'
        '<p>HTML structures, CSS styles, JavaScript behaves. Semantic HTML helps accessibility and SEO. Responsive design fits '
        'every screen; frameworks give ready-made parts.</p>'
        '<p>div and span mark ranges; input and button let the user type and press. CSS: selector { property: value; }.</p></div>'))
    p.append(page('<h2>Class work</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
                  + exercise(1, 1) + exercise(2, 2)))
    p.append(page('<h2>Class work</h2><p class="ar">كمّل مع زميلك.</p>'
                  + exercise(3, 3) + exercise(4, 4)))
    p.append(page('<h2>Class work &middot; on the platform</h2><p class="ar">اقرا الكود وجاوب.</p>'
                  + exercise(5, 5)))
    p.append(page('<h2>Class work &middot; on the platform</h2><p class="ar">كمّل.</p>'
                  + exercise(6, 6)))
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
    ('class', [1, 2, 3]), ('class', [4, 5, 6]),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [7, 8, 9, 10]), ('hw', [11, 12, 13]), ('hw', [14, 15]),
    ('hw', [16, 17, 18]), ('hw', [19, 20, 21]), ('hw', [22, 23, 24]),
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
                     '<div class="src">' + esc(EX[n]['src']) + '</div>' + code_block(EX[n])
                     + '<div class="key">' + answer_html(n) + '</div></div>')
        pages.append(page(''.join(b)))
    return head + ''.join(pages) + tail


# ------------------------------------------------------------ model answers
# For the students, not the teacher: full sentences they can learn from, each
# with an Arabic line saying why -- no marking points. It lives in _teacher/
# so it has no public URL before the homework is in; the teacher prints it
# and hands it out afterwards. Numbered exactly as the student's own sheets.
MODEL_PAGES = [
    ('class', [1, 2]), ('class', [3, 4]), ('class', [5, 6]),
    ('hw', [7, 8, 9]), ('hw', [10, 11]), ('hw', [12, 13]), ('hw', [14, 15]),
    ('hw', [16, 17, 18]), ('hw', [19, 20, 21]), ('hw', [22, 23]), ('hw', [24]),
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
                     '<span class="exq">' + esc(EX[n]['prompt']) + '</span></div>' + code_block(EX[n])
                     + '<div class="key">' + rows + '</div></div>')
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
    L11 = "Lecture 11 %s — " + TITLE
    outs = [
        (ROOT / 'lecture11/handout/index.html', booklet(head, tail), L11 % "Booklet"),
        (ROOT / 'lecture11/homework/index.html', homework(head, tail), L11 % "Homework"),
        (ROOT / 'lecture11/_teacher/answer-key.html', key(head, tail), L11 % "Answer Key"),
        (ROOT / 'lecture11/_teacher/model-answers.html', model_answers(head, tail), L11 % "Model Answers"),
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
