#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Lecture 6's printed material.

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
checked by rendering each sheet on its own.
"""
import io, json, re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "lecture6" / "_teacher"
DATA = json.loads((T / "exercises.json").read_text(encoding="utf-8"))
EX = {x["n"]: x for x in DATA["SHEET"]["parts"][0]["exercises"]}

TITLE = "What if one wall falls?"
ACCENT = "#B5531C"

# Class work: the book's Worked Example and Try, all quick to mark together.
IN_CLASS = [1, 2, 3, 4]

HW_SECTIONS = [
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
HOMEWORK = [n for _, _, pages in HW_SECTIONS for g in pages for n in g]

EXTRA_CSS = '''
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
    src = (ROOT / "scripts" / "build_lecture6_slides.py").read_text(encoding="utf-8")
    m = re.search(r"^%s = '''(.*?)'''" % name, src, re.DOTALL | re.MULTILINE)
    assert m, "diagram %s not found in the slide builder" % name
    return m.group(1).strip()


def shell():
    t = (ROOT / "templates/handout-template.html").read_text(encoding="utf-8")
    t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    t = (t.replace("__LECTURE_NUM__", "6").replace("__TITLE_HTML__", esc(TITLE))
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
            ' &middot; Lecture 6</div><div class="namebox"><div><span>Name</span><i></i></div>'
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
            + '</p><div class="src">' + esc(x['src']) + '</div>' + body + '</div>')


def term(h, p, ar):
    return '<div class="term"><h4>' + h + '</h4><p>' + p + '</p><p class="ar">' + ar + '</p></div>'


def lastpage(kind):
    """Closing sheet, with no QR and no quiz address: the exam is taken in the
    lesson, not at home the night before with an AI to hand."""
    if kind == 'booklet':
        head = ('<h2>What to revise</h2><div class="summary">'
                '<p>Learn the five terms word for word first &mdash; firewall, VPN, DMZ, defense in depth, zero trust '
                '&mdash; then the four layers with the measure in each, and why a DMZ protects the internal network. '
                'Then the perimeter: what it was, and why cloud and remote work blurred it.</p>'
                '<p class="ar">احفظ الخمس مصطلحات بالتعريف الأول، وبعدين الطبقات الأربعة وإجراء كل طبقة، وليه المنطقة '
                'المعزولة بتحمي الشبكة الداخلية، وبعدين المحيط الأمني وليه بقى مش كفاية.</p></div>')
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
    Only the title and the exam QR have no page of their own."""
    DMZ, LAYERS, TRUST = slide_svg("DMZ"), slide_svg("LAYERS"), slide_svg("TRUST")
    p = []
    # slides 2-6: recap, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Before we start &middot; lesson 2-1</h2>'
        '<table><tr><th>Technology</th><th>What it protects</th></tr>'
        '<tr><td class="k">Encryption</td><td>The content, from being read</td></tr>'
        '<tr><td class="k">Digital certificate</td><td>That the other side is genuine</td></tr>'
        '<tr><td class="k">Digital signature</td><td>The data, from being altered</td></tr>'
        '<tr><td class="k">Multi-factor authentication</td><td>The account, from unauthorized login</td></tr></table>'
        '<p class="ar">في الدرس 2-1 اتعلمت إزاي تقنيات التشفير والمصادقة بتحمي الاتصال والحسابات. النهارده هنوسّع الحماية لتصميم الشبكة نفسها.</p>'
        '<h2>One lock on the front door is not enough</h2>'
        '<p>An organization&#8217;s network holds confidential data &mdash; customer records, financial files and '
        'private messages &mdash; and attackers constantly look for a way in. If a single lock is picked, '
        'everything inside is exposed. So modern network security uses several layers: even when one defense '
        'is breached, the next one still protects the system.</p>'
        '<p class="ar">وسيلة حماية واحدة مش كفاية؛ لو فشلت، موارد تانية ممكن تبقى في خطر. عشان كده بنستخدم الدفاع في العمق.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> How can an organization design its network so that, '
        'even if one defense is breached, the system stays protected?</p>'
        '<p class="ar">السؤال الرئيسي: إزاي مؤسسة تقدر تصمم شبكتها بحيث، حتى لو دفاع واحد اتخرق، النظام يفضل محمي؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> A company has a public website, staff who work '
        'from home, and a customer database. Predict where an attacker would try to get in &mdash; and if you could '
        'build only one wall, where you would put it.</p>'
        '<p class="ar">توقّعوا: المهاجم هيحاول يدخل منين؟ ولو هتبني حيطة واحدة بس، هتحطها فين؟</p></div>'))
    # slides 7-9: the firewall, the VPN, not a use of a VPN
    p.append(page(
        '<h2>Part 1 &middot; The firewall</h2>'
        + term('Firewall', 'A system installed at the entry/exit point of a network that allows or denies communication based on '
               'rules set in advance. <i>e.g.</i> Allow access to the web server, but deny direct external access to the database server.',
               'جدار الحماية: بيراقب حركة الشبكة وبيسمح بيها أو يمنعها حسب قواعد. ممكن يكون عند حدود الشبكة، أو بين أجزائها، أو على جهاز مضيف.')
        + '<h2>Part 2 &middot; VPN (Virtual Private Network)</h2>'
        + term('VPN', 'A technology that creates an encrypted virtual private line (a tunnel) over the Internet, allowing safe '
               'connection to a network from a remote location. Because the content is encrypted, the risk of eavesdropping is reduced '
               'even on public Wi-Fi.',
               'الـ VPN: اتصال منطقي خاص عبر شبكة عامة، بيستخدم التشفير وتقنيات النفق.')
        + '<table><tr><th>Main use</th><th>What it means</th></tr>'
        '<tr><td class="k">Remote work</td><td>Connecting safely to the organization&#8217;s network from home or while away</td></tr>'
        '<tr><td class="k">Connecting branches</td><td>Connecting offices in different locations safely</td></tr>'
        '<tr><td class="k">NOT a use</td><td>Automatically deleting files infected with viruses &mdash; that is antivirus software</td></tr></table>'))
    # slides 10-11: the DMZ, pause & think
    p.append(page(
        '<h2>Part 3 &middot; DMZ (Demilitarized Zone)</h2>'
        + term('DMZ', 'An area where servers exposed to the external network (web servers, mail servers, etc.) are placed separately '
               'from the internal network. If a public-facing server is attacked, damage to the internal network can be prevented.',
               'المنطقة المعزولة: الخوادم العامة منفصلة عن الشبكة الداخلية، فلو واحد اتخرق، الهجوم ميوصلش للداخل.')
        + dg(DMZ)
        + '<div class="summary hw"><p><b>Pause and think.</b> Why is it safer to place a public web server in a DMZ rather '
        'than inside the internal network?</p>'
        '<p class="ar">ليه حط خادم ويب عام في المنطقة المعزولة أأمن من حطه جوه الشبكة الداخلية؟</p></div>'))
    # slides 12-14: defense in depth, which layer, the exam-style question
    p.append(page(
        '<h2>Part 4 &middot; Defense in depth</h2>'
        + term('Defense in depth', 'Layering multiple security measures so that, even if one is breached, the next can still protect the system.',
               'الدفاع في العمق: طبقات كتير من الضوابط الأمنية، لو طبقة فشلت، الباقي يقلل الخطر ويحد من أثر الاختراق.')
        + dg(LAYERS)
        + '<table><tr><th>Security measure</th><th style="width:32%">Layer</th></tr>'
        '<tr><td>Blocking unauthorized communication with a firewall</td><td>1 &middot; Network entry</td></tr>'
        '<tr><td>Encrypting communication with a VPN</td><td>2 &middot; Communication path</td></tr>'
        '<tr><td>Separating public-facing servers using a DMZ</td><td>3 &middot; Server placement</td></tr>'
        '<tr><td>Installing antivirus software; keeping the OS updated</td><td>4 &middot; Endpoints</td></tr></table>'
        '<div class="summary"><p><b>Why is layering better than a firewall alone?</b> A firewall alone is one barrier: if it '
        'is breached, everything inside is exposed. With several layers, if one is breached, the next still protects the '
        'system &mdash; so one breach is far less likely to expose the whole network.</p>'
        '<p class="ar">حاجز واحد لو اتخرق كل حاجة بتتكشف؛ الطبقات: لو واحدة وقعت، اللي بعدها لسه بتحمي.</p></div>'))
    # slides 15-19: the perimeter, zero trust, true or false, which term, exam warning
    p.append(page(
        '<h2>Part 5 &middot; The perimeter has blurred</h2>'
        + term('Perimeter', 'The old boundary built on the idea that &#8220;inside the organization&#8217;s network is safe, and outside '
               'is dangerous&#8221;. With cloud services and remote work, the line between inside and outside has blurred, and designs '
               'that protect only the perimeter are no longer enough.',
               'المحيط الأمني: الحدود التقليدية اللي بتفترض إن الداخل آمن، واللي طمستها الخدمات السحابية والشغل عن بُعد.')
        + term('Zero trust', 'The system does not trust any communication, including from within the organization&#8217;s network, and '
               'always verifies it. <i>e.g.</i> Even for access from inside, identity verification and access-permission checks are '
               'performed every time.',
               'نهج انعدام الثقة: مفيش ثقة تلقائية لمجرد إنك جوه الشبكة؛ الهوية والصلاحيات والسياق بيتفحصوا عند كل وصول.')
        + dg(TRUST)
        + '<table><tr><th>Looks right, but is false</th><th>Why</th></tr>'
        '<tr><td>Access from inside the network is safe, so verification is unnecessary.</td><td>Zero trust verifies inside access too.</td></tr>'
        '<tr><td>A firewall alone is sufficient.</td><td>If it is breached, nothing else stands.</td></tr>'
        '<tr><td>A DMZ exposes all servers to the outside, or improves speed.</td><td>It keeps public servers apart, to protect the inside.</td></tr></table>'))
    # slides 20-22: think as an engineer, new context, key takeaway
    p.append(page(
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A company has a public website, staff who work from home, and confidential customer data. '
        '<b>Collect data</b>: its three assets and the main threat to each. <b>Rank the layers</b> for this company and justify '
        'your top choice. <b>Decide</b>: recommend a design with two reasons why layering is safer than a single firewall.</p>'
        '<p class="ar">تلميح: حط الخادم العام في المنطقة المعزولة، ومتعتمدش على العزل لوحده.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A hospital moves its patient records to a cloud service and lets doctors access them from home. '
        'Using zero trust and defense in depth, suggest two measures and say where each one helps, then identify one risk that could still remain.</p>'
        '<p class="ar">اقترح إجراءين وبيّن كل واحد بيساعد فين، وحدد خطر واحد ممكن يفضل موجود.</p></div>'
        '<h2>Key takeaway &middot; layer your defenses</h2><div class="summary">'
        '<p>Layer your defenses &mdash; firewall, VPN, DMZ, endpoints &mdash; and verify every access (zero trust). One breach is '
        'then far less likely to expose the whole network.</p>'
        '<p class="ar">كدّس دفاعاتك، واتأكد من كل عملية وصول — ساعتها خرق واحد مش هيكشف الشبكة كلها.</p></div>'
        '<h2>Lesson question &mdash; answered</h2>'
        '<p>Layering: a firewall controls what enters and leaves, a VPN encrypts remote communication, a DMZ keeps public '
        'servers apart, and endpoint measures protect each device &mdash; and zero trust verifies every request.</p>'))
    p.append(page('<h2>Class work</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
                  + exercise(1, 1) + exercise(2, 2)))
    # exercise 4's options run long: with an Arabic line under the heading
    # this page is a few millimetres past one sheet, so the heading carries it
    p.append(page('<h2>Class work &middot; كمّل مع زميلك</h2>'
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
    ('class', IN_CLASS),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [5, 6, 8]), ('hw', [12, 13, 9]), ('hw', [10, 11, 7]),
    ('hw', [14, 15]), ('hw', [18, 16]), ('hw', [17, 19, 20]),
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
                     '<div class="src">' + esc(EX[n]['src']) + '</div>'
                     '<div class="key">' + answer_html(n) + '</div></div>')
        pages.append(page(''.join(b)))
    return head + ''.join(pages) + tail


# ------------------------------------------------------------ model answers
# For the students, not the teacher: full sentences they can learn from, each
# with an Arabic line saying why -- no marking points. It lives in _teacher/
# so it has no public URL before the homework is in; the teacher prints it
# and hands it out afterwards. Numbered exactly as the student's own sheets.
MODEL_PAGES = [
    ('class', [1]), ('class', [2, 3, 4]),
    ('hw', [5, 6, 8]), ('hw', [12, 13, 9]), ('hw', [10, 11, 7]),
    ('hw', [14, 15, 18]), ('hw', [16, 17, 19, 20]),
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
                     '<span class="exq">' + esc(EX[n]['prompt']) + '</span></div>'
                     '<div class="key">' + rows + '</div></div>')
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
    L6 = "Lecture 6 %s — " + TITLE
    outs = [
        (ROOT / 'lecture6/handout/index.html', booklet(head, tail), L6 % "Booklet"),
        (ROOT / 'lecture6/homework/index.html', homework(head, tail), L6 % "Homework"),
        (ROOT / 'lecture6/_teacher/answer-key.html', key(head, tail), L6 % "Answer Key"),
        (ROOT / 'lecture6/_teacher/model-answers.html', model_answers(head, tail), L6 % "Model Answers"),
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
