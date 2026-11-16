#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Lecture 10's printed material.

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
checked by rendering each sheet on its own.
"""
import io, json, re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "lecture10" / "_teacher"
DATA = json.loads((T / "exercises.json").read_text(encoding="utf-8"))
EX = {x["n"]: x for x in DATA["SHEET"]["parts"][0]["exercises"]}

TITLE = "How do they talk?"
ACCENT = "#5E6B1F"

# Class work: the book's Worked Example and Try, all quick to mark together.
IN_CLASS = [1, 2, 3, 4]

HW_SECTIONS = [
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
HOMEWORK = [n for _, _, pages in HW_SECTIONS for g in pages for n in g]

EXTRA_CSS = '''
.code{font-family:'JetBrains Mono',monospace;font-size:9pt;line-height:1.5;background:#F4F6F8;border:1px solid var(--line);border-radius:2mm;padding:2.5mm 3.5mm;margin:1.5mm 0 2.5mm 9.5mm;white-space:pre;font-variant-ligatures:none}.sheet>.code,.summary .code,.fcrow .code{margin-left:0}.fcx svg{width:62mm;height:auto;display:block}.ex .fcx{margin:1mm 0 2mm 9.5mm}.fcrow{display:flex;gap:6mm;align-items:flex-start;margin:2mm 0 3mm}.fcrow>div{flex:1;min-width:0}
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
    src = (ROOT / "scripts" / "build_lecture10_slides.py").read_text(encoding="utf-8")
    m = re.search(r"^%s = '''(.*?)'''" % name, src, re.DOTALL | re.MULTILINE)
    assert m, "diagram %s not found in the slide builder" % name
    return m.group(1).strip()


def code_block(x):
    return ((('<div class="code">' + esc(x['code']) + '</div>') if x.get('code') else '')
            + (('<div class="fcx">' + x['svg'] + '</div>') if x.get('svg') else ''))


def shell():
    t = (ROOT / "templates/handout-template.html").read_text(encoding="utf-8")
    t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    t = (t.replace("__LECTURE_NUM__", "10").replace("__TITLE_HTML__", esc(TITLE))
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
            ' &middot; Lecture 10</div><div class="namebox"><div><span>Name</span><i></i></div>'
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
                '<p>Learn the client and the server first, then HTTP and HTTPS and why HTTPS is safer. Then GET and POST with '
                'an example of each, the status codes 200, 404 and 500, and what an API and JSON are. On the platform: the '
                'four flowchart symbols, and how a diamond becomes an if ... else.</p>'
                '<p class="ar">احفظ العميل والخادم، و HTTP و HTTPS وليه HTTPS أأمن، و GET و POST بمثال لكل واحد، ورموز الحالة '
                '200 و 404 و 500، ويعني إيه API و JSON. وعلى المنصة: أشكال المخطط الانسيابي الأربعة، وإزاي المعين بيبقى if ... else.</p></div>')
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
    The players (the request flow and the flowcharts) print as their finished
    trace tables. The title and the exam QR have no page."""
    CS, SYM, PRICE, AB, REVIEW = (slide_svg(n) for n in ("CLIENTSERVER", "FLOWSYM", "PRICE", "AB", "REVIEW"))

    def code(t):
        return '<div class="code">' + esc(t) + '</div>'

    def chart(svg):
        return '<div class="fcx">' + svg + '</div>'

    p = []
    # slides 2-6: recap, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Before we start &middot; lesson 3-1</h2>'
        '<table><tr><th>Tier</th><th>Its job</th></tr>'
        '<tr><td class="k">Frontend</td><td>shows and collects</td></tr>'
        '<tr><td class="k">Backend</td><td>decides and processes</td></tr>'
        '<tr><td class="k">Database</td><td>stores and retrieves</td></tr></table>'
        '<p class="ar">في الدرس 3-1 اتعلمت إن الواجهة الأمامية والخلفية بيتعاونوا؛ في الدرس ده هتتعلم إزاي الطلبات والاستجابات بتتنقل بين العميل والخادم.</p>'
        '<h2>Your device asks, a server answers</h2>'
        '<p>When you click a link or press &#8220;search&#8221;, your device does not hold the whole website &mdash; it asks a '
        'distant computer for it. Your browser is the <b>client</b> that makes the <b>request</b>; a <b>server</b> somewhere '
        'answers with a <b>response</b>. This exchange, governed by shared rules called <b>protocols</b>, is how every web '
        'application communicates.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> How do the client and server communicate to make a web '
        'application work, and what rules and messages do they use?</p>'
        '<p class="ar">إزاي العميل والخادم بيتواصلوا عشان يشغّلوا تطبيق الويب، وإيه القواعد والرسائل اللي بيستخدموها؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> You open YouTube and search <i>cats</i>. What does your '
        'phone send? What comes back? Should your password travel as it is, or locked?</p>'
        '<p class="ar">اكتبوا إجاباتكم قبل ما تكمّلوا.</p></div>'))
    # slides 7-10: client and server, client or server, HTTP and HTTPS
    p.append(page(
        '<h2>Part 1 &middot; Client and server</h2>'
        + dg(CS)
        + '<table><tr><th style="width:18%">Term</th><th>Meaning</th></tr>'
        '<tr><td class="k">Client</td><td>The side that requests data or processing from the server. Web browsers and smartphone apps.</td></tr>'
        '<tr><td class="k">Server</td><td>The side that receives requests from clients, processes them, and returns responses.</td></tr></table>'
        '<p class="ar">العميل: برنامج أو جهاز بيبعت طلب لخدمة تانية. الخادم: بيستقبل الطلبات ويعالجها ويرجّع الاستجابات.</p>'
        '<h2>Part 2 &middot; HTTP and HTTPS</h2>'
        + term('HTTP (HyperText Transfer Protocol)', 'A communication protocol for exchanging data between clients (browsers and apps) and servers.',
               'بروتوكول بيستخدم لتبادل الرسائل بين عميل وخادم على الويب.')
        + term('HTTPS (HTTP Secure)', 'HTTP with TLS encryption added. The content is encrypted, so the risk of it being read by '
               'third parties is reduced. Addresses that begin with https:// use it.',
               'استخدام HTTP عبر اتصال TLS آمن: بيحمي سرية الاتصال وسلامته وبيتحقق من الخادم.')
        + '<div class="summary hw"><p><b>Pause and think.</b> Why should a login page use HTTPS rather than plain HTTP?</p>'
        '<p class="ar">ليه صفحة الدخول لازم تستخدم HTTPS؟</p></div>'))
    # slides 11-14: methods, status codes, the request flow, 404
    p.append(page(
        '<h2>Part 3 &middot; The request carries an HTTP method</h2>'
        '<table><tr><th style="width:14%">Method</th><th style="width:30%">Role</th><th>Examples</th></tr>'
        '<tr><td class="k">GET</td><td>Retrieve data from the server</td><td>Displaying a web page, retrieving search results</td></tr>'
        '<tr><td class="k">POST</td><td>Send data to the server</td><td>Sending login information, submitting a form</td></tr></table>'
        '<h2>The response carries a status code</h2>'
        '<table><tr><th style="width:18%">Status code</th><th>Meaning</th></tr>'
        '<tr><td class="k">200</td><td>Success &mdash; the request was processed successfully</td></tr>'
        '<tr><td class="k">404</td><td>Page not found &mdash; the requested address does not exist</td></tr>'
        '<tr><td class="k">500</td><td>Server error &mdash; a problem occurred on the server side (on its own it does not say the detailed cause)</td></tr></table>'
        '<h2>One request, one matching response</h2>'
        '<table><tr><th style="width:8%">Step</th><th style="width:16%">Where</th><th>What happens</th></tr>'
        '<tr><td>&#9312;</td><td class="k">Client</td><td>You search <i>cats</i>: the browser sends a <b>GET</b> request</td></tr>'
        '<tr><td>&#9313;</td><td class="k">Server</td><td>Receives the request and processes it</td></tr>'
        '<tr><td>&#9314;</td><td class="k">Client</td><td>The response arrives: status code <b>200</b> and the results page</td></tr>'
        '<tr><td>&#9315;</td><td class="k">Client</td><td>You log in: a <b>POST</b> request, over <b>HTTPS</b>, so the password is encrypted</td></tr>'
        '<tr><td>&#9316;</td><td class="k">Server</td><td>Receives the login data and checks it</td></tr>'
        '<tr><td>&#9317;</td><td class="k">Client</td><td>Status code <b>200</b>, and your account page comes back</td></tr></table>'
        '<div class="summary hw"><p><b>Pause and think.</b> If a browser receives status code 404, what should it tell the user '
        '&mdash; and whose side had the problem?</p></div>'))
    # slides 15-19: true or false, API and JSON, match, exam warning, exam-style
    p.append(page(
        '<table><tr><th>True or false?</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>The client requests data or processing; the server returns the response.</td><td>True</td></tr>'
        '<tr><td>HTTPS is a communication protocol that adds encryption to HTTP.</td><td>True</td></tr>'
        '<tr><td>The GET method is for sending data to the server.</td><td><b>False</b> &mdash; POST sends</td></tr>'
        '<tr><td>Status code 404 indicates that the page is not found.</td><td>True</td></tr></table>'
        '<h2>Part 4 &middot; API and JSON</h2>'
        + term('API (Application Programming Interface)', 'A system for exchanging data between different pieces of software. '
               'In web applications, the frontend often sends requests to the backend through an API and receives data.',
               'مجموعة قواعد واضحة بتسمح لبرنامج يطلب بيانات أو وظائف من برنامج تاني.')
        + term('JSON (JavaScript Object Notation)', 'A data format that is easy for humans to read and for computers to process. '
               'It is made of keys and their values.', 'صيغة نصية شائعة لتمثيل وتبادل البيانات المهيكلة.')
        + code('{\n  "city": "Cairo",\n  "temperature": 31\n}')
        + '<p>Key <b>&quot;city&quot;</b> has the value <b>&quot;Cairo&quot;</b>; key <b>&quot;temperature&quot;</b> has the value <b>31</b>.</p>'
        '<table><tr><th>Looks right, but is false</th><th style="width:38%">Why</th></tr>'
        '<tr><td>Status code 500 means the request was processed successfully.</td><td>500 is a server error; success is 200.</td></tr>'
        '<tr><td>An API adjusts the appearance of web pages.</td><td>It exchanges data between software.</td></tr>'
        '<tr><td>JSON encrypts the connection.</td><td>JSON is a data format; HTTPS encrypts.</td></tr></table>'))
    # slides 20-23: exam-style, engineer, new context, takeaway
    p.append(page(
        '<div class="summary"><p><b>Exam-style question &middot; 6 marks.</b> Explain what happens, step by step, when a '
        'browser requests a web page and the server responds. Refer to: client, request, HTTP method, response, status code.</p>'
        '<p class="ar">اشرح خطوة بخطوة لما المتصفح يطلب صفحة ويب والخادم يستجيب.</p></div>'
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A school wants a web app where students log in, view their timetable and download a PDF. '
        '<b>Choose the method</b> (GET or POST) for loading grade history, submitting the login form, and requesting today&#8217;s '
        'schedule from another school system &mdash; is an API involved in the last? <b>Choose the protocol</b> for the login. '
        '<b>Decide</b>, with two reasons.</p>'
        '<p class="ar">تلميح: GET بيجيب ويعرض؛ POST بيبعت بيانات زي الدخول؛ HTTPS بيشفّر عشان الباسورد ميتسرقش.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A weather service offers an API that returns today&#8217;s forecast. Which HTTP method would '
        'the client use? Why should the service use HTTPS? One advantage of receiving the data as JSON?</p></div>'
        '<h2>Key takeaway &middot; lesson 3-2</h2><div class="summary">'
        '<p>Client requests, server responds &mdash; over HTTP/HTTPS, with a method (GET/POST), a status code, and often an API '
        'returning JSON.</p>'
        '<p class="ar">العميل بيطلب، والخادم بيستجيب — عبر HTTP/HTTPS، بأسلوب (GET/POST)، ورمز حالة، وغالبًا API بترجّع JSON.</p></div>'))
    # slides 24-27: Qureo 32 -- symbols, follow the arrows, to the code
    p.append(page(
        '<h2>Part 5 &middot; On the platform: Flowchart (Qureo chapter 32)</h2>'
        '<p>A <b>flowchart</b> draws a program&#8217;s steps in order. Arrows show which step comes next.</p>'
        + dg(SYM)
        + '<div class="fcrow">' + chart(PRICE)
        + '<div><table><tr><th>Step</th><th>Shape</th><th>What happens</th></tr>'
        '<tr><td>1</td><td>Rectangle</td><td>price = 40</td></tr>'
        '<tr><td>2</td><td>Rectangle</td><td>total = 40 &times; 3 = 120</td></tr>'
        '<tr><td>3</td><td>Diamond</td><td>120 &gt; 100? <b>Yes</b></td></tr>'
        '<tr><td>4</td><td>Parallelogram</td><td>shows &quot;Too expensive&quot;</td></tr></table>'
        + code('let price = 40;\nlet total = price * 3;\nif (total > 100) {\n  console.log("Too expensive");\n} else {\n  console.log("Buy it");\n}')
        + '</div></div>'
        '<p class="ar">كل شكل بيتحول لسطر: المستطيل = let أو حساب، المعين = if، سهم Yes = جوّه if، سهم No = else، متوازي الأضلاع = console.log.</p>'))
    # slides 28-32: your turn, rules, Qureo 33 review, what we learned
    p.append(page(
        '<h2>Your turn &middot; write the code</h2>'
        '<div class="fcrow">' + chart(AB)
        + '<div>' + code('let a = 8;\nlet b = 5;\nif (a > b) {\n  console.log(a);\n} else {\n  console.log(b);\n}')
        + '<p>It shows <b>8</b>. If b were 11, it would show <b>11</b>.</p>'
        '<table><tr><th>Rules of a good flowchart</th></tr>'
        '<tr><td>One Start and one End, both ovals</td></tr>'
        '<tr><td>A diamond has two exits: Yes and No</td></tr>'
        '<tr><td>A calculation goes in a rectangle, not a diamond</td></tr>'
        '<tr><td>The arrows show the order the steps run in</td></tr></table></div></div>'
        '<h2>Part 6 &middot; Review of chapters 31-32 (Qureo chapter 33)</h2>'
        '<div class="fcrow">' + chart(REVIEW)
        + '<div>' + code('function add3(a, b, c) {\n  return a + b + c;\n}')
        + '<p>add3(2, 4, 6) returns <b>12</b>, so total = 12. 12 &gt; 10 is true: it shows <b>&quot;Big total&quot;</b>. '
        'With add3(1, 2, 3) the total is 6, so it shows &quot;Small total&quot;.</p></div></div>'
        '<p class="ar">الدالة بترجّع قيمة، والمخطط بيقرر بيها.</p>'))
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
    L10 = "Lecture 10 %s — " + TITLE
    outs = [
        (ROOT / 'lecture10/handout/index.html', booklet(head, tail), L10 % "Booklet"),
        (ROOT / 'lecture10/homework/index.html', homework(head, tail), L10 % "Homework"),
        (ROOT / 'lecture10/_teacher/answer-key.html', key(head, tail), L10 % "Answer Key"),
        (ROOT / 'lecture10/_teacher/model-answers.html', model_answers(head, tail), L10 % "Model Answers"),
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
