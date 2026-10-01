# -*- coding: utf-8 -*-
"""Build Lecture 4's deck.

    python scripts/build_lecture4_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/lecture4_slides_base.html and writes lecture4/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the photo CSS
added. Always starts from the base, never from the published deck: the
injections check for their own CSS before adding markup, so rebuilding on
top of an already-built deck would drop the lightbox dialog.

Content is Lesson 1-4, Ethical Issues with AI, textbook pp. 26-32, and
nothing outside the curriculum: the recap is lesson 1-3's own list of
cautions, and the closing map is Unit 1's four lessons, because this lesson
closes the unit and the chapter exam covers all four. Two ideas the English
book states in one line are given a slide each, because the ministry's
assessment book asks about them directly: responsibility against
accountability, and the proxy variable as a cause of bias.

The helpers, the photo CSS, port_lightbox(), the exam-code gate and the
build block are copied unchanged from build_lecture3_slides.py, which is
where they were proven. The Arabic follows the Arabic textbook's lesson 1-4
(pp. 24-30) point by point -- its definitions, questions and Think boxes --
said in Egyptian Arabic, with the book's own terms kept as they are.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "lecture4/slides/index.html"


# --------------------------------------------------------------------------
# diagrams — inline SVG, coloured from the page's CSS variables so they follow
# LECTURE_ACCENT like everything else. Explanatory sentences stay OUT of the
# SVG (they become unreadable once the slide is scaled); labels only.
# --------------------------------------------------------------------------

BIAS = '''
<svg viewBox="0 0 900 250" role="img" aria-label="Lopsided training data produces a lopsided judgment">
  <text x="30" y="24" font-size="12.5" font-weight="600" fill="var(--soft)">It is not told to be unfair. It copies the data it was given.</text>

  <rect x="30" y="46" width="210" height="136" rx="9" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="2"/>
  <text x="135" y="70" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">training data</text>
  <g fill="var(--teal)">
    <circle cx="62" cy="100" r="11"/><circle cx="96" cy="100" r="11"/><circle cx="130" cy="100" r="11"/>
    <circle cx="164" cy="100" r="11"/><circle cx="198" cy="100" r="11"/>
    <circle cx="62" cy="136" r="11"/><circle cx="96" cy="136" r="11"/><circle cx="130" cy="136" r="11"/>
  </g>
  <g fill="var(--gold)"><circle cx="164" cy="136" r="11"/></g>
  <text x="135" y="170" text-anchor="middle" font-size="11" fill="var(--soft)">8 of one group, 1 of another</text>

  <line x1="246" y1="114" x2="304" y2="114" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="304,114 296,109 296,119" fill="var(--teal)"/>

  <rect x="310" y="60" width="200" height="108" rx="10" fill="var(--teal)" opacity=".22" stroke="var(--teal)" stroke-width="2.5">
    <animate attributeName="opacity" values=".22;.40;.22" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <text x="410" y="104" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">the AI learns</text>
  <text x="410" y="126" text-anchor="middle" font-size="11" fill="var(--soft)">whatever pattern is there</text>

  <line x1="516" y1="114" x2="574" y2="114" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="574,114 566,109 566,119" fill="var(--teal)"/>

  <rect x="580" y="46" width="290" height="136" rx="9" fill="#9C3B2E" opacity=".08" stroke="#9C3B2E" stroke-width="2"/>
  <text x="725" y="72" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">its judgment</text>
  <text x="725" y="104" text-anchor="middle" font-size="12" fill="var(--ink)">accurate for the big group</text>
  <text x="725" y="136" text-anchor="middle" font-size="12" font-weight="600" fill="#9C3B2E">misjudges the small one</text>

  <text x="30" y="222" font-size="12" fill="var(--ink)">That is <tspan font-weight="600">algorithmic bias</tspan> &#8212; bias in the judgment, caused by bias in the training data.</text>
</svg>'''

XAI = '''
<svg viewBox="0 0 900 270" role="img" aria-label="A black box shows only the answer; explainable AI also shows the reasons">
  <text x="30" y="26" font-size="13" font-weight="600" fill="#9C3B2E">Black box &#8212; the answer, and nothing else</text>
  <rect x="30" y="40" width="150" height="54" rx="7" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>
  <text x="105" y="72" text-anchor="middle" font-size="12" fill="var(--ink)">a job application</text>
  <line x1="186" y1="67" x2="236" y2="67" stroke="var(--soft)" stroke-width="2"/>
  <polygon points="236,67 228,62 228,72" fill="var(--soft)"/>
  <rect x="242" y="36" width="220" height="62" rx="8" fill="var(--ink)" opacity=".88"/>
  <text x="352" y="74" text-anchor="middle" font-size="16" font-weight="600" fill="#fff">?</text>
  <line x1="468" y1="67" x2="518" y2="67" stroke="var(--soft)" stroke-width="2"/>
  <polygon points="518,67 510,62 510,72" fill="var(--soft)"/>
  <rect x="524" y="40" width="160" height="54" rx="7" fill="#9C3B2E" opacity=".10" stroke="#9C3B2E" stroke-width="2"/>
  <text x="604" y="72" text-anchor="middle" font-size="12.5" font-weight="600" fill="#9C3B2E">&#8220;rejected&#8221;</text>
  <text x="700" y="64" font-size="11" fill="var(--soft)">why? nobody</text>
  <text x="700" y="80" font-size="11" fill="var(--soft)">can check it</text>

  <line x1="30" y1="126" x2="870" y2="126" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="5 5"/>

  <text x="30" y="160" font-size="13" font-weight="600" fill="var(--teal)">Explainable AI (XAI) &#8212; the answer, and why</text>
  <rect x="30" y="174" width="150" height="54" rx="7" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>
  <text x="105" y="206" text-anchor="middle" font-size="12" fill="var(--ink)">a job application</text>
  <line x1="186" y1="201" x2="236" y2="201" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="236,201 228,196 228,206" fill="var(--teal)"/>
  <rect x="242" y="170" width="220" height="62" rx="8" fill="var(--teal)" opacity=".20" stroke="var(--teal)" stroke-width="2.5">
    <animate attributeName="opacity" values=".20;.38;.20" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <text x="352" y="196" text-anchor="middle" font-size="11.5" fill="var(--ink)">reasons shown:</text>
  <text x="352" y="216" text-anchor="middle" font-size="11.5" fill="var(--ink)">experience, test score</text>
  <line x1="468" y1="201" x2="518" y2="201" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="518,201 510,196 510,206" fill="var(--teal)"/>
  <rect x="524" y="174" width="160" height="54" rx="7" fill="var(--gold)" opacity=".22" stroke="var(--gold)" stroke-width="2"/>
  <text x="604" y="206" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">&#8220;rejected&#8221;</text>
  <text x="700" y="198" font-size="11" fill="var(--soft)">now a person can</text>
  <text x="700" y="214" font-size="11" fill="var(--soft)">check whether it is fair</text>
</svg>'''

WHO = '''
<svg viewBox="0 0 900 250" role="img" aria-label="When an AI gets it wrong, the developer, the operator and the user each hold a different part of the responsibility">
  <rect x="340" y="24" width="220" height="62" rx="10" fill="#9C3B2E" opacity=".10" stroke="#9C3B2E" stroke-width="2.5">
    <animate attributeName="opacity" values=".10;.26;.10" dur="3s" repeatCount="indefinite"/>
  </rect>
  <text x="450" y="52" text-anchor="middle" font-size="13" font-weight="600" fill="#9C3B2E">the AI gets it wrong</text>
  <text x="450" y="72" text-anchor="middle" font-size="11.5" fill="var(--soft)">who answers for it?</text>

  <line x1="450" y1="90" x2="150" y2="146" stroke="var(--soft)" stroke-width="1.8"/>
  <line x1="450" y1="90" x2="450" y2="146" stroke="var(--soft)" stroke-width="1.8"/>
  <line x1="450" y1="90" x2="750" y2="146" stroke="var(--soft)" stroke-width="1.8"/>

  <rect x="40" y="150" width="220" height="70" rx="9" fill="var(--teal)" opacity=".13" stroke="var(--teal)" stroke-width="2"/>
  <text x="150" y="178" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">the developer</text>
  <text x="150" y="200" text-anchor="middle" font-size="11" fill="var(--soft)">built it, chose the data</text>

  <rect x="340" y="150" width="220" height="70" rx="9" fill="var(--teal)" opacity=".13" stroke="var(--teal)" stroke-width="2"/>
  <text x="450" y="178" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">the operator</text>
  <text x="450" y="200" text-anchor="middle" font-size="11" fill="var(--soft)">the company running it</text>

  <rect x="640" y="150" width="220" height="70" rx="9" fill="var(--teal)" opacity=".13" stroke="var(--teal)" stroke-width="2"/>
  <text x="750" y="178" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">the user</text>
  <text x="750" y="200" text-anchor="middle" font-size="11" fill="var(--soft)">acted on its result</text>

  <text x="450" y="244" text-anchor="middle" font-size="11.5" fill="var(--soft)">Each sees it differently &#8212; and no clear standard has been agreed yet.</text>
</svg>'''


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



# ---------------- side visuals ----------------
# A slide whose content fills only the left half of a wide screen gets an
# animated explainer on the right. Each drawing plays once when the slide
# opens and again when tapped. Under 1000px wide the drawing is hidden and
# the slide keeps its one-column layout, because the drawing adds to the
# content and never replaces it. The final frame of every animation is the
# element's own style, so with reduced motion (every animation off) and in
# print the drawing shows complete.

def vcap(en, arabic):
    return '<p class="vcap"><b>%s</b><span dir="rtl">%s</span></p>' % (en, arabic)


def face(x, y, tone, mark, d):
    """A face at (x, y), coloured by group, with the system's verdict (a
    tick or a cross) popping in after delay d seconds."""
    m = ('<path class="vk" style="animation-delay:%.2fs" d="M%d %d l5 5 l9 -10"/>' % (d, x - 7, y + 30)
         if mark == "ok" else
         '<path class="vx" style="animation-delay:%.2fs" d="M%d %d l12 12 M%d %d l-12 12"/>' % (d, x - 6, y + 25, x + 6, y + 25))
    return ('<g><circle cx="%d" cy="%d" r="15" class="%s"/>'
            '<circle cx="%d" cy="%d" r="1.8" class="eye"/><circle cx="%d" cy="%d" r="1.8" class="eye"/>'
            '<path d="M%d %d q6 5 12 0" class="mouth"/>%s</g>'
            % (x, y, tone, x - 5, y - 3, x + 5, y - 3, x - 6, y + 5, m))


def v_scan():
    a = "".join(face(95 + 60 * k, 70, "tA", "ok", 1.6 + .12 * k) for k in range(5))
    marks_b = ["ok", "no", "ok", "no", "no"]
    b = "".join(face(95 + 60 * k, 175, "tB", marks_b[k], 2.3 + .12 * k) for k in range(5))
    return ('<aside class="rise viz">'
            '<svg viewBox="0 0 400 260" role="img" aria-label="A face-recognition system checks two groups of faces and makes more mistakes with group B">'
            '<text x="18" y="74" class="lbl">Group A</text><text x="18" y="179" class="lbl">Group B</text>'
            + a + b +
            '<rect class="scan" x="60" y="30" width="330" height="4" rx="2"/>'
            '</svg>'
            + vcap("Same system &#8212; more mistakes for one group.",
                   "نفس النظام، بس بيغلط أكتر مع مجموعة واحدة.")
            + '</aside>')


def v_flow_trust():
    return ('<aside class="rise viz">'
            '<svg viewBox="0 0 400 220" role="img" aria-label="Data goes into an AI, which makes a decision about a person">'
            '<path class="wire" d="M92 110 H168"/><path class="wire" d="M232 110 H308"/>'
            '<g class="node n1"><rect x="20" y="75" width="72" height="70" rx="12"/><text x="56" y="115" class="ntext">Data</text></g>'
            '<g class="node n2"><rect x="168" y="75" width="64" height="70" rx="12" class="core"/><text x="200" y="115" class="ntext ink">AI</text></g>'
            '<g class="node n3"><rect x="308" y="75" width="72" height="70" rx="12"/><text x="344" y="106" class="ntext">Decision</text><text x="344" y="126" class="ntext sm">about you</text></g>'
            '<text x="344" y="190" class="qmark">?</text>'
            '</svg>'
            + vcap("Fair? And who answers if it is wrong?",
                   "عادل؟ ولو غلط، مين المسؤول؟")
            + '</aside>')


def v_decides():
    rows = [("&#128196;", "Who gets a job interview"),
            ("&#128247;", "What a camera says you are"),
            ("&#128451;", "How your personal data is used")]
    out = []
    for k, (ico, t) in enumerate(rows):
        out.append('<div class="drow" style="animation-delay:%.2fs"><span class="dico">%s</span>'
                   '<span class="dai">AI</span><span class="darrow">&#8594;</span>'
                   '<span class="dt">%s</span></div>' % (.5 + .55 * k, ico, t))
    return ('<aside class="rise viz">' + "".join(out)
            + vcap("Real decisions, about real people.",
                   "قرارات حقيقية، عن ناس حقيقيين.")
            + '</aside>')


def v_issues():
    tiles = [("&#9878;", "Bias", "Is it fair?"),
             ("&#128274;", "Privacy", "Is our data safe?"),
             ("&#11035;", "Black box", "Why did it decide?"),
             ("&#128587;", "Responsibility", "Who answers?")]
    out = "".join('<div class="tile" style="animation-delay:%.2fs"><span>%s</span><b>%s</b><i>%s</i></div>'
                  % (.4 + .45 * k, ico, t, q) for k, (ico, t, q) in enumerate(tiles))
    return ('<aside class="rise viz"><div class="tiles">' + out + '</div>'
            + vcap("Four issues today &#8212; one principle for each.",
                   "أربع مشاكل النهارده، ولكل واحدة مبدأ.")
            + '</aside>')


def v_bias_flow():
    dots = []
    for k in range(10):
        cx, cy = 34 + (k % 5) * 16, 88 + (k // 5) * 18
        tone = "tB" if k in (4, 9) else "tA"
        dots.append('<circle cx="%d" cy="%d" r="6" class="%s"/>' % (cx, cy, tone))
    return ('<aside class="rise viz">'
            '<svg viewBox="0 0 400 230" role="img" aria-label="Biased training data goes into an AI, and its judgments come out biased">'
            '<g class="node n1"><rect x="14" y="60" width="104" height="90" rx="12"/>' + "".join(dots) +
            '<text x="66" y="175" class="lbl mid">Training data</text></g>'
            '<path class="wire" d="M122 105 H164"/>'
            '<g class="node n2"><rect x="164" y="70" width="72" height="70" rx="12" class="core"/><text x="200" y="110" class="ntext ink">AI</text>'
            '<text x="200" y="175" class="lbl mid">learns</text></g>'
            '<path class="wire" d="M240 105 H282"/>'
            '<g class="node n3"><rect x="282" y="60" width="104" height="90" rx="12"/>'
            '<rect class="bar tA grow" x="306" y="76" width="22" height="60" style="animation-delay:1.9s"/>'
            '<rect class="bar tB grow" x="340" y="118" width="22" height="18" style="animation-delay:2.1s"/>'
            '<text x="334" y="175" class="lbl mid">Judgments</text></g>'
            '</svg>'
            + vcap("Bias in the data &#8594; bias in the judgments.",
                   "تحيز في البيانات ← تحيز في الأحكام.")
            + '</aside>')


def v_proxy():
    return ('<aside class="rise viz"><div class="cv">'
            '<div class="cvh">CV</div>'
            '<div class="cvl"><span>Name</span><i></i></div>'
            '<div class="cvl gone"><span>Gender</span><i></i><em>removed</em></div>'
            '<div class="cvl"><span>Experience</span><i></i></div>'
            '<div class="cvl hot"><span>&#8220;captain of the <b>women&#8217;s</b> chess club&#8221;</span></div>'
            '<div class="score"><span>AI score</span><div class="meter"><div class="fill"></div></div></div>'
            '</div>'
            + vcap("The word still points to gender.",
                   "الكلمة لسه بتشاور على النوع.")
            + '</aside>')


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


def v_xai():
    return ('<aside class="rise viz">'
            '<svg viewBox="0 0 400 240" role="img" aria-label="A black box hides why the AI decided; XAI shows which factors led to the judgment">'
            '<text x="20" y="118" class="ntext" text-anchor="start">Input</text>'
            '<path class="wire" d="M72 112 H130"/>'
            '<rect x="130" y="52" width="140" height="120" rx="12" class="glass"/>'
            '<rect class="bar tA grow" x="150" y="80" width="80" height="14" style="animation-delay:2.2s"/>'
            '<rect class="bar tA grow" x="150" y="105" width="52" height="14" style="animation-delay:2.4s"/>'
            '<rect class="bar tB grow" x="150" y="130" width="28" height="14" style="animation-delay:2.6s"/>'
            '<text x="240" y="92" class="lbl sm2">A</text><text x="210" y="117" class="lbl sm2">B</text><text x="186" y="142" class="lbl sm2">C</text>'
            '<rect x="130" y="52" width="140" height="120" rx="12" class="blackbox"/>'
            '<text x="200" y="120" class="bbq">?</text>'
            '<path class="wire" d="M270 112 H314"/>'
            '<text x="326" y="118" class="ntext" text-anchor="start">Result</text>'
            '<text x="200" y="205" class="lbl mid bbl">Black box</text>'
            '<text x="200" y="205" class="lbl mid xail">XAI: the factors behind it</text>'
            '</svg>'
            + vcap("XAI shows why it made that judgment.",
                   "الـ XAI بيورّينا ليه أخد القرار ده.")
            + '</aside>')


def v_principles():
    items = [("&#9878;", "Fairness"), ("&#128269;", "Transparency"),
             ("&#128274;", "Privacy protection"), ("&#9989;", "Accountability")]
    out = "".join('<div class="pchip" style="animation-delay:%.2fs"><span>%s</span>%s</div>'
                  % (.6 + .4 * k, ico, t) for k, (ico, t) in enumerate(items))
    return ('<aside class="rise viz">' + out
            + vcap("Four principles for using AI responsibly.",
                   "أربع مبادئ عشان نستخدم الذكاء الاصطناعي بمسؤولية.")
            + '</aside>')


def v_unit():
    steps = ["1-1", "1-2", "1-3", "1-4"]
    out = "".join('<div class="ustep" style="animation-delay:%.2fs"><b>&#10003;</b>%s</div>'
                  % (.5 + .4 * k, t) for k, t in enumerate(steps))
    return ('<aside class="rise viz unit">'
            '<svg viewBox="0 0 200 200" role="img" aria-label="Unit 1: four of four lessons complete">'
            '<circle cx="100" cy="100" r="80" class="track"/>'
            '<circle cx="100" cy="100" r="80" class="ring done"/>'
            '<text x="100" y="98" class="big">4/4</text><text x="100" y="126" class="small">lessons</text>'
            '</svg><div class="usteps">' + out + '</div>'
            + vcap("Unit 1 complete. Next: the Chapter 1 exam.",
                   "خلّصنا الوحدة الأولى. اللي جاي: امتحان الفصل الأول.")
            + '</aside>')


# heading text (unique to one slide) -> its drawing
VIZ = {
    "Can we trust it?": v_flow_trust,
    "AI helps decide things about people": v_decides,
    "What ethical issues arise as AI spreads": v_issues,
    "Before you read on": v_scan,
    "Bias in, bias out": v_bias_flow,
    "A proxy variable": v_proxy,
    "A hiring AI was found to rate": v_timer,
    "Face recognition in public spaces can improve": v_timer,
    "If no one can explain why an AI rejected": v_timer,
    "Seeing why it decided": v_xai,
    "Accurate is not enough": v_principles,
    "Information technology and society, in four lessons": v_unit,
}
VIZ_USED = []


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
    h2("Can we trust it?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("AI now helps make real decisions about people. Today: when is that fair, and who answers when it goes wrong?",
        "max-width:56ch;margin-top:1rem"),
    ar("الـ AI بقى بيساعد ياخد قرارات حقيقية عن ناس. النهارده هنشوف: إمتى ده يبقى عادل، ولما يغلط مين اللي يتحاسب؟")))

# 2 recap — lesson 1-3 ended on a list of cautions; this lesson explains them
A(s("",
    eyebrow("Before we start &#183; Lesson 1-3"),
    h2("Last time ended on a list of cautions"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>What AI is good at</h3><ul>'
    '<li>Finding and classifying patterns in data</li>'
    '<li>Recognising and generating images, audio, text</li>'
    '<li>Prediction based on data</li>'
    '</ul></div>'
    '<div class="pane b"><h3>What needs caution</h3><ul>'
    '<li>Ethical judgments &#8212; discrimination, prejudice</li>'
    '<li>Personal information and privacy</li>'
    '<li>Biased training data</li>'
    '<li>The black-box problem, and who is responsible</li>'
    '<li>Copyright, when protected works are training data</li>'
    '</ul></div>'
    '</div>',
    sub("That right-hand column is today&#8217;s whole lesson. We open each caution up.",
        "max-width:60ch;margin-top:.9rem"),
    ar("المرة اللي فاتت خلصنا بقايمة تحذيرات. العمود اليمين ده هو درس النهارده كله — هنفتح كل تحذير ونفهمه.")))

# 3 hook
A(s("",
    eyebrow("This is already happening"),
    h2("AI helps decide things about people", "max-width:22ch"),
    '<div class="rise fields">'
    '<span class="chip">who gets a job interview</span>'
    '<span class="chip">who a camera says you are</span>'
    '<span class="chip">how your personal data is used</span>'
    '</div>',
    sub("If the data it learned from was biased, it can be <b>unfair</b>. And it can be hard to know <b>why</b> it decided at all.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> would you let an AI decide who gets the job? Remember your answer &#8212; we ask again at the end.</p></div>',
    ar("الذكاء الاصطناعي النهارده بيساعد في قرارات بتأثر على الناس، زي فرز طلبات التوظيف، والتعرف على الأشخاص، وتحليل البيانات الشخصية. ولو البيانات أو طريقة تصميم النظام أو استخدامه فيها انحياز، ممكن يطلّع نتايج مش عادلة — وساعات يبقى صعب نفسّر هو وصل للقرار ده على أساس إيه.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("What ethical issues arise as AI spreads &#8212; and what principles should guide how we use it?",
       "max-width:26ch"),
    ar("السؤال الرئيسي: إيه القضايا الأخلاقية اللي بتظهر مع انتشار الذكاء الاصطناعي، وإيه المبادئ اللي المفروض توجّه استخدامنا ليه؟")))

# 4b the four principles up front: the map for the lecture. Part 5 comes
#    back to them once every issue has been seen.
A(s("",
    eyebrow("Today&#8217;s map &#183; four principles"),
    h2("Four principles guide how we use AI", "max-width:26ch"),
    sub("Each part of today meets one ethical issue &#8212; and the principle that answers it.",
        "max-width:56ch;margin-top:.6rem"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#9878;</div><div class="role">Part 1 &#183; Bias</div>'
    '<h3>Fairness</h3><p>Is anyone unjustly discriminated against?</p></div>'
    '<div class="card"><div class="ico">&#128274;</div><div class="role">Part 2 &#183; Privacy</div>'
    '<h3>Privacy protection</h3><p>Is personal information handled appropriately?</p></div>'
    '<div class="card"><div class="ico">&#128269;</div><div class="role">Part 3 &#183; XAI</div>'
    '<h3>Transparency</h3><p>Can we see how it made its decision?</p></div>'
    '<div class="card"><div class="ico">&#9989;</div><div class="role">Part 4 &#183; Responsibility</div>'
    '<h3>Accountability</h3><p>Who is answerable for its decisions?</p></div>'
    '</div>',
    sub("Keep these four in mind. At the end, you will match situations to them.", "margin-top:.6rem;color:var(--soft)"),
    ar("قبل ما نبدأ، دي الخريطة بتاعة المحاضرة: أربع مبادئ بتوجّه استخدامنا للذكاء الاصطناعي. كل جزء هنشوف فيه مشكلة أخلاقية والمبدأ اللي بيحلها: التحيز ← العدالة، الخصوصية ← حماية الخصوصية، الذكاء الاصطناعي القابل للتفسير ← الشفافية، المسؤولية ← المساءلة. خلّوهم في دماغكم، وفي الآخر هنرجعلهم كلهم مع بعض.")))

# 5 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("A face-recognition AI is more likely to <b>misidentify</b> people from some ethnic groups than others. With your partner, predict: <b>who could be harmed</b> by this, and how? Give a reason.",
        "max-width:56ch;margin-top:1rem"),
    '<div class="rise shots" style="max-width:420px">'
    + shot("Face_detection.jpg", "Face recognition at work",
           "Each box is a face the system found. Would it find every face equally well?",
           "كل مربع وش النظام لقاه. هل هيلاقي كل الوشوش بنفس الدقة؟")
    + '</div>',
    CREDIT,
    sub("Keep your answer. It is exactly what Part 1 explains.", "margin-top:.6rem;color:var(--soft)"),
    ar("مع زميلك، بصّوا على الموقف ده: ذكاء اصطناعي للتعرف على الوجه بيغلط في التعرف على ناس من مجموعات عرقية معينة أكتر من غيرهم. قبل ما تكمّلوا، توقّعوا: مين ممكن يتضرر من ده، وإزاي؟ وقولوا سبب.")))

A(video("TWWsW1w-BVo", "Gender Shades", "MIT Media Lab",
          "Watch &#183; the real study", "Was your prediction right?",
          "which faces did the systems get wrong most often &#8212; and why would the training data cause that?",
          "بعد التوقع ده، نشوف الدليل: باحثة في MIT جرّبت أنظمة التعرف على الوجه. وانتو بتتفرجوا: أنهي وشوش الأنظمة غلطت فيها أكتر؟ وليه بيانات التدريب ممكن تكون السبب؟"))

# ---------------- part 1: algorithmic bias ----------------

A(s("",
    eyebrow("Part 1 &#183; Algorithmic bias &#8594; Fairness"),
    h2("Bias in, bias out", "max-width:24ch"),
    '<div class="rise statement"><em>Algorithmic bias</em> &#8212; bias in AI judgments caused by bias in the training data.</div>',
    '<table class="rise">'
    '<tr><th>Example from the book</th><th>Who is treated unfairly</th></tr>'
    '<tr><td>A hiring AI</td><td>Unfairly evaluates applicants of a particular gender</td></tr>'
    '<tr><td>A face-recognition AI</td><td>Is more likely to misidentify particular ethnic groups</td></tr>'
    '</table>',
    ar("التحيز في أنظمة الذكاء الاصطناعي يعني انحراف أو نمط ممكن يوصّل لنتايج مش عادلة أو بتضر. وممكن ييجي من البيانات، أو من تصميم النظام، أو من طريقة استخدامه والظروف البشرية والاجتماعية حواليه. مثال: نظام توظيف بيفضّل فئة على غيرها من غير وجه حق، أو نظام تعرف على الوجه دقته بتقل مع فئة معينة.")))

A(s("",
    eyebrow("1 &#183; See it happen"),
    h2("It copies the data it was given"),
    fig(BIAS),
    ar("الـ AI محدش قاله يبقى ظالم. هو بيتعلم النمط اللي في الداتا — ولو مجموعة واحدة ماليا الداتا، هيبقى دقيق معاها ويغلط مع الباقي.")))

A(s("",
    eyebrow("1 &#183; Where it comes from"),
    h2("Two places bias gets in", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>In the training data</h3><ul>'
    '<li><b>Insufficient data</b> on certain attributes</li>'
    '<li><b>Past discriminatory tendencies</b> reflected in the data</li>'
    '</ul></div>'
    '<div class="pane b"><h3>In the way the system is built</h3><ul>'
    '<li>An <b>inappropriate choice of variables</b></li>'
    '<li>A <b>proxy variable</b> &#8212; one that indirectly stands in for a protected attribute</li>'
    '<li>The <b>design of the model</b> itself</li>'
    '</ul></div>'
    '</div>',
    ar("الأسباب الرئيسية للتحيز: أولًا بيانات التدريب نفسها تبقى متحيزة — بيانات مش كفاية عن سمات معينة، أو بيانات شايلة نزعات تمييزية قديمة. وتانيًا طريقة بناء النظام: متغيرات مش مناسبة، أو متغير بديل بيمثّل سمة محمية بشكل غير مباشر، أو تصميم النموذج نفسه.")))

A(video("x2mRoFNm22g", "AI: Training Data &amp; Bias", "Code.org",
          "Watch &#183; how data becomes bias", "Where does the bias come from?",
          "listen for the cause from the last slide &#8212; what is wrong with the data the AI learned from?",
          "الفيديو ده بيشرح إزاي بيانات التدريب بتأثر على قرارات الـ AI. وانتو بتتفرجوا: دوّروا على السبب اللي في السلايد اللي فاتت — إيه الغلط في البيانات اللي اتعلم منها؟"))

A(s("",
    eyebrow("1 &#183; The one students skip"),
    h2("A proxy variable", "max-width:24ch"),
    sub("A <b>protected attribute</b> is something a decision must not discriminate on &#8212; gender, or ethnic group. Removing it from the data is <b>not enough</b>.",
        "max-width:58ch;margin-top:.6rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--teal-pale);border-radius:12px;max-width:64ch">'
    # A real, reported case rather than an invented one: a teacher could not
    # make the abstract version land. Slide only -- the booklet had already
    # been printed and handed out when this was changed.
    '<p style="font-size:clamp(13px,1.45vw,19px)"><b>A real case.</b> Amazon built an AI to sort job CVs. It learned from ten years of past CVs &#8212; mostly from men. Nobody told it anyone&#8217;s gender. But CVs containing the word <b>&#8220;women&#8217;s&#8221;</b> &#8212; as in <i>&#8220;captain of the women&#8217;s chess club&#8221;</i> &#8212; had rarely been accepted before, so it learned to <b>mark them down</b>. The word was standing in for gender. Amazon scrapped the tool. <span style="color:var(--soft)">(Reported by Reuters, 2018 &#8212; not from the textbook.)</span></p>'
    '</div>',
    ar("السمة المحمية حاجة ممنوع القرار يميّز بيها، زي النوع. أمازون عملت AI يفرز الـ CVs، واتعلم من CVs قديمة أغلبها لرجالة. محدش قاله المتقدم ولد ولا بنت — بس أي CV فيه كلمة women's (زي «كابتن فريق الشطرنج للبنات») كان نادر يتقبل، فبقى ينزّل تقييمه. الكلمة فضحت إنها بنت: ده «المتغير البديل».")))

A(s("dark",
    eyebrow("Think it through"),
    h2("A hiring AI was found to rate applicants of one gender lower. What is the most likely cause &#8212; and one measure to fix it?",
       "max-width:27ch"),
    ar("AI توظيف طلع بيقيّم نوع معين أقل. إيه السبب الأرجح؟ واقترح إجراء واحد يصلّح ده.")))

# ---------------- part 2: privacy ----------------

A(s("",
    eyebrow("Part 2 &#183; Privacy &#8594; Privacy protection"),
    h2("AI created new privacy problems", "max-width:24ch"),
    '<div class="rise statement"><em>Privacy</em> &#8212; the appropriate handling and protection of personal data.</div>',
    '<div class="rise shots two">'
    + shot("CCTV_camera_Round_Church_Street_Cambridge.jpg", "1 &#183; Surveillance",
           "Face-recognition cameras in public spaces can <b>identify and track</b> individuals.",
           "كاميرات التعرف على الوجه في الأماكن العامة تقدر تتعرف على الناس وتتتبعهم.")
    + shot("Datacenter-telecom.jpg", "2 &#183; Mass collection",
           "Large amounts of <b>online behaviour data</b> are collected and analysed.",
           "كميات ضخمة من بيانات سلوكك على الإنترنت بتتجمع وتتحلل.")
    + '</div>',
    CREDIT,
    ar("تطور الذكاء الاصطناعي طلّع قضايا جديدة في الخصوصية:<br>① المراقبة بالتعرف على الوجه: الكاميرات في الأماكن العامة تقدر تتعرف على الناس وتتتبعهم.<br>② الجمع الجماعي للبيانات الشخصية: بيتجمع ويتحلل كميات ضخمة من بيانات سلوكنا على الإنترنت.")))

A(s("dark",
    eyebrow("Think it through"),
    h2("Face recognition in public spaces can improve safety and convenience &#8212; and raise privacy concerns. How should the three be balanced?",
       "max-width:27ch"),
    ar("لما بنستخدم التعرف على الوجه في الأماكن العامة، الأمان والراحة بيتحسنوا، بس في نفس الوقت بتظهر مخاوف على الخصوصية. اشرح إزاي نوازن بين الراحة والأمان وحماية الخصوصية، وقول أنهي مبدأ من مبادئ أخلاقيات الذكاء الاصطناعي أقرب لرأيك.")))

# ---------------- part 3: XAI ----------------

A(s("",
    eyebrow("Part 3 &#183; Explainable AI &#8594; Transparency"),
    h2("Why did it decide that?"),
    fig(XAI),
    ar("لو الـ AI صندوق أسود بيديك النتيجة بس، محدش يقدر يتأكد هي صح ولا عادلة. الـ XAI بيطلّع الأسباب كمان — فبني آدم يقدر يراجعها.")))

A(s("",
    eyebrow("3 &#183; The definition"),
    h2("Seeing why it decided", "max-width:24ch"),
    # the definition is long: the full statement size filled the slide and
    # repeated the heading word for word
    '<div class="rise statement" style="font-size:clamp(20px,3vw,40px)"><em>Explainable AI (XAI)</em> &#8212; technology that makes it possible for humans to understand why an AI made a particular judgment.</div>',
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--teal-pale);border-radius:12px;max-width:64ch">'
    '<p style="font-size:clamp(13px,1.45vw,19px)">When the decision-making process is opaque &#8212; a <b>black box</b> &#8212; it is difficult to verify whether the result is correct. So &#8220;the answer is right, so the process does not matter&#8221; is <b>false</b>.</p>'
    '</div>',
    ar("الذكاء الاصطناعي القابل للتفسير (XAI): أساليب بتساعدنا نفهم إيه العوامل اللي خلّت النظام يوصل للنتيجة أو القرار ده. ولما طريقة الوصول للنتيجة تبقى مش واضحة، بيبقى صعب نقيّمها أو نكتشف فيها غلط أو تحيز. عشان كده جملة «طالما النتيجة صح مفيش مشكلة» غلط — وبتيجي في الامتحان.")))

# ---------------- part 4: responsibility ----------------

A(s("",
    eyebrow("Part 4 &#183; Responsibility &#8594; Accountability"),
    h2("It got it wrong. Who answers?"),
    fig(WHO),
    ar("المسؤولية: إننا نحدد أدوار وواجبات كل طرف ليه علاقة بتطوير النظام وتشغيله واستخدامه — المطوّر، والجهة اللي بتشغّله، والمستخدم. ومفيش توزيع واحد للمسؤولية ينفع في كل الحالات؛ ده بيختلف حسب النظام وطريقة استخدامه والقواعد الموجودة.")))

A(s("",
    eyebrow("4 &#183; Two words that sound the same"),
    h2("Responsibility is not accountability", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Responsibility</h3><ul>'
    '<li>The <b>roles and duties</b> of each party</li>'
    '<li>Developer, operator, user &#8212; who does what</li>'
    '<li>Who answers when an AI judgment is wrong</li>'
    '</ul></div>'
    '<div class="pane b"><h3>Accountability</h3><ul>'
    '<li><b>Being answerable</b> for the AI&#8217;s decisions</li>'
    '<li>Knowing who can be <b>held to account</b>, according to their role</li>'
    '<li>One of the four principles of AI ethics</li>'
    '</ul></div>'
    '</div>',
    ar("المسؤولية: إننا نحدد أدوار وواجبات كل طرف في تطوير النظام وتشغيله واستخدامه.<br>المساءلة: إننا نحدد مين الجهات المسؤولة عن النظام وقراراته وتأثيره، ونقدر نحاسبها حسب دورها.<br>خد بالك: المساءلة مش إنك تشرح القرار — دي وظيفة الذكاء الاصطناعي القابل للتفسير (XAI) — المساءلة إننا نعرف مين اللي يتحاسب على النتيجة.")))


A(s("dark",
    eyebrow("Pause & think"),
    h2("If no one can explain why an AI rejected someone&#8217;s job application, is that fair? Which principle is missing?",
       "max-width:27ch"),
    ar("لو محدش قدر يشرح الذكاء الاصطناعي رفض طلب توظيف حد ليه، يبقى ده عادل؟ وأنهي مبدأ من مبادئ أخلاقيات الذكاء الاصطناعي ناقص هنا؟")))

# ---------------- part 5: the four principles ----------------

A(s("",
    eyebrow("Part 5 &#183; Back to the four principles"),
    h2("Four principles for using AI appropriately", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#9878;</div><div class="role">Principle 1</div>'
    '<h3>Fairness</h3><p>Not unjustly discriminating against any particular person or group</p></div>'
    '<div class="card"><div class="ico">&#128269;</div><div class="role">Principle 2</div>'
    '<h3>Transparency</h3><p>Showing the AI&#8217;s decision-making process and inner workings clearly</p></div>'
    '<div class="card"><div class="ico">&#128274;</div><div class="role">Principle 3</div>'
    '<h3>Privacy protection</h3><p>Handling personal information appropriately and protecting privacy</p></div>'
    '<div class="card"><div class="ico">&#9989;</div><div class="role">Principle 4</div>'
    '<h3>Accountability</h3><p>Being answerable for the AI&#8217;s decisions</p></div>'
    '</div>',
    ar("العدالة: إننا منميّزش ظلم ضد أي شخص أو مجموعة.<br>الشفافية: نوفّر معلومات واضحة ومناسبة عن النظام، وإزاي بيتستخدم، وإزاي بياخد القرار، وحدوده إيه.<br>حماية الخصوصية: نتعامل مع المعلومات الشخصية بشكل مناسب ونحمي خصوصية الناس.<br>المساءلة: نحدد مين الجهات المسؤولة عن النظام وقراراته وتأثيره، ونقدر نحاسبها حسب دورها.")))

A(s("",
    eyebrow("5 &#183; Your turn"),
    h2("Which principle is it?"),
    '<table class="rise">'
    '<tr><th>Situation</th><th>Principle</th></tr>'
    '<tr><td>A hiring AI evaluates fairly regardless of gender</td><td class="reveal"><span>Fairness</span></td></tr>'
    '<tr><td>The AI&#8217;s decision-making process is disclosed to users in an easy-to-understand way</td><td class="reveal"><span>Transparency</span></td></tr>'
    '<tr><td>Collected personal data is not used for other purposes than originally intended</td><td class="reveal"><span>Privacy protection</span></td></tr>'
    '<tr><td>Someone is answerable when an AI&#8217;s diagnostic result turns out to be wrong</td><td class="reveal"><span>Accountability</span></td></tr>'
    '</table>',
    sub("Answer first, then tap a blurred cell to reveal it. These four are the book&#8217;s own exercise.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("جاوبوا الأول، وبعدين دوسوا على الخانة المتغبّشة تظهر الإجابة. الأربع مواقف دول هما تمرين الكتاب نفسه، وبييجوا كسؤال توصيل.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?", "max-width:26ch"),
    sub("All three sound right. Vote with your hands, then tap each one.", "max-width:60ch;margin-top:.4rem;color:var(--soft)"),
    '<ul class="rise check">'
    '<li class="reveal rv">&#8220;Even if an AI&#8217;s process is opaque, there is no problem as long as the result is correct.&#8221; <span class="ans">&#8212; <b>false</b>: an opaque result cannot be verified.</span></li>'
    '<li class="reveal rv">&#8220;Who is responsible when an AI is wrong has already been clearly determined.&#8221; <span class="ans">&#8212; <b>false</b>: views differ and no clear standard exists yet.</span></li>'
    '<li class="reveal rv">&#8220;Algorithmic bias is caused by the AI&#8217;s processing speed.&#8221; <span class="ans">&#8212; <b>false</b>: it comes from bias in the training data.</span></li>'
    '</ul>',
    ar("تلات جمل شكلها صح وهي غلط، وبييجوا في الامتحان: «حتى لو طريقة القرار مش واضحة، مفيش مشكلة طالما النتيجة صح» ✗، «مين المسؤول لما الـ AI يغلط متحدد بوضوح» ✗، «التحيز الخوارزمي سببه سرعة معالجة الذكاء الاصطناعي» ✗ — سببه البيانات.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("A company wants to use a hiring AI", "max-width:26ch"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Investigate</b> one documented case of an AI accused of bias. What group did it affect, and what data might have caused it?</li>'
    '<li><b>Consider responsibility</b>: the developer, the company using it, or the operator &#8212; what does each hold?</li>'
    '<li><b>Decide</b> one rule the company must follow before using it. Justify it with the principles.</li>'
    '</ul>',
    sub("Stuck? If the training data reflects past bias, the AI can repeat it &#8212; one fix is to check the data and test the results across different groups.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس — ابحث وبعدين قرّر: دوّر على حالة موثّقة اتّهموا فيها نظام ذكاء اصطناعي إنه طلّع نتايج مش عادلة أو متحيزة. فكّر في المسؤولية: المطوّر، ولا الشركة اللي بتستخدمه، ولا المشغّل؟ وبعدين قرّر قاعدة واحدة لازم الشركة تمشي عليها عشان النظام يبقى أعدل، وبرّرها بمبادئ أخلاقيات الذكاء الاصطناعي.")))

A(s("",
    eyebrow("In a new context"),
    h2("A school wants face recognition at its gate", "max-width:26ch"),
    sub("The cameras would record attendance automatically.", "max-width:54ch;margin-top:.7rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li>Identify <b>one practical benefit</b> for the school.</li>'
    '<li>Identify <b>one privacy concern</b>.</li>'
    '<li>If the camera <b>misidentifies a student</b>, who should be responsible &#8212; the school, or the company that made the AI? Give a reason.</li>'
    '</ul>',
    ar("مدرسة عايزة تستخدم كاميرات تعرف على الوجه على البوابة عشان تسجّل الحضور أوتوماتيك. حدد فايدة واحدة للمدرسة، ومشكلة واحدة ليها علاقة بالخصوصية. وبعدين: لو الكاميرا غلطت في التعرف على طالب، مين المفروض يبقى المسؤول — المدرسة، ولا الشركة اللي عملت الذكاء الاصطناعي؟ وقول السبب.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 1-4"),
    h2("Accurate is not enough", "max-width:28ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> would you let an AI decide who gets the job <i>now</i> &#8212; and on what condition?</p>'
    '<div class="rise statement">If training data is biased, an AI can reproduce that bias. Using AI responsibly means <em>checking for bias</em>, being able to <em>explain decisions</em>, and knowing <em>who is accountable</em> &#8212; guided by fairness, transparency, privacy protection and accountability.</div>',
    ar("خلّي بالك: لو بيانات التدريب متحيزة، الذكاء الاصطناعي ممكن يكرر نفس التحيز. واستخدام الذكاء الاصطناعي بمسؤولية يعني نراجع التحيز، ونقدر نشرح القرارات، ونعرف مين المسؤول — ماشيين بالعدالة والشفافية وحماية الخصوصية والمساءلة.")))

# unit wrap — this lesson closes Unit 1, and the chapter exam covers all four
A(s("",
    eyebrow("Unit 1 &#183; complete"),
    h2("Information technology and society, in four lessons", "max-width:28ch"),
    '<div class="rise timeline">'
    '<div class="tl"><h3>1-1 &#183; How IT developed</h3><p>Five stages, Moore&#8217;s Law, social changes, emerging technologies</p></div>'
    '<div class="tl"><h3>1-2 &#183; How AI works</h3><p>AI &#8594; machine learning &#8594; deep learning &#8594; generative AI, nested; neural networks and their hidden layers</p></div>'
    '<div class="tl"><h3>1-3 &#183; AI in daily life and industry</h3><p>Where it is used, what it is good at, what needs caution</p></div>'
    '<div class="tl"><h3>1-4 &#183; Ethical issues with AI</h3><p>Bias, privacy, XAI and responsibility, the four principles</p></div>'
    '</div>',
    ar("خلصنا الوحدة الأولى: 1-1 تطور تكنولوجيا المعلومات، 1-2 إزاي الـ AI بيشتغل، 1-3 الـ AI في الحياة والصناعة، 1-4 القضايا الأخلاقية. امتحان الشابتر الأول على الأربعة.")))

# QR — must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 4"),
    # Covered until the teacher reveals it (press E, or the dashboard switch),
    # so the code is not handed to a class in advance.
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 4 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers this lesson and reviews the rest of Unit 1. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس ده ومراجعة للوحدة الأولى. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))


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
.viz .eye{fill:var(--white)} .viz .mouth{stroke:var(--white); stroke-width:1.8; fill:none; stroke-linecap:round}
.viz .vk{stroke:var(--teal); stroke-width:3.5; fill:none; stroke-linecap:round; stroke-linejoin:round}
.viz .vx{stroke:var(--wrong); stroke-width:3.5; fill:none; stroke-linecap:round}
.viz .scan{fill:var(--wrong); opacity:0}
.viz .qmark{font:700 44px Fraunces,serif; fill:var(--gold); text-anchor:middle}
.viz .bar{rx:3}
.viz .glass{fill:var(--white); stroke:var(--teal); stroke-width:2}
.viz .blackbox{fill:var(--ink); opacity:0}
.viz .bbq{font:700 40px Fraunces,serif; fill:var(--paper); text-anchor:middle; opacity:0}
.viz .bbl{opacity:0}
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
/* CV card */
.cv{background:var(--white); border:1px solid var(--line); border-radius:14px; padding:1.1rem 1.2rem; font-size:clamp(13px,1.2vw,16px); box-shadow:0 1px 2px rgba(22,35,63,.05)}
.cvh{font:600 1.2em Fraunces,serif; color:var(--ink); margin-bottom:.6rem}
.cvl{display:flex; align-items:center; gap:.6rem; padding:.4rem 0; border-bottom:1px dashed var(--line); color:var(--soft); position:relative}
.cvl span{min-width:6.5em} .cvl i{flex:1; height:8px; border-radius:4px; background:var(--line)}
.cvl.gone span,.cvl.gone i{text-decoration:line-through; opacity:.35}
.cvl.gone em{font-style:normal; font-size:.8em; font-weight:700; color:var(--wrong); border:1.5px solid var(--wrong); border-radius:6px; padding:0 .35rem}
.cvl.hot{color:var(--ink); border-radius:8px; padding:.45rem .5rem; margin:.3rem -.5rem; background:var(--gold-pale)}
.cvl.hot b{color:var(--wrong)}
.score{display:flex; align-items:center; gap:.7rem; margin-top:.8rem; font-weight:600; color:var(--ink)}
.meter{flex:1; height:12px; border-radius:6px; background:var(--line); overflow:hidden}
.meter .fill{height:100%; width:28%; background:var(--wrong); border-radius:6px}
/* rings */
.viz .track{fill:none; stroke:#3A4867; stroke-width:12}
.viz .ring{fill:none; stroke:var(--gold); stroke-width:12; stroke-linecap:round; transform:rotate(-90deg); transform-origin:100px 100px; stroke-dasharray:503; stroke-dashoffset:0}
.viz .big{font:700 46px Fraunces,serif; fill:var(--paper); text-anchor:middle}
.viz .small{font:500 15px Inter,system-ui,sans-serif; fill:#AAB6CC; text-anchor:middle}
.timer,.unit{max-width:320px}
.tps{display:flex; justify-content:center; gap:.5rem; margin-top:.9rem}
.tps span{border:1px solid #3A4867; border-radius:99px; padding:.25rem .8rem; color:var(--paper); font-size:clamp(13px,1.15vw,16px)}
.unit .track{stroke:var(--line)} .unit .big{fill:var(--ink)} .unit .small{fill:var(--soft)} .unit .ring{stroke:var(--teal)}
.usteps{display:flex; justify-content:center; gap:.45rem; margin-top:.8rem}
.ustep{border:1px solid var(--line); background:var(--white); border-radius:99px; padding:.2rem .7rem; font-weight:600; color:var(--ink); font-size:clamp(13px,1.1vw,15px)}
.ustep b{color:var(--teal); margin-right:.25rem}

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
.slide.on .viz .scan{animation:vScan 1.6s .3s ease-in-out both}
.slide.on .viz .vk,.slide.on .viz .vx{animation:vPop .45s cubic-bezier(.2,.8,.3,1.2) both; transform-box:fill-box; transform-origin:center}
.slide.on .viz .grow{animation:vGrowY .6s cubic-bezier(.2,.8,.3,1) both; transform-box:fill-box; transform-origin:bottom}
.slide.on .viz svg[aria-label^="A black box"] .grow{animation-name:vGrowX; transform-origin:left}
.slide.on .viz .drow,.slide.on .viz .tile,.slide.on .viz .pchip,.slide.on .viz .ustep,.slide.on .viz .tps span{animation:vIn .45s both}
.slide.on .viz .blackbox{animation:vHideBox 2s .2s ease-in both; opacity:0}
.slide.on .viz .bbq{animation:vHideBox 2s .2s ease-in both; opacity:0}
.slide.on .viz .bbl{animation:vShowThen 2s .2s both; opacity:0}
.slide.on .viz .xail{animation:vLateIn 2.2s .2s both}
.slide.on .viz .cvl.gone span,.slide.on .viz .cvl.gone i{animation:vStrike .5s .5s both}
.slide.on .viz .cvl.gone em{animation:vPop .45s .9s both; display:inline-block}
.slide.on .viz .cvl.hot{animation:vGlow 1.2s 1.4s 2 ease-in-out both}
.slide.on .viz .meter .fill{animation:vDrop 1s 2.2s cubic-bezier(.3,.7,.3,1) both}
.slide.on .viz .ring{animation:vRing 60s .4s linear both}
.slide.on .unit .ring{animation:vRingFill 1.6s .3s cubic-bezier(.3,.7,.3,1) both}

/* the two videos: bigger on a wide screen, as long as the slide still fits */
@media(min-width:1001px){.slide .vid{width:min(100%, 960px, calc((100vh - 380px) * 16 / 9))}}
@media print{.slide.on .viz *{animation:none!important} .viz .blackbox,.viz .bbq,.viz .bbl{opacity:0!important}}

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
BASE = "scripts/lecture4_slides_base.html"
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

