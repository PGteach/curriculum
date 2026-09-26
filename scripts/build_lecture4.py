#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Lecture 4's printed material, and the Unit 1 exam.

    python scripts/build_lecture4.py

Writes:
    lecture4/handout/index.html            student booklet: lesson 1-4 + class work
    lecture4/homework/index.html           take-home exercises
    lecture4/_teacher/answer-key.html      key to the class work and homework
    lecture4/_teacher/unit1-exam.html      the Unit 1 exam paper, to print
    lecture4/_teacher/unit1-exam-key.html  its marking scheme

Content comes from lecture4/_teacher/exercises.json and unit1-exam.json. Both
live under _teacher/ on purpose: Jekyll does not serve underscore-prefixed
paths, and this script is itself unpublished (scripts/ is excluded in
_config.yml), so neither the exam nor its answers has a public URL. The exam
is printed by the teacher and handed out in the room.

Everything is textbook material -- lesson 1-4 (pp. 26-32) for the lecture,
lessons 1-1 to 1-4 for the exam -- plus the ministry's assessment book,
which is where the exam's shape comes from: essay questions and four-option
MCQ together. Nothing from the programming foundations of lecture 1.

Every printed document is one section.sheet per A4 page, as everywhere else
in this repo. When an exercise or question is added, add it to a page in the
lists below and re-render each sheet to check it is still one page.

The diagrams are read out of build_lecture4_slides.py rather than copied,
so the booklet shows exactly the picture the deck was taught with.
"""
import io, json, re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "lecture4" / "_teacher"
DATA = json.loads((T / "exercises.json").read_text(encoding="utf-8"))
EXAM = json.loads((T / "unit1-exam.json").read_text(encoding="utf-8"))
EX = {x["n"]: x for x in DATA["SHEET"]["parts"][0]["exercises"]}

TITLE = "Can we trust it?"
ACCENT = "#A63D5B"

# Class work: the book's Worked Example and Try, all quick to mark together.
IN_CLASS = [1, 2, 3, 4]

HW_SECTIONS = [
    ("Part 1 &middot; Bias and privacy",
     "الجزء الأول — التحيز والخصوصية",
     # the first sheet also carries the masthead and the intro box
     [[5], [7, 8, 9], [10]]),
    ("Part 2 &middot; Explainable AI, responsibility, the four principles",
     "الجزء التاني — التفسير والمسؤولية والمبادئ الأربعة",
     # 6 sorts situations into the principles, so it sits with the principles table
     [[11, 12], [6, 13]]),
    ("Part 3 &middot; Apply it",
     "الجزء التالت — طبّق",
     [[14], [15, 16]]),
    ("Challenge &middot; optional",
     "تحدي — اختياري",
     [[17, 18]]),
]
HOMEWORK = [n for _, _, pages in HW_SECTIONS for g in pages for n in g]

EXTRA_CSS = '''
.namebox{display:flex;gap:5mm;margin:0 0 6mm}.namebox>div{flex:1;display:flex;align-items:flex-end;gap:2mm}.namebox span{font-size:9pt;color:var(--soft);font-weight:600}.namebox i{flex:1;border-bottom:1px solid var(--rule);height:6mm}.ex{margin:0 0 5mm;break-inside:avoid}.exhead{display:flex;gap:3mm;align-items:baseline;margin-bottom:1.5mm}.exn{flex:0 0 auto;width:6.5mm;height:6.5mm;border-radius:50%;background:var(--teal);color:#fff;font-size:9pt;font-weight:600;display:flex;align-items:center;justify-content:center}.exq{font-size:10.5pt;font-weight:600}.src{font-size:8pt;color:var(--soft);font-style:italic;margin:0 0 1.5mm 9.5mm}.passage{font-size:10pt;line-height:1.8;background:#FCFCFA;border:1px solid var(--line);padding:3mm}.marks{font-size:9pt;font-weight:600;color:var(--gold);margin:2mm 0}.key{margin-left:9.5mm;font-size:10pt}.teacherwarn{background:#FBF0EE;border-left:3px solid #9C3B2E;padding:3mm}.summary.hw{background:var(--teal-pale)}.keygroup{font-size:9.5pt;color:var(--soft);font-weight:600;text-transform:uppercase;letter-spacing:.04em;margin:5mm 0 2mm}.key ul{margin-left:4mm}.key li{margin-bottom:1mm}.key .note{font-size:9.5pt;color:var(--soft);font-style:italic;margin-top:1.5mm}ol.blanks{list-style:none;margin:3mm 0 0}ol.blanks li{display:flex;align-items:flex-end;gap:3mm;margin-bottom:4.5mm}ol.blanks li b{flex:0 0 auto;font-size:10.5pt}ol.blanks .rule{flex:1;height:6mm;border-bottom:1px solid var(--rule)}.opt{display:block;margin:1.2mm 0 0 4mm}.srcinline{font-size:8pt;color:var(--soft);font-style:italic;margin-left:2mm}ol.qs li{margin-bottom:3mm}.optlead{font-size:10pt;font-weight:600;margin:2.5mm 0 1.5mm}.fields{display:flex;flex-wrap:wrap;gap:2.5mm;margin:0 0 2mm}.chip{border:1px solid var(--line);border-radius:20mm;padding:1.5mm 4mm;font-size:10pt;background:#FCFCFA}
.dg{margin:3mm 0 4mm}.dg svg{display:block;width:100%;height:auto}
.principles{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin:3mm 0}
.principles .pr{border:1px solid var(--line);border-left:3px solid var(--teal);border-radius:1.5mm;padding:2.5mm 3.5mm;background:#FCFCFA}
.principles .pr h4{font-size:10.5pt;margin-bottom:1mm}.principles .pr p{font-size:9.5pt;margin:0}
/* ---------- exam paper ---------- */
.examcover{border:1.5px solid var(--ink);border-radius:2mm;padding:3.5mm 4.5mm;margin:0 0 5mm}
.examcover .facts{display:flex;gap:6mm;font-size:10pt;font-weight:600;margin-bottom:2mm}
.examcover ul{margin:0 0 0 4.5mm;font-size:9.5pt}.examcover li{margin-bottom:.8mm}
.examsec{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.5px solid var(--ink);padding-bottom:1mm;margin:0 0 3mm}
.examsec h2{margin:0}.examsec .tot{font-size:10pt;font-weight:600}
.lvl{font-size:9pt;font-weight:600;color:var(--teal);text-transform:uppercase;letter-spacing:.05em;margin:3.5mm 0 2mm}
.lvl .ar{display:inline;margin-left:2mm;text-transform:none;letter-spacing:0;font-weight:400;color:var(--soft)}
.mq{margin:0 0 3.2mm;break-inside:avoid}
.mq .qline{display:flex;gap:2.5mm;font-size:10pt;font-weight:600;line-height:1.4}
.mq .qn{flex:0 0 7mm}
.mq .opts{display:grid;grid-template-columns:1fr 1fr;gap:.8mm 5mm;margin:1.4mm 0 0 9.5mm;font-size:9.5pt;line-height:1.35}
.mq .opts.long{grid-template-columns:1fr}
.mq .opts b{display:inline-block;width:5mm}
.eq{margin:0 0 4mm;break-inside:avoid}
.eq .qline{display:flex;gap:2.5mm;font-size:10.5pt;font-weight:600;line-height:1.4}
.eq .qn{flex:0 0 7mm}.eq .mk{flex:0 0 auto;margin-left:auto;font-size:9pt;color:var(--gold);white-space:nowrap}
.eq .rule{margin-left:9.5mm}
.answergrid{width:100%;border-collapse:collapse;margin:2mm 0 4mm}
.answergrid td,.answergrid th{border:1px solid var(--line);padding:.9mm 1.8mm;font-size:8.8pt;line-height:1.3;text-align:left}
.answergrid td.let{font-weight:700;color:var(--teal);text-align:center;width:9mm}
'''


def slide_svg(name):
    """Read a diagram out of the deck's builder, so the booklet cannot drift
    from the picture the lesson was taught with."""
    src = (ROOT / "scripts" / "build_lecture4_slides.py").read_text(encoding="utf-8")
    m = re.search(r"^%s = '''(.*?)'''" % name, src, re.DOTALL | re.MULTILINE)
    assert m, "diagram %s not found in the slide builder" % name
    return m.group(1).strip()


def shell():
    t = (ROOT / "templates/handout-template.html").read_text(encoding="utf-8")
    t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    t = (t.replace("__LECTURE_NUM__", "4").replace("__TITLE_HTML__", esc(TITLE))
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
            ' &middot; Lecture 4</div><div class="namebox"><div><span>Name</span><i></i></div>'
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
                '<p>Learn the four principles word for word first &mdash; fairness, transparency, '
                'privacy protection, accountability &mdash; then the two causes of bias, the two '
                'privacy issues, and the difference between responsibility and accountability.</p>'
                '<p class="ar">احفظ المبادئ الأربعة بالتعريف الأول، وبعدين سببين التحيز، ومشكلتين '
                'الخصوصية، والفرق بين المسؤولية والمساءلة.</p></div>')
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
    Only the dividers, the title and the exam QR have no page of their own."""
    BIAS, XAI, WHO = slide_svg("BIAS"), slide_svg("XAI"), slide_svg("WHO")
    p = []
    # slides 2-5: recap, hook, guiding question, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Before we start &middot; lesson 1-3</h2>'
        '<table><tr><th>What AI is good at</th><th>What needs caution</th></tr>'
        '<tr><td>Finding and classifying patterns in data</td><td>Ethical judgments &mdash; discrimination, prejudice</td></tr>'
        '<tr><td>Recognising and generating images, audio, text</td><td>Personal information and privacy</td></tr>'
        '<tr><td>Prediction based on data</td><td>Biased training data</td></tr>'
        '<tr><td></td><td>The black-box problem, and who is responsible</td></tr></table>'
        '<p class="ar">العمود اليمين ده هو درس النهارده كله — هنفتح كل تحذير ونفهمه.</p>'
        '<h2>AI helps decide things about people</h2>'
        '<p>AI now helps make real decisions about people: selecting candidates for job interviews, '
        'identifying individuals through face recognition, and determining how personal data is used. '
        'If the data it learned from was biased, it can be <b>unfair</b> &mdash; and it can be hard to '
        'know <b>why</b> it decided at all.</p>'
        '<p class="ar">الـ AI بيساعد يقرر مين ياخد انترفيو، والكاميرا تقول انت مين، وبياناتك تتستخدم '
        'إزاي. لو الداتا متحيزة ممكن يبقى ظالم، وساعات مش هتعرف قرر كده ليه.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> What ethical issues arise as AI spreads, '
        'and what principles should guide how we use it?</p>'
        '<p class="ar">سؤال النهارده: إيه المشاكل الأخلاقية اللي بتظهر مع انتشار الـ AI، وإيه المبادئ '
        'اللي لازم تمشّي استخدامه؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> A face-recognition AI is more '
        'likely to misidentify people from some ethnic groups than others. Predict who could be harmed '
        'by this, and how. Give a reason. Part 1 explains it.</p>'
        '<p class="ar">مع زميلك: نظام تعرّف على الوجه بيغلط أكتر مع مجموعات معينة. مين ممكن يتأذي، '
        'وإزاي؟ وليه؟</p></div>'))
    # slides 6-9: part 1, definition, diagram, the two places bias gets in
    p.append(page(
        '<h2>Part 1 &middot; Algorithmic bias</h2>'
        + term('Algorithmic bias', 'Bias in AI judgments caused by bias in the training data.',
               'التحيز الخوارزمي: الـ AI بيحكم بشكل متحيز لأن الداتا اللي اتدرب عليها كانت متحيزة.')
        + '<table><tr><th>Example from the book</th><th>Who is treated unfairly</th></tr>'
        '<tr><td class="k">A hiring AI</td><td>Unfairly evaluates applicants of a particular gender</td></tr>'
        '<tr><td class="k">A face-recognition AI</td><td>Is more likely to misidentify particular ethnic groups</td></tr></table>'
        + dg(BIAS)
        + '<h2>Two places bias gets in</h2>'
        '<table><tr><th>In the training data</th><th>In the way the system is built</th></tr>'
        '<tr><td>Insufficient data on certain attributes</td><td>An inappropriate choice of variables</td></tr>'
        '<tr><td>Past discriminatory tendencies reflected in the data</td><td>A <b>proxy variable</b> that '
        'indirectly stands in for a protected attribute</td></tr>'
        '<tr><td></td><td>The design of the model itself</td></tr></table>'
        '<p class="ar">التحيز بيدخل من الداتا (داتا قليلة عن فئات، أو تمييز قديم جوه الداتا) أو من طريقة '
        'بناء النظام (متغيرات غلط، متغير بديل، أو تصميم النموذج).</p>'))
    # slides 10-14: proxy variable, think it through, part 2 privacy, think it through
    p.append(page(
        '<h2>A proxy variable</h2>'
        '<p>A <b>protected attribute</b> is something a decision must not discriminate on &mdash; gender, '
        'or ethnic group. Removing it from the data is <b>not enough</b>. A hiring AI is never told an '
        'applicant&#8217;s gender, but it is given another detail that goes closely with gender: it can '
        'still learn the old bias through that detail, which is standing in for gender.</p>'
        '<p class="ar">لو شلت النوع من الداتا مش كفاية: لو فيه متغير تاني مرتبط بيه أوي، الـ AI هيتعلم '
        'التحيز من خلاله. ده الـ proxy variable.</p>'
        '<div class="summary"><p><b>Think it through.</b> A hiring AI was found to rate applicants of '
        'one gender lower. What is the most likely cause &mdash; and one measure to fix it?</p>'
        '<p class="ar">AI توظيف بيقيّم نوع معين أقل. إيه السبب الأرجح؟ واقترح إجراء واحد يصلّحه.</p></div>'
        '<h2>Part 2 &middot; Privacy</h2>'
        + term('Privacy', 'The appropriate handling and protection of personal data.',
               'الخصوصية: التعامل الصح مع البيانات الشخصية وحمايتها.')
        + '<table><tr><th>1 &middot; Surveillance</th><th>2 &middot; Mass collection</th></tr>'
        '<tr><td>Face-recognition cameras in public spaces</td><td>Large amounts of online behaviour data</td></tr>'
        '<tr><td>Can identify and track individuals</td><td>Collected and analysed</td></tr></table>'
        '<div class="summary"><p><b>Think it through.</b> Face recognition in public spaces can improve '
        'safety and convenience &mdash; and raise privacy concerns. How should the three be balanced, '
        'and which principle is closest to your view?</p>'
        '<p class="ar">إزاي نوازن بين الأمان والراحة والخصوصية؟ وأنهي مبدأ أقرب لرأيك؟</p></div>'))
    # slides 15-18: part 3, black box vs XAI, the definition, who answers
    p.append(page(
        '<h2>Part 3 &middot; Explainable AI and responsibility</h2>'
        + dg(XAI)
        + term('Explainable AI (XAI)',
               'Technology that makes it possible for humans to understand why an AI made a particular judgment.',
               'الـ XAI: تقنية بتخلي البني آدم يفهم الـ AI أخد الحكم ده ليه.')
        + '<p>When the decision-making process is opaque &mdash; a <b>black box</b> &mdash; it is difficult '
        'to verify whether the result is correct. So &#8220;the answer is right, so the process does not '
        'matter&#8221; is <b>false</b>.</p>'
        '<h2>It got it wrong. Who answers?</h2>'
        + dg(WHO)
        + '<p class="ar">المطوّر والمشغّل والمستخدم كل واحد شايفها بشكل، ولسه مفيش معيار واضح متفق عليه.</p>'))
    # slides 19-21: responsibility vs accountability, where it becomes real, pause & think
    p.append(page(
        '<h2>Responsibility is not accountability</h2>'
        '<table><tr><th>Responsibility</th><th>Accountability</th></tr>'
        '<tr><td>The roles and duties of each party</td><td>Being answerable for the AI&#8217;s decisions</td></tr>'
        '<tr><td>Developer, operator, user &mdash; who does what</td><td>Knowing who can be held to account, '
        'according to their role</td></tr>'
        '<tr><td>Who answers when an AI judgment is wrong</td><td>One of the four principles of AI ethics</td></tr></table>'
        '<p class="ar">المسؤولية = أدوار وواجبات كل طرف. المساءلة = إن فيه حد يتحاسب فعلاً حسب دوره، ودي '
        'من المبادئ الأربعة. الوزارة بتسأل على الفرق ده.</p>'
        '<h2>Two places these questions are not theory</h2>'
        '<table><tr><th>Where</th><th>The question it raises</th></tr>'
        '<tr><td class="k">Face recognition</td><td>Useful at a gate &mdash; and it can track people, and '
        'misidentify some groups more than others</td></tr>'
        '<tr><td class="k">Image-diagnosis AI</td><td>If its result is wrong, who is answerable &mdash; and '
        'can anyone see why it decided?</td></tr></table>'
        '<p class="ar">التعرّف على الوجه: خصوصية وتحيز. التشخيص بالصور: صندوق أسود ومسؤولية.</p>'
        '<div class="summary"><p><b>Pause and think.</b> If no one can explain why an AI rejected '
        'someone&#8217;s job application, is that fair? Which principle is missing?</p>'
        '<p class="ar">لو محدش يقدر يشرح الـ AI رفض طلب توظيف ليه، ده عادل؟ وأنهي مبدأ ناقص؟</p></div>'))
    # slides 22-25: part 4, the four principles, which principle is it, exam warning
    p.append(page(
        '<h2>Part 4 &middot; The four principles of AI ethics</h2>'
        '<div class="principles">'
        '<div class="pr"><h4>Fairness</h4><p>Not unjustly discriminating against any particular person or group</p></div>'
        '<div class="pr"><h4>Transparency</h4><p>Showing the AI&#8217;s decision-making process and inner workings clearly</p></div>'
        '<div class="pr"><h4>Privacy protection</h4><p>Handling personal information appropriately and protecting privacy</p></div>'
        '<div class="pr"><h4>Accountability</h4><p>Being answerable for the AI&#8217;s decisions</p></div>'
        '</div>'
        '<p class="ar">احفظهم بالتعريف: العدالة، الشفافية، حماية الخصوصية، المساءلة.</p>'
        '<h2>Which principle is it?</h2>'
        '<table><tr><th>Situation</th><th style="width:26%">Principle</th></tr>'
        '<tr><td>A hiring AI evaluates fairly regardless of gender</td><td>Fairness</td></tr>'
        '<tr><td>The decision-making process is disclosed to users in an easy-to-understand way</td><td>Transparency</td></tr>'
        '<tr><td>Collected personal data is not used for other purposes than originally intended</td><td>Privacy protection</td></tr>'
        '<tr><td>Someone is answerable when an AI&#8217;s diagnostic result turns out to be wrong</td><td>Accountability</td></tr></table>'
        '<h2>Exam warning</h2>'
        '<table><tr><th>Looks right, but is false</th><th>Why</th></tr>'
        '<tr><td>Even if an AI&#8217;s process is opaque, there is no problem as long as the result is correct.</td>'
        '<td>An opaque result cannot be verified.</td></tr>'
        '<tr><td>Who is responsible when an AI is wrong has already been clearly determined.</td>'
        '<td>Views differ; no clear standard exists yet.</td></tr>'
        '<tr><td>Algorithmic bias is caused by the AI&#8217;s processing speed.</td>'
        '<td>It comes from bias in the training data.</td></tr></table>'))
    # slides 26-29: think as an engineer, new context, key takeaway, unit 1
    p.append(page(
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A company wants to use a hiring AI. <b>Investigate</b> one documented '
        'case of an AI accused of bias &mdash; what group did it affect, and what data might have caused '
        'it? <b>Consider responsibility</b>: the developer, the company using it, or the operator. '
        '<b>Decide</b> one rule the company must follow before using it, justified with the principles.</p>'
        '<p class="ar">دوّر على حالة حقيقية، حدد مسؤولية كل طرف، واقترح قاعدة واحدة وبرّرها بالمبادئ.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A school wants face-recognition cameras at its gate to record '
        'attendance automatically. Identify one practical benefit and one privacy concern. If the camera '
        'misidentifies a student, who should be responsible &mdash; the school, or the company that made '
        'the AI? Give a reason.</p>'
        '<p class="ar">فايدة واحدة، ومشكلة خصوصية واحدة، ولو الكاميرا غلطت مين المسؤول وليه.</p></div>'
        '<h2>Key takeaway &middot; accurate is not enough</h2><div class="summary">'
        '<p>If training data is biased, an AI can reproduce that bias. Using AI responsibly means checking '
        'for bias, being able to explain decisions, and knowing who is accountable &mdash; guided by '
        'fairness, transparency, privacy protection and accountability.</p>'
        '<p class="ar">الداتا المتحيزة بتطلّع AI متحيز. الاستخدام المسؤول = نراجع التحيز، ونشرح القرار، '
        'ونعرف مين يتحاسب.</p></div>'
        '<h2>Unit 1 &middot; complete</h2>'
        '<table><tr><th>Lesson</th><th>What to know for the unit exam</th></tr>'
        '<tr><td class="k">1-1 How IT developed</td><td>Five stages, Moore&#8217;s Law, social changes, emerging technologies</td></tr>'
        '<tr><td class="k">1-2 How AI works</td><td>AI &gt; machine learning &gt; deep learning &gt; generative AI, nested</td></tr>'
        '<tr><td class="k">1-3 AI in life and industry</td><td>Where it is used, what it is good at, what needs caution</td></tr>'
        '<tr><td class="k">1-4 Ethical issues with AI</td><td>Bias, privacy, XAI and responsibility, the four principles</td></tr></table>'))
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
    ('hw', [5, 6, 7]), ('hw', [8, 9, 10]), ('hw', [11, 12, 13]),
    ('hw', [14]), ('hw', [15, 16]), ('hw', [17, 18]),
]


def teacher_warn():
    return '<div class="teacherwarn">Teacher copy &mdash; do not hand this to students.</div>'


def key(head, tail):
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


# ---------------------------------------------------------------- the exam
LETTERS = "ABCD"


def placed(item):
    """Options are stored correct-first; put the correct one at `pos`."""
    o = list(item["o"])
    right = o.pop(0)
    i = LETTERS.index(item["pos"])
    o.insert(i, right)
    return o, i


def check_exam():
    mcq, essay = EXAM["mcq"], EXAM["essay"]
    assert len(mcq) == 20, len(mcq)
    for q in mcq:
        assert len(q["o"]) == 4 and len(set(q["o"])) == 4, q["q"]
    letters = [q["pos"] for q in mcq]
    counts = {L: letters.count(L) for L in LETTERS}
    assert set(counts.values()) == {5}, "answer letters not balanced: %s" % counts
    # no run of three of the same letter: a pattern a guesser could ride
    for k in range(len(letters) - 2):
        assert len(set(letters[k:k + 3])) > 1, "three %s in a row at Q%d" % (letters[k], k + 1)
    levels = [q["level"] for q in mcq]
    assert levels == sorted(levels), "MCQ not ordered easy to hard"
    marks = [e["marks"] for e in essay]
    assert marks == sorted(marks), "essays not ordered easy to hard"
    total_mcq, total_essay = len(mcq), sum(marks)
    for e in essay:
        n_pts = len(e["points"])
        assert n_pts == e["marks"], "essay points %d != marks %d: %s" % (n_pts, e["marks"], e["q"][:40])
    for L in ("1-1", "1-2", "1-3", "1-4"):
        assert any(L in q["lesson"] for q in mcq), "no MCQ on lesson " + L
    return total_mcq, total_essay


def exam_head_block(total):
    return ('<div class="brand">Programming &amp; Artificial Intelligence &middot; Grade 11</div>'
            '<h1>' + esc(EXAM["title"]) + ' &mdash; ' + esc(EXAM["unit"]) + '</h1>'
            '<div class="docsub">' + esc(EXAM["lessons"]) + '</div>'
            '<div class="namebox"><div><span>Name</span><i></i></div>'
            '<div><span>Class</span><i></i></div><div><span>Date</span><i></i></div></div>'
            '<div class="examcover"><div class="facts"><span>Time: %d minutes</span>'
            '<span>Total: %d marks</span><span>Section A: %d &middot; Section B: %d</span></div>'
            '<ul><li>Answer <b>all</b> questions.</li>'
            '<li>Section A: circle the letter of the <b>one</b> correct answer.</li>'
            '<li>Section B: write your answer in the space given. The marks show how much to write.</li>'
            '<li>The questions get harder as you go.</li></ul>'
            '<p class="ar">جاوب على كل الأسئلة. القسم أ: حوّط حرف الإجابة الصح الوحيدة. القسم ب: اكتب '
            'إجابتك في المكان المخصص، والدرجات بتوضح تكتب قد إيه. الأسئلة بتصعب واحدة واحدة.</p></div>'
            % (EXAM["minutes"], total[0] + total[1], total[0], total[1]))


def mcq_html(n, item):
    o, _ = placed(item)
    long_ = max(len(x) for x in o) > 42
    return ('<div class="mq"><div class="qline"><span class="qn">' + str(n) + '.</span><span>'
            + esc(item["q"]) + '</span></div><div class="opts' + (' long' if long_ else '') + '">'
            + ''.join('<span><b>' + LETTERS[i] + '</b>' + esc(x) + '</span>' for i, x in enumerate(o))
            + '</div></div>')


def essay_html(n, e):
    return ('<div class="eq"><div class="qline"><span class="qn">' + str(n) + '.</span><span>'
            + esc(e["q"]) + '</span><span class="mk">[' + str(e["marks"]) + ' marks]</span></div>'
            + rules(e["lines"]) + '</div>')


# which questions go on which printed page -- verified by rendering each
# sheet alone and counting one A4 page
EXAM_PAGES = [
    # page 1 carries the cover, which takes about a third of the sheet
    ("A", [0, 1, 2, 3, 4]),
    ("A", [5, 6, 7, 8, 9, 10, 11]),
    ("A", [12, 13, 14, 15, 16, 17, 18, 19]),
    ("B", [0, 1, 2]),
    ("B", [3, 4]),
    ("B", [5]),
]


def exam_paper(head, tail):
    total = check_exam()
    pages, seen_sec, seen_lvl = [], set(), set()
    for sec, idx in EXAM_PAGES:
        b = []
        if not pages:
            b.append(exam_head_block(total))
        if sec not in seen_sec:
            if sec == "A":
                b.append('<div class="examsec"><h2>Section A &middot; Multiple choice</h2>'
                         '<span class="tot">%d marks &middot; 1 mark each</span></div>' % total[0])
            else:
                b.append('<div class="examsec"><h2>Section B &middot; Written answers</h2>'
                         '<span class="tot">%d marks</span></div>' % total[1])
            seen_sec.add(sec)
        for i in idx:
            if sec == "A":
                lv = EXAM["mcq"][i]["level"]
                if lv not in seen_lvl:
                    L = EXAM["levels"][lv]
                    b.append('<div class="lvl">' + esc(L["name"]) + '<span class="ar">'
                             + esc(L["nameAr"]) + '</span></div>')
                    seen_lvl.add(lv)
                b.append(mcq_html(i + 1, EXAM["mcq"][i]))
            else:
                b.append(essay_html(len(EXAM["mcq"]) + i + 1, EXAM["essay"][i]))
        if sec == "B" and idx[-1] == len(EXAM["essay"]) - 1:
            b.append('<p style="text-align:center;margin-top:4mm;font-weight:600">End of the exam</p>')
        pages.append(page(''.join(b)))
    return head + ''.join(pages) + tail


def exam_key(head, tail):
    total = check_exam()
    rows = []
    for i, q in enumerate(EXAM["mcq"]):
        o, k = placed(q)
        rows.append('<tr><td>%d</td><td class="let">%s</td><td>%s</td><td>%s</td></tr>'
                    % (i + 1, LETTERS[k], esc(o[k]), esc(q["lesson"] + " — " + q["src"])))
    grid = ('<table class="answergrid"><tr><th style="width:8mm">Q</th><th>Ans</th>'
            '<th>Correct option</th><th style="width:34%">Source</th></tr>' + ''.join(rows) + '</table>')
    first = page(masthead_exam_key(total)
                 + '<div class="keygroup">Section A &mdash; answers (1 mark each)</div>' + grid)
    essays = []
    for i, e in enumerate(EXAM["essay"]):
        n = len(EXAM["mcq"]) + i + 1
        block = ('<div class="ex"><div class="exhead"><span class="exn">' + str(n) + '</span>'
                 '<span class="exq">' + esc(e["q"]) + '</span></div>'
                 '<div class="src">' + esc(e["lesson"] + " — " + e["src"]) + '</div>'
                 '<div class="key"><div class="marks">[' + str(e["marks"]) + ' marks]</div>'
                 '<p><b>Model answer.</b> ' + esc(e["model"]) + '</p>'
                 '<p><b>Award a mark for each:</b></p><ul>'
                 + ''.join('<li>' + esc(x) + '</li>' for x in e["points"]) + '</ul>'
                 + ('<p class="note"><b>Marking.</b> ' + esc(e["marking"]) + '</p>' if e.get("marking") else '')
                 + '</div></div>')
        essays.append(block)
    # essays 21-23 on one page, 24-25 on the next, 26 alone
    p2 = page('<div class="keygroup">Section B &mdash; marking scheme</div>' + ''.join(essays[0:3]))
    p3 = page(''.join(essays[3:5]))
    p4 = page(essays[5]
              + '<div class="summary"><p><b>Total: %d marks.</b> Section A %d, Section B %d. '
                'Accept any wording that carries the point; the book&#8217;s words are not required, '
                'the idea is.</p><p class="ar">اقبل أي صياغة فيها الفكرة؛ مش لازم كلام الكتاب بالحرف.</p></div>'
              % (total[0] + total[1], total[0], total[1]))
    return head + first + p2 + p3 + p4 + tail


def masthead_exam_key(total):
    return ('<div class="brand">Programming &amp; Artificial Intelligence &middot; Grade 11</div>'
            '<h1>' + esc(EXAM["title"]) + ' &mdash; Marking scheme</h1>'
            '<div class="docsub">' + esc(EXAM["unit"]) + ' &middot; ' + esc(EXAM["lessons"])
            + ' &middot; %d marks</div>' % (total[0] + total[1]) + teacher_warn())


if __name__ == "__main__":
    head, tail = shell()
    outs = [
        (ROOT / 'lecture4/handout/index.html', booklet(head, tail)),
        (ROOT / 'lecture4/homework/index.html', homework(head, tail)),
        (ROOT / 'lecture4/_teacher/answer-key.html', key(head, tail)),
        (ROOT / 'lecture4/_teacher/unit1-exam.html', exam_paper(head, tail)),
        (ROOT / 'lecture4/_teacher/unit1-exam-key.html', exam_key(head, tail)),
    ]
    for path, html in outs:
        # the template ships author instructions in HTML comments; not ours to publish
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        assert not re.search(r"\{[%{]", html), "Liquid delimiter in " + path.name
        with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print("%-40s %6d bytes, %2d sheets" % (path.relative_to(ROOT), len(html),
                                               html.count('<section class="sheet')))
