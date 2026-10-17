# -*- coding: utf-8 -*-
"""Build Lecture 7's deck.

    python scripts/build_lecture7_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/lecture7_slides_base.html and writes lecture7/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the side drawings
added. Always starts from the base, never from the published deck.

Content is Lesson 2-3, Incident Response and Risk Management, the English
textbook pp. 48-54, and nothing outside the curriculum. Where the Arabic
textbook (pp. 44-49) and the ministry's assessment book go further, the deck
follows them: the incident defined by confidentiality, integrity and
availability; stage 6's second name, "lessons learned and improvement";
stages that overlap or repeat in practice; and high impact with low
likelihood counted as medium. This lesson closes Unit 2, so the deck ends
with the unit's three lessons.

Everything but the content is lecture 5's builder, unchanged -- this file was
derived from it. The Arabic follows the Arabic textbook's lesson 2-3 point by
point, said in Egyptian Arabic, with the book's own terms kept as they are.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "lecture7/slides/index.html"


# --------------------------------------------------------------------------
# diagrams -- inline SVG, coloured from the page's CSS variables so they follow
# LECTURE_ACCENT. Labels only, never the sentence that explains them; no label
# under 14 units. Fills are #fff, never var(--white): the booklet template
# does not define --white. The booklet reads these out of this file.
# --------------------------------------------------------------------------

STAGES = '''
<svg viewBox="0 0 900 230" role="img" aria-label="The six stages of incident response in order: preparation, detection, containment, eradication, recovery, prevention of recurrence">
  <g font-size="15" text-anchor="middle">
    <line x1="80" y1="70" x2="820" y2="70" stroke="var(--line)" stroke-width="4"/>
    <polygon points="832,70 818,62 818,78" fill="var(--line)"/>
    <circle cx="80" cy="70" r="30" fill="var(--teal)"/><text x="80" y="77" font-size="20" font-weight="700" fill="#fff">1</text>
    <circle cx="228" cy="70" r="30" fill="var(--teal)"/><text x="228" y="77" font-size="20" font-weight="700" fill="#fff">2</text>
    <circle cx="376" cy="70" r="30" fill="var(--gold)"/><text x="376" y="77" font-size="20" font-weight="700" fill="#fff">3</text>
    <circle cx="524" cy="70" r="30" fill="var(--gold)"/><text x="524" y="77" font-size="20" font-weight="700" fill="#fff">4</text>
    <circle cx="672" cy="70" r="30" fill="var(--teal)"/><text x="672" y="77" font-size="20" font-weight="700" fill="#fff">5</text>
    <circle cx="820" cy="70" r="30" fill="var(--teal)"/><text x="820" y="77" font-size="20" font-weight="700" fill="#fff">6</text>
    <text x="80" y="128" font-weight="700" fill="var(--ink)">Preparation</text>
    <text x="80" y="150" fill="var(--soft)">plan in advance</text>
    <text x="228" y="128" font-weight="700" fill="var(--ink)">Detection</text>
    <text x="228" y="150" fill="var(--soft)">find and confirm</text>
    <text x="376" y="128" font-weight="700" fill="var(--ink)">Containment</text>
    <text x="376" y="150" fill="var(--soft)">stop it spreading</text>
    <text x="524" y="128" font-weight="700" fill="var(--ink)">Eradication</text>
    <text x="524" y="150" fill="var(--soft)">remove the cause</text>
    <text x="672" y="128" font-weight="700" fill="var(--ink)">Recovery</text>
    <text x="672" y="150" fill="var(--soft)">back to normal</text>
    <text x="820" y="128" font-weight="700" fill="var(--ink)">Prevention of</text>
    <text x="820" y="148" font-weight="700" fill="var(--ink)">recurrence</text>
    <text x="820" y="170" fill="var(--soft)">so it never returns</text>
    <rect x="320" y="190" width="260" height="30" rx="8" fill="var(--gold)" opacity=".2"/>
    <text x="450" y="211" font-weight="600" fill="var(--ink)">contain first, then eradicate</text>
  </g>
</svg>'''

MATRIX = '''
<svg viewBox="0 0 900 330" role="img" aria-label="Risk evaluation matrix: impact across, likelihood up; the score is impact times likelihood, and the high-high corner is addressed first">
  <g font-size="15" text-anchor="middle">
    <text x="60" y="170" transform="rotate(-90 60 170)" font-weight="700" fill="var(--ink)">Likelihood</text>
    <text x="96" y="78" fill="var(--soft)">high 3</text>
    <text x="96" y="168" fill="var(--soft)">medium 2</text>
    <text x="96" y="258" fill="var(--soft)">low 1</text>
    <rect x="140" y="40" width="160" height="80" rx="8" fill="var(--gold)" opacity=".35"/><text x="220" y="88" font-size="20" font-weight="700" fill="var(--ink)">3</text>
    <rect x="310" y="40" width="160" height="80" rx="8" fill="#9C3B2E" opacity=".35"/><text x="390" y="88" font-size="20" font-weight="700" fill="var(--ink)">6</text>
    <rect x="480" y="40" width="160" height="80" rx="8" fill="#9C3B2E" opacity=".75"/><text x="560" y="88" font-size="20" font-weight="700" fill="#fff">9</text>
    <rect x="140" y="130" width="160" height="80" rx="8" fill="var(--teal)" opacity=".18"/><text x="220" y="178" font-size="20" font-weight="700" fill="var(--ink)">2</text>
    <rect x="310" y="130" width="160" height="80" rx="8" fill="var(--gold)" opacity=".35"/><text x="390" y="178" font-size="20" font-weight="700" fill="var(--ink)">4</text>
    <rect x="480" y="130" width="160" height="80" rx="8" fill="#9C3B2E" opacity=".35"/><text x="560" y="178" font-size="20" font-weight="700" fill="var(--ink)">6</text>
    <rect x="140" y="220" width="160" height="80" rx="8" fill="var(--teal)" opacity=".18"/><text x="220" y="268" font-size="20" font-weight="700" fill="var(--ink)">1</text>
    <rect x="310" y="220" width="160" height="80" rx="8" fill="var(--teal)" opacity=".18"/><text x="390" y="268" font-size="20" font-weight="700" fill="var(--ink)">2</text>
    <rect x="480" y="220" width="160" height="80" rx="8" fill="var(--gold)" opacity=".35"/><text x="560" y="268" font-size="20" font-weight="700" fill="var(--ink)">3</text>
    <text x="220" y="322" fill="var(--soft)">small 1</text>
    <text x="390" y="322" fill="var(--soft)">medium 2</text>
    <text x="560" y="322" fill="var(--soft)">large 3</text>
    <text x="780" y="322" font-weight="700" fill="var(--ink)">Impact &#8594;</text>
    <text x="770" y="70" font-weight="700" fill="#9C3B2E">address first</text>
    <line x1="700" y1="76" x2="648" y2="80" stroke="#9C3B2E" stroke-width="2.5"/>
    <text x="770" y="150" font-weight="700" fill="var(--ink)">risk size =</text>
    <text x="770" y="174" font-weight="700" fill="var(--ink)">impact &#215; likelihood</text>
  </g>
</svg>'''


# ---------------- side visuals ----------------
# A slide whose content fills only the left half of a wide screen gets an
# animated explainer on the right. Each drawing plays once when the slide
# opens and again when tapped. Under 1000px wide the drawing is hidden. The
# final frame of every animation is the element's own style, so with reduced
# motion and in print the drawing shows complete.

def vcap(en, arabic):
    return '<p class="vcap"><b>%s</b><span dir="rtl">%s</span></p>' % (en, arabic)


def v_timer():
    return ('<aside class="rise viz timer">'
            '<svg viewBox="0 0 200 200" role="img" aria-label="One minute to think">'
            '<circle cx="100" cy="100" r="80" class="track"/>'
            '<circle cx="100" cy="100" r="80" class="ring"/>'
            '<text x="100" y="98" class="big">1</text><text x="100" y="126" class="small">minute</text>'
            '</svg>'
            '<div class="tps"><span style="animation-delay:.3s">Think</span><span style="animation-delay:.6s">Pair</span><span style="animation-delay:.9s">Share</span></div>'
            + vcap("Think alone first, then tell your partner.",
                   "فكّر لوحدك الأول، وبعدين قول لزميلك.")
            + '</aside>')


def v_alarm():
    return ('<aside class="rise viz"><div class="alarm">'
            '<div class="al1">&#128737; Protected system</div>'
            '<div class="al2">&#9888; Incident detected</div>'
            '<div class="al3"><span>1 Contain</span><span>2 Remove</span><span>3 Recover</span><span>4 Learn</span></div>'
            '</div>'
            + vcap("Not if it happens — what you do next.",
                   "مش بس إزاي نمنعها — لكن نعمل إيه لما تحصل.")
            + '</aside>')


def v_incidents():
    rows = [("&#128228;", "Information leak", "personal or confidential data goes outside"),
            ("&#9998;", "Data tampering", "data is altered without authorization"),
            ("&#128683;", "Service outage", "the service becomes unavailable")]
    out = "".join('<div class="drow" style="animation-delay:%.2fs"><span class="dico">%s</span>'
                  '<span class="dt"><b>%s</b><br><small>%s</small></span></div>' % (.4 + .5 * k, ico, t, why)
                  for k, (ico, t, why) in enumerate(rows))
    return ('<aside class="rise viz">' + out
            + vcap("Three typical incidents.",
                   "تلات أمثلة نموذجية للحوادث الأمنية.")
            + '</aside>')


def v_spread():
    return ('<aside class="rise viz">'
            '<svg viewBox="0 0 400 230" role="img" aria-label="An infected computer is cut off from the network before the malware spreads to the others">'
            '<line x1="200" y1="115" x2="70" y2="45" class="lnk l1"/><line x1="200" y1="115" x2="330" y2="45" class="lnk l2"/>'
            '<line x1="200" y1="115" x2="70" y2="185" class="lnk l3"/><line x1="200" y1="115" x2="330" y2="185" class="lnk cut"/>'
            '<rect x="170" y="92" width="60" height="46" rx="8" class="hub"/><text x="200" y="121" class="ntext">network</text>'
            '<rect x="40" y="22" width="60" height="46" rx="8" class="pc"/><rect x="300" y="22" width="60" height="46" rx="8" class="pc"/>'
            '<rect x="40" y="162" width="60" height="46" rx="8" class="pc"/>'
            '<rect x="300" y="162" width="60" height="46" rx="8" class="pc bad"/><text x="330" y="191" class="ntext wh">&#9763;</text>'
            '<text x="330" y="226" class="lbl mid redl">infected &#8212; cut off</text>'
            '</svg>'
            + vcap("Contain first: isolate the infected machine.",
                   "احتوِ الأول: اعزل الجهاز المصاب.")
            + '</aside>')


def v_multiply():
    """A worked example on a risk that is not in the table, so the drawing
    does not give away the answers the slide asks the class to reveal."""
    return ('<aside class="rise viz"><div class="mult">'
            '<div class="mrow"><span class="mi">Impact<b>medium (2)</b></span><span class="mop">&#215;</span>'
            '<span class="mi">Likelihood<b>medium (2)</b></span><span class="mop">=</span><span class="mres">4</span></div>'
            '<p class="mnote">Do the same for a, b, c and d &#8212; then rank the sizes, biggest first.</p>'
            '</div>'
            + vcap("Multiply, then rank.",
                   "اضرب، وبعدين رتّب.")
            + '</aside>')


def v_keep():
    items = [("1", "Preparation"), ("2", "Detection"), ("3", "Containment"),
             ("4", "Eradication"), ("5", "Recovery"), ("6", "Prevention of recurrence")]
    out = "".join('<div class="pchip" style="animation-delay:%.2fs"><span>%s</span><div>%s</div></div>'
                  % (.4 + .3 * k, n, t) for k, (n, t) in enumerate(items))
    return ('<aside class="rise viz">' + out
            + vcap("In order — and the worst risks first.",
                   "بالترتيب — والمخاطر الأخطر الأول.")
            + '</aside>')


def v_shopleak():
    return ('<aside class="rise viz"><div class="shopv">'
            '<div class="sv sv1"><span>&#9888;</span><b>Leak detected</b><i>stage 2 is done</i></div>'
            '<div class="sv sv2"><span>&#10067;</span><b>The next two stages</b><i>and why that order</i></div>'
            '<div class="sv sv3"><span>&#128202;</span><b>One risk to prioritize</b><i>impact &#215; likelihood</i></div>'
            '</div>'
            + vcap("Respond in order, then fix the biggest risk.",
                   "استجب بالترتيب، وبعدين عالج أكبر خطر.")
            + '</aside>')


# heading text (unique to one slide) -> its drawing
VIZ = {
    "When something goes wrong": v_alarm,
    "Before you read on": v_timer,
    "What is a security incident?": v_incidents,
    "Why must containment come before eradication": v_timer,
    "Contain first, then remove the cause": v_spread,
    "Put the risks in order": v_multiply,
    "An online shop finds its customer data leaked": v_shopleak,
    "Respond in order; fix the worst first": v_keep,
}
VIZ_USED = []


PHOTO_CSS = """
/* ---------- photo slides ---------- */
.shots{display:grid; gap:.85rem; margin:1rem 0 .35rem}
.shots.two{grid-template-columns:repeat(2,1fr)}
.shots.three{grid-template-columns:repeat(3,1fr)}
.shots.four{grid-template-columns:repeat(4,1fr)}
@media (max-width:900px){.shots.three,.shots.four{grid-template-columns:repeat(2,1fr)}}
.shot{background:var(--white); border:1px solid var(--line); border-radius:10px;
      overflow:hidden; display:flex; flex-direction:column}
.shot img{width:100%; height:21vh; object-fit:contain; background:#F1F0EB;
          display:block; padding:6px; font-size:11px; color:var(--soft)}
.shot .cap{padding:.5rem .6rem .65rem; font-size:clamp(10.5px,1vw,13.5px);
           line-height:1.4; color:var(--ink-2)}
.shot .cap b{display:block; color:var(--ink); font-size:clamp(11.5px,1.12vw,15px);
             margin-bottom:.18rem}
.shot .cap .ar{display:block; color:var(--soft); margin-top:.28rem; font-size:.94em}
.credit{font-size:clamp(9px,.82vw,11.5px); color:var(--soft); margin-top:.15rem}
"""


def shot(src, title, body, arabic):
    return ('<figure class="shot"><img src="media/%s" alt="%s" loading="lazy" '
            'referrerpolicy="no-referrer">'
            '<figcaption class="cap"><b>%s</b>%s<span class="ar">%s</span></figcaption>'
            '</figure>' % (src, title, title, body, arabic))


CREDIT = ('<p class="rise credit">Photos: Wikimedia Commons &#183; public domain or '
          'Creative Commons. Used for teaching.</p>')



def with_viz(parts):
    """Put a slide's content beside its drawing; the Arabic line stays below
    both, full width, where it is on every other slide."""
    heads = [p for p in parts if p.startswith(("<h1", "<h2"))]
    hit = [k for k in VIZ if any(k in h for h in heads)]
    if not hit:
        return parts
    assert len(hit) == 1, hit
    VIZ_USED.append(hit[0])
    main = [p for p in parts if "arline" not in p]
    rest = [p for p in parts if "arline" in p]
    return ['<div class="split"><div class="main">\n      ' + "\n      ".join(main)
            + '\n    </div>\n    ' + VIZ[hit[0]]() + '</div>'] + rest


def s(cls, *parts):
    parts = with_viz(list(parts))
    return '  <section class="slide%s">\n%s\n  </section>' % (
        (" " + cls) if cls else "", "\n".join("    " + p for p in parts))


def ar(t):
    return '<p class="rise arline ar">%s</p>' % t


def eyebrow(t):
    return '<div class="rise eyebrow">%s</div>' % t


def h2(t, style=""):
    return '<h2 class="rise"%s>%s</h2>' % ((' style="%s"' % style) if style else "", t)


def sub(t, style=""):
    return '<p class="rise sub"%s>%s</p>' % ((' style="%s"' % style) if style else "", t)


def fig(svg):
    return '<div class="rise" style="margin:1.1rem 0 .4rem">%s</div>' % svg.strip()




def video(ytid, title, source, eyebrow_t, heading, watch_for, arline):
    """A video that loads only when clicked -- a poster, then the player.
    Leaving the slide stops it (see VIDEO_JS). The link underneath is the
    fallback for a classroom where the embed is blocked."""
    return s("",
        eyebrow(eyebrow_t),
        h2(heading, "max-width:26ch"),
        '<div class="rise vid" data-yt="%s" role="button" tabindex="0" aria-label="Play video: %s">'
        '<img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">'
        '<span class="play">&#9654;</span>'
        '<span class="vcap"><b>%s</b> &#183; %s</span></div>' % (ytid, title, ytid, title, source),
        sub("<b>While you watch:</b> " + watch_for, "max-width:62ch;margin-top:.5rem"),
        '<p class="rise credit">Video: %s, on YouTube &#183; '
        '<a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">open it on YouTube</a> '
        'if it will not play here. Not from the textbook.</p>' % (source, ytid),
        ar(arline))

SLIDES = []
A = SLIDES.append

# 1 title
A(s("dark",
    '<div class="rise eyebrow" id="lectureBadge">Programming &amp; Artificial Intelligence</div>',
    h2("When something goes wrong", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("Even a well-protected system can be attacked. Today: how to respond, in the right order &#8212; and how to decide which risks to fix first.",
        "max-width:56ch;margin-top:1rem"),
    ar("حتى النظام المحمي كويس ممكن يتهاجم. النهارده: إزاي نستجيب بالترتيب الصح — وإزاي نقرر نعالج أنهي خطر الأول.")))

# 2 recap -- lesson 2-2, and the Arabic book's bridge into this lesson
A(s("",
    eyebrow("Before we start &#183; Lesson 2-2"),
    h2("Last time: layers, and verify every access"),
    '<table class="rise">'
    '<tr><th>Layer</th><th>Measure</th></tr>'
    '<tr><td>1 &#183; Network entry</td><td>Firewall</td></tr>'
    '<tr><td>2 &#183; Communication path</td><td>VPN</td></tr>'
    '<tr><td>3 &#183; Server placement</td><td>DMZ</td></tr>'
    '<tr><td>4 &#183; Endpoints</td><td>Antivirus, an updated OS</td></tr>'
    '</table>',
    sub("Defense in depth makes a breach less likely &#8212; not impossible. Today moves from <b>prevention</b> to <b>response</b>.",
        "max-width:60ch;margin-top:.9rem"),
    ar("حتى مع تقنيات الحماية والدفاع في العمق، ممكن يحصل حادث أمني؛ عشان كده الدرس ده بينقلنا من الوقاية للاستجابة وإدارة المخاطر.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("This is already happening"),
    h2("A rushed reaction makes it worse", "max-width:22ch"),
    '<div class="rise fields">'
    '<span class="chip">data leaked</span>'
    '<span class="chip">files tampered with</span>'
    '<span class="chip">a service knocked offline</span>'
    '</div>',
    sub("Organizations follow a clear, ordered response, so that damage is contained, the cause is removed, and the same problem does not return. And they decide in advance which risks to guard against first &#8212; no team can fix everything at once.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> ransomware has locked the school&#8217;s files. Would you restore from the backup straight away? Remember your answer.</p></div>',
    ar("حتى النظام المحمي كويس ممكن يتعرض لحادث أمني، زي تسرب بيانات، أو التلاعب بالملفات، أو تعطل خدمة. عشان كده المؤسسات بتستخدم خطة منظمة: توقف انتشار المشكلة، وتشيل التهديد، وترجّع الخدمة، وبعدين تتعلم من الحادث. وبتقيّم المخاطر عشان تحدد الأولويات، لأن الفريق مش هيقدر يعالج كل حاجة في نفس الوقت.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("When a security incident happens, how should an organization respond in order &#8212; and how does it decide which risks to address first?",
       "max-width:28ch"),
    ar("السؤال الرئيسي: لما يحصل حادث أمني، المؤسسة المفروض تنظّم استجابتها إزاي بالترتيب — وإزاي تقرر أنهي مخاطر تعالجها الأول؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map &#183; three parts"),
    h2("What happened, what to do, what to fix first", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#9888;</div><div class="role">Part 1</div>'
    '<h3>Security incident</h3><p>When real damage occurs</p></div>'
    '<div class="card"><div class="ico">&#128221;</div><div class="role">Part 2</div>'
    '<h3>Six stages</h3><p>The response, in order</p></div>'
    '<div class="card"><div class="ico">&#128202;</div><div class="role">Part 3</div>'
    '<h3>Risk assessment</h3><p>Impact &#215; likelihood</p></div>'
    '</div>',
    ar("خريطة المحاضرة: الجزء الأول: يعني إيه حادث أمني. الجزء التاني: المراحل الست للاستجابة بالترتيب. الجزء التالت: تقييم المخاطر — التأثير × الاحتمالية.")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("A school computer is infected with malware that is <b>spreading</b>. With your partner, put these four actions in order: <b>restore the files from a backup</b> &#183; <b>unplug it from the network</b> &#183; <b>find out how it got in</b> &#183; <b>remove the malware</b>.",
        "max-width:56ch;margin-top:1rem"),
    sub("Keep your order. Part 2 gives the book&#8217;s.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: جهاز في المدرسة اتصاب ببرمجية خبيثة وبتنتشر. رتّبوا الأربع خطوات دول: نرجّع الملفات من نسخة احتياطية، نفصله عن الشبكة، نعرف دخلت إزاي، نشيل البرمجية الخبيثة.")))

# ---------------- part 1: security incidents ----------------

A(s("",
    eyebrow("Part 1 &#183; What is a security incident"),
    h2("What is a security incident?", "max-width:24ch"),
    '<div class="rise statement def"><em>Security incident</em> &#8212; a situation in which actual damage occurs due to an information security problem.</div>',
    '<table class="rise" style="margin-top:.9rem">'
    '<tr><th>Type</th><th>Description</th></tr>'
    '<tr><td>Information leak</td><td>Personal or confidential information is leaked to the outside</td></tr>'
    '<tr><td>Data tampering</td><td>Data within a system is altered without authorization</td></tr>'
    '<tr><td>Service outage</td><td>A service becomes unavailable due to attacks on the server, etc.</td></tr>'
    '</table>',
    ar("الحادث الأمني: حدث بيأثر على سرية المعلومات أو سلامتها أو توافرها، أو بيهددها بجدية، أو بيخالف سياسة أمنية. أمثلة: تسرب المعلومات للخارج، والتلاعب بالبيانات من غير تصريح، وانقطاع الخدمة بسبب هجوم على الخادم.")))

A(video("AuYNXgO_f3Y", "The Internet: Cybersecurity &amp; Crime", "Code.org",
        "Watch &#183; incidents in the real world", "What does an attack look like?",
        "which of the three incident types &#8212; leak, tampering, outage &#8212; does each attack in the video cause?",
        "وانتو بتتفرجوا: كل هجوم في الفيديو بيعمل أنهي نوع من الحوادث التلاتة — تسرب، ولا تلاعب، ولا انقطاع خدمة؟"))

A(s("",
    eyebrow("1 &#183; Your turn"),
    h2("Which is NOT a security incident?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">Data was encrypted by a ransomware infection. <span class="ans">&#8212; <b>an incident</b>: real damage.</span></li>'
    '<li class="reveal rv tf-t">Customer information was leaked to the outside through unauthorized access. <span class="ans">&#8212; <b>an incident</b>: an information leak.</span></li>'
    '<li class="reveal rv">A software update was performed to add new features. <span class="ans">&#8212; <b>NOT an incident</b>: nothing was damaged.</span></li>'
    '<li class="reveal rv tf-t">A web service became unavailable due to an attack on the server. <span class="ans">&#8212; <b>an incident</b>: a service outage.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("أنهي واحد مش حادث أمني؟ تحديث برنامج عشان يضيف مميزات جديدة — ده مفيهوش أي ضرر، فمش حادث.")))

# ---------------- part 2: the six stages ----------------

A(s("",
    eyebrow("Part 2 &#183; The flow of incident response"),
    h2("Six stages, in order"),
    fig(STAGES),
    sub("When a security incident occurs, the response proceeds through these six stages &#8212; <b>in order</b>.",
        "max-width:62ch;margin-top:.3rem"),
    ar("لما يحصل حادث أمني، الاستجابة بتمشي في المراحل الست دي بالترتيب: التحضير، الاكتشاف، الاحتواء، إزالة التهديد (الاستئصال)، الاستعادة، الدروس المستفادة والتحسين.")))

A(s("",
    eyebrow("2 &#183; What each stage does"),
    h2("What happens at each stage"),
    '<table class="rise">'
    '<tr><th>Stage</th><th>What happens</th></tr>'
    '<tr><td>1 Preparation</td><td>Establish response procedures and structures in advance, in preparation for incidents</td></tr>'
    '<tr><td>2 Detection</td><td>Discover and confirm that an incident has occurred</td></tr>'
    '<tr><td>3 Containment</td><td>Limit the scope of impact so that damage does not spread further</td></tr>'
    '<tr><td>4 Eradication</td><td>Remove the cause of the incident (e.g. remove malware)</td></tr>'
    '<tr><td>5 Recovery</td><td>Return systems and services to their normal state</td></tr>'
    '<tr><td>6 Prevention of recurrence</td><td>Analyze the cause and take measures so that the same incident does not occur again</td></tr>'
    '</table>',
    ar("1 التحضير: إجراءات وهياكل استجابة مسبقًا. 2 الاكتشاف: نكتشف ونتأكد إن فيه حادث. 3 الاحتواء: نحدد نطاق التأثير عشان الضرر ميتنشرش. 4 إزالة التهديد (الاستئصال): نشيل التهديد ومسبباته زي البرمجيات الخبيثة ونعالج الثغرة. 5 الاستعادة: نرجّع الأنظمة لحالة تشغيل آمنة، وممكن من نسخة احتياطية سليمة. 6 الدروس المستفادة والتحسين: نحلل اللي حصل ونوثّق الدروس ونحسّن الضوابط.")))

A(s("",
    eyebrow("2 &#183; Two names, one stage"),
    h2("Stage 6 has two names", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>English book</h3><ul>'
    '<li><b>Prevention of recurrence</b></li>'
    '<li>Analyze the cause and take measures so the same incident does not occur again</li>'
    '</ul></div>'
    '<div class="pane b"><h3>Arabic book and ministry</h3><ul>'
    '<li><b>Lessons learned and improvement</b> &#8212; الدروس المستفادة والتحسين</li>'
    '<li>Analyze what happened, document the lessons, and improve the controls</li>'
    '</ul></div>'
    '</div>',
    sub("Learn both names: the exam can use either. They are the same last stage.", "max-width:60ch;margin-top:.9rem"),
    ar("خلّي بالك: المرحلة السادسة اسمها في الكتاب الإنجليزي \"منع التكرار\"، وفي الكتاب العربي وامتحانات الوزارة \"الدروس المستفادة والتحسين\". الاتنين نفس المرحلة: نحلل اللي حصل، ونوثّق الدروس، ونحسّن الضوابط.")))

A(s("",
    eyebrow("2 &#183; The order matters"),
    h2("Contain first, then remove the cause", "max-width:24ch"),
    '<div class="rise statement def"><em>Containment</em> limits the spread of damage. <em>Eradication</em> removes the cause. Containment comes <em>first</em>.</div>',
    sub("Disconnecting an infected computer from the network is containment; removing the malware is eradication. And if recovery is performed without removing the cause, <b>the same incident may occur again</b>.",
        "max-width:58ch;margin-top:.9rem"),
    ar("الاحتواء: الحد من انتشار الضرر. الاستئصال: إزالة السبب. الاحتواء بييجي الأول. ولو عملنا استعادة قبل ما نشيل السبب، نفس الحادث ممكن يتكرر.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("Why must containment come before eradication in the six-stage response?",
       "max-width:27ch"),
    ar("وقّف وفكّر: ليه الاحتواء لازم ييجي قبل الاستئصال في الاستجابة ذات المراحل الست؟")))

A(s("",
    eyebrow("2 &#183; In practice"),
    h2("The order is a guide, not a cage", "max-width:24ch"),
    sub("The six stages give the general sequence. In a real response some activities can <b>overlap</b> or <b>repeat</b>.",
        "max-width:58ch;margin-top:.6rem"),
    '<div class="rise statement def" style="margin-top:.9rem"><em>e.g.</em> Recovery can reveal traces of the threat that are still there &#8212; and then the team goes back to containment or eradication.</div>',
    sub("So: follow the order, and be ready to step back.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("ترتيب المراحل بيساعدنا نفهم التسلسل العام، بس الاستجابة الفعلية ممكن يحصل فيها تداخل أو تكرار بين بعض الأنشطة. مثلًا، الاسترداد ممكن يكشف بقايا للتهديد، فنضطر نرجع للاحتواء أو إزالة التهديد.")))

A(s("",
    eyebrow("2 &#183; Your turn &#183; worked example"),
    h2("Which stage is it?"),
    '<table class="rise">'
    '<tr><th>Action</th><th>Stage</th></tr>'
    '<tr><td>Establishing response procedures in advance, in preparation for incidents</td><td class="reveal"><span>Preparation</span></td></tr>'
    '<tr><td>Discovering and confirming that an incident has occurred</td><td class="reveal"><span>Detection</span></td></tr>'
    '<tr><td>Disconnecting a malware-infected computer from the network</td><td class="reveal"><span>Containment</span></td></tr>'
    '<tr><td>Removing the malware infection</td><td class="reveal"><span>Eradication</span></td></tr>'
    '<tr><td>Restoring a clean system from a backup</td><td class="reveal"><span>Recovery</span></td></tr>'
    '<tr><td>Analyzing the cause and taking measures so it does not occur again</td><td class="reveal"><span>Prevention of recurrence</span></td></tr>'
    '</table>',
    ar("لكل إجراء، أنهي مرحلة؟ الإجراءات المسبقة ← التحضير. التأكد إن فيه حادث ← الاكتشاف. فصل الجهاز المصاب عن الشبكة ← الاحتواء. إزالة البرمجية الخبيثة ← الاستئصال. الرجوع من نسخة احتياطية سليمة ← الاستعادة. تحليل السبب ← الدروس المستفادة والتحسين.")))

A(s("",
    eyebrow("2 &#183; Exam-style question &#183; 6 marks"),
    h2("Why must the six stages go in order?", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane b"><h3>Recover first</h3><ul>'
    '<li>The system is back, but the cause is <b>still there</b></li>'
    '<li>The same incident can happen again</li>'
    '</ul></div>'
    '<div class="pane a"><h3>Eradicate, then recover</h3><ul>'
    '<li>The cause is removed first</li>'
    '<li>Recovery returns a <b>clean</b> system</li>'
    '</ul></div>'
    '</div>',
    sub("Use recovery and eradication as the example, and say what happens if the cause is not removed.", "max-width:60ch;margin-top:.9rem"),
    ar("سؤال على نمط الامتحان: اشرح ليه المراحل الست لازم تتنفذ بالترتيب، مستخدمًا الاستعادة والاستئصال كمثال. استعن بـ: إيه اللي بيحصل لو السبب متشالش.")))

# ---------------- part 3: risk assessment ----------------

A(s("",
    eyebrow("Part 3 &#183; The concept of risk assessment"),
    h2("Risk = impact &#215; likelihood"),
    '<div class="rise statement def"><em>Risk</em> &#8212; the possibility of an information security problem occurring in the future, and its impact.</div>',
    '<table class="rise" style="margin-top:.9rem">'
    '<tr><th>Factor</th><th>Meaning</th></tr>'
    '<tr><td>Impact</td><td>How much damage occurs if the risk actually materializes</td></tr>'
    '<tr><td>Likelihood</td><td>How high the probability is that the risk will actually materialize</td></tr>'
    '</table>',
    sub("<b>Risk size = Impact &#215; Likelihood.</b> Not impact alone, and not likelihood alone.", "max-width:58ch;margin-top:.8rem"),
    ar("الخطر: احتمال إن يحصل حدث بيسبب ضرر، مع مراعاة احتمال وقوعه وحجم أثره. درجة الخطر = درجة التأثير × درجة الاحتمالية. التأثير: حجم الضرر لو الحدث وقع. الاحتمالية: مدى احتمال وقوع الحدث.")))

A(s("",
    eyebrow("3 &#183; Risk evaluation matrix"),
    h2("Fix the worst first"),
    fig(MATRIX),
    sub("Risks with both <b>high impact and high likelihood</b> are addressed first. It is difficult to address every risk at the same time, so priorities are set and measures taken systematically.",
        "max-width:62ch;margin-top:.3rem"),
    ar("المخاطر اللي تأثيرها عالي واحتماليتها عالية هي أعلى أولوية. أما ترتيب باقي الحالات فبيعتمد على درجات المصفوفة والسياق والضوابط المتاحة. مثلًا: تأثير كبير واحتمالية منخفضة = 3، يعني خطورة متوسطة.")))

A(s("",
    eyebrow("3 &#183; Your turn"),
    h2("Put the risks in order", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>Risk</th><th>Impact</th><th>Likelihood</th><th>Size</th></tr>'
    '<tr><td>a</td><td>large (3)</td><td>high (3)</td><td class="reveal"><span>9 &#8212; 1st</span></td></tr>'
    '<tr><td>b</td><td>small (1)</td><td>high (3)</td><td class="reveal"><span>3 &#8212; 3rd</span></td></tr>'
    '<tr><td>c</td><td>large (3)</td><td>medium (2)</td><td class="reveal"><span>6 &#8212; 2nd</span></td></tr>'
    '<tr><td>d</td><td>small (1)</td><td>low (1)</td><td class="reveal"><span>1 &#8212; 4th</span></td></tr>'
    '</table>',
    sub("Multiply each row, rank the sizes from biggest to smallest &#8212; then tap each size to check.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("رتّب المخاطر من الأعلى أولوية للأقل: اضرب التأثير × الاحتمالية لكل خطر، وبعدين رتّب الدرجات من الأكبر للأصغر.")))

A(s("",
    eyebrow("Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">A security incident is a situation in which actual damage occurs due to an information security problem. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv tf-t">In incident response, it is important first to prevent the spread of damage before removing the cause. <span class="ans">&#8212; <b>true</b>: containment before eradication.</span></li>'
    '<li class="reveal rv">The size of a risk can be determined by impact alone. <span class="ans">&#8212; <b>false</b>: by impact and likelihood.</span></li>'
    '<li class="reveal rv tf-t">The final stage of incident response is prevention of recurrence. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: تعريف الحادث الأمني — صح. منع انتشار الضرر قبل إزالة السبب — صح. حجم المخاطرة بالتأثير وحده — غلط. المرحلة الأخيرة الدروس المستفادة والتحسين — صح.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">It is enough to address only risks with large impact. <span class="ans">&#8212; <b>false</b>: likelihood counts too.</span></li>'
    '<li class="reveal rv">It is enough to address only risks with high likelihood. <span class="ans">&#8212; <b>false</b>: impact counts too.</span></li>'
    '<li class="reveal rv">All risks must be addressed simultaneously. <span class="ans">&#8212; <b>false</b>: set priorities.</span></li>'
    '<li class="reveal rv">Detection &#8594; Eradication &#8594; Containment &#8594; Recovery is the right order. <span class="ans">&#8212; <b>false</b>: containment comes before eradication.</span></li>'
    '</ul>',
    ar("خلّي بالك، كل الجمل دي غلط: نعالج المخاطر الكبيرة في التأثير بس — غلط. الاحتمالية العالية بس — غلط. كل المخاطر مع بعض — غلط. الاستئصال قبل الاحتواء — غلط.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("Ransomware hits the school&#8217;s records", "max-width:26ch"),
    sub("Files are encrypted and staff cannot log in. You lead the response. Restore from backup immediately &#8212; or follow the six stages in order?",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Respond from here.</b> The incident has just been detected. List the stages still to carry out, and what each means for this incident.</li>'
    '<li><b>Assess the risks.</b> (i) another ransomware attack, (ii) a brief power cut: estimate impact and likelihood, and say which to address first.</li>'
    '<li><b>Decide.</b> The first three actions, and one reason why order matters. In pairs, agree on the single most important first step.</li>'
    '</ul>',
    sub("Stuck? If you recover before you eradicate the cause, the malware is still there &#8212; and the same incident can happen again.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: نظام سجلات الطلاب في مدرسة اتهاجم ببرمجية فدية: الملفات اتشفرت والموظفين مش قادرين يدخلوا. اذكر المراحل اللي لسه هتتنفذ من دلوقتي، وقيّم مخاطرتين (فدية تانية، وانقطاع كهربا قصير)، وقرّر أول تلات إجراءات.")))

A(s("",
    eyebrow("In a new context"),
    h2("An online shop finds its customer data leaked", "max-width:26ch"),
    sub("The leak has just been detected.", "max-width:54ch;margin-top:.7rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li>Name the <b>next two stages</b> it should carry out, and why.</li>'
    '<li>Using risk assessment, identify <b>one risk to prioritize</b> afterward.</li>'
    '</ul>',
    ar("طبّق اللي اتعلمته: متجر إلكتروني لسه مكتشف إن بيانات العملاء اتسربت. باستخدام المراحل الست وتقييم المخاطر، حدد المرحلتين الجايين وليه، وحدد خطر واحد لازم ياخد الأولوية بعد كده.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 2-3"),
    h2("Respond in order; fix the worst first", "max-width:28ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> restore the school&#8217;s files from the backup straight away? What comes first?</p>'
    '<div class="rise statement">Follow the six stages in order &#8212; <em>prepare, detect, contain, eradicate, recover, prevent</em> &#8212; and prioritize risks by <em>impact &#215; likelihood</em>.</div>',
    ar("افتكر: اتبع التسلسل العام للمراحل الست (تحضير ← اكتشاف ← احتواء ← استئصال ← استعادة ← الدروس المستفادة والتحسين) مع إمكانية التداخل أو الرجوع لمرحلة سابقة، وحدد أولويات المخاطر بالتأثير × الاحتمالية.")))

# unit wrap -- this lesson closes Unit 2
A(s("",
    eyebrow("Unit 2 &#183; complete"),
    h2("Cybersecurity, in three lessons", "max-width:28ch"),
    '<div class="rise timeline">'
    '<div class="tl"><h3>2-1 &#183; Cryptographic technologies and authentication</h3><p>HTTPS, common-key and public-key, certificates, signatures, multi-factor login</p></div>'
    '<div class="tl"><h3>2-2 &#183; Network security design</h3><p>Firewall, VPN, DMZ, defense in depth, zero trust</p></div>'
    '<div class="tl"><h3>2-3 &#183; Incident response and risk management</h3><p>Security incidents, the six stages, risk = impact &#215; likelihood</p></div>'
    '</div>',
    ar("خلصنا الوحدة التانية: 2-1 تقنيات التشفير والمصادقة، 2-2 تصميم أمان الشبكات، 2-3 الاستجابة للحوادث وإدارة المخاطر.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 7"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 7 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers this lesson. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس ده. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))


def port_lightbox(out):
    """Copy lecture2's photo lightbox in: its CSS, its dialog markup, and the
    navigation handlers guarded by zoomOpen().

    The checker requires that guard once a deck carries photographs — an arrow
    key must not move the slide behind an open photo. This runs as part of the
    build so a rebuild cannot silently drop it, which it did once already."""
    if "#zoom" in out:
        return out
    l2 = io.open("lecture2/slides/index.html", encoding="utf-8").read()
    SCRIPT = l2.index("<script>")

    css = l2[l2.index(".shot img{cursor:zoom-in}"):
             l2.index("@media print{#zoom{display:none!important}}")
             + len("@media print{#zoom{display:none!important}}")]
    markup = re.search(r'<div id="zoom".*?</div>\s*(?=<script>|<div id="nav")',
                       l2, re.DOTALL).group(0).rstrip()
    # Index from the script tag. The same comment heading appears in the CSS,
    # and slicing from the first occurrence swallows the end of the style
    # block, the body and the opening script tag.
    block = l2[l2.index("/* ---- photo lightbox ---", SCRIPT):
               l2.index("const start = parseInt(location.hash", SCRIPT)].rstrip()
    for bad in ("</style>", "<script>", "<section"):
        assert bad not in block, "lightbox block swallowed %s" % bad

    out = out.replace("</style>", css + "\n</style>", 1)
    out = out.replace('<div id="nav">', markup + "\n\n" + '<div id="nav">', 1)
    key = out.index("addEventListener('keydown'")
    end = out.index("const start = parseInt(location.hash", key)
    out = out[:key] + block + "\n\n" + out[end:]

    # images land after first paint and change the height fit() measured
    hook = ("/* images arrive after first paint and change the height under us */\n"
            "Array.from(document.images).forEach(function(img){\n"
            "  if(!img.complete) img.addEventListener('load', refit);\n"
            "});\n\n")
    if "img.addEventListener('load', refit)" not in out:
        out = out.replace("function go(n){", hook + "function go(n){", 1)

    assert out.count("</style>") == 1 and out.count("<script>") == 1
    return out


GATE_CSS = """
/* ---------- exam code, covered until the teacher reveals it ---------- */
.qrgate{position:relative;cursor:pointer}
.qrgate .qrhide{
  position:absolute; inset:0; z-index:2;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:.35rem; text-align:center; padding:1rem;
  background:#16233F; border-radius:12px;
}
.qrgate.on .qrhide{display:none}
.qrgate .qrhide b{font-size:clamp(14px,1.7vw,22px); color:var(--paper)}
.qrgate .qrhide span{font-size:clamp(11px,1.15vw,15px); color:#A8B2C6; max-width:34ch}
.qrgate kbd{font:inherit; font-weight:600; background:rgba(255,255,255,.16);
  border-radius:4px; padding:0 .35em}
@media print{.qrgate .qrhide{display:none}}
"""

def gate_js(out):
 """Wire the reveal. Kept out of the QR-building code so the code is still
 generated from LECTURE.quizUrl exactly as the checker requires -- it is only
 covered up until the teacher asks for it."""
 hook = """
/* ---- exam code stays covered until the teacher reveals it ----------------
   The deck is published, so a student can open it at home. Hiding the code
   behind a deliberate action keeps the exam something taken in the lesson.
   Not security -- the quiz URL is guessable -- but it stops the easy path. */
(function(){
  const gate = document.getElementById('qrgate');
  if(!gate) return;
  /* Take the generated src off the image and hold it here, so the code is
     never fetched or drawn until it is asked for. A cover alone is not
     enough: a partly transparent panel still leaves a scannable code. */
  /* The code is still generated from LECTURE.quizUrl on load -- the repo's
     harness checks that, and it is what stops a stale QR shipping. It is the
     VIEW that is gated: an opaque panel sits over it until revealed.

     Worth being straight about what this is: the quiz address is guessable
     from the slides address, so this stops the code being handed to a class
     in advance, not a student who goes looking. */
  const link = document.getElementById('quizLink');
  const href = link ? link.textContent : '';
  if(link) link.textContent = '';
  function reveal(){
    gate.classList.add('on');
    if(link && href) link.textContent = href;
  }
  /* the dashboard sets this, and it is served from the same origin, so the
     teacher's own browser can have the code already showing. Storage throws
     in a private window, so the deck must work without it. */
  try {
    if(localStorage.getItem('pgteach.examCode') === 'shown') reveal();
  } catch(e){}

  gate.addEventListener('click', reveal);
  gate.addEventListener('keydown', function(e){
    if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); reveal(); }
  });
  addEventListener('keydown', function(e){
    if(zoomOpen && zoomOpen()) return;
    if(e.key === 'e' || e.key === 'E') reveal();
  });
})();
"""
 anchor = "const start = parseInt(location.hash"
 return out.replace(anchor, hook.strip() + chr(10) + chr(10) + anchor, 1)


ENGAGE_CSS = """
/* ---- side visuals (see VIZ in the builder) ---- */
.split{display:grid; grid-template-columns:minmax(0,1.2fr) minmax(0,1fr); gap:clamp(28px,4vw,80px); align-items:center}
.split>.main{min-width:0}
.viz{max-width:520px; width:100%; justify-self:center; cursor:pointer; -webkit-tap-highlight-color:transparent}
.viz svg{width:100%; height:auto; display:block; overflow:visible}
@media(max-width:1000px){.split{display:block} .split>.viz{display:none}}
p.vcap{margin-top:.8rem; text-align:center; font-size:clamp(13px,1.2vw,17px); color:var(--soft); line-height:1.5}
p.vcap b{display:block; color:var(--ink); font-weight:600}
p.vcap span{display:block; font-size:.92em}
.dark p.vcap{color:#AAB6CC} .dark p.vcap b{color:var(--paper)}
.viz .lbl{font:600 13px Inter,system-ui,sans-serif; fill:var(--soft)}
.viz .lbl.mid{text-anchor:middle} .viz .lbl.sm2{font-size:11px}
.viz .ntext{font:600 15px Inter,system-ui,sans-serif; fill:var(--ink); text-anchor:middle}
.viz .ntext.sm{font-size:12px; font-weight:500; fill:var(--soft)}
.dark .viz .ntext{fill:var(--paper)} .dark .viz .ntext.ink{fill:var(--ink)}
.viz .node rect{fill:var(--white); stroke:var(--line); stroke-width:1.5}
.dark .viz .node rect{fill:#1F2E4F; stroke:#3A4867}
.viz .node rect.core,.dark .viz .node rect.core{fill:var(--gold-pale); stroke:var(--gold)}
.viz .wire{stroke:var(--teal); stroke-width:3; fill:none; stroke-dasharray:6 7}
.dark .viz .wire{stroke:var(--gold)}
.viz .tA,.viz .node rect.tA{fill:var(--teal)} .viz .tB,.viz .node rect.tB{fill:var(--gold)}
.viz .node rect.bar{stroke:none}
.viz .vk{stroke:var(--teal); stroke-width:3.5; fill:none; stroke-linecap:round; stroke-linejoin:round}
.viz .vx{stroke:var(--wrong); stroke-width:3.5; fill:none; stroke-linecap:round}
.viz .qmark{font:700 44px Fraunces,serif; fill:var(--gold); text-anchor:middle}
.viz .bar{rx:3}
/* rows, tiles, chips */
.drow{display:flex; align-items:center; gap:.7rem; background:var(--white); border:1px solid var(--line); border-radius:12px; padding:.75rem 1rem; margin-bottom:.65rem; font-size:clamp(14px,1.3vw,18px)}
.drow .dico{font-size:1.5em} .drow .dai{background:var(--gold-pale); color:var(--ink); font-weight:700; border-radius:8px; padding:.15rem .5rem; font-size:.85em}
.drow .darrow{color:var(--teal); font-weight:700} .drow .dt{color:var(--ink)}
.tiles{display:grid; grid-template-columns:1fr 1fr; gap:.8rem}
.tile{background:#1F2E4F; border:1px solid #3A4867; border-radius:14px; padding:1rem; text-align:center; color:var(--paper)}
.tile span{display:block; font-size:2em; line-height:1.2} .tile b{display:block; margin-top:.3rem; font-size:clamp(14px,1.3vw,18px)}
.tile i{display:block; font-style:normal; color:#AAB6CC; font-size:clamp(12px,1.05vw,15px)}
.pchip{display:flex; align-items:center; gap:.8rem; background:var(--white); border:1px solid var(--line); border-left:4px solid var(--gold); border-radius:12px; padding:.8rem 1rem; margin-bottom:.6rem; font-weight:600; font-size:clamp(15px,1.4vw,20px); color:var(--ink)}
.pchip span{font-size:1.3em}
/* rings */
.viz .track{fill:none; stroke:#3A4867; stroke-width:12}
.viz .ring{fill:none; stroke:var(--gold); stroke-width:12; stroke-linecap:round; transform:rotate(-90deg); transform-origin:100px 100px; stroke-dasharray:503; stroke-dashoffset:0}
.viz .big{font:700 46px Fraunces,serif; fill:var(--paper); text-anchor:middle}
.viz .small{font:500 15px Inter,system-ui,sans-serif; fill:#AAB6CC; text-anchor:middle}
.tps{display:flex; justify-content:center; gap:.5rem; margin-top:.9rem}
.tps span{border:1px solid #3A4867; border-radius:99px; padding:.25rem .8rem; color:var(--paper); font-size:clamp(13px,1.15vw,16px)}

/* motion: only on the slide being shown, so opening the slide plays it */
@keyframes vIn{from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none}}
@keyframes vPop{0%{opacity:0; transform:scale(.3)} 70%{opacity:1; transform:scale(1.25)} 100%{transform:scale(1)}}
@keyframes vDash{to{stroke-dashoffset:-26}}
@keyframes vScan{0%{opacity:.85; transform:translateY(0)} 90%{opacity:.85; transform:translateY(190px)} 100%{opacity:0; transform:translateY(190px)}}
@keyframes vGrowY{from{transform:scaleY(0)} to{transform:scaleY(1)}}
@keyframes vGrowX{from{transform:scaleX(0)} to{transform:scaleX(1)}}
@keyframes vBreathe{0%,100%{opacity:.35; transform:scale(.92)} 50%{opacity:1; transform:scale(1.08)}}
@keyframes vStrike{from{opacity:1; text-decoration-color:transparent} to{opacity:.35}}
@keyframes vGlow{0%,100%{box-shadow:0 0 0 0 rgba(201,150,59,0)} 50%{box-shadow:0 0 0 6px rgba(201,150,59,.35)}}
@keyframes vDrop{from{width:88%; background:var(--teal)} to{width:28%; background:var(--wrong)}}
@keyframes vRing{from{stroke-dashoffset:0} to{stroke-dashoffset:503}}
@keyframes vRingFill{from{stroke-dashoffset:503} to{stroke-dashoffset:0}}
@keyframes vHideBox{0%,45%{opacity:1} 100%{opacity:0}}
@keyframes vShowThen{0%,45%{opacity:1} 60%,100%{opacity:0}}
@keyframes vLateIn{0%,55%{opacity:0} 100%{opacity:1}}
.slide.on .viz .wire{animation:vDash 1s linear infinite}
.slide.on .viz .n1{animation:vIn .45s .2s both} .slide.on .viz .n2{animation:vIn .45s .6s both} .slide.on .viz .n3{animation:vIn .45s 1s both}
.slide.on .viz .qmark{animation:vBreathe 2.2s 1.4s ease-in-out infinite both; transform-box:fill-box; transform-origin:center}
.slide.on .viz .vk,.slide.on .viz .vx{animation:vPop .45s cubic-bezier(.2,.8,.3,1.2) both; transform-box:fill-box; transform-origin:center}
.slide.on .viz .grow{animation:vGrowY .6s cubic-bezier(.2,.8,.3,1) both; transform-box:fill-box; transform-origin:bottom}
.slide.on .viz .drow,.slide.on .viz .tile,.slide.on .viz .pchip,.slide.on .viz .ustep,.slide.on .viz .tps span{animation:vIn .45s both}
.slide.on .viz .ring{animation:vRing 60s .4s linear both}

/* lecture 5's drawings */
.timer{max-width:320px}
.slide:not(.dark) .timer .big{fill:var(--ink)} .slide:not(.dark) .timer .small{fill:var(--soft)}
.slide:not(.dark) .timer .track{stroke:var(--line)} .slide:not(.dark) .tps span{border-color:var(--line); color:var(--ink)}
.shopv .sv{display:grid; grid-template-columns:auto 1fr; column-gap:.8rem; align-items:center; background:var(--white); border:1px solid var(--line); border-radius:12px; padding:.75rem 1rem; margin-bottom:.6rem; font-size:clamp(14px,1.3vw,18px); color:var(--ink)}
.shopv .sv span{grid-row:span 2; font-size:1.6em} .shopv .sv i{font-style:normal; color:var(--soft); font-size:.85em}
.shopv .sv3{border-color:var(--wrong); background:#FBF0EE}
.slide.on .viz .sv{animation:vIn .45s both} .slide.on .viz .sv2{animation-delay:.5s} .slide.on .viz .sv3{animation-delay:1s}
.viz .bar0{fill:var(--white); stroke:var(--line); stroke-width:2}
.dark .viz .bar0{fill:#1F2E4F; stroke:#3A4867}
.viz .url{font:600 19px Inter,system-ui,sans-serif; fill:var(--teal)}
.dark .viz .url{fill:var(--gold)} .viz .url.host{fill:var(--soft); font-weight:500} .dark .viz .url.host{fill:#AAB6CC}
.viz .lkbody{fill:var(--gold)} .viz .lkshackle{fill:none; stroke:var(--gold); stroke-width:3}
.viz .body{fill:var(--gold)} .viz .shackle{fill:none; stroke:var(--gold); stroke-width:14; stroke-linecap:round}
.viz .hole{fill:var(--ink)}
.drow small{color:var(--soft); font-size:.85em}
.msg{position:relative; font:600 clamp(16px,1.6vw,22px) ui-monospace,Consolas,monospace; background:var(--white); border:1px solid var(--line); border-radius:12px; padding:.7rem 1rem; text-align:center; color:var(--ink)}
.msg.cipher{background:var(--ink); color:var(--gold); border-color:var(--ink)}
.msg.cipher .c0{position:absolute; left:0; right:0; opacity:0; color:var(--paper)}
.kk{text-align:center; color:var(--teal); font-weight:600; margin:.45rem 0; font-size:clamp(13px,1.2vw,16px)}
.kk span{color:var(--soft); font-weight:500}
.cert{background:var(--white); border:1px solid var(--line); border-top:5px solid var(--teal); border-radius:14px; padding:1rem 1.2rem}
.certh{font:600 1.15em Fraunces,serif; color:var(--ink)}
.certn{font-family:ui-monospace,Consolas,monospace; color:var(--soft); margin:.3rem 0 .7rem}
.ck{display:flex; gap:.6rem; align-items:center; padding:.45rem 0; border-top:1px dashed var(--line); color:var(--ink); font-size:clamp(13px,1.2vw,16px)}
.ck b{color:var(--teal); display:inline-block}
.leak>div{border-radius:12px; padding:.75rem 1rem; margin-bottom:.55rem; font-size:clamp(14px,1.3vw,18px)}
.lk1{background:var(--white); border:1px solid var(--line); display:flex; justify-content:space-between; align-items:center; color:var(--ink)}
.lk1 em{font-style:normal; font-weight:700; color:var(--wrong); border:2px solid var(--wrong); border-radius:6px; padding:0 .4rem; display:inline-block; transform:rotate(-6deg)}
.leak .lkarrow{color:var(--soft); text-align:center; padding:.1rem 0}
.lk2{background:var(--gold-pale); color:var(--ink)}
.lk3{background:var(--teal-pale); color:var(--teal); font-weight:700; text-align:center}
.pchip div small{display:block; font-weight:500; color:var(--soft); font-size:.8em}
.ustep2{display:flex; gap:.8rem; align-items:center; background:var(--white); border:1px solid var(--line); border-radius:12px; padding:.75rem 1rem; margin-bottom:.6rem; color:var(--soft); font-size:clamp(14px,1.3vw,18px)}
.ustep2 b{color:var(--ink); font-family:Fraunces,serif; font-size:1.2em}
.ustep2.now{border-color:var(--teal); border-left:5px solid var(--teal); color:var(--ink); background:var(--teal-pale)}
@keyframes vShackle{0%,30%{transform:translateY(-24px)} 70%{transform:translateY(3px)} 100%{transform:none}}
.slide.on .viz .shackle{animation:vShackle 1.4s .3s cubic-bezier(.3,.7,.3,1.2) both}
.slide.on .viz .lockmini{animation:vPop .45s 1.5s both; transform-box:fill-box; transform-origin:center}
.slide.on .viz .url{animation:vIn .5s 1.7s both}
.slide.on .viz .msg.plain{animation:vIn .45s .2s both}
.slide.on .viz .kk{animation:vIn .45s .7s both}
.slide.on .viz .msg.cipher{animation:vIn .45s 1.1s both}
.slide.on .viz .msg.cipher .c0{animation:vShowThen 1.4s 1.1s both}
.slide.on .viz .msg.cipher .c1{animation:vLateIn 1.4s 1.1s both; display:inline-block}
.slide.on .viz .kk.late{animation-delay:2.5s}
.slide.on .viz .msg.late2{animation-delay:2.9s}
.slide.on .viz .ck{animation:vIn .45s both}
.slide.on .viz .ck b{animation:vPop .45s .3s both}
.slide.on .viz .lk1{animation:vIn .45s .2s both}
.slide.on .viz .lk1 em{animation:vPop .45s .8s both}
.slide.on .viz .lkarrow{animation:vIn .45s 1.2s both}
.slide.on .viz .lk2{animation:vIn .45s 1.7s both}
.slide.on .viz .lk3{animation:vPop .5s 2.3s both}
.slide.on .viz .ustep2{animation:vIn .45s both}
/* a statement that is true gets a tick when revealed, not the cross */
.check li.rv.tf-t.shown::before{content:"\\2713"; color:var(--teal)}

/* lecture 7's drawings */
.statement.def{font-size:clamp(18px,2.15vw,30px); line-height:1.28; max-width:46ch}
.alarm>div{border-radius:12px; padding:.8rem 1rem; margin-bottom:.6rem; font-weight:700; font-size:clamp(14px,1.35vw,19px)}
.al1{background:#1F2E4F; color:var(--paper); border:1px solid #3A4867}
.al2{background:#5A2A26; color:#FFD9D2; border:1px solid #9C3B2E}
.al3{display:flex; gap:.4rem; flex-wrap:wrap; background:transparent!important; padding:0!important}
.al3 span{background:var(--gold); color:var(--ink); border-radius:99px; padding:.25rem .7rem; font-size:.8em}
@keyframes vAlarm{0%,100%{box-shadow:0 0 0 0 rgba(156,59,46,0)} 50%{box-shadow:0 0 0 8px rgba(156,59,46,.35)}}
.slide.on .viz .al1{animation:vIn .45s .2s both}
.slide.on .viz .al2{animation:vPop .5s .8s both, vAlarm 1.2s 1.4s 2 ease-in-out}
.slide.on .viz .al3 span{animation:vIn .4s both}
.slide.on .viz .al3 span:nth-child(1){animation-delay:1.8s} .slide.on .viz .al3 span:nth-child(2){animation-delay:2.1s}
.slide.on .viz .al3 span:nth-child(3){animation-delay:2.4s} .slide.on .viz .al3 span:nth-child(4){animation-delay:2.7s}
.viz .lnk{stroke:var(--teal); stroke-width:4}
.viz .lnk.cut{stroke:var(--wrong); stroke-dasharray:8 8; opacity:.35}
.viz .hub{fill:var(--gold-pale); stroke:var(--gold); stroke-width:2}
.viz .pc{fill:#fff; stroke:var(--line); stroke-width:2}
.viz .pc.bad{fill:var(--wrong); stroke:var(--wrong)}
.viz .ntext.wh{fill:#fff; font-size:20px}
.viz .redl{fill:var(--wrong)}
@keyframes vCut{0%,45%{opacity:1; stroke-dasharray:0 0} 100%{opacity:.35; stroke-dasharray:8 8}}
.slide.on .viz .lnk.cut{animation:vCut 1.8s .4s both}
.slide.on .viz .redl{animation:vIn .45s 2s both}
.lad{display:grid; grid-template-columns:3rem 1fr; column-gap:.8rem; align-items:center; background:#fff; border:1px solid var(--line); border-radius:12px; padding:.6rem .9rem; margin-bottom:.5rem; color:var(--ink); font-size:clamp(14px,1.3vw,18px)}
.lad b{grid-row:span 2; font:700 1.6em Fraunces,serif; color:var(--wrong); text-align:center}
.lad span{font-weight:700} .lad small{color:var(--soft)}
.lad:nth-child(2) b{color:#B5531C} .lad:nth-child(3) b{color:var(--gold)} .lad:nth-child(4) b{color:var(--teal)}
.slide.on .viz .lad{animation:vIn .45s both}
.mult{background:#fff; border:1px solid var(--line); border-radius:14px; padding:1.2rem}
.mrow{display:flex; align-items:center; justify-content:center; gap:.6rem; flex-wrap:wrap}
.mi{display:flex; flex-direction:column; align-items:center; font-size:clamp(12px,1.1vw,15px); color:var(--soft)}
.mi b{font-size:1.25em; color:var(--ink)}
.mop{font:700 1.8em Fraunces,serif; color:var(--gold)}
.mres{font:700 2.4em Fraunces,serif; color:var(--wrong)}
.mnote{margin-top:.9rem; text-align:center; color:var(--ink); font-size:clamp(13px,1.2vw,16px)}
.slide.on .viz .mi,.slide.on .viz .mop{animation:vIn .45s both}
.slide.on .viz .mi:nth-child(3){animation-delay:.5s} .slide.on .viz .mop:nth-child(2){animation-delay:.3s} .slide.on .viz .mop:nth-child(4){animation-delay:.8s}
.slide.on .viz .mres{animation:vPop .5s 1.1s both; display:inline-block}
.slide.on .viz .mnote{animation:vIn .45s 1.7s both}

/* the video: bigger on a wide screen, as long as the slide still fits */
@media(min-width:1001px){.slide .vid{width:min(100%, 960px, calc((100vh - 380px) * 16 / 9))}}

/* ---------- video: a poster until clicked, then the player ---------- */
.vid{position:relative; width:min(680px,100%); aspect-ratio:16/9; margin:.9rem 0 .3rem;
  border-radius:12px; overflow:hidden; background:#16233F; cursor:pointer}
.vid img{width:100%; height:100%; object-fit:cover; display:block; opacity:.82}
.vid .play{position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
  width:clamp(52px,6vw,78px); height:clamp(52px,6vw,78px); border-radius:50%;
  background:var(--teal); color:#fff; font-size:clamp(20px,2.4vw,32px);
  display:flex; align-items:center; justify-content:center; box-shadow:0 6px 24px rgba(0,0,0,.35)}
.vid .vcap{position:absolute; left:0; right:0; bottom:0; padding:.55rem .9rem;
  background:linear-gradient(transparent,rgba(0,0,0,.78)); color:#fff; font-size:clamp(12px,1.3vw,16px)}
.vid iframe{position:absolute; inset:0; width:100%; height:100%; border:0}
.vid:focus-visible{outline:3px solid var(--gold); outline-offset:3px}
/* ---------- tap to reveal ---------- */
/* Hidden: blurred, breathing gently so it reads as "tap me". Revealed: the
   blur clears as the word pops in with a small overshoot, a gold flash
   behind it fades, and it settles in the lecture colour -- each on its own
   tap. The base stylesheet turns every animation off under
   prefers-reduced-motion. */
@keyframes revealPop{
  0%  {transform:scale(.6); opacity:.2; filter:blur(8px)}
  55% {transform:scale(1.18); opacity:1; filter:blur(0)}
  75% {transform:scale(.96)}
  100%{transform:scale(1)}
}
@keyframes revealFlash{0%{background:var(--gold-pale)} 100%{background:transparent}}
@keyframes revealStamp{
  0%  {transform:scale(2.4) rotate(-25deg); opacity:0}
  60% {transform:scale(.9) rotate(4deg); opacity:1}
  100%{transform:scale(1) rotate(0)}
}
@keyframes hintBreathe{0%,100%{opacity:.55} 50%{opacity:.9}}
td.reveal{cursor:pointer}
td.reveal span{display:inline-block}
td.reveal:not(.shown) span{filter:blur(7px); user-select:none; animation:hintBreathe 2.4s ease-in-out infinite}
td.reveal.shown{animation:revealFlash 1.1s ease-out}
td.reveal.shown span{animation:revealPop .65s cubic-bezier(.2,.8,.3,1.1) both; color:var(--teal); font-weight:600}
.check li.rv{cursor:pointer}
.check li.rv::before{content:"?"; color:var(--gold); display:inline-block}
.check li.rv.shown::before{content:"\\2715"; color:var(--wrong); animation:revealStamp .5s cubic-bezier(.2,.8,.3,1.2) both}
.check li.rv .ans{display:inline-block}
.check li.rv:not(.shown) .ans{filter:blur(7px); user-select:none; animation:hintBreathe 2.4s ease-in-out infinite}
.check li.rv.shown .ans{animation:revealPop .65s cubic-bezier(.2,.8,.3,1.1) .12s both}
@media print{.vid{display:none} td.reveal span,.check li.rv .ans{filter:none!important;animation:none!important}}
"""


def engage_js(out):
    """Videos load on click and stop when the slide changes; blurred answers
    show on tap. Written not to assume a full DOM -- the behavioural harness
    runs this against a stub, and a call it lacks fails CI."""
    hook = """
/* ---- videos and tap-to-reveal ------------------------------------------
   A video is a poster until clicked, so a slow school connection does not
   stall the deck; leaving the slide puts the poster back, which stops it.
   Enter/space on a focused poster plays it without also turning the slide. */
(function(){
  if(!document.querySelectorAll) return;
  function play(el){
    if(el.getAttribute('data-on')) return;
    el.setAttribute('data-on', '1');
    el.setAttribute('data-poster', el.innerHTML);
    el.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' +
      el.getAttribute('data-yt') + '?autoplay=1&rel=0" title="' +
      (el.getAttribute('aria-label') || 'video') +
      '" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
  }
  function stopAll(){
    document.querySelectorAll('.vid[data-on]').forEach(function(el){
      el.innerHTML = el.getAttribute('data-poster');
      el.removeAttribute('data-on');
    });
  }
  document.querySelectorAll('.vid').forEach(function(el){
    el.addEventListener('click', function(){ play(el); });
    el.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); e.stopPropagation(); play(el); }
    });
  });
  addEventListener('hashchange', stopAll);
  document.querySelectorAll('.reveal').forEach(function(el){
    el.addEventListener('click', function(){ el.classList.add('shown'); });
  });
  /* tapping a drawing plays it again: a fresh copy restarts every animation */
  function replay(){
    var el = this;
    if(!el.cloneNode || !el.parentNode) return;
    var copy = el.cloneNode(true);
    el.parentNode.replaceChild(copy, el);
    copy.addEventListener('click', replay);
  }
  document.querySelectorAll('.viz').forEach(function(el){ el.addEventListener('click', replay); });
})();
"""
    anchor = "const start = parseInt(location.hash"
    assert out.count(anchor) == 1
    return out.replace(anchor, hook.strip() + chr(10) + chr(10) + anchor, 1)


body = "\n\n".join(SLIDES)
BASE = "scripts/lecture7_slides_base.html"
src = io.open(BASE, encoding="utf-8").read()
start = src.index('<div id="stage">') + len('<div id="stage">')
end = src.index('<div id="nav">')
# keep whatever closes the stage div
tail = src[end - 20:end]
close = "\n</div>\n\n" if "</div>" in tail else "\n"
out = src[:start] + "\n\n" + body + close + src[end:]
out = port_lightbox(out)
out = gate_js(out)
out = engage_js(out)
if ".vid{" not in out:
    out = out.replace("</style>", ENGAGE_CSS.strip() + chr(10) + "</style>", 1)
if ".qrgate{" not in out:
    out = out.replace("</style>", GATE_CSS.strip() + chr(10) + "</style>", 1)
if ".shots{" not in out:
    out = out.replace("</style>", PHOTO_CSS.strip() + chr(10) + "</style>", 1)

# never let a Liquid delimiter into the page
assert not re.search(r"\{[%{]", out), "Liquid delimiter in generated slides"
io.open(DST, "w", encoding="utf-8", newline="\n").write(out)
print("slides written:", len(SLIDES), "slides,", len(out), "bytes")

