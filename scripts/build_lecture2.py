#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Lecture 2's three printable documents from one source of truth.

    python scripts/build_lecture2.py

Writes:
    lecture2/handout/index.html       the student booklet (lesson + class work)
    lecture2/homework/index.html      the take-home exercises
    lecture2/_teacher/answer-key.html the teacher copy, both sets
                                     (_teacher/ is not served by Jekyll)

The lesson prose is BOOKLET below; the exercises and their answers come from
lecture2/_teacher/exercises.json, which was written from the textbook (Programming and
Artificial Intelligence, Part One, Egyptian Baccalaureate 2nd Year, MOETE 2026,
pp. 4-12). Every exercise carries the page it came from.

Nothing here invents content: the prose says what the slides say, and the
exercises are the book's own.
"""

from __future__ import annotations

import io
import json
import re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "lecture2" / "_teacher" / "exercises.json")
                  .read_text(encoding="utf-8"))
SHEET, ANSWERS = DATA["SHEET"], DATA["ANSWERS"]
TEMPLATE = ROOT / "templates" / "handout-template.html"

LETTERS = "ABCDEFGH"

# Which exercises are done in the session and which go home. Kept short in
# class on purpose — the session is 90-120 minutes and most of it is teaching.
IN_CLASS = [1, 2, 7, 8]
HOMEWORK = [3, 4, 5, 6, 9, 10, 11, 12, 13]


# --------------------------------------------------------------------------
# The lesson, as it is taught on the slides. One list per printed page.
# Blocks: h2 p lead ar table term stages callout ex pagebreak
# Prose may contain <b>/<i>; it is written here, not user input.
# --------------------------------------------------------------------------
BOOKLET = [
    # ---------------- page 1 ----------------
    [
        ("h2", "Before we start"),
        ("lead", "Last time we said three things. Today's lesson stands on them."),
        ("stages", [
            ("1", "A computer is dumb",
             "Input &rarr; processing &rarr; output. Nothing more."),
            ("2", "Programming vs. AI",
             "You write the rule, or the computer works it out from examples."),
            ("3", "The tools",
             "An editor writes, a compiler translates, an IDE does both."),
        ]),
        ("ar", "مراجعة سريعة لمحاضرة 1. والنهارده هنشوف الجهاز ده أخد تمانين سنة "
               "عشان يصغّر لدرجة إنه يبقى في جيبك."),
        ("h2", "Part A &middot; What is actually inside the box?"),
        ("p", "Before we talk about how computers changed the world, let us open one. "
              "Every computer you have ever touched &mdash; your phone, a laptop, the "
              "server running YouTube &mdash; has the same four kinds of part."),
        ("table", ["Part", "What it does"], [
            ["CPU", "Does the thinking. Follows instructions one after another."],
            ["RAM", "Holds only what you are using right now."],
            ["Storage", "Keeps your files even when the power is off."],
            ["Input / Output", "How you talk to it, and how it answers."],
        ]),
        ("ar", "أي كمبيوتر لمسته في حياتك فيه نفس الأربع أنواع دي — موبايل، لابتوب، "
               "أو سيرفر. المعالج بيفكر، الرام بتشيل اللي بتشتغل عليه دلوقتي، وحدة "
               "التخزين بتحفظ للأبد، والإدخال والإخراج هما طريقتك تتكلم مع الجهاز."),
        ("term", "The CPU &mdash; Central Processing Unit",
         "This is where the <b>processing</b> stage from Lecture 1 actually happens. "
         "It follows your instructions one after another, extremely fast. More "
         "transistors inside it means more work per second &mdash; remember that, it "
         "comes back later in this lesson."),
    ],
    # ---------------- page 2 ----------------
    [
        ("h2", "RAM is not storage"),
        ("p", "This is the one students mix up most, and it is worth getting right "
              "now. Watch what happens when the power goes off."),
        ("table", ["", "RAM &mdash; the desk you work on", "Storage &mdash; the cupboard"], [
            ["Speed", "Fast", "Slower"],
            ["Power off", "Wiped clean", "Still all there"],
            ["Holds", "Your open apps and tabs", "Your photos and files"],
            ["Lasts", "Only while the power is on", "Permanently"],
        ]),
        ("callout", None, [
            "<b>If you never saved it, it was only ever in RAM.</b> That is why an "
            "hour of unsaved work disappears when the battery dies.",
        ]),
        ("ar", "دي أكتر حاجة الطلبة بيلخبطوا فيها. لو محفظتش الملف، يبقى كان في الرام "
               "بس — وضاع. الرام مؤقتة وسريعة وبتتمسح لما الجهاز يتقفل. وحدة التخزين "
               "أبطأ بس بتحتفظ بكل حاجة."),
        ("h2", "Input and output devices"),
        ("table", ["Input &mdash; you &rarr; machine", "Output &mdash; machine &rarr; you"], [
            ["Keyboard, mouse", "Screen"],
            ["Microphone, camera", "Speakers, headphones"],
            ["Fingerprint sensor", "Printer, vibration"],
        ]),
        ("callout", None, [
            "A <b>touchscreen is both</b> &mdash; it takes your finger in and shows "
            "the picture out. This is a very common exam question.",
        ]),
        ("ar", "الشاشة اللي بتلمس هي إدخال وإخراج في نفس الوقت — بتاخد لمستك وبتوريك "
               "الصورة. ودي بتيجي في الامتحان كتير."),
    ],
    # ---------------- page 3 ----------------
    [
        ("h2", "Class work &middot; Part A"),
        ("ex", 1),
        ("ex", 2),
    ],
    # ---------------- page 4 ----------------
    [
        ("h2", "Part B &middot; How information technology developed"),
        ("p", "Those same four parts, eighty years ago, filled a whole room. "
              "Information technology developed in five stages. At each one it "
              "introduced a new technology or service <b>and</b> changed how society "
              "communicates, works, learns and pays."),
        ("table", ["Period", "Major technologies and events", "Impact on society"], [
            ["1940s&ndash;60s", "Birth of the computer (ENIAC, vacuum tubes)",
             "Mainly military and scientific computation"],
            ["1970s&ndash;80s", "Spread of personal computers (PCs)",
             "Beginning of personal computer use"],
            ["1990s", "Commercialization of the Internet; the Web",
             "Globalization of information; spread of email"],
            ["2000s", "Rise of smartphones", "Explosive spread of mobile Internet"],
            ["2010s onward", "Spread of cloud computing",
             "Large-scale data analysis and AI; &ldquo;IT as a service&rdquo;"],
        ]),
        ("ar", "الجدول ده حرفيًا من الكتاب. خلي بالك من الترتيب — بييجي في الامتحان "
               "كسؤال ترتيب زمني. نفس الوظيفة، بس الجهاز بيصغر في كل مرحلة."),
    ],
    # ---------------- page 5 ----------------
    [
        ("h2", "Moore&rsquo;s Law"),
        ("p", "A <b>transistor</b> is a tiny switch inside a chip. More switches means "
              "more computing power. Moore noticed that the number of them "
              "<b>doubles about every two years</b>."),
        ("table", ["After", "Transistors"], [
            ["Year 0", "1"],
            ["2 years", "2"],
            ["4 years", "4"],
            ["6 years", "8"],
            ["20 years", "&times;1,024 more than you started with"],
        ]),
        ("callout", None, [
            "Doubling looks small at first, then gets enormous fast. That is why a "
            "phone caught up with machines that once filled a room.",
            "Moore never said it <i>must</i> happen &mdash; he just noticed that it "
            "kept happening. It is an <b>observation</b>, not a physical law. That "
            "distinction is examined.",
        ]),
        ("ar", "الترانزستور مفتاح صغير جوه الشريحة — مفاتيح أكتر معناها قدرة أكبر. "
               "وقانون مور ملاحظة إن عددهم بيتضاعف كل سنتين تقريبًا. خلي بالك: دي "
               "ملاحظة مش قانون فيزيائي، وده اللي بيتسأل عليه في الامتحان."),
        ("h2", "Why shrinking is getting hard"),
        ("table", ["The problems", "The responses"], [
            ["<b>Quantum tunneling</b> &mdash; electrons slip straight through a "
             "barrier once it is made too thin",
             "<b>Parallel processing</b> using multiple processor cores"],
            ["<b>Leakage current</b> &mdash; current escapes unintentionally",
             "<b>Quantum computers</b> based on the principles of quantum mechanics"],
            ["Hard to get higher performance and lower power at the same time", ""],
        ]),
        ("ar", "لما الترانزستورات تصغر أوي بتحصل مشكلتين: النفق الكمومي (الإلكترونات "
               "بتتسرب من الحواجز) وتسرب التيار. والحلول: المعالجة المتوازية بأنوية "
               "متعددة، والحواسيب الكمومية."),
    ],
    # ---------------- page 6 ----------------
    [
        ("h2", "Five things IT changed about daily life"),
        ("table", ["Change", "What it means"], [
            ["SNS<br><span class='tiny'>Social Networking Service</span>",
             "Services that let users connect, post and share information. Highly "
             "effective at spreading information rapidly."],
            ["E-commerce<br><span class='tiny'>EC</span>",
             "Buying and selling goods and services <b>through the Internet</b>. "
             "For example Amazon, eBay."],
            ["Remote work",
             "Work performed from home or other remote locations using the Internet."],
            ["Online learning",
             "Classes and study materials delivered using the Internet."],
            ["Cashless payment",
             "Payment using electronic money, QR codes and similar, without cash."],
        ]),
        ("ar", "الخمس تغييرات بتعريفاتها من الكتاب. أشهر غلطة: إن التجارة الإلكترونية "
               "تتعرّف على إنها شراء من محل بالكاش — ده عكس التعريف بالظبط."),
    ],
    # ---------------- page 7 ----------------
    [
        ("h2", "Emerging technologies"),
        ("term", "Autonomous driving",
         "Uses AI to drive a vehicle <b>without human operation</b>. Cameras and "
         "sensors recognise the surroundings, it makes driving decisions, and it "
         "controls the vehicle. A delay of even <b>0.1 seconds</b> can cause an "
         "accident, so it uses <b>edge computing</b> &mdash; the decision is made "
         "instantly on the vehicle itself, not sent to the cloud for judgment."),
        ("term", "AR &mdash; Augmented Reality",
         "Overlays digital information on real-world images. The real world is still "
         "there; you add to it."),
        ("term", "VR &mdash; Virtual Reality",
         "Lets users immerse themselves in a virtual space generated by a computer. "
         "The real world is replaced."),
        ("term", "Quantum computing",
         "Expected to dramatically speed up computations that are difficult or "
         "impossible for traditional computers, by using the principles of quantum "
         "mechanics. A normal bit is 0 <i>or</i> 1; a qubit uses <b>superposition</b> "
         "and can hold both at once."),
        ("ar", "الواقع المعزز بيضيف معلومات رقمية فوق صور العالم الحقيقي. الواقع "
               "الافتراضي بيحط المستخدم جوه فضاء افتراضي. والقيادة الذاتية بتعتمد على "
               "الحوسبة الطرفية عشان عُشر ثانية كفاية تعمل حادثة."),
    ],
    # ---------------- page 8 ----------------
    [
        ("h2", "Exam warning &middot; two sentences that look right but are wrong"),
        ("p", "Both of these appear in the textbook exercises, and students pick them "
              "every year."),
        ("table", ["The wrong sentence", "Why it is wrong"], [
            ["&#10007; &ldquo;VR speeds up a computer&rdquo;",
             "VR has nothing to do with speed. It puts you inside a space the "
             "computer generates. The thing that speeds computation up is "
             "<b>quantum computing</b>."],
            ["&#10007; &ldquo;E-commerce is paying cash in a shop&rdquo;",
             "That is just ordinary shopping. E-commerce is buying and selling "
             "<b>over the Internet</b>. No Internet, no e-commerce."],
        ]),
        ("ar", "الجملتين دول موجودين في تمارين الكتاب والطلبة بيختاروهم غلط كل سنة. "
               "الأولى: VR ملهاش علاقة بالسرعة — اللي بيسرّع هو الحوسبة الكمومية. "
               "الثانية: التجارة الإلكترونية لازم تكون عبر الإنترنت."),
        ("h2", "Key takeaway"),
        ("callout", None, [
            "IT developed in stages &mdash; computers, the Internet, smartphones, "
            "cloud computing.",
            "At each stage it introduced a new technology or service <b>and</b> "
            "changed how society communicates, works, learns and pays.",
            "The same four parts &mdash; CPU, RAM, storage, input/output &mdash; "
            "filled a room eighty years ago and are in your pocket now.",
        ]),
        ("ar", "الخلاصة: تكنولوجيا المعلومات اتطورت على مراحل — كمبيوتر، إنترنت، "
               "موبايل، سحابة. وكل مرحلة ضافت تقنية جديدة وغيّرت طريقة تواصل المجتمع "
               "وشغله وتعلّمه ودفعه."),
    ],
    # ---------------- last page: the work done in the session ----------------
    [
        ("h2", "Class work &middot; Part B"),
        ("ex", 7),
        ("ex", 8),
        ("homework_note", None),
    ],
]


# --------------------------------------------------------------------------
# exercise rendering
# --------------------------------------------------------------------------
def rules(n, tight=True):
    cls = "rule tight" if tight else "rule"
    return "".join('<div class="%s"></div>' % cls for _ in range(n))


def ex_head(ex):
    out = ['<div class="ex">',
           '<div class="exhead"><span class="exn">%d</span>'
           '<span class="exq">%s</span></div>' % (ex["n"], esc(ex["prompt"]))]
    if ex.get("promptAr"):
        out.append('<p class="ar">%s</p>' % esc(ex["promptAr"]))
    if ex.get("src"):
        out.append('<div class="src">%s</div>' % esc(ex["src"]))
    return "\n".join(out)


def render_ex(ex):
    t = ex["type"]
    b = [ex_head(ex)]

    if t == "match":
        # the right column is already scrambled in the data, so the rows
        # cannot simply be paired off top to bottom
        b.append('<table class="matchtbl"><tr><th style="width:6%">#</th>'
                 '<th>Item</th><th style="width:10%">Answer</th>'
                 '<th style="width:6%">&nbsp;</th><th>Options</th></tr>')
        for i, left in enumerate(ex["left"]):
            right = ex["right"][i] if i < len(ex["right"]) else ""
            b.append('<tr><td>%d</td><td>%s</td><td class="blank"></td>'
                     '<td>%s</td><td>%s</td></tr>'
                     % (i + 1, esc(left), LETTERS[i], esc(right)))
        b.append("</table>")

    elif t == "table":
        b.append("<table>")
        b.append("<tr>%s</tr>" % "".join("<th>%s</th>" % esc(h) for h in ex["head"]))
        for row in ex["rows"]:
            cells = []
            for j, c in enumerate(row):
                if set(c.strip()) == {"_"}:
                    cells.append('<td class="blank"></td>')
                else:
                    cells.append('<td%s>%s</td>'
                                 % (' class="k"' if j == 0 else "", esc(c)))
            b.append("<tr>%s</tr>" % "".join(cells))
        b.append("</table>")

    elif t == "short":
        qs = ex["questions"]
        # a single untitled question is just the prompt with room to answer
        if len(qs) == 1 and not qs[0]["q"].strip():
            b.append(rules(qs[0].get("lines", 3), tight=False))
            b.append("</div>")
            return "\n".join(b)
        b.append('<ol class="qs">')
        for q in qs:
            src = ('<span class="srcinline">%s</span>' % esc(q["src"])) if q.get("src") else ""
            b.append("<li>%s%s%s</li>"
                     % (esc(q["q"]), src, rules(q.get("lines", 1))))
        b.append("</ol>")

    elif t == "sort":
        b.append('<div class="fields">%s</div>'
                 % "".join('<span class="chip">%s</span>' % esc(i) for i in ex["items"]))
        b.append("<table><tr>%s</tr><tr>%s</tr></table>"
                 % ("".join("<th>%s</th>" % esc(c) for c in ex["columns"]),
                    "".join('<td class="sortcell"></td>' for _ in ex["columns"])))

    elif t == "fill":
        b.append('<p class="passage">%s</p>' % esc(ex["passage"]))
        b.append('<ol class="qs lettered">')
        for letter in "abcde":
            if "( %s )" % letter in ex["passage"]:
                b.append("<li><b>( %s )</b>%s</li>" % (letter, rules(1)))
        b.append("</ol>")

    elif t == "order":
        b.append('<table class="ordtbl"><tr><th style="width:14%">Order</th>'
                 '<th>Stage</th></tr>')
        for item in ex["items"]:
            b.append('<tr><td class="blank"></td><td>%s</td></tr>' % esc(item))
        b.append("</table>")

    elif t == "truefalse":
        b.append('<table class="tftbl"><tr><th style="width:8%">&#10003; / &#10007;</th>'
                 '<th>Statement</th></tr>')
        for s in ex["statements"]:
            b.append('<tr><td class="blank"></td><td>%s</td></tr>' % esc(s))
        b.append("</table>")

    elif t == "category":
        b.append('<table class="cattbl"><tr><th style="width:12%">A / B / C</th>'
                 '<th>Item</th></tr>')
        for item in ex["items"]:
            b.append('<tr><td class="blank"></td><td>%s</td></tr>' % esc(item))
        b.append("</table>")

    elif t == "extended":
        if ex.get("marks"):
            b.append('<div class="marks">[%d marks]</div>' % ex["marks"])
        b.append(rules(ex.get("lines", 5), tight=False))

    else:
        raise SystemExit("unknown exercise type: %s" % t)

    b.append("</div>")
    return "\n".join(b)


BY_N = {}
for _part in SHEET["parts"]:
    for _ex in _part["exercises"]:
        BY_N[_ex["n"]] = _ex


# --------------------------------------------------------------------------
# booklet block rendering
# --------------------------------------------------------------------------
def render_block(kind, *args):
    if kind == "h2":
        return "<h2>%s</h2>" % args[0]
    if kind == "p":
        return "<p>%s</p>" % args[0]
    if kind == "lead":
        return '<p class="lead">%s</p>' % args[0]
    if kind == "ar":
        return '<p class="ar">%s</p>' % args[0]
    if kind == "table":
        heads, rows = args
        out = ["<table>", "<tr>%s</tr>" % "".join("<th>%s</th>" % h for h in heads)]
        for row in rows:
            out.append("<tr>%s</tr>"
                       % "".join('<td%s>%s</td>' % (' class="k"' if j == 0 else "", c)
                                 for j, c in enumerate(row)))
        out.append("</table>")
        return "\n".join(out)
    if kind == "term":
        return '<div class="term"><h4>%s</h4><p>%s</p></div>' % args
    if kind == "stages":
        cells = "".join('<div class="stage"><div class="n">%s</div>'
                        '<h4>%s</h4><p>%s</p></div>' % s for s in args[0])
        return '<div class="stages">%s</div>' % cells
    if kind == "callout":
        _, lines = args
        return '<div class="summary">%s</div>' % "".join("<p>%s</p>" % l for l in lines)
    if kind == "ex":
        return render_ex(BY_N[args[0]])
    if kind == "homework_note":
        return ('<div class="summary hw"><p><b>Homework</b> is on a separate sheet '
                '&mdash; nine exercises, including two written answers. '
                'Bring it to the next session.</p>'
                '<p class="ar">الواجب في ورقة منفصلة — تسع تمارين، منهم سؤالين '
                'إجابة مكتوبة. هاتها معاك المرة الجاية.</p></div>')
    raise SystemExit("unknown block: %s" % kind)


FOOT = ('<div class="foot"><span>Prepared by: Mr. Eissa Islam</span>'
        '<span class="pageno"></span></div>')

EXTRA_CSS = """
/* ---------- exercises ---------- */
.namebox{display:flex; gap:5mm; margin:0 0 6mm}
.namebox > div{flex:1; display:flex; align-items:flex-end; gap:2mm}
.namebox span{font-size:9pt; color:var(--soft); font-weight:600; white-space:nowrap}
.namebox i{flex:1; border-bottom:1px solid var(--rule); height:6mm}
.ex{margin:0 0 5mm; break-inside:avoid}
.exhead{display:flex; gap:3mm; align-items:baseline; margin-bottom:1.5mm}
.exn{
  flex:0 0 auto; width:6.5mm; height:6.5mm; border-radius:50%;
  background:var(--teal); color:#fff; font-size:9pt; font-weight:600;
  display:flex; align-items:center; justify-content:center;
}
.exq{font-size:10.5pt; font-weight:600}
.src{font-size:8pt; color:var(--soft); font-style:italic; margin:0 0 1.5mm 9.5mm}
.srcinline{font-size:8pt; color:var(--soft); font-style:italic; margin-left:2mm}
.passage{
  font-size:10pt; line-height:1.9; background:#FCFCFA;
  border:1px solid var(--line); border-radius:2mm; padding:3.5mm; margin:2mm 0 3mm;
}
td.blank{background:#FCFCFA}
td.sortcell{height:26mm; background:#FCFCFA; vertical-align:top}
ol.qs.lettered{list-style:none; margin-left:0}
.marks{font-size:9pt; font-weight:600; color:var(--gold); margin-bottom:2mm}
.matchtbl td,.ordtbl td,.tftbl td,.cattbl td{vertical-align:middle}
.tiny{font-size:8pt; color:var(--soft); font-weight:400}
.summary.hw{background:var(--teal-pale)}

/* ---------- teacher key ---------- */
.keysheet{min-height:auto}
.teacherwarn{
  background:#FBF0EE; border-left:3px solid #9C3B2E; color:#9C3B2E;
  font-size:9.5pt; font-weight:600; padding:2.5mm 3.5mm; margin-bottom:6mm;
}
.keygroup{font-size:9.5pt; color:var(--soft); font-weight:600;
  text-transform:uppercase; letter-spacing:.04em; margin:5mm 0 2mm}
.key{margin-left:9.5mm; font-size:10pt}
.key ul{margin-left:4mm}
.key li{margin-bottom:1mm}
.key .note{font-size:9.5pt; color:var(--soft); font-style:italic; margin-top:1.5mm}
"""


def shell():
    """The template with our CSS added, split at the point pages go in."""
    tpl = TEMPLATE.read_text(encoding="utf-8")
    tpl = tpl.replace("</style>", EXTRA_CSS + "</style>", 1)
    # the template ships with placeholders new_lecture.py fills in
    tpl = (tpl.replace("__LECTURE_NUM__", "2")
              .replace("__TITLE_HTML__", esc(SHEET["title"]))
              .replace("__TITLE_JS__", SHEET["title"].replace('"', '\\"'))
              .replace("__TOPIC_HTML__", "Programming &amp; Artificial Intelligence")
              .replace("__TOPIC_JS__", "Programming & Artificial Intelligence")
              .replace("__ACCENT__", "#6A4C93"))
    head = tpl[:tpl.index('<div id="pagesTop"></div>') + len('<div id="pagesTop"></div>')]
    tail = tpl[tpl.index("<script>"):]
    qr = re.search(r'<!-- =+ LAST PAGE \(keep the QR\) =+ -->\s*'
                   r'(<section class="sheet">.*?</section>)', tpl, re.DOTALL).group(1)
    return head, tail, qr


def masthead(subtitle, with_names=True):
    out = ['<div class="brand" id="brand">Programming &amp; Artificial Intelligence</div>',
           '<h1 id="docTitle">%s</h1>' % esc(SHEET["title"]),
           '<div class="docsub">%s &middot; Lecture %d</div>'
           % (esc(subtitle), SHEET["lecture"])]
    if with_names:
        out.append('<div class="namebox">'
                   '<div><span>Name</span><i></i></div>'
                   '<div><span>Class</span><i></i></div>'
                   '<div><span>Date</span><i></i></div></div>')
    return "\n".join(out)


def qr_panel(qr, heading, blurb):
    return (qr.replace("<h2>Session Summary</h2>", "<h2>Test yourself online</h2>")
              .replace('<div class="summary">\n    <p>Three or four one-line takeaways from the session.</p>\n    <p>One per line, in the order they were taught.</p>\n  </div>', "")
              .replace("<p>Three or four one-line takeaways from the session.</p>", "")
              .replace("<p>One per line, in the order they were taught.</p>", "")
              .replace("<h3>Test yourself · about 5 minutes</h3>",
                       "<h3>%s</h3>" % heading)
              .replace("which parts of this session you have understood",
                       blurb)
              .replace("<h2>My Notes</h2>", "<h2>My notes</h2>"))


def build_booklet(head, tail, qr):
    pages = []
    for i, blocks in enumerate(BOOKLET):
        body = [masthead("Student Booklet")] if i == 0 else []
        body += [render_block(*b) for b in blocks]
        body.append(FOOT)
        pages.append('<section class="sheet">\n%s\n</section>' % "\n".join(body))
    panel = qr_panel(qr, "Exam &middot; Lectures 1 and 2 &middot; about 10 minutes",
                     "which parts of the two sessions you have understood")
    return head + "\n\n" + "\n\n".join(pages) + "\n\n" + panel + "\n\n" + tail


# each group is one printed A4 page; verified by rendering
HW_PAGES = [[3, 4], [5, 6], [9, 10], [11, 12], [13]]


def build_homework(head, tail, qr):
    pages = []
    for i, group in enumerate(HW_PAGES):
        body = []
        if i == 0:
            body.append(masthead("Homework"))
            body.append('<div class="summary"><p>Nine exercises. Everything here was '
                        'taught in the session &mdash; the booklet has the notes if '
                        'you need them. Bring this to the next class.</p>'
                        '<p class="ar">تسع تمارين. كل حاجة هنا اتشرحت في الحصة، '
                        'والكتيّب معاك لو محتاج ترجعله. هات الورقة دي المرة الجاية.</p></div>')
        for n in group:
            body.append(render_ex(BY_N[n]))
        body.append(FOOT)
        pages.append('<section class="sheet">\n%s\n</section>' % "\n".join(body))
    panel = qr_panel(qr, "Exam &middot; Lectures 1 and 2 &middot; about 10 minutes",
                     "which parts of the two sessions you have understood")
    return head + "\n\n" + "\n\n".join(pages) + "\n\n" + panel + "\n\n" + tail


def key_entry(ex):
    a = ANSWERS.get(str(ex["n"]))
    out = ['<div class="ex"><div class="exhead">'
           '<span class="exn">%d</span><span class="exq">%s</span></div>'
           % (ex["n"], esc(ex["prompt"]))]
    if ex.get("src"):
        out.append('<div class="src">%s</div>' % esc(ex["src"]))
    out.append('<div class="key">')
    if isinstance(a, list):
        out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % esc(str(x)) for x in a))
    elif isinstance(a, dict):
        items = []
        for k, v in a.items():
            if k in ("note", "src"):
                continue
            val = ", ".join(v) if isinstance(v, list) else str(v)
            items.append("<li><b>%s</b> &mdash; %s</li>" % (esc(k), esc(val)))
        out.append("<ul>%s</ul>" % "".join(items))
        if a.get("note"):
            out.append('<p class="note">%s</p>' % esc(a["note"]))
        if a.get("src"):
            out.append('<div class="src">%s</div>' % esc(a["src"]))
    elif a is not None:
        out.append("<p>%s</p>" % esc(str(a)))
    else:
        out.append('<p class="note">Open response &mdash; mark on the points named '
                   'in the question.</p>')
    out.append("</div></div>")
    return "\n".join(out)


def build_key(head, tail):
    body = [masthead("Teacher Answer Key", with_names=False),
            '<div class="teacherwarn">Teacher copy &mdash; do not hand this to '
            'students.</div>']
    for label, nums in (("Class work &mdash; done in the session", IN_CLASS),
                        ("Homework &mdash; separate sheet", HOMEWORK)):
        body.append('<div class="keygroup">%s</div>' % label)
        for n in nums:
            body.append(key_entry(BY_N[n]))
    body.append(FOOT)
    return (head + '\n\n<section class="sheet keysheet">\n%s\n</section>\n\n'
            % "\n".join(body)) + tail


def main():
    head, tail, qr = shell()
    targets = {
        ROOT / "lecture2" / "handout" / "index.html": build_booklet(head, tail, qr),
        ROOT / "lecture2" / "homework" / "index.html": build_homework(head, tail, qr),
        # _teacher/ is ignored by Jekyll, so the answers are versioned and
        # backed up but never served from the public site.
        ROOT / "lecture2" / "_teacher" / "answer-key.html": build_key(head, tail),
    }
    for path, html in targets.items():
        if path.name == "answer-key.html":
            html = html.replace("<title>Lecture 2 Handout",
                                "<title>Lecture 2 Answer Key")
        elif "homework" in path.parts:
            html = html.replace("<title>Lecture 2 Handout",
                                "<title>Lecture 2 Homework")
        path.parent.mkdir(parents=True, exist_ok=True)
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)
        print("%-44s %6d bytes" % (path.relative_to(ROOT).as_posix(), len(html)))

    missing = sorted(set(BY_N) - set(IN_CLASS) - set(HOMEWORK))
    if missing:
        raise SystemExit("exercises in neither set: %s" % missing)
    print("\nclass work: %s   homework: %s" % (IN_CLASS, HOMEWORK))


if __name__ == "__main__":
    main()
