#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Lecture 7's printed material.

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
checked by rendering each sheet on its own.
"""
import io, json, re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "lecture7" / "_teacher"
DATA = json.loads((T / "exercises.json").read_text(encoding="utf-8"))
EX = {x["n"]: x for x in DATA["SHEET"]["parts"][0]["exercises"]}

TITLE = "When something goes wrong"
ACCENT = "#4F55B8"

# Class work: the book's Worked Example and Try, all quick to mark together.
IN_CLASS = [1, 2, 3, 4]

HW_SECTIONS = [
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
    src = (ROOT / "scripts" / "build_lecture7_slides.py").read_text(encoding="utf-8")
    m = re.search(r"^%s = '''(.*?)'''" % name, src, re.DOTALL | re.MULTILINE)
    assert m, "diagram %s not found in the slide builder" % name
    return m.group(1).strip()


def shell():
    t = (ROOT / "templates/handout-template.html").read_text(encoding="utf-8")
    t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    t = (t.replace("__LECTURE_NUM__", "7").replace("__TITLE_HTML__", esc(TITLE))
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
            ' &middot; Lecture 7</div><div class="namebox"><div><span>Name</span><i></i></div>'
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
                '<p>Learn the six stages in order first, with what each one does &mdash; and stage 6 by both its names. '
                'Then why containment comes before eradication, and recovery after it; the three types of incident; and '
                'risk = impact &times; likelihood, with how to rank risks by it.</p>'
                '<p class="ar">احفظ المراحل الست بالترتيب وكل مرحلة بتعمل إيه، والمرحلة السادسة باسميها. وبعدين ليه '
                'الاحتواء قبل الاستئصال، وأنواع الحوادث التلاتة، والخطر = التأثير × الاحتمالية وإزاي نرتّب بيه.</p></div>')
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
    Only the title, the video and the exam QR have no page of their own."""
    STAGES, MATRIX = slide_svg("STAGES"), slide_svg("MATRIX")
    p = []
    # slides 2-6: recap, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Before we start &middot; lesson 2-2</h2>'
        '<table><tr><th>Layer</th><th>Measure</th></tr>'
        '<tr><td class="k">1 &middot; Network entry</td><td>Firewall</td></tr>'
        '<tr><td class="k">2 &middot; Communication path</td><td>VPN</td></tr>'
        '<tr><td class="k">3 &middot; Server placement</td><td>DMZ</td></tr>'
        '<tr><td class="k">4 &middot; Endpoints</td><td>Antivirus, an updated OS</td></tr></table>'
        '<p class="ar">حتى مع الدفاع في العمق ممكن يحصل حادث أمني؛ الدرس ده بينقلنا من الوقاية للاستجابة وإدارة المخاطر.</p>'
        '<h2>A rushed reaction makes it worse</h2>'
        '<p>Even a well-protected system can be attacked: data leaked, files tampered with, a service knocked offline. '
        'A rushed, unplanned reaction only makes the damage worse. Organizations follow a clear, ordered response so that '
        'damage is contained, the cause is removed, and the same problem does not return &mdash; and they decide in advance '
        'which risks to guard against first, because no team can fix everything at once.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> When a security incident happens, how should an organization '
        'respond in order &mdash; and how does it decide which risks to address first?</p>'
        '<p class="ar">السؤال الرئيسي: لما يحصل حادث أمني، المؤسسة تنظّم استجابتها إزاي بالترتيب، وتقرر أنهي مخاطر تعالجها الأول؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> A school computer is infected with malware that is '
        'spreading. Put these in order: restore the files from a backup &middot; unplug it from the network &middot; find out '
        'how it got in &middot; remove the malware.</p>'
        '<p class="ar">رتّبوا الأربع خطوات دول قبل ما تكمّلوا.</p></div>'))
    # slides 7-9: security incidents, (video), not an incident
    p.append(page(
        '<h2>Part 1 &middot; What is a security incident?</h2>'
        + term('Security incident', 'A situation in which actual damage occurs due to an information security problem.',
               'الحادث الأمني: حدث بيأثر على سرية المعلومات أو سلامتها أو توافرها، أو بيهددها بجدية، أو بيخالف سياسة أمنية.')
        + '<table><tr><th>Type</th><th>Description</th></tr>'
        '<tr><td class="k">Information leak</td><td>Personal or confidential information is leaked to the outside</td></tr>'
        '<tr><td class="k">Data tampering</td><td>Data within a system is altered without authorization</td></tr>'
        '<tr><td class="k">Service outage</td><td>A service becomes unavailable due to attacks on the server, etc.</td></tr></table>'
        '<table><tr><th>Is it a security incident?</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>Data was encrypted by a ransomware infection</td><td>Yes</td></tr>'
        '<tr><td>Customer information was leaked through unauthorized access</td><td>Yes &mdash; an information leak</td></tr>'
        '<tr><td>A software update was performed to add new features</td><td><b>No</b> &mdash; nothing was damaged</td></tr>'
        '<tr><td>A web service became unavailable due to an attack on the server</td><td>Yes &mdash; a service outage</td></tr></table>'
        '<h2>Part 2 &middot; Six stages, in order</h2>'
        + dg(STAGES)))
    # slides 10-13: what each stage does, two names, contain first
    p.append(page(
        '<table><tr><th style="width:26%">Stage</th><th>What happens</th></tr>'
        '<tr><td class="k">1 Preparation</td><td>Establish response procedures and structures in advance, in preparation for incidents</td></tr>'
        '<tr><td class="k">2 Detection</td><td>Discover and confirm that an incident has occurred</td></tr>'
        '<tr><td class="k">3 Containment</td><td>Limit the scope of impact so that damage does not spread further</td></tr>'
        '<tr><td class="k">4 Eradication</td><td>Remove the cause of the incident (e.g. remove malware)</td></tr>'
        '<tr><td class="k">5 Recovery</td><td>Return systems and services to their normal state (may restore from a clean backup)</td></tr>'
        '<tr><td class="k">6 Prevention of recurrence</td><td>Analyze the cause and take measures so that the same incident does not occur again</td></tr></table>'
        '<p class="ar">التحضير ← الاكتشاف ← الاحتواء ← إزالة التهديد (الاستئصال) ← الاستعادة ← الدروس المستفادة والتحسين.</p>'
        '<div class="summary"><p><b>Stage 6 has two names.</b> The English book says <b>prevention of recurrence</b>; the Arabic '
        'book and the ministry say <b>lessons learned and improvement</b> &mdash; analyze what happened, document the lessons, '
        'improve the controls. Learn both.</p>'
        '<p class="ar">المرحلة السادسة: \"منع التكرار\" = \"الدروس المستفادة والتحسين\".</p></div>'
        '<h2>Contain first, then remove the cause</h2>'
        + term('Containment &middot; eradication', 'Containment limits the spread of damage; eradication removes the cause. Containment comes first. '
               'If recovery is performed without removing the cause, the same incident may occur again.',
               'الاحتواء: الحد من انتشار الضرر. الاستئصال: إزالة السبب. الاحتواء الأول.')))
    # slides 14-17: pause & think, in practice, which stage, exam-style question
    p.append(page(
        '<div class="summary hw"><p><b>Pause and think.</b> Why must containment come before eradication in the six-stage response?</p>'
        '<p class="ar">ليه الاحتواء لازم ييجي قبل الاستئصال؟</p></div>'
        '<h2>The order is a guide, not a cage</h2>'
        '<p>The six stages give the general sequence, but in a real response some activities can <b>overlap</b> or <b>repeat</b>. '
        'For example, recovery can reveal traces of the threat that are still there &mdash; and the team goes back to containment or eradication.</p>'
        '<p class="ar">الاستجابة الفعلية ممكن يحصل فيها تداخل أو تكرار؛ الاسترداد ممكن يكشف بقايا للتهديد فنرجع للاحتواء أو إزالة التهديد.</p>'
        '<h2>Which stage is it?</h2>'
        '<table><tr><th>Action</th><th style="width:30%">Stage</th></tr>'
        '<tr><td>Establishing response procedures in advance</td><td>Preparation</td></tr>'
        '<tr><td>Discovering and confirming that an incident has occurred</td><td>Detection</td></tr>'
        '<tr><td>Disconnecting a malware-infected computer from the network</td><td>Containment</td></tr>'
        '<tr><td>Removing the malware infection</td><td>Eradication</td></tr>'
        '<tr><td>Restoring a clean system from a backup</td><td>Recovery</td></tr>'
        '<tr><td>Analyzing the cause so it does not occur again</td><td>Prevention of recurrence</td></tr></table>'
        '<div class="summary"><p><b>Why must the six stages go in order?</b> If recovery is done before eradication, the system '
        'is back but the cause is still there, so the same incident can happen again. Eradicate first, and recovery returns a clean system.</p>'
        '<p class="ar">لو رجّعنا النظام قبل ما نشيل السبب، الحادث ممكن يتكرر.</p></div>'))
    # slides 18-22: risk, the matrix, put the risks in order, the exam warning
    p.append(page(
        '<h2>Part 3 &middot; Risk = impact &times; likelihood</h2>'
        + term('Risk', 'The possibility of an information security problem occurring in the future, and its impact.',
               'الخطر: احتمال إن يحصل حدث بيسبب ضرر، مع مراعاة احتمال وقوعه وحجم أثره.')
        + '<table><tr><th>Factor</th><th>Meaning</th></tr>'
        '<tr><td class="k">Impact</td><td>How much damage occurs if the risk actually materializes</td></tr>'
        '<tr><td class="k">Likelihood</td><td>How high the probability is that the risk will actually materialize</td></tr></table>'
        + dg(MATRIX)
        + '<p>Risks with both <b>high impact and high likelihood</b> are addressed first; it is difficult to address every risk at '
        'the same time, so priorities are set. High impact with low likelihood (3 &times; 1 = 3) is usually classed as medium.</p>'
        '<p class="ar">التأثير العالي والاحتمالية العالية أعلى أولوية؛ ومش هنقدر نعالج كل المخاطر في نفس الوقت.</p>'
        '<table><tr><th>Looks right, but is false</th><th>Why</th></tr>'
        '<tr><td>The size of a risk can be determined by impact alone.</td><td>Impact and likelihood, multiplied.</td></tr>'
        '<tr><td>It is enough to address only high-impact, or only high-likelihood, risks.</td><td>Both factors count.</td></tr>'
        '<tr><td>All risks must be addressed simultaneously.</td><td>Set priorities.</td></tr>'
        '<tr><td>Detection &rarr; Eradication &rarr; Containment &rarr; Recovery.</td><td>Containment comes before eradication.</td></tr></table>'))
    # slides 23-27: think as an engineer, new context, key takeaway, unit 2
    p.append(page(
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>Ransomware hits a school&#8217;s student records: files encrypted, staff locked out, the incident '
        'just detected. <b>Respond from here</b>: list the stages still to do. <b>Assess the risks</b>: another ransomware attack, '
        'or a brief power cut? <b>Decide</b>: the first three actions, and why order matters.</p>'
        '<p class="ar">تلميح: لو رجّعت قبل ما تشيل السبب، البرمجية الخبيثة لسه موجودة.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>An online shop has just detected that customer data has been leaked. Name the next two '
        'stages it should carry out and why, and identify one risk it should prioritize afterward.</p>'
        '<p class="ar">حدد المرحلتين الجايين وليه، وخطر واحد ياخد الأولوية بعد كده.</p></div>'
        '<h2>Key takeaway &middot; respond in order, fix the worst first</h2><div class="summary">'
        '<p>Follow the six stages in order (prepare &rarr; detect &rarr; contain &rarr; eradicate &rarr; recover &rarr; prevent), '
        'and prioritize risks by impact &times; likelihood.</p>'
        '<p class="ar">اتبع المراحل الست بالترتيب مع إمكانية الرجوع لمرحلة سابقة، وحدد أولويات المخاطر بالتأثير × الاحتمالية.</p></div>'
        '<h2>Unit 2 &middot; complete</h2>'
        '<table><tr><th>Lesson</th><th>What to know</th></tr>'
        '<tr><td class="k">2-1</td><td>HTTPS, common-key and public-key, certificates, signatures, multi-factor login</td></tr>'
        '<tr><td class="k">2-2</td><td>Firewall, VPN, DMZ, defense in depth, zero trust</td></tr>'
        '<tr><td class="k">2-3</td><td>Security incidents, the six stages, risk = impact &times; likelihood</td></tr></table>'))
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
    ('class', IN_CLASS),
    # in HOMEWORK order, so the key reads 1, 2, 3 ... exactly as the
    # student's sheet does; check_key_order() below enforces it
    ('hw', [5, 8, 13]), ('hw', [10, 14, 7]), ('hw', [6, 9, 11]),
    ('hw', [12, 15, 16]), ('hw', [17, 18]), ('hw', [19, 20]),
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
    ('hw', [5, 8, 13]), ('hw', [10, 14, 7]), ('hw', [6, 9, 11]),
    ('hw', [12, 15, 16]), ('hw', [17, 18, 19, 20]),
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
    L7 = "Lecture 7 %s — " + TITLE
    outs = [
        (ROOT / 'lecture7/handout/index.html', booklet(head, tail), L7 % "Booklet"),
        (ROOT / 'lecture7/homework/index.html', homework(head, tail), L7 % "Homework"),
        (ROOT / 'lecture7/_teacher/answer-key.html', key(head, tail), L7 % "Answer Key"),
        (ROOT / 'lecture7/_teacher/model-answers.html', model_answers(head, tail), L7 % "Model Answers"),
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
