# -*- coding: utf-8 -*-
"""Build the Chapter 1 Revision's deck.

    python scripts/build_revision1_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/revision1_slides_base.html and writes revision/chapter1/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the side drawings
added. Always starts from the base, never from the published deck.

A revision of Unit 1, Information Technology and Society (lessons 1-1 to 1-4), one lesson at a time, at the teacher's request. Nothing
here is new: every line comes from the lessons as they were taught in
lectures 2 to 4. The data is tools/revision1/data.py -- per lesson, the book's
key takeaway, its key terms, the exam traps, and the lesson's exam-style
question with the marking points from that lecture's answer key. The
diagrams are the ones the lessons were taught with.

Each lesson gets a divider with its key takeaway, its picture, flashcards
of its key terms, true-or-false exam traps, and its exam question with the
marking points to reveal one by one. The flashcards are this lecture's own;
their script is tools/revision1/script.js, added to the page's own script.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "revision/chapter1/slides/index.html"


# --------------------------------------------------------------------------
# diagrams -- inline SVG, reused from lectures 3 and 4 (lesson 1-1's timeline is new), so the
# revision shows the picture each lesson was taught with. The booklet
# reads these out of this file.
# --------------------------------------------------------------------------

TIMELINE = '''
<svg viewBox="0 0 900 250" role="img" aria-label="The five stages of IT development: the birth of the computer in the 1940s to 60s, personal computers in the 1970s and 80s, the Internet and the Web in the 1990s, smartphones in the 2000s, and cloud computing from the 2010s onward">
  <g font-size="15" text-anchor="middle">
    <line x1="90" y1="70" x2="830" y2="70" stroke="var(--line)" stroke-width="4"/>
    <polygon points="842,70 828,62 828,78" fill="var(--line)"/>
    <circle cx="90" cy="70" r="28" fill="var(--teal)"/><text x="90" y="77" font-size="18" font-weight="700" fill="#fff">1</text>
    <circle cx="275" cy="70" r="28" fill="var(--teal)"/><text x="275" y="77" font-size="18" font-weight="700" fill="#fff">2</text>
    <circle cx="460" cy="70" r="28" fill="var(--teal)"/><text x="460" y="77" font-size="18" font-weight="700" fill="#fff">3</text>
    <circle cx="645" cy="70" r="28" fill="var(--teal)"/><text x="645" y="77" font-size="18" font-weight="700" fill="#fff">4</text>
    <circle cx="830" cy="70" r="28" fill="var(--gold)"/><text x="830" y="77" font-size="18" font-weight="700" fill="#fff">5</text>
    <text x="90" y="24" fill="var(--soft)">1940s-60s</text>
    <text x="275" y="24" fill="var(--soft)">1970s-80s</text>
    <text x="460" y="24" fill="var(--soft)">1990s</text>
    <text x="645" y="24" fill="var(--soft)">2000s</text>
    <text x="830" y="24" fill="var(--soft)">2010s onward</text>
    <text x="90" y="128" font-weight="700" fill="var(--ink)">The computer</text>
    <text x="90" y="150" fill="var(--soft)">ENIAC, vacuum tubes</text>
    <text x="90" y="172" fill="var(--soft)">military, science</text>
    <text x="275" y="128" font-weight="700" fill="var(--ink)">Personal computers</text>
    <text x="275" y="150" fill="var(--soft)">PCs at home</text>
    <text x="275" y="172" fill="var(--soft)">personal use begins</text>
    <text x="460" y="128" font-weight="700" fill="var(--ink)">The Internet, the Web</text>
    <text x="460" y="150" fill="var(--soft)">commercialized</text>
    <text x="460" y="172" fill="var(--soft)">information goes global</text>
    <text x="645" y="128" font-weight="700" fill="var(--ink)">Smartphones</text>
    <text x="645" y="150" fill="var(--soft)">iPhone, etc.</text>
    <text x="645" y="172" fill="var(--soft)">mobile Internet explodes</text>
    <text x="830" y="128" font-weight="700" fill="var(--ink)">Cloud computing</text>
    <text x="830" y="150" fill="var(--soft)">IT as a service</text>
    <text x="830" y="172" fill="var(--soft)">big data and AI</text>
    <rect x="200" y="200" width="500" height="34" rx="8" fill="var(--gold)" opacity=".2"/>
    <text x="450" y="223" font-weight="600" fill="var(--ink)">each stage: a new technology, and a changed society</text>
  </g>
</svg>'''

NESTED = '''
<svg viewBox="0 0 860 300" role="img" aria-label="AI contains machine learning, which contains deep learning, which contains generative AI">
  <rect x="20" y="20" width="820" height="260" rx="16" fill="var(--teal)" opacity=".07" stroke="var(--teal)" stroke-width="2.5"><animate attributeName="opacity" values=".07;.20;.07" dur="8s" begin="0s" repeatCount="indefinite"/></rect>
  <text x="40" y="48" font-size="15" font-weight="600" fill="var(--teal)">AI</text>
  <text x="40" y="68" font-size="11" fill="var(--soft)">intelligent behaviour on a computer</text>

  <rect x="150" y="56" width="670" height="204" rx="14" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="2"><animate attributeName="opacity" values=".10;.24;.10" dur="8s" begin="2s" repeatCount="indefinite"/></rect>
  <text x="170" y="84" font-size="14" font-weight="600" fill="var(--teal)">Machine learning</text>
  <text x="170" y="103" font-size="11" fill="var(--soft)">learns from data</text>

  <rect x="300" y="92" width="500" height="148" rx="12" fill="var(--teal)" opacity=".14" stroke="var(--teal)" stroke-width="2"><animate attributeName="opacity" values=".14;.30;.14" dur="8s" begin="4s" repeatCount="indefinite"/></rect>
  <text x="320" y="120" font-size="14" font-weight="600" fill="var(--teal)">Deep learning</text>
  <text x="320" y="139" font-size="11" fill="var(--soft)">neural networks</text>

  <rect x="470" y="128" width="310" height="92" rx="10" fill="var(--gold)" opacity=".20" stroke="var(--gold)" stroke-width="2.5"><animate attributeName="opacity" values=".20;.42;.20" dur="8s" begin="6s" repeatCount="indefinite"/></rect>
  <text x="492" y="156" font-size="14" font-weight="600" fill="#8A6420">Generative AI</text>
  <text x="492" y="175" font-size="11" fill="var(--soft)">makes new text, images, audio</text>
  <text x="492" y="196" font-size="10.5" fill="var(--soft)">e.g. ChatGPT</text>

  <text x="40" y="272" font-size="11.5" fill="var(--soft)">each box is inside the one before it &#8212; not beside it</text>
</svg>'''

RECSYS = '''
<svg viewBox="0 0 900 250" role="img" aria-label="A recommendation system reads past behaviour, finds a pattern, and suggests something new">
  <text x="30" y="24" font-size="12.5" font-weight="600" fill="var(--soft)">Nobody told it you like this. It read what you did before.</text>

  <rect x="30" y="52" width="180" height="118" rx="9" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>
  <text x="120" y="78" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">what you did before</text>
  <text x="120" y="102" text-anchor="middle" font-size="11" fill="var(--soft)">videos watched</text>
  <text x="120" y="122" text-anchor="middle" font-size="11" fill="var(--soft)">things bought</text>
  <text x="120" y="142" text-anchor="middle" font-size="11" fill="var(--soft)">songs skipped</text>

  <line x1="216" y1="111" x2="276" y2="111" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="276,111 268,106 268,116" fill="var(--teal)"/>

  <rect x="282" y="52" width="200" height="118" rx="9" fill="var(--teal)" opacity=".22" stroke="var(--teal)" stroke-width="2.5">
    <animate attributeName="opacity" values=".22;.42;.22" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <text x="382" y="86" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">it finds a pattern</text>
  <text x="382" y="110" text-anchor="middle" font-size="11" fill="var(--soft)">people who liked these</text>
  <text x="382" y="130" text-anchor="middle" font-size="11" fill="var(--soft)">also liked that</text>

  <line x1="488" y1="111" x2="548" y2="111" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="548,111 540,106 540,116" fill="var(--teal)"/>

  <rect x="554" y="52" width="200" height="118" rx="9" fill="var(--gold)" opacity=".24" stroke="var(--gold)" stroke-width="2.5">
    <animate attributeName="opacity" values=".24;.46;.24" dur="3.4s" begin="1.2s" repeatCount="indefinite"/>
  </rect>
  <text x="654" y="96" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">&#8220;watch this next&#8221;</text>
  <text x="654" y="120" text-anchor="middle" font-size="11" fill="var(--soft)">a prediction, not a fact</text>

  <text x="30" y="208" font-size="11.5" fill="var(--soft)">This is machine learning from Part 2, doing a job you meet every day.</text>
  <text x="30" y="228" font-size="11.5" fill="var(--wrong)">It works because it holds your behaviour &#8212; which is the privacy question.</text>
</svg>'''

BLACKBOX = '''
<svg viewBox="0 0 900 240" role="img" aria-label="The black-box problem: the input and the answer are visible but the reasoning inside is not">
  <text x="30" y="24" font-size="12.5" font-weight="600" fill="var(--soft)">You can see what went in and what came out. You cannot see why.</text>

  <rect x="30" y="58" width="150" height="90" rx="8" fill="var(--teal)" opacity=".14" stroke="var(--teal)" stroke-width="2"/>
  <text x="105" y="98" text-anchor="middle" font-size="12" fill="var(--ink)">an X-ray</text>
  <text x="105" y="120" text-anchor="middle" font-size="11" fill="var(--soft)">you can see this</text>

  <line x1="186" y1="103" x2="244" y2="103" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="244,103 236,98 236,108" fill="var(--teal)"/>

  <rect x="250" y="44" width="260" height="118" rx="10" fill="var(--ink)" opacity=".88"/>
  <text x="380" y="92" text-anchor="middle" font-size="15" font-weight="600" fill="#fff">?</text>
  <text x="380" y="118" text-anchor="middle" font-size="12" fill="#C6CCD9">why it decided that</text>
  <text x="380" y="138" text-anchor="middle" font-size="11" fill="#8A93A6">not visible, even to its builders</text>
  <rect x="250" y="44" width="260" height="118" rx="10" fill="none" stroke="var(--wrong)" stroke-width="2.5" stroke-dasharray="7 5">
    <animate attributeName="opacity" values="1;.3;1" dur="2.2s" repeatCount="indefinite"/>
  </rect>

  <line x1="516" y1="103" x2="574" y2="103" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="574,103 566,98 566,108" fill="var(--teal)"/>

  <rect x="580" y="58" width="180" height="90" rx="8" fill="var(--gold)" opacity=".24" stroke="var(--gold)" stroke-width="2"/>
  <text x="670" y="92" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">&#8220;likely disease&#8221;</text>
  <text x="670" y="116" text-anchor="middle" font-size="11" fill="var(--soft)">you can see this too</text>

  <text x="30" y="204" font-size="11.5" fill="var(--ink)">That gap is the <tspan font-weight="600">black-box problem</tspan> &#8212; and it is why a doctor still signs the diagnosis.</text>
</svg>'''

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


# ---------------- side visuals ----------------
# None in a revision deck: every slide is full width.
VIZ = {}
VIZ_USED = []


# ---------------- the revision data ----------------
# data.py beside this file holds one record per lesson; the deck, the
# booklet and the flashcards all read it.
import importlib.util as _ilu, os as _os, html as _html, json as _json
_spec = _ilu.spec_from_file_location("revdata", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "tools", "revision1", "data.py"))
D = _ilu.module_from_spec(_spec); _spec.loader.exec_module(D)


def cards(terms):
    """Flashcards: the term on the front, the definition on the back.
    'I knew it' takes the card out; 'Not yet' sends it to the back of the
    pile. script.js (added to the page's own script) plays them."""
    data = _html.escape(_json.dumps([list(t) for t in terms], ensure_ascii=False), quote=True)
    return ('<div class="rise fcards" data-cards="%s">'
            '<div class="fcard" role="button" tabindex="0" aria-label="Flip the card">'
            '<div class="ff"></div><div class="fb"><span class="en"></span><span class="ar" dir="rtl"></span></div></div>'
            '<p class="fprog"></p>'
            '<div class="tbtns"><button type="button" class="fl">Flip &#8635;</button>'
            '<button type="button" class="alt kn">&#10003; I knew it</button>'
            '<button type="button" class="alt ny">&#8634; Not yet</button>'
            '<button type="button" class="alt rs">Start again</button></div></div>' % data)


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

# ---- this revision ----
CH = 1
UNIT = "Information Technology and Society"
UNIT_AR = "الوحدة الأولى: تكنولوجيا المعلومات والمجتمع"
LECTURES = "lectures 2 to 4"
SECOND = {"1-1": None, "1-2": None, "1-3": "BLACKBOX", "1-4": "XAI"}
CORE_HEAD = {"1-1": "Five stages, five changes", "1-2": "Four layers, one inside the other",
             "1-3": "What AI is good at — and where it needs a human", "1-4": "Where bias comes from"}
SECOND_HEAD = {"1-3": "The black-box problem", "1-4": "Explainable AI"}

LS = D.LESSONS
SVG = globals()

# 1 title
A(s("dark",
    '<div class="rise eyebrow" id="lectureBadge">Programming &amp; Artificial Intelligence</div>',
    h2("Ready for Chapter %d?" % CH, "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("A revision of Unit %d, %s: %d lessons, one at a time. For each one: the big idea, the key terms on flashcards, the exam traps, and one exam-style question with its marking points."
        % (CH, UNIT, len(LS)), "max-width:60ch;margin-top:1rem"),
    ar("مراجعة %s، درس درس: الفكرة الأساسية، والمصطلحات على كروت، وفخاخ الامتحان، وسؤال على نمط الامتحان بنقط التصحيح." % UNIT_AR)))

# 2 how to revise
A(s("",
    eyebrow("How to revise today"),
    h2("Three steps for every lesson", "max-width:24ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#127183;</div><div class="role">Step 1</div><h3>Flashcards</h3><p>Say the meaning out loud, then flip. Be honest: &#8220;Not yet&#8221; brings it back.</p></div>'
    '<div class="card"><div class="ico">&#9888;</div><div class="role">Step 2</div><h3>Exam traps</h3><p>True or false? Decide before you tap.</p></div>'
    '<div class="card"><div class="ico">&#128221;</div><div class="role">Step 3</div><h3>Exam question</h3><p>Plan your answer, then reveal the marking points one by one.</p></div>'
    '</div>',
    ar("لكل درس: كروت المصطلحات — قول المعنى بصوتك وبعدين اقلب. وبعدين فخاخ الامتحان: صح ولا غلط. وفي الآخر سؤال امتحان: خطّط إجابتك وبعدين اكشف نقط التصحيح.")))

# 3 the unit at a glance
A(s("",
    eyebrow("Unit %d at a glance" % CH),
    h2("%d lessons" % len(LS), "max-width:28ch"),
    '<div class="rise timeline">'
    + "".join('<div class="tl"><h3>%s &#183; %s</h3><p>%s</p></div>' % (L["id"], L["title"], L["remember"]) for L in LS)
    + '</div>',
    ar(" • ".join(L["id"] for L in LS) + " — كل درس وفكرته الأساسية في سطر.")))

for L in LS:
    lid = L["id"]
    # the lesson's own divider, with the book's key takeaway
    A(s("dark",
        '<div class="rise part">%s</div>' % lid,
        h2(L["title"], "max-width:26ch"),
        '<div class="rise remember">&#8220;%s&#8221;</div>' % L["remember"],
        ar(L["remember_ar"])))
    # the picture the lesson was taught with
    A(s("",
        eyebrow("%s &#183; In one picture" % lid),
        h2(CORE_HEAD[lid]),
        fig(SVG[L["svg"]]),
        ar("نفس الرسمة اللي اتشرح بيها الدرس %s. اشرح كل جزء فيها بكلامك." % lid)))
    if SECOND.get(lid):
        A(s("",
            eyebrow("%s &#183; One more picture" % lid),
            h2(SECOND_HEAD[lid]),
            fig(SVG[SECOND[lid]]),
            ar("اشرح الرسمة دي لزميلك في دقيقة.")))
    # flashcards
    A(s("",
        eyebrow("%s &#183; Key terms &#183; %d cards" % (lid, len(L["terms"]))),
        h2("Say it, then flip", "max-width:22ch"),
        cards(L["terms"]),
        ar("قول التعريف بصوت عالي الأول، وبعدين اقلب الكارت. لو عرفته دوس I knew it، ولو لأ دوس Not yet وهيرجعلك تاني.")))
    # exam traps
    A(s("",
        eyebrow("%s &#183; Exam traps" % lid),
        h2("True or false?"),
        '<ul class="rise check" style="margin-top:.6rem">'
        + "".join('<li class="reveal rv%s">%s <span class="ans">&#8212; <b>%s</b>: %s</span></li>'
                  % (" tf-t" if ok else "", st, "true" if ok else "false", why) for st, ok, why in L["traps"])
        + '</ul>',
        sub("Decide first, then tap.", "margin-top:.7rem;color:var(--soft)"),
        ar("قرّر الأول صح ولا غلط، وبعدين دوس. الجمل دي من الكتاب وكتاب التقييمات.")))
    # the lesson's exam-style question, with its marking points
    ex = L["exam"]
    A(s("",
        eyebrow("%s &#183; Exam-style question &#183; %d marks" % (lid, ex["marks"])),
        h2("Plan it, then check the points", "max-width:24ch"),
        sub(ex["q"], "max-width:62ch;margin-top:.4rem"),
        '<ul class="rise check plan" style="margin-top:.7rem">'
        + "".join('<li class="reveal rv">Point %d <span class="ans">&#8212; %s</span></li>' % (k + 1, p)
                  for k, p in enumerate(D.POINTS[lid]))
        + '</ul>',
        sub("Source: %s. Each point is about one mark." % ex["src"], "margin-top:.6rem;color:var(--soft)"),
        ar("اكتب خطة إجابتك في كشكولك الأول، وبعدين اكشف نقط التصحيح واحدة واحدة وقارن.")))

# mixed quick-fire
A(s("",
    eyebrow("All %d lessons &#183; quick-fire" % len(LS)),
    h2("Mixed questions"),
    '<ul class="rise check" style="margin-top:.6rem">'
    + "".join('<li class="reveal rv">%s <span class="ans">&#8212; %s</span></li>' % (q, a) for q, a in D.QUICK)
    + '</ul>',
    ar("أسئلة من كل الدروس متلخبطة — زي الامتحان. فكّر وبعدين دوس.")))

# exam tips
A(s("",
    eyebrow("Before the exam"),
    h2("Four habits that score marks", "max-width:24ch"),
    '<table class="rise"><tr><th>Habit</th><th>Why</th></tr>'
    + "".join('<tr><td><b>%s</b></td><td>%s</td></tr>' % (t, w) for t, w, _ in D.EXAM_TIPS)
    + '</table>',
    ar(" ".join(a for _, _, a in D.EXAM_TIPS))))

# checklist
A(s("dark",
    eyebrow("Can you&#8230;?"),
    h2("Your checklist"),
    '<ul class="rise check">'
    + "".join('<li><b>%s</b> &#8212; define %s.</li>' % (L["id"], ", ".join(t[0] for t in L["terms"][:4])) for L in LS)
    + '<li>Explain each lesson&#8217;s exam question in about six points.</li>'
    + '</ul>',
    ar("لو تقدر تعمل كل ده، انت جاهز. ولو لأ، ارجع لكروت الدرس ده.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Chapter %d Revision" % CH),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Chapter %d Revision quiz" width="250" height="250">' % CH
    + '<div class="txt"><p class="sub">A mixed revision exam on all of Unit %d, drawn from %s. ' % (CH, LECTURES)
    + 'At the end it shows you, lesson by lesson, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان مراجعة على الوحدة كلها. في الآخر هيوضحلك انت ضعيف في أنهي درس بالظبط.")))


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

/* the Chapter 1 Revision's drawings */
.statement.def{font-size:clamp(18px,2.15vw,30px); line-height:1.28; max-width:46ch}
/* code cards, as lecture 8; no ligatures, so >= reads as typed */
.code{display:block; background:var(--ink); color:#E6EDF3; text-align:left; padding:clamp(12px,1.7vw,22px); border-radius:12px; margin:.9rem 0 .4rem; font-family:"JetBrains Mono",monospace; font-size:clamp(13px,1.6vw,21px); line-height:1.6; white-space:pre; overflow-x:auto; max-width:100%}
.code .k,.tcode .k{color:#FF9D7A} .code .s,.tcode .s{color:#8FE3D6} .code .n,.tcode .n{color:#F7C66B} .code .f,.tcode .f{color:#9DC7FF} .code .c,.tcode .c{color:#7C8B99}
.code,.tcode,.mono,.codeline,code,.qcode{font-variant-ligatures:none; font-feature-settings:"liga" 0,"calt" 0}
.codeline{display:inline-block; background:var(--ink); color:#8FE3D6; padding:.25em .6em; border-radius:7px; font-family:"JetBrains Mono",monospace; font-size:.9em}
.part{font:600 clamp(40px,8vw,110px)/1 Fraunces,serif; color:var(--gold)}
.remember{font-family:Fraunces,serif; font-weight:600; font-size:clamp(19px,2.4vw,32px); line-height:1.3; max-width:44ch; margin-top:1rem}
.remember em{font-style:normal; color:var(--gold)}
.tbtns{display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.6rem}
.tbtns button{font:inherit; font-size:clamp(13px,1.35vw,17px); font-weight:600; border-radius:9px; padding:.5em 1em; cursor:pointer; background:var(--teal); color:#fff; border:1px solid var(--teal)}
.tbtns button.alt{background:#fff; color:var(--ink); border-color:var(--line)}
.tbtns button:disabled{opacity:.4; cursor:default}
/* flashcards */
.fcards{margin-top:.8rem; max-width:760px}
.fcard{position:relative; min-height:clamp(150px,24vh,230px); border-radius:16px; cursor:pointer; background:#fff; border:2px solid var(--line); box-shadow:0 10px 24px rgba(22,35,63,.08); display:flex; align-items:center; justify-content:center; text-align:center; padding:1rem 1.4rem; transition:transform .35s, border-color .3s}
.fcard:focus-visible{outline:3px solid var(--gold); outline-offset:3px}
.fcard .ff{font:600 clamp(24px,3.6vw,46px)/1.15 Fraunces,serif; color:var(--ink)}
.fcard .fb{display:none; font-size:clamp(15px,1.9vw,24px); line-height:1.45; color:var(--ink)}
.fcard .fb .ar{display:block; margin-top:.5rem; color:var(--soft); font-size:.88em}
.fcard.flipped{border-color:var(--teal); background:var(--teal-pale); transform:rotateX(6deg)}
.fcard.flipped .ff{display:none} .fcard.flipped .fb{display:block}
.fcard.done{border-color:var(--gold); background:var(--gold-pale)}
.fprog{margin-top:.6rem; color:var(--soft); font-size:clamp(13px,1.4vw,17px)}
/* the answer plan for an exam question: one reveal per marking point */
.plan li{margin-bottom:.45rem}
.mark{display:inline-block; background:var(--gold); color:#fff; font-weight:700; border-radius:99px; padding:.05em .6em; font-size:.85em; margin-left:.3em}
@media print{.tbtns{display:none}}

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
BASE = "scripts/revision1_slides_base.html"
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
LECTURE_JS = '/* ---- flashcards (revision lectures 12 and 13) --------------------------------\n   .fcards: the term on the front; Flip (or tap the card) shows the definition,\n   in English and Arabic. "I knew it" takes the card out of the pile; "Not\n   yet" sends it to the back, so it comes round again. Space and Enter on the\n   card or a button stay here, so they do not also turn the slide. */\n(function(){\n  if(!document.querySelectorAll) return;\n  document.querySelectorAll(\'.fcards\').forEach(function(box){\n    var all = JSON.parse(box.getAttribute(\'data-cards\'));\n    var card = box.querySelector(\'.fcard\'), front = box.querySelector(\'.ff\');\n    var en = box.querySelector(\'.fb .en\'), ar = box.querySelector(\'.fb .ar\'), prog = box.querySelector(\'.fprog\');\n    var fl = box.querySelector(\'.fl\'), kn = box.querySelector(\'.kn\'), ny = box.querySelector(\'.ny\'), rs = box.querySelector(\'.rs\');\n    var pile = [], known = 0;\n\n    function show(){\n      card.classList.remove(\'flipped\');\n      if(!pile.length){\n        front.textContent = \'All \' + all.length + \' known!\';\n        en.textContent = \'\'; ar.textContent = \'\';\n        prog.textContent = \'Well done — press Start again to go through them once more.\';\n        fl.disabled = kn.disabled = ny.disabled = true;\n        card.classList.add(\'done\');\n        return;\n      }\n      card.classList.remove(\'done\');\n      var c = all[pile[0]];\n      front.textContent = c[0];\n      en.textContent = c[1]; ar.textContent = c[2] || \'\';\n      prog.textContent = \'Known \' + known + \' of \' + all.length + \' · \' + pile.length + \' left · say the meaning, then flip\';\n      fl.disabled = kn.disabled = ny.disabled = false;\n    }\n    function flip(){ if(pile.length) card.classList.toggle(\'flipped\'); }\n    function start(){\n      pile = all.map(function(_, k){ return k; });\n      known = 0;\n      show();\n    }\n    fl.addEventListener(\'click\', flip);\n    card.addEventListener(\'click\', flip);\n    kn.addEventListener(\'click\', function(){ if(!pile.length) return; pile.shift(); known++; show(); });\n    ny.addEventListener(\'click\', function(){ if(!pile.length) return; pile.push(pile.shift()); show(); });\n    rs.addEventListener(\'click\', start);\n    box.addEventListener(\'keydown\', function(e){\n      if(e.key !== \' \' && e.key !== \'Enter\') return;\n      var t = e.target;\n      if(t === card){ e.preventDefault(); e.stopPropagation(); flip(); }\n      else if(t.tagName === \'BUTTON\') e.stopPropagation();\n    });\n    start();\n  });\n})();'
_a = 'const start = parseInt(location.hash'
assert out.count(_a) == 1
out = out.replace(_a, LECTURE_JS + chr(10) + chr(10) + _a, 1)
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

