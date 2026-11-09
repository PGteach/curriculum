#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Lecture 9's printed material.

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
checked by rendering each sheet on its own.
"""
import io, json, re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "lecture9" / "_teacher"
DATA = json.loads((T / "exercises.json").read_text(encoding="utf-8"))
EX = {x["n"]: x for x in DATA["SHEET"]["parts"][0]["exercises"]}

TITLE = "What happens when you click?"
ACCENT = "#7D5A1E"

# Class work: the book's Worked Example and Try, all quick to mark together.
IN_CLASS = [1, 2, 3, 4]

HW_SECTIONS = [
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
HOMEWORK = [n for _, _, pages in HW_SECTIONS for g in pages for n in g]

EXTRA_CSS = '''
.code{font-family:'JetBrains Mono',monospace;font-size:9pt;line-height:1.5;background:#F4F6F8;border:1px solid var(--line);border-radius:2mm;padding:2.5mm 3.5mm;margin:1.5mm 0 2.5mm 9.5mm;white-space:pre;font-variant-ligatures:none}.sheet>.code,.summary .code{margin-left:0}
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
    src = (ROOT / "scripts" / "build_lecture9_slides.py").read_text(encoding="utf-8")
    m = re.search(r"^%s = '''(.*?)'''" % name, src, re.DOTALL | re.MULTILINE)
    assert m, "diagram %s not found in the slide builder" % name
    return m.group(1).strip()


def code_block(x):
    return ('<div class="code">' + esc(x['code']) + '</div>') if x.get('code') else ''


def shell():
    t = (ROOT / "templates/handout-template.html").read_text(encoding="utf-8")
    t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    t = (t.replace("__LECTURE_NUM__", "9").replace("__TITLE_HTML__", esc(TITLE))
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
            ' &middot; Lecture 9</div><div class="namebox"><div><span>Name</span><i></i></div>'
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
                '<p>Learn what a web application is, then the three tiers by their roles: the frontend shows and collects, '
                'the backend decides and processes, the database stores and retrieves. Then the six steps of a search, '
                'and which tier does each job on a video site, a social network and a shop. On the platform: a function '
                'takes arguments and gives back a return value.</p>'
                '<p class="ar">احفظ تعريف تطبيق الويب، والطبقات التلاتة بأدوارها، وخطوات البحث الست، وكل طبقة بتعمل إيه في '
                'موقع الفيديو والتواصل والتسوق. وعلى المنصة: الدالة بتاخد وسائط وترجّع قيمة.</p></div>')
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
    The two players (the request flow and the code tracer) print as their
    finished trace tables. The title and the exam QR have no page."""
    TIERS = slide_svg("TIERS")

    def code(t):
        return '<div class="code">' + esc(t) + '</div>'

    p = []
    # slides 2-6: unit 3, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Unit 3 &middot; Web applications</h2>'
        '<table><tr><th>Lesson</th><th>Topic</th></tr>'
        '<tr><td class="k">3-1 &middot; today</td><td>The overall structure of web applications</td></tr>'
        '<tr><td class="k">3-2</td><td>Web application communication methods</td></tr>'
        '<tr><td class="k">3-3</td><td>Fundamentals of frontend technology</td></tr></table>'
        '<h2>Every time you go online</h2>'
        '<p>Every time you search on YouTube, buy on Amazon, or open Gmail, you are using a <b>web application</b> &mdash; '
        'a program you use through your browser, with nothing to install. Behind the simple screen, three tiers work '
        'together: the page you interact with, the hidden server that processes the request, and the database that holds '
        'all the data. Understanding these three tiers explains how almost every online service is built.</p>'
        '<p class="ar">لما بتدوّر في موقع فيديو، أو بتتسوق أونلاين، أو بتستخدم إيميل على الويب، إنت بتستخدم تطبيق ويب، '
        'وورا اللي بتشوفه فيه أجزاء مختلفة شغالة مع بعض.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> How is a web application structured, and how do its three '
        'tiers work together to respond to what a user does?</p>'
        '<p class="ar">إزاي بيتبني تطبيق الويب، وإزاي طبقاته التلاتة بتشتغل مع بعض عشان تستجيب للمستخدم؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> You type <i>red shoes</i> in a shopping site and press '
        'Enter. Who read your words? Who found the shoes? Where were the shoes kept? Write three guesses.</p>'
        '<p class="ar">اكتبوا تلات تخمينات قبل ما تكمّلوا.</p></div>'))
    # slides 7-9: what is a web application, which one is, the three tiers
    p.append(page(
        '<h2>Part 1 &middot; What is a web application?</h2>'
        + term('Web application', 'An application used through a web browser. It can be used as long as you have a browser, '
               'without installing dedicated software. e.g. YouTube, Amazon, Gmail, Google Maps.',
               'تطبيق الويب: تطبيق بيتستخدم عادةً من خلال متصفح الويب، وبعض تطبيقات الويب ممكن كمان تتثبت على الجهاز.')
        + '<table><tr><th>Is it a web application?</th><th style="width:34%">Answer</th></tr>'
        '<tr><td>A video player on the device</td><td>No &mdash; installed on the device</td></tr>'
        '<tr><td>A maps website on the Internet</td><td><b>Yes</b> &mdash; used through a browser</td></tr>'
        '<tr><td>A calculator app on the desktop</td><td>No &mdash; installed on the computer</td></tr>'
        '<tr><td>A photo-editing program</td><td>No &mdash; installed software</td></tr></table>'
        '<h2>Part 2 &middot; The three tiers of a web application</h2>'
        '<p>A web application is broadly composed of three tiers: the <b>frontend</b>, the <b>backend</b> and the '
        '<b>database</b>. This is the <b>three-tier architecture</b>.</p>'
        + dg(TIERS)))
    # slides 10-13: what each tier does, the restaurant, true or false, match
    p.append(page(
        '<table><tr><th style="width:16%">Tier</th><th>Role</th><th style="width:30%">Examples</th></tr>'
        '<tr><td class="k">Frontend</td><td>The screen component that users see directly. It runs on the browser and accepts user input.</td><td>Search screen, product listing pages, input forms</td></tr>'
        '<tr><td class="k">Backend</td><td>The server-side processing that users do not see. It processes data and makes decisions.</td><td>Searching for matching products, login authentication</td></tr>'
        '<tr><td class="k">Database</td><td>A system that organizes, stores and manages data. It retrieves data when needed and records new data.</td><td>Product information, user information, order history</td></tr></table>'
        '<p class="ar">الواجهة الأمامية: الجزء اللي بنشوفه ونتعامل معاه في المتصفح. الواجهة الخلفية: بتشتغل على الخادم وبتعالج الطلبات. '
        'قاعدة البيانات: بتحفظ البيانات وتوفرها وقت الحاجة.</p>'
        '<h2>A way to remember: a restaurant</h2>'
        '<table><tr><th>In a restaurant</th><th>In a web application</th></tr>'
        '<tr><td>The <b>waiter</b>: takes your order, brings your plate</td><td><b>Frontend</b> &mdash; shows and collects</td></tr>'
        '<tr><td>The <b>kitchen</b> you never see: decides and cooks</td><td><b>Backend</b> &mdash; decides and processes</td></tr>'
        '<tr><td>The <b>storeroom</b>: keeps the food, hands it over</td><td><b>Database</b> &mdash; stores and retrieves</td></tr></table>'
        '<p class="ar">المطعم مثال مننا مش من الكتاب؛ الجمل اللي على اليمين هي جمل الكتاب — احفظها.</p>'
        '<table><tr><th>True or false?</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>The frontend is the screen component that users see directly.</td><td>True</td></tr>'
        '<tr><td>The backend is the part that runs on the browser.</td><td><b>False</b> &mdash; on the server</td></tr>'
        '<tr><td>A database organizes, stores and manages data.</td><td>True</td></tr>'
        '<tr><td>A web application operates with the frontend alone.</td><td><b>False</b> &mdash; all three tiers</td></tr></table>'))
    # slides 14-17: the flow, pause & think, familiar services, which tier
    p.append(page(
        '<h2>Part 3 &middot; How the three tiers cooperate</h2>'
        '<p>Searching for a product on an online shopping site. A request flows down the tiers, and the reply returns:</p>'
        '<table><tr><th style="width:8%">Step</th><th style="width:18%">Tier</th><th>What happens</th></tr>'
        '<tr><td>&#9312;</td><td class="k">Frontend</td><td>Receives the search keywords entered by the user</td></tr>'
        '<tr><td>&#9313;</td><td class="k">Frontend</td><td>Sends the search keywords to the backend</td></tr>'
        '<tr><td>&#9314;</td><td class="k">Backend</td><td>Searches the database for products that match the criteria</td></tr>'
        '<tr><td>&#9315;</td><td class="k">Database</td><td>Returns the data of the matching products to the backend</td></tr>'
        '<tr><td>&#9316;</td><td class="k">Backend</td><td>Organizes the search results and returns them to the frontend</td></tr>'
        '<tr><td>&#9317;</td><td class="k">Frontend</td><td>Displays the search results on the user&#8217;s screen</td></tr></table>'
        '<div class="summary hw"><p><b>Pause and think.</b> When you type in a search box and see results, which tier '
        'collected your input, and which tier found the answer?</p>'
        '<p class="ar">أنهي طبقة جمعت المدخلات، وأنهي طبقة لقت الإجابة؟</p></div>'
        '<h2>Familiar web applications</h2>'
        '<table><tr><th>Service</th><th>Frontend</th><th>Backend</th><th>Database</th></tr>'
        '<tr><td class="k">Video sharing</td><td>Playback and search screens</td><td>Recommended videos; view counts</td><td>Videos, users, viewing history</td></tr>'
        '<tr><td class="k">SNS</td><td>Timeline and post screens</td><td>Who sees a post; push notifications</td><td>Posts, follow relationships, messages</td></tr>'
        '<tr><td class="k">E-commerce</td><td>Product listings, cart screens</td><td>Stock checking; payments</td><td>Products, order history, customers</td></tr></table>'
        '<p class="ar">كل خدمة: واجهة أمامية بتعرض وتجمع، وواجهة خلفية بتقرر وتعالج، وقاعدة بيانات بتخزن وتسترجع.</p>'))
    # slides 18-23: exam warning, exam-style, engineer, new context, takeaway
    p.append(page(
        '<table><tr><th>Looks right, but is false</th><th style="width:40%">Why</th></tr>'
        '<tr><td>The frontend has the role of storing and managing data.</td><td>That is the database.</td></tr>'
        '<tr><td>The backend is the part users interact with directly on the browser.</td><td>That is the frontend.</td></tr>'
        '<tr><td>The database has the role of displaying screens to users.</td><td>The frontend displays.</td></tr>'
        '<tr><td>The frontend sends the request straight to the database.</td><td>The <b>backend</b> asks the database.</td></tr></table>'
        '<div class="summary"><p><b>Exam-style question &middot; 6 marks.</b> Explain how the three tiers cooperate when a '
        'user posts a photo on a social media app. Refer to the role of the frontend, backend, and database.</p>'
        '<p class="ar">اشرح دور كل طبقة لما المستخدم ينشر صورة.</p></div>'
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A clinic wants a web app where patients book appointments, check free time slots and see '
        'past visits. <b>Assign</b> each job to a tier. <b>Diagnose</b>: the booking page opens but no free slots appear. '
        '<b>Decide</b>: three tiers or not, with two reasons.</p>'
        '<p class="ar">تلميح: الأمامية تعرض وتجمع؛ الخلفية تقرر وتعالج؛ قاعدة البيانات تخزن وتسترجع.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A weather app lets users type a city and see the forecast. Which tier takes the city name, '
        'looks up the forecast, and stores past forecasts? Name one job the frontend cannot do on its own.</p></div>'
        '<h2>Key takeaway &middot; lesson 3-1</h2><div class="summary">'
        '<p>The frontend shows and collects, the backend decides and processes, the database stores and retrieves &mdash; '
        'three tiers cooperating make a web application work. (The Arabic book: a simplified teaching model; real '
        'applications can differ.)</p>'
        '<p class="ar">الواجهة الأمامية بتعرض وتجمع، والخلفية بتقرر وتعالج، وقاعدة البيانات بتخزن وتسترجع.</p></div>'))
    # slides 24-27: Qureo chapter 31 -- a function, add, add3
    p.append(page(
        '<h2>Part 4 &middot; On the platform: Functions (4)</h2>'
        '<p>Qureo chapter 31: a function that adds two values, adds three, and compares three. A function is a small '
        'machine: it receives values, processes them, and gives a value back.</p>'
        + code('function name(argumentName) {\n  // processing\n  return result;\n}')
        + '<table><tr><th style="width:26%">Word</th><th>Meaning</th></tr>'
        '<tr><td class="k">argument</td><td>the value you pass <b>into</b> the function</td></tr>'
        '<tr><td class="k">return value</td><td>the value the function gives <b>back</b> with <span class="mono">return</span></td></tr></table>'
        '<p class="ar">الدالة زي ماكينة العصير: الوسيط هو اللي بتحطه، والقيمة المرجعة هي اللي بتطلع بـ return.</p>'
        '<h2>A function to add two values</h2>'
        + code('function add(a, b) {\n  return a + b;\n}\n\nconsole.log(add(3, 5));')
        + '<table><tr><th>Step</th><th>What happens</th><th style="width:22%">Values</th></tr>'
        '<tr><td>1</td><td>The call add(3, 5) runs the function</td><td></td></tr>'
        '<tr><td>2</td><td>The arguments go in</td><td>a = 3, b = 5</td></tr>'
        '<tr><td>3</td><td>a + b is computed; return sends it back</td><td>return 8</td></tr>'
        '<tr><td>4</td><td>console.log prints the return value</td><td>prints 8</td></tr></table>'))
    # slides 27-28: add three, compare three
    p.append(page(
        '<h2>A function that adds three values</h2>'
        + code('function add3(a, b, c) {\n  return a + b + c;\n}\n\nconsole.log(add3(2, 4, 6));      // 12\nconsole.log(add3(10, 20, 30));   // 60')
        + '<p class="ar">نفس الفكرة بتلات وسائط مفصولين بفواصل.</p>'
        '<h2>A function that compares three values</h2>'
        + code('function biggest(a, b, c) {\n  let big = a;\n  if (b > big) {\n    big = b;\n  }\n  if (c > big) {\n    big = c;\n  }\n  return big;\n}\n\nconsole.log(biggest(4, 9, 7));')
        + '<table><tr><th>Step</th><th>Question</th><th style="width:30%">big</th></tr>'
        '<tr><td>1</td><td>let big = a;</td><td>4</td></tr>'
        '<tr><td>2</td><td>b &gt; big? 9 &gt; 4 is true</td><td>9</td></tr>'
        '<tr><td>3</td><td>c &gt; big? 7 &gt; 9 is false</td><td>stays 9</td></tr>'
        '<tr><td>4</td><td>return big</td><td>prints 9</td></tr></table>'
        '<p class="ar">بنبدأ ونقول إن الأولاني هو الأكبر، وبعدين نقارن بـ if — زي المحاضرة 8.</p>'))
    # slides 29-31: Math.max, no return, what we learned
    p.append(page(
        '<h2>A shortcut: Math.max and Math.min</h2>'
        + code('console.log(Math.max(4, 9, 7));   // 9\nconsole.log(Math.min(4, 9, 7));   // 4')
        + '<div class="summary hw"><p><b>Watch out: no return.</b> If you write <span class="mono">a + b;</span> without '
        '<span class="mono">return</span>, the function gives nothing back and console.log prints <b>undefined</b> &mdash; '
        'a juice machine with no cup.</p>'
        '<p class="ar">من غير return بيطبع undefined.</p></div>'
        '<h2>What we learned</h2><div class="summary">'
        '<p>A web application is used through a browser. Frontend shows and collects; backend decides and processes; '
        'database stores and retrieves. A request flows down the tiers and the reply comes back.</p>'
        '<p>A function takes arguments, processes them, and gives back a return value.</p></div>'))
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
    ('class', [1, 2]), ('class', [3, 4]),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [5, 6, 7, 8]), ('hw', [9, 10, 11]), ('hw', [12, 13]),
    ('hw', [14, 15]), ('hw', [16, 17]), ('hw', [18, 19, 20]),
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
    ('class', [1]), ('class', [2, 3]), ('class', [4]),
    ('hw', [5, 6]), ('hw', [7, 8]), ('hw', [9, 10, 11]), ('hw', [12, 13]),
    ('hw', [14, 15, 16]), ('hw', [17, 18]), ('hw', [19, 20]),
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
    L9 = "Lecture 9 %s — " + TITLE
    outs = [
        (ROOT / 'lecture9/handout/index.html', booklet(head, tail), L9 % "Booklet"),
        (ROOT / 'lecture9/homework/index.html', homework(head, tail), L9 % "Homework"),
        (ROOT / 'lecture9/_teacher/answer-key.html', key(head, tail), L9 % "Answer Key"),
        (ROOT / 'lecture9/_teacher/model-answers.html', model_answers(head, tail), L9 % "Model Answers"),
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
