#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Lecture 5's printed material.

    python scripts/build_lecture5.py

Writes:
    lecture5/handout/index.html            student booklet: lesson 2-1 + class work
    lecture5/homework/index.html           take-home exercises
    lecture5/_teacher/answer-key.html      key to the class work and homework

Content comes from lecture5/_teacher/exercises.json, which lives under
_teacher/ on purpose: Jekyll does not serve underscore-prefixed paths, and
this script is itself unpublished (scripts/ is excluded in _config.yml).

Everything is lesson 2-1, Cryptographic Technologies and Authentication: the
English textbook pp. 33-40, the Arabic textbook pp. 31-37 where it goes
further (session keys, the certificate checks, 2FA against MFA), and the
ministry's assessment book for the lesson. Every exercise names its source.

Every printed document is one section.sheet per A4 page, as everywhere else
in this repo. When an exercise is added, add it to a page in the lists below
and re-render each sheet to check it is still one page.

The diagrams are read out of build_lecture5_slides.py rather than copied,
so the booklet shows exactly the picture the deck was taught with.
"""
import io, json, re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "lecture5" / "_teacher"
DATA = json.loads((T / "exercises.json").read_text(encoding="utf-8"))
EX = {x["n"]: x for x in DATA["SHEET"]["parts"][0]["exercises"]}

TITLE = "Is this connection safe?"
ACCENT = "#2D7A4B"

# Class work: the book's Worked Example and Try, all quick to mark together.
IN_CLASS = [1, 2, 3, 4]

HW_SECTIONS = [
    ("Part 1 &middot; Encryption, HTTPS and certificates",
     "الجزء الأول — التشفير وHTTPS والشهادات",
     # the first sheet also carries the masthead and the intro box
     [[5], [6, 12], [13, 11]]),
    ("Part 2 &middot; Authentication",
     "الجزء التاني — المصادقة",
     [[9, 10], [8, 14]]),
    ("Part 3 &middot; Combining technologies, and apply it",
     "الجزء التالت — الجمع بين التقنيات، وطبّق",
     [[7, 15], [16, 17], [18]]),
    ("Challenge &middot; optional",
     "تحدي — اختياري",
     [[19, 20]]),
]
HOMEWORK = [n for _, _, pages in HW_SECTIONS for g in pages for n in g]

EXTRA_CSS = '''
.namebox{display:flex;gap:5mm;margin:0 0 6mm}.namebox>div{flex:1;display:flex;align-items:flex-end;gap:2mm}.namebox span{font-size:9pt;color:var(--soft);font-weight:600}.namebox i{flex:1;border-bottom:1px solid var(--rule);height:6mm}.ex{margin:0 0 5mm;break-inside:avoid}.exhead{display:flex;gap:3mm;align-items:baseline;margin-bottom:1.5mm}.exn{flex:0 0 auto;width:6.5mm;height:6.5mm;border-radius:50%;background:var(--teal);color:#fff;font-size:9pt;font-weight:600;display:flex;align-items:center;justify-content:center}.exq{font-size:10.5pt;font-weight:600}.src{font-size:8pt;color:var(--soft);font-style:italic;margin:0 0 1.5mm 9.5mm}.passage{font-size:10pt;line-height:1.8;background:#FCFCFA;border:1px solid var(--line);padding:3mm}.marks{font-size:9pt;font-weight:600;color:var(--gold);margin:2mm 0}.key{margin-left:9.5mm;font-size:10pt}.teacherwarn{background:#FBF0EE;border-left:3px solid #9C3B2E;padding:3mm}.summary.hw{background:var(--teal-pale)}.keygroup{font-size:9.5pt;color:var(--soft);font-weight:600;text-transform:uppercase;letter-spacing:.04em;margin:5mm 0 2mm}.key ul{margin-left:4mm}.key li{margin-bottom:1mm}.key .note{font-size:9.5pt;color:var(--soft);font-style:italic;margin-top:1.5mm}ol.blanks{list-style:none;margin:3mm 0 0}ol.blanks li{display:flex;align-items:flex-end;gap:3mm;margin-bottom:4.5mm}ol.blanks li b{flex:0 0 auto;font-size:10.5pt}ol.blanks .rule{flex:1;height:6mm;border-bottom:1px solid var(--rule)}.opt{display:block;margin:1.2mm 0 0 4mm}.srcinline{font-size:8pt;color:var(--soft);font-style:italic;margin-left:2mm}ol.qs li{margin-bottom:3mm}.optlead{font-size:10pt;font-weight:600;margin:2.5mm 0 1.5mm}.fields{display:flex;flex-wrap:wrap;gap:2.5mm;margin:0 0 2mm}.chip{border:1px solid var(--line);border-radius:20mm;padding:1.5mm 4mm;font-size:10pt;background:#FCFCFA}
.dg{margin:3mm 0 4mm}.dg svg{display:block;width:100%;height:auto}
.principles{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin:3mm 0}
.principles .pr{border:1px solid var(--line);border-left:3px solid var(--teal);border-radius:1.5mm;padding:2.5mm 3.5mm;background:#FCFCFA}
.principles .pr h4{font-size:10.5pt;margin-bottom:1mm}.principles .pr p{font-size:9.5pt;margin:0}
'''


def slide_svg(name):
    """Read a diagram out of the deck's builder, so the booklet cannot drift
    from the picture the lesson was taught with."""
    src = (ROOT / "scripts" / "build_lecture5_slides.py").read_text(encoding="utf-8")
    m = re.search(r"^%s = '''(.*?)'''" % name, src, re.DOTALL | re.MULTILINE)
    assert m, "diagram %s not found in the slide builder" % name
    return m.group(1).strip()


def shell():
    t = (ROOT / "templates/handout-template.html").read_text(encoding="utf-8")
    t = t.replace("</style>", EXTRA_CSS + "</style>", 1)
    t = (t.replace("__LECTURE_NUM__", "5").replace("__TITLE_HTML__", esc(TITLE))
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
            ' &middot; Lecture 5</div><div class="namebox"><div><span>Name</span><i></i></div>'
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
                '<p>Learn first which key does what in the three stages of HTTPS, and why: public-key to '
                'share the key safely, common-key to move the data quickly. Then the four technologies and '
                'the threat each stops, and the three factors with an example of each &mdash; and why two '
                'passwords are not multi-factor.</p>'
                '<p class="ar">احفظ الأول مراحل HTTPS التلاتة وكل مرحلة بأنهي مفتاح وليه، وبعدين التقنيات '
                'الأربعة وكل واحدة بتوقف أنهي تهديد، والعوامل التلاتة بمثال لكل واحد — وليه كلمتين مرور مش مصادقة ثنائية.</p></div>')
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
    KEYS, HANDSHAKE, FACTORS, SHOP = (slide_svg("KEYS"), slide_svg("HANDSHAKE"),
                                      slide_svg("FACTORS"), slide_svg("SHOP"))
    p = []
    # slides 2-5: unit 2, the hook, the guiding question, the map
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Unit 2 &middot; Cybersecurity</h2>'
        '<table><tr><th style="width:14%">Lesson</th><th>Topic</th></tr>'
        '<tr><td class="k">2-1 &middot; today</td><td>Cryptographic technologies and authentication</td></tr>'
        '<tr><td class="k">2-2</td><td>Network security design</td></tr>'
        '<tr><td class="k">2-3</td><td>Incident response and risk management</td></tr></table>'
        '<h2>Every login hides three jobs</h2>'
        '<p>Every time you log in to a bank app, buy something online, or open a website with a padlock in '
        'the address bar, hidden technologies keep your information safe: messages are <b>scrambled</b> so '
        'no one else can read them, the website <b>proves that it is genuine</b>, and your <b>identity is '
        'checked</b> before you are let in. Without them, passwords could be stolen and private data read.</p>'
        '<p class="ar">فيه كذا تقنية بتحمي الاتصال: TLS بيشفّر البيانات، والمتصفح بيتأكد من شهادة الموقع، والخدمة بتتأكد من هويتك — بس ده مش معناه إن محتوى الموقع موثوق أو إن الحماية مطلقة.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> How do cryptographic technologies and '
        'authentication work together to keep online communication and services secure?</p>'
        '<p class="ar">السؤال الرئيسي: إزاي تقنيات التشفير والمصادقة بتشتغل مع بعض عشان تحافظ على أمان الاتصال والخدمات عبر الإنترنت؟</p></div>'
        '<table><tr><th>Technology</th><th>Threat it answers</th></tr>'
        '<tr><td class="k">Encryption</td><td>Eavesdropping &mdash; content read by a third party</td></tr>'
        '<tr><td class="k">Digital certificate</td><td>Impersonation &mdash; a fake site</td></tr>'
        '<tr><td class="k">Digital signature</td><td>Tampering &mdash; data altered on the way</td></tr>'
        '<tr><td class="k">Multi-factor authentication</td><td>Unauthorized login</td></tr></table>'))
    # slides 6-9: explore, part 1, the two kinds of encryption, which key does what
    p.append(page(
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> You send your password to your bank. '
        'Predict what three things must be true so that no one can read it, change it, or receive it by '
        'pretending to be your bank.</p>'
        '<p class="ar">توقّعوا: إيه التلات حاجات اللي لازم يتحققوا عشان محدش يقرا الباسورد، ولا يغيّره، ولا ياخده وهو بيضحك عليك إنه البنك؟</p></div>'
        +         '<h2>Part 1 &middot; Encryption</h2>'
        + term('Encryption', 'Scrambles a message so that only someone with the right key can read it &mdash; it keeps content private.',
               'التشفير بيحافظ على خصوصية المحتوى: محدش يقدر يقرا الرسالة غير اللي معاه المفتاح الصح.')
        + '<h2>One key, or a pair of keys</h2>'
        + dg(KEYS)
        + '<p><b>Common-key (symmetric-key) cryptography</b> exchanges data quickly; <b>public-key cryptography</b> '
        'shares a key safely.</p>'
        '<p class="ar">التشفير المتماثل بيبادل البيانات بسرعة، والتشفير بالمفتاح العام بيشارك المفتاح بأمان.</p>'
        + '<h2>Which key does what</h2>'
        '<table><tr><th></th><th>Locks / signs with</th><th>Unlocks / verifies with</th></tr>'
        '<tr><td class="k">Encryption (public-key)</td><td>the receiver&#8217;s public key</td><td>the receiver&#8217;s private key</td></tr>'
        '<tr><td class="k">Digital signature</td><td>the sender&#8217;s private key</td><td>the sender&#8217;s public key</td></tr></table>'
        '<p class="ar">في التوقيع الرقمي الاتجاه بيتعكس: المفتاح الخاص بيوقّع والعام بيتحقق.</p>'))
    # slides 10-12: part 2, HTTPS, the three stages, (video)
    p.append(page(
        '<h2>Part 2 &middot; HTTPS and the TLS handshake</h2>'
        + term('HTTPS (HTTP Secure)', 'A communication protocol that adds TLS encryption to HTTP. It provides encryption, '
               'detection of tampering and verification of the communication partner, protecting users from eavesdropping, '
               'tampering and impersonation. Setting up the secure connection is the <b>TLS handshake</b>.',
               'HTTPS: بروتوكول HTTP منقول عبر اتصال TLS مؤمَّن. وخطوات إنشاء الاتصال الآمن اسمها مصافحة TLS.')
        + '<h2>Three stages, two kinds of key</h2>'
        + dg(HANDSHAKE)
        + '<table><tr><th style="width:20%">Stage</th><th>What happens</th><th style="width:20%">Method</th></tr>'
        '<tr><td class="k">1 Connection</td><td>The server sends a digital certificate and a public key; the browser verifies the server through a certificate authority (CA).</td><td>Public-key</td></tr>'
        '<tr><td class="k">2 Key exchange</td><td>The browser creates a common key, encrypts it with the server&#8217;s public key and sends it; the server decrypts it with its private key.</td><td>Public-key</td></tr>'
        '<tr><td class="k">3 Data</td><td>Data is encrypted and exchanged using the shared common key.</td><td>Common-key</td></tr></table>'))
    # slides 13-16: why not public-key, certificates, signatures, true or false
    p.append(page(
        '<div class="summary"><p><b>Why not public-key for everything?</b> Public-key cryptography shares keys safely '
        'but is slow; common-key cryptography exchanges large amounts of data quickly. This division of roles gives both '
        '<b>security</b> and <b>speed</b>. The common key for one connection is a <b>session key</b>; current versions of '
        'TLS agree on it by Diffie-Hellman key agreement.</p>'
        '<p class="ar">آليات المفتاح العام للمصادقة والاتفاق الآمن على مفاتيح الجلسة، والتشفير المتماثل لحماية بيانات الجلسة بسرعة.</p></div>'
        +         '<h2>Who vouches for the website?</h2>'
        + term('Digital certificate', 'Verifies that the communication partner is authentic. A certificate authority (CA) vouches that a site is genuine.',
               'الشهادة الرقمية بتساعد المتصفح يتأكد من هوية الخادم وارتباط الشهادة باسم النطاق اللي بيتصل بيه.')
        + '<p>During the handshake the browser checks that the certificate is <b>valid</b>, that it leads back to an '
        'authority it trusts (the <b>chain of trust</b>), and that it <b>matches the name</b> of the site.</p>'
        '<p class="ar">المتصفح بيتأكد من صلاحيتها وسلسلة الثقة وملاءمتها لاسم الموقع.</p>'
        '<h2>Proving who sent it, and that it was not changed</h2>'
        + term('Digital signature', 'Detects data tampering or impersonation of the sender, and makes it impossible for the '
               'sender to deny having sent the data afterward: <b>non-repudiation</b>.',
               'التوقيع الرقمي بيكشف التلاعب وانتحال الشخصية، وبيوفّر دليل بيدعم عدم التنصل.')
        + '<table><tr><th>Digital certificate</th><th>Digital signature</th></tr>'
        '<tr><td>Is the other side genuine?</td><td>Was this data altered, and who sent it?</td></tr>'
        '<tr><td>Stops a fake website</td><td>Detects tampering; gives non-repudiation</td></tr></table>'
        '<div class="summary"><p><b>The padlock.</b> It shows the connection is encrypted and the site matches its '
        'certificate. It does <b>not</b> mean the content can be trusted completely, or that protection is absolute.</p>'
        '<p class="ar">القفل مش معناه إن محتوى الموقع موثوق أو إن الحماية مطلقة.</p></div>'))
    # slides 17-21: part 3, factors, MFA, 2FA and MFA, services, two passwords
    p.append(page(
        '<h2>Part 3 &middot; Authentication</h2>'
        + dg(FACTORS)
        + '<p class="ar">المعرفة (كلمة مرور، سؤال سري) &middot; الحيازة (كلمة مرور لمرة واحدة، SMS، بطاقة ذكية) &middot; السمات الحيوية (بصمة، وجه).</p>'
        + term('Multi-factor authentication (MFA)', 'Combining two or more of the three factors: knowledge, possession, biometric. '
               'With one factor, breaking it lets an attacker in; with several, even if one is broken, another can still prevent access.',
               'لو عامل واحد واتكسر، اللي هاجم يدخل. لكن عامل تاني مستقل بيقلل احتمال الدخول غير المصرح به.')
        + '<table><tr><th>Two-factor authentication (2FA)</th><th>Multi-factor authentication (MFA)</th></tr>'
        '<tr><td>Exactly two independent factors, from two different categories</td><td>Two or more independent factors, from different categories</td></tr></table>'
        '<table><tr><th>Service</th><th>Authentication used</th><th style="width:28%">Factors</th></tr>'
        '<tr><td class="k">Online banking</td><td>Password + one-time password</td><td>knowledge + possession</td></tr>'
        '<tr><td class="k">SNS login</td><td>Password + SMS authentication</td><td>knowledge + possession</td></tr>'
        '<tr><td class="k">Online shopping</td><td>Password + one-time code from 3-D Secure</td><td>knowledge + possession</td></tr>'
        '<tr><td class="k">Company laptop login</td><td>Smart card + fingerprint authentication</td><td>possession + biometric</td></tr></table>'
        '<div class="summary"><p><b>Exam warning.</b> Two passwords, or a password and a secret question, are '
        '<b>not</b> multi-factor: both are knowledge, the same factor twice (two-step authentication).</p>'
        '<p class="ar">كلمتين مرور مش مصادقة ثنائية — الاتنين من عامل المعرفة.</p></div>'))
    # slides 22-26: pause & think, part 4, one purchase, which technology, true or false
    p.append(page(
        '<div class="summary hw"><p><b>Pause and think.</b> If a password is leaked, why can a second factor '
        'sent to a phone still keep the account safe?</p>'
        '<p class="ar">لو كلمة المرور اتسربت، ليه عامل تاني بيتبعت على الموبايل لسه ممكن يحمي الحساب؟</p></div>'
        '<h2>Part 4 &middot; Layers, not one lock</h2>'
        '<table><tr><th>Technology</th><th>Effect</th></tr>'
        '<tr><td class="k">Encryption (common-key, public-key)</td><td>Prevents communication content from being read by third parties</td></tr>'
        '<tr><td class="k">Digital signature</td><td>Detects data tampering or impersonation of the sender; non-repudiation</td></tr>'
        '<tr><td class="k">Digital certificate</td><td>Verifies that the communication partner is authentic</td></tr>'
        '<tr><td class="k">Multi-factor authentication</td><td>Prevents unauthorized logins</td></tr></table>'
        '<h2>One online purchase</h2>'
        + dg(SHOP)
        + '<p class="ar">الجمع ده بيقلل مخاطر التنصت والتلاعب وانتحال الهوية والدخول غير المصرح به في نفس الوقت، من غير ما نفترض إن أي تقنية بتمنع الخطر منع مطلق.</p>'
        '<table><tr><th>Looks right, but is false</th><th>Why</th></tr>'
        '<tr><td>Digital signatures improve communication speed.</td><td>They detect tampering and impersonation.</td></tr>'
        '<tr><td>One strong technology is enough.</td><td>Security comes from combining several.</td></tr></table>'))
    # slides 27-29: think as an engineer, new context, key takeaway
    p.append(page(
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A school portal lets students check grades and pay fees. Password only, or a '
        'password plus a one-time password sent to the phone? <b>Collect data</b> from ten classmates. '
        '<b>Analyze the stakeholders</b> &mdash; a student, the school, a student with no smartphone. '
        '<b>Decide</b>, with two reasons.</p>'
        '<p class="ar">اجمع بيانات، وحلّل أصحاب المصلحة، وبعدين قرّر واذكر سببين.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A small online shop wants to secure both customer login and payment. Name two '
        'security technologies it should use and say where each one helps, then identify one threat that could still remain.</p>'
        '<p class="ar">سمّي تقنيتين أمان وبيّن كل واحدة بتساعد فين، وحدد تهديد واحد ممكن يفضل موجود.</p></div>'
        '<h2>Key takeaway &middot; share the key safely, move the data quickly</h2><div class="summary">'
        '<p>HTTPS uses public-key cryptography to share a key safely and common-key cryptography to move data quickly. '
        'Services stay safe by layering encryption, certificates, signatures and multi-factor authentication.</p>'
        '<p class="ar">افتكر: آليات المفتاح العام للمصادقة ومفاتيح الجلسة، والتشفير المتماثل لبيانات الجلسة. والخدمات بتفضل آمنة بتكديس التشفير والشهادات والتوقيعات والمصادقة الثنائية.</p></div>'
        '<h2>Lesson question &mdash; answered</h2>'
        '<p>HTTPS combines public-key cryptography, to share a key safely, with common-key cryptography, to exchange '
        'data quickly, so communication is both secure and fast. Services stay safe by combining encryption (hides '
        'content), digital certificates (prove a site is genuine), digital signatures (detect tampering) and '
        'multi-factor authentication (blocks unauthorized logins), so many threats are addressed at the same time.</p>'))
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
    ('hw', [5, 6, 12]), ('hw', [13, 11, 9]), ('hw', [10, 8, 14]),
    ('hw', [7, 15, 16]), ('hw', [17, 18]), ('hw', [19, 20]),
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
    L5 = "Lecture 5 %s — " + TITLE
    outs = [
        (ROOT / 'lecture5/handout/index.html', booklet(head, tail), L5 % "Booklet"),
        (ROOT / 'lecture5/homework/index.html', homework(head, tail), L5 % "Homework"),
        (ROOT / 'lecture5/_teacher/answer-key.html', key(head, tail), L5 % "Answer Key"),
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
