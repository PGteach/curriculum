# -*- coding: utf-8 -*-
"""Build Lecture 6's deck.

    python scripts/build_lecture6_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/lecture6_slides_base.html and writes lecture6/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the side drawings
added. Always starts from the base, never from the published deck.

Content is Lesson 2-2, Network Security Design, the English textbook
pp. 41-47, and nothing outside the curriculum. Where the Arabic textbook
(pp. 38-43) and the ministry's assessment book go further, the deck follows
them: a firewall can also sit between parts of a network or on a host; a VPN
uses encryption and tunnelling; zero trust checks identity, permissions and
context; and the perimeter is a term the ministry asks for by name.

Everything but the content is lecture 5's builder, unchanged -- this file was
derived from it. The Arabic follows the Arabic textbook's lesson 2-2 point by
point, said in Egyptian Arabic, with the book's own terms kept as they are.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "lecture6/slides/index.html"


# --------------------------------------------------------------------------
# diagrams -- inline SVG, coloured from the page's CSS variables so they follow
# LECTURE_ACCENT. Labels only, never the sentence that explains them; no label
# under 14 units. Fills are #fff, never var(--white): the booklet template
# does not define --white. The booklet reads these out of this file.
# --------------------------------------------------------------------------

DMZ = '''
<svg viewBox="0 0 900 300" role="img" aria-label="DMZ network configuration: the Internet, a firewall, the DMZ with the web and mail servers, a second firewall, then the internal network with the database and confidential data">
  <rect x="10" y="40" width="170" height="200" rx="12" fill="#9C3B2E" opacity=".08" stroke="#9C3B2E" stroke-width="2"/>
  <text x="95" y="72" text-anchor="middle" font-size="17" font-weight="700" fill="var(--ink)">The Internet</text>
  <text x="95" y="96" text-anchor="middle" font-size="14" fill="var(--soft)">external network</text>
  <text x="95" y="150" text-anchor="middle" font-size="16" fill="var(--ink)">users</text>
  <text x="95" y="190" text-anchor="middle" font-size="16" font-weight="600" fill="#9C3B2E">attacker</text>

  <rect x="200" y="30" width="34" height="220" rx="6" fill="var(--gold)"/>
  <text x="217" y="272" text-anchor="middle" font-size="14" font-weight="600" fill="var(--ink)">firewall</text>

  <rect x="256" y="40" width="250" height="200" rx="12" fill="var(--gold)" opacity=".14" stroke="var(--gold)" stroke-width="2"/>
  <text x="381" y="72" text-anchor="middle" font-size="17" font-weight="700" fill="var(--ink)">DMZ</text>
  <text x="381" y="96" text-anchor="middle" font-size="14" fill="var(--soft)">servers exposed to the Internet</text>
  <rect x="286" y="118" width="190" height="42" rx="8" fill="#fff" stroke="var(--line)" stroke-width="1.5"/>
  <text x="381" y="145" text-anchor="middle" font-size="16" fill="var(--ink)">web server</text>
  <rect x="286" y="172" width="190" height="42" rx="8" fill="#fff" stroke="var(--line)" stroke-width="1.5"/>
  <text x="381" y="199" text-anchor="middle" font-size="16" fill="var(--ink)">mail server</text>

  <rect x="528" y="30" width="34" height="220" rx="6" fill="var(--gold)"/>
  <text x="545" y="272" text-anchor="middle" font-size="14" font-weight="600" fill="var(--ink)">firewall</text>

  <rect x="584" y="40" width="306" height="200" rx="12" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="2"/>
  <text x="737" y="72" text-anchor="middle" font-size="17" font-weight="700" fill="var(--ink)">Internal network</text>
  <text x="737" y="96" text-anchor="middle" font-size="14" fill="var(--soft)">the organization</text>
  <rect x="604" y="118" width="128" height="42" rx="8" fill="#fff" stroke="var(--line)" stroke-width="1.5"/>
  <text x="668" y="145" text-anchor="middle" font-size="15" fill="var(--ink)">database</text>
  <rect x="742" y="118" width="128" height="42" rx="8" fill="#fff" stroke="var(--line)" stroke-width="1.5"/>
  <text x="806" y="145" text-anchor="middle" font-size="15" fill="var(--ink)">staff PCs</text>
  <rect x="604" y="172" width="266" height="42" rx="8" fill="#fff" stroke="var(--teal)" stroke-width="1.5"/>
  <text x="737" y="199" text-anchor="middle" font-size="15" font-weight="600" fill="var(--teal)">confidential data</text>
</svg>'''

LAYERS = '''
<svg viewBox="0 0 900 290" role="img" aria-label="Defense in depth: four layers, from network entry to endpoints, each with its own measure">
  <g font-size="16">
    <rect x="10" y="10" width="880" height="62" rx="10" fill="var(--gold)" opacity=".16" stroke="var(--gold)" stroke-width="2"/>
    <text x="30" y="48" font-weight="700" fill="var(--ink)">Layer 1 &#183; Network entry</text>
    <text x="400" y="48" fill="var(--ink)">block unauthorized communication with a <tspan font-weight="700">firewall</tspan></text>
    <rect x="10" y="80" width="880" height="62" rx="10" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="2"/>
    <text x="30" y="118" font-weight="700" fill="var(--ink)">Layer 2 &#183; Communication path</text>
    <text x="400" y="118" fill="var(--ink)">encrypt communication with a <tspan font-weight="700">VPN</tspan></text>
    <rect x="10" y="150" width="880" height="62" rx="10" fill="var(--gold)" opacity=".16" stroke="var(--gold)" stroke-width="2"/>
    <text x="30" y="188" font-weight="700" fill="var(--ink)">Layer 3 &#183; Server placement</text>
    <text x="400" y="188" fill="var(--ink)">separate public-facing servers with a <tspan font-weight="700">DMZ</tspan></text>
    <rect x="10" y="220" width="880" height="62" rx="10" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="2"/>
    <text x="30" y="258" font-weight="700" fill="var(--ink)">Layer 4 &#183; Endpoints</text>
    <text x="400" y="258" fill="var(--ink)"><tspan font-weight="700">antivirus</tspan> software, and keep the OS updated</text>
  </g>
</svg>'''

TRUST = '''
<svg viewBox="0 0 900 270" role="img" aria-label="Traditional security trusts everything inside the perimeter; zero trust verifies every access, inside or outside">
  <rect x="10" y="10" width="430" height="250" rx="12" fill="#fff" stroke="var(--line)" stroke-width="2"/>
  <text x="225" y="42" text-anchor="middle" font-size="18" font-weight="700" fill="var(--ink)">Traditional: protect the perimeter</text>
  <rect x="60" y="66" width="330" height="140" rx="14" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="4"/>
  <text x="225" y="120" text-anchor="middle" font-size="17" font-weight="700" fill="var(--teal)">inside = safe</text>
  <text x="225" y="148" text-anchor="middle" font-size="15" fill="var(--ink)">no checks once you are in</text>
  <text x="225" y="236" text-anchor="middle" font-size="15" font-weight="600" fill="#9C3B2E">outside = dangerous</text>

  <rect x="460" y="10" width="430" height="250" rx="12" fill="#fff" stroke="var(--line)" stroke-width="2"/>
  <text x="675" y="42" text-anchor="middle" font-size="18" font-weight="700" fill="var(--ink)">Zero trust: verify every access</text>
  <g font-size="15" fill="var(--ink)">
    <rect x="490" y="66" width="370" height="40" rx="8" fill="var(--gold)" opacity=".16"/>
    <text x="510" y="92">&#10003; who is it? &#8212; identity</text>
    <rect x="490" y="114" width="370" height="40" rx="8" fill="var(--gold)" opacity=".16"/>
    <text x="510" y="140">&#10003; may they? &#8212; permissions</text>
    <rect x="490" y="162" width="370" height="40" rx="8" fill="var(--gold)" opacity=".16"/>
    <text x="510" y="188">&#10003; does it fit? &#8212; context</text>
  </g>
  <text x="675" y="236" text-anchor="middle" font-size="15" font-weight="600" fill="var(--teal)">every time &#8212; inside or outside</text>
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


def v_walls():
    rows = [("Firewall", "w1"), ("VPN", "w2"), ("DMZ", "w3"), ("Endpoints", "w4")]
    out = "".join('<div class="wall %s" style="animation-delay:%.2fs"><span>%s</span></div>'
                  % (c, .3 + .3 * k, t) for k, (t, c) in enumerate(rows))
    return ('<aside class="rise viz"><div class="walls">' + out
            + '<div class="wcrack">&#9889; one layer breached</div></div>'
            + vcap("One wall falls &#8212; the next still holds.",
                   "حيطة وقعت، واللي بعدها لسه صامدة.")
            + '</aside>')


def v_firewall():
    pk = [("web server", "ok", "allow"), ("database (from outside)", "no", "deny"),
          ("web server", "ok", "allow"), ("unknown port", "no", "deny")]
    out = "".join('<div class="pkt %s" style="animation-delay:%.2fs"><span>&#8594; %s</span><b>%s</b></div>'
                  % (c, .4 + .45 * k, t, v) for k, (t, c, v) in enumerate(pk))
    return ('<aside class="rise viz"><div class="fw">'
            '<div class="fwh">&#129521; Firewall rules</div>' + out + '</div>'
            + vcap("Each request is checked against rules set in advance.",
                   "كل طلب بيتقارن بقواعد محطوطة مسبقًا.")
            + '</aside>')


def v_tunnel():
    return ('<aside class="rise viz">'
            '<svg viewBox="0 0 400 220" role="img" aria-label="A VPN carries locked data through a tunnel across the Internet, from a home to the office">'
            '<rect x="10" y="80" width="76" height="60" rx="10" class="nodebox"/><text x="48" y="116" class="ntext">Home</text>'
            '<rect x="314" y="80" width="76" height="60" rx="10" class="nodebox"/><text x="352" y="116" class="ntext">Office</text>'
            '<text x="200" y="40" class="lbl mid">the Internet &#8212; public Wi-Fi</text>'
            '<path d="M86 96 H314 M86 124 H314" class="tube"/>'
            '<g class="pkg"><rect x="96" y="100" width="34" height="20" rx="4" class="pkgbox"/><text x="113" y="115" class="pkglk">&#128274;</text></g>'
            '<text x="200" y="176" class="lbl mid">encrypted tunnel</text>'
            '<text x="200" y="204" class="eav">&#128066; eavesdropper sees only locked data</text>'
            '</svg>'
            + vcap("Safe from home, even on public Wi-Fi.",
                   "اتصال آمن من البيت، حتى على Wi-Fi عام.")
            + '</aside>')


def v_perimeter():
    return ('<aside class="rise viz"><div class="per">'
            '<div class="perbox"><b>inside = safe?</b><span>&#127970; office network</span></div>'
            '<div class="perout">'
            '<span class="po1">&#9729; cloud services</span>'
            '<span class="po2">&#127968; staff at home</span>'
            '<span class="po3">&#128241; phones everywhere</span>'
            '</div></div>'
            + vcap("Where is the “inside” now?",
                   "الداخل بقى فين دلوقتي؟")
            + '</aside>')


def v_keep():
    items = [("&#129521;", "Firewall", "controls what enters and leaves"),
             ("&#128274;", "VPN", "encrypts remote communication"),
             ("&#127970;", "DMZ", "keeps public servers apart"),
             ("&#128187;", "Endpoints", "protect each device"),
             ("&#128269;", "Zero trust", "verifies every access")]
    out = "".join('<div class="pchip" style="animation-delay:%.2fs"><span>%s</span><div>%s<small>%s</small></div></div>'
                  % (.4 + .35 * k, ico, t, why) for k, (ico, t, why) in enumerate(items))
    return ('<aside class="rise viz">' + out
            + vcap("Layer them, and verify every access.",
                   "كدّس الطبقات، واتأكد من كل وصول.")
            + '</aside>')


def v_hospital():
    return ('<aside class="rise viz"><div class="shopv">'
            '<div class="sv sv1"><span>&#129658;</span><b>Doctor at home</b><i>verify every access &#8212; zero trust</i></div>'
            '<div class="sv sv2"><span>&#9729;</span><b>Records in the cloud</b><i>which layers protect them?</i></div>'
            '<div class="sv sv3"><span>&#9888;</span><b>One risk that remains</b><i>no design is absolute</i></div>'
            '</div>'
            + vcap("Outside the office — and still protected.",
                   "برّه المستشفى، وبرضه محمي.")
            + '</aside>')


# heading text (unique to one slide) -> its drawing
VIZ = {
    "What if one wall falls?": v_walls,
    "One lock on the front door is not enough": v_walls,
    "Before you read on": v_timer,
    "The firewall: rules at the door": v_firewall,
    "A private line through a public network": v_tunnel,
    "Why is it safer to place a public web server": v_timer,
    "The perimeter has blurred": v_perimeter,
    "Layer your defenses": v_keep,
    "A hospital moves its records to the cloud": v_hospital,
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
    h2("What if one wall falls?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("Last lesson protected a message and an account. Today: how to design a whole network so that one breach does not expose everything.",
        "max-width:56ch;margin-top:1rem"),
    ar("الدرس اللي فات حمينا الرسالة والحساب. النهارده: إزاي نصمم الشبكة كلها بحيث لو دفاع واحد اتخرق، النظام كله ميتكشفش.")))

# 2 recap -- lesson 2-1, and the Arabic book's bridge into this lesson
A(s("",
    eyebrow("Before we start &#183; Lesson 2-1"),
    h2("Last time: four technologies, one connection"),
    '<table class="rise">'
    '<tr><th>Technology</th><th>What it protects</th></tr>'
    '<tr><td>Encryption</td><td>The content, from being read</td></tr>'
    '<tr><td>Digital certificate</td><td>That the other side is genuine</td></tr>'
    '<tr><td>Digital signature</td><td>The data, from being altered</td></tr>'
    '<tr><td>Multi-factor authentication</td><td>The account, from unauthorized login</td></tr>'
    '</table>',
    sub("All four protect one connection or one account. Today we widen it to the <b>network itself</b>.",
        "max-width:60ch;margin-top:.9rem"),
    ar("في الدرس 2-1 اتعلمت إزاي تقنيات التشفير والمصادقة بتحمي الاتصال والحسابات. في الدرس ده هنوسّع الحماية لتصميم الشبكة نفسها.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("This is already happening"),
    h2("One lock on the front door is not enough", "max-width:22ch"),
    '<div class="rise fields">'
    '<span class="chip">customer records</span>'
    '<span class="chip">financial files</span>'
    '<span class="chip">private messages</span>'
    '</div>',
    sub("An organization&#8217;s network holds confidential data, and attackers constantly look for a way in. If the single lock is picked, <b>everything inside is exposed</b>.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> if a company has a strong firewall, is its data safe? Remember your answer &#8212; we come back to it.</p></div>',
    ar("شبكات المؤسسات فيها بيانات وخدمات مهمة ممكن مهاجم يحاول يوصلها. ووسيلة حماية واحدة مش كفاية: لو فشلت، موارد تانية ممكن تبقى في خطر. عشان كده بنستخدم الدفاع في العمق — طبقات كتير بتقلل احتمال الاختراق وبتحد من أثره.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("How can an organization design its network so that, even if one defense is breached, the system stays protected?",
       "max-width:28ch"),
    ar("السؤال الرئيسي: إزاي مؤسسة تقدر تصمم شبكتها بحيث، حتى لو دفاع واحد اتخرق، النظام يفضل محمي؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map &#183; five ideas"),
    h2("Four layers, and one rule", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#129521;</div><div class="role">Part 1 &#183; network entry</div>'
    '<h3>Firewall</h3><p>Allows or denies by rules</p></div>'
    '<div class="card"><div class="ico">&#128274;</div><div class="role">Part 2 &#183; communication path</div>'
    '<h3>VPN</h3><p>An encrypted private line</p></div>'
    '<div class="card"><div class="ico">&#127970;</div><div class="role">Part 3 &#183; server placement</div>'
    '<h3>DMZ</h3><p>Public servers kept apart</p></div>'
    '<div class="card"><div class="ico">&#128269;</div><div class="role">Part 5 &#183; the rule</div>'
    '<h3>Zero trust</h3><p>Verify every access</p></div>'
    '</div>',
    sub("Part 4 puts the layers together: <b>defense in depth</b>.", "margin-top:.6rem;color:var(--soft)"),
    ar("دي خريطة المحاضرة: جدار الحماية عند مدخل الشبكة، والشبكة الافتراضية الخاصة لمسار الاتصال، والمنطقة المعزولة لوضع الخوادم — وده كله اسمه الدفاع في العمق. وفي الآخر نهج انعدام الثقة: اتأكد من كل عملية وصول.")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("A company has a <b>public website</b>, staff who <b>work from home</b>, and a <b>customer database</b>. With your partner, predict: where would an attacker try to get in &#8212; and if you could build only one wall, where would you put it?",
        "max-width:56ch;margin-top:1rem"),
    sub("Keep your answer. By Part 4 you will want more than one wall.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: شركة عندها موقع عام، وموظفين بيشتغلوا من البيت، وقاعدة بيانات عملاء. توقّعوا: المهاجم هيحاول يدخل منين؟ ولو هتبني حيطة واحدة بس، هتحطها فين؟")))

# ---------------- part 1: the firewall ----------------

A(s("",
    eyebrow("Part 1 &#183; The role of firewalls"),
    h2("The firewall: rules at the door", "max-width:24ch"),
    '<div class="rise statement def"><em>Firewall</em> &#8212; a system installed at the entry/exit point of a network that allows or denies communication based on rules set in advance.</div>',
    sub("<b>e.g.</b> Allow access to the web server, but deny direct external access to the database server.",
        "max-width:58ch;margin-top:.9rem"),
    ar("جدار الحماية: نظام أو برنامج بيراقب حركة مرور الشبكة وبيسمح بيها أو يمنعها حسب قواعد أمنية. ممكن يكون عند حدود الشبكة، أو بين أجزائها، أو على جهاز مضيف. مثال: نسمح بالوصول لخادم الويب ونمنع الوصول الخارجي المباشر لقاعدة البيانات.")))

# ---------------- part 2: VPN ----------------

A(s("",
    eyebrow("Part 2 &#183; VPN (Virtual Private Network)"),
    h2("A private line through a public network", "max-width:24ch"),
    '<div class="rise statement def"><em>VPN</em> &#8212; a technology that creates an encrypted virtual private line (a tunnel) over the Internet, allowing safe connection to a network from a remote location.</div>',
    '<table class="rise" style="margin-top:.9rem">'
    '<tr><th>Main use</th><th>What it means</th></tr>'
    '<tr><td>Remote work</td><td>Connecting safely to the organization&#8217;s network from home or while away</td></tr>'
    '<tr><td>Connecting branches</td><td>Connecting offices in different locations safely</td></tr>'
    '</table>',
    sub("Because the content is encrypted, the risk of <b>eavesdropping</b> is reduced &#8212; even on public Wi-Fi.",
        "max-width:58ch;margin-top:.8rem"),
    ar("الشبكة الافتراضية الخاصة (VPN): اتصال أو شبكة منطقية خاصة عبر شبكة عامة زي الإنترنت، بتستخدم التشفير وتقنيات النفق عشان تحمي البيانات بين الطرفين. استخداماتها: الشغل عن بُعد، وربط الفروع. ولأن المحتوى متشفّر، مخاطر التنصت بتقل حتى على Wi-Fi عام.")))

A(s("",
    eyebrow("2 &#183; Your turn"),
    h2("Which is NOT a use of a VPN?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">Connecting safely from home to an organization&#8217;s network <span class="ans">&#8212; <b>a use</b>: remote work.</span></li>'
    '<li class="reveal rv tf-t">Connecting offices in different locations safely <span class="ans">&#8212; <b>a use</b>: connecting branches.</span></li>'
    '<li class="reveal rv">Automatically deleting files infected with viruses <span class="ans">&#8212; <b>NOT a use</b>: that is antivirus software, on the endpoints.</span></li>'
    '<li class="reveal rv tf-t">Encrypting communication content on public Wi-Fi <span class="ans">&#8212; <b>a use</b>: it reduces eavesdropping.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("أنهي واحد مش استخدام مناسب للـ VPN؟ الحذف التلقائي للملفات المصابة بالفيروسات — ده شغل برنامج مكافحة الفيروسات، مش الـ VPN.")))

# ---------------- part 3: DMZ ----------------

A(s("",
    eyebrow("Part 3 &#183; DMZ (Demilitarized Zone)"),
    h2("Keep public servers in their own zone"),
    '<div class="rise statement def"><em>DMZ</em> &#8212; an area where servers exposed to the external network (web servers, mail servers, etc.) are placed separately from the internal network.</div>',
    fig(DMZ),
    sub("If a public-facing server is attacked, damage to the internal network can be prevented.",
        "max-width:60ch;margin-top:.2rem"),
    ar("المنطقة المعزولة (DMZ): منطقة بتتحط فيها الخوادم المعرّضة للشبكة الخارجية — خوادم الويب والبريد — منفصلة عن الشبكة الداخلية. فصلها بيقلل احتمال إن الهجوم يوصل منها للشبكة الداخلية لو واحد منها اتخرق.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("Why is it safer to place a public web server in a DMZ rather than inside the internal network?",
       "max-width:27ch"),
    ar("وقّف وفكّر: ليه حط خادم ويب عام في المنطقة المعزولة أأمن من حطه جوه الشبكة الداخلية؟")))

# ---------------- part 4: defense in depth ----------------

A(s("",
    eyebrow("Part 4 &#183; Defense in depth"),
    h2("If one layer falls, the next holds"),
    '<div class="rise statement def"><em>Defense in depth</em> &#8212; layering multiple security measures so that, even if one is breached, the next can still protect the system.</div>',
    fig(LAYERS),
    ar("الدفاع في العمق: استخدام طبقات كتير من الضوابط الأمنية، بحيث لو طبقة فشلت، الطبقات التانية تقلل الخطر وتحد من أثر الاختراق. الطبقة 1 مدخل الشبكة: جدار الحماية. الطبقة 2 مسار الاتصال: VPN. الطبقة 3 وضع الخوادم: DMZ. الطبقة 4 الأجهزة الطرفية: برنامج مكافحة فيروسات وتحديث نظام التشغيل.")))

A(s("",
    eyebrow("4 &#183; Your turn"),
    h2("Which layer does each belong to?"),
    '<table class="rise">'
    '<tr><th>Security measure</th><th>Layer</th></tr>'
    '<tr><td>Blocking unauthorized communication with a firewall</td><td class="reveal"><span>1 &#183; Network entry</span></td></tr>'
    '<tr><td>Encrypting communication with a VPN</td><td class="reveal"><span>2 &#183; Communication path</span></td></tr>'
    '<tr><td>Installing antivirus software</td><td class="reveal"><span>4 &#183; Endpoints</span></td></tr>'
    '<tr><td>Separating public-facing servers from the internal network using a DMZ</td><td class="reveal"><span>3 &#183; Server placement</span></td></tr>'
    '</table>',
    ar("لكل إجراء، أنهي طبقة من طبقات الدفاع في العمق؟ جدار الحماية ← مدخل الشبكة. الـ VPN ← مسار الاتصال. مكافحة الفيروسات ← الأجهزة الطرفية. الـ DMZ ← وضع الخوادم.")))

A(s("",
    eyebrow("4 &#183; Exam-style question &#183; 6 marks"),
    h2("Why is layering better than a firewall alone?", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane b"><h3>A firewall alone</h3><ul>'
    '<li>One barrier</li>'
    '<li>If it is breached, <b>everything inside</b> is exposed</li>'
    '</ul></div>'
    '<div class="pane a"><h3>Defense in depth</h3><ul>'
    '<li>Several layers, each with its own measure</li>'
    '<li>If one is breached, <b>the next still protects</b> the system</li>'
    '</ul></div>'
    '</div>',
    sub("Refer to what happens if one measure is breached &#8212; that is the whole answer.", "max-width:60ch;margin-top:.9rem"),
    ar("سؤال على نمط الامتحان: اشرح ليه تكديس إجراءات أمنية في طبقات بيحمي المؤسسة أحسن من الاعتماد على جدار الحماية لوحده. استعن بـ: إيه اللي بيحصل لو إجراء واحد اتخرق.")))

# ---------------- part 5: zero trust ----------------

A(s("",
    eyebrow("Part 5 &#183; The perimeter"),
    h2("The perimeter has blurred", "max-width:24ch"),
    '<div class="rise statement def"><em>Perimeter</em> &#8212; the old boundary built on the idea that &#8220;inside the organization&#8217;s network is safe, and outside is dangerous&#8221;.</div>',
    sub("With cloud services and remote work, the line between <b>inside</b> and <b>outside</b> has blurred, and designs that protect only the perimeter are no longer enough.",
        "max-width:58ch;margin-top:.9rem"),
    ar("أمان الشبكات التقليدي اتصمم أساسًا حوالين حماية المحيط الأمني، على أساس إن \"جوه شبكة المؤسسة آمن، وبرّه خطر\". بس مع انتشار الخدمات السحابية والشغل عن بُعد، الحدود بين \"الداخل\" و\"الخارج\" بقت مش واضحة، والتصاميم اللي بتحمي المحيط بس بقت مش كفاية.")))

A(s("",
    eyebrow("5 &#183; Zero trust"),
    h2("Trust nothing automatically"),
    '<div class="rise statement def"><em>Zero trust</em> &#8212; the system does not trust any communication, including from within the organization&#8217;s network, and always verifies it.</div>',
    fig(TRUST),
    sub("<b>e.g.</b> Even for access from inside the organization, identity verification and access-permission checks are performed every time.",
        "max-width:62ch;margin-top:.2rem"),
    ar("نهج انعدام الثقة: نهج أمني مش بيدّي ثقة تلقائية لمستخدم أو جهاز لمجرد إنه جوه الشبكة أو ملك المؤسسة. الهوية والصلاحيات والسياق بيتفحصوا عند طلب الوصول للموارد، حسب سياسة المؤسسة.")))

A(s("",
    eyebrow("Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">A firewall allows or denies communication based on rules set in advance. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv tf-t">Using a VPN can reduce the risk of eavesdropping even on public Wi-Fi. <span class="ans">&#8212; <b>true</b>: the content is encrypted.</span></li>'
    '<li class="reveal rv">A DMZ is a system that exposes all servers to the outside. <span class="ans">&#8212; <b>false</b>: it keeps public-facing servers apart from the internal network.</span></li>'
    '<li class="reveal rv tf-t">Defense in depth is the concept of layering multiple security measures. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: جدار الحماية بيسمح أو يمنع حسب قواعد — صح. الـ VPN بتقلل التنصت على Wi-Fi عام — صح. المنطقة المعزولة بتعرّض كل الخوادم — غلط. الدفاع في العمق تكديس إجراءات — صح.")))

A(s("",
    eyebrow("Your turn"),
    h2("Which term is it?"),
    '<table class="rise">'
    '<tr><th>Description</th><th>Term</th></tr>'
    '<tr><td>An encrypted virtual private line over the Internet for safe connection from a remote location</td><td class="reveal"><span>VPN</span></td></tr>'
    '<tr><td>An area where servers exposed to the outside are placed separately from the internal network</td><td class="reveal"><span>DMZ</span></td></tr>'
    '<tr><td>A system that allows or denies communication based on rules set in advance</td><td class="reveal"><span>Firewall</span></td></tr>'
    '<tr><td>The old boundary that assumes inside is safe, blurred by cloud and remote work</td><td class="reveal"><span>Perimeter</span></td></tr>'
    '<tr><td>No access is trusted automatically; every request is verified</td><td class="reveal"><span>Zero trust</span></td></tr>'
    '</table>',
    ar("طابق كل وصف بالمصطلح: الخط الخاص الافتراضي المشفر ← VPN. منطقة الخوادم المعزولة ← DMZ. نظام بيسمح أو يمنع ← جدار الحماية. الحدود القديمة ← المحيط الأمني. التحقق من كل وصول ← نهج انعدام الثقة.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Access from within the organization&#8217;s network is safe, so verification is unnecessary. <span class="ans">&#8212; <b>false</b>: zero trust verifies inside access too.</span></li>'
    '<li class="reveal rv">A firewall alone is sufficient to protect the network. <span class="ans">&#8212; <b>false</b>: if it is breached, nothing else stands.</span></li>'
    '<li class="reveal rv">A DMZ is provided to improve communication speed. <span class="ans">&#8212; <b>false</b>: it protects the internal network if a public server is attacked.</span></li>'
    '<li class="reveal rv">Only access from outside needs to be monitored. <span class="ans">&#8212; <b>false</b>: every access is verified.</span></li>'
    '</ul>',
    ar("خلّي بالك، كل الجمل دي غلط: الوصول من جوه آمن فمش محتاج تحقق — غلط. جدار الحماية لوحده كفاية — غلط. الـ DMZ لتحسين السرعة — غلط. نراقب الوصول من برّه بس — غلط.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("Advise a company on its office network", "max-width:26ch"),
    sub("It has a public website, staff who work from home, and confidential customer data. A firewall only &#8212; or a layered design that also verifies every access?",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Collect data.</b> List the three assets (website, remote staff, customer database) and the main threat to each.</li>'
    '<li><b>Rank the layers.</b> Rank network entry, communication path, server placement and endpoints for this company; justify your top choice.</li>'
    '<li><b>Decide.</b> Recommend a design with two reasons why layering is safer. In pairs, agree on the strongest reason.</li>'
    '</ul>',
    sub("Stuck? Start with the most exposed asset &#8212; the public website &#8212; and place it in a DMZ, so an attack there cannot reach the database.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: شركة بتجهز شبكة مكتبها، عندها موقع عام، وموظفين من البيت، وبيانات عملاء سرية. اذكر الأصول التلاتة والتهديد الرئيسي لكل واحد، واربط كل واحد بطبقة الحماية، وبعدين أوصِ بتصميم بسببين. تلميح: حط الخادم العام في المنطقة المعزولة، ومتعتمدش على العزل لوحده.")))

A(s("",
    eyebrow("In a new context"),
    h2("A hospital moves its records to the cloud", "max-width:26ch"),
    sub("Doctors will open patient records from home.", "max-width:54ch;margin-top:.7rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li>Using <b>zero trust</b> and <b>defense in depth</b>, suggest <b>two measures</b>.</li>'
    '<li>Say <b>where each one helps</b>.</li>'
    '<li>Identify <b>one risk that could still remain</b>.</li>'
    '</ul>',
    ar("طبّق اللي اتعلمته: مستشفى بينقل سجلات المرضى لخدمة سحابية، وبيسمح للدكاترة يفتحوها من البيت. باستخدام نهج انعدام الثقة والدفاع في العمق، اقترح إجراءين وبيّن كل واحد بيساعد فين، وحدد خطر واحد ممكن يفضل موجود.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 2-2"),
    h2("Layer your defenses", "max-width:28ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> is a company with a strong firewall safe? What else does it need?</p>'
    '<div class="rise statement">Layer your defenses &#8212; <em>firewall, VPN, DMZ, endpoints</em> &#8212; and verify every access (<em>zero trust</em>). One breach is then far less likely to expose the whole network.</div>',
    ar("افتكر: كدّس دفاعاتك — جدار الحماية، والشبكة الافتراضية الخاصة، والمنطقة المعزولة، والأجهزة الطرفية — واتأكد من كل عملية وصول (نهج انعدام الثقة). ساعتها خرق واحد مش هيكشف الشبكة كلها.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 6"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 6 quiz" width="250" height="250">'
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

/* lecture 6's drawings */
.statement.def{font-size:clamp(18px,2.15vw,30px); line-height:1.28; max-width:46ch}
.walls{display:flex; flex-direction:column; gap:.5rem}
.wall{border-radius:10px; padding:.7rem 1rem; font-weight:700; color:var(--ink); font-size:clamp(14px,1.35vw,19px); background:var(--gold-pale); border-left:6px solid var(--gold)}
.wall.w2,.wall.w4{background:var(--teal-pale); border-left-color:var(--teal)}
.dark .wall{color:var(--ink)}
.wall.w1{position:relative}
.wcrack{margin-top:.6rem; text-align:center; font-weight:700; color:var(--wrong); font-size:clamp(13px,1.2vw,16px)}
.dark .wcrack{color:#F2A08F}
@keyframes vBreach{0%,40%{opacity:1; transform:none} 70%{opacity:.35; transform:translateX(-6px) rotate(-1.5deg)} 100%{opacity:.35; transform:translateX(-6px) rotate(-1.5deg)}}
.slide.on .viz .wall{animation:vIn .45s both}
.slide.on .viz .wall.w1{animation:vIn .45s .3s both, vBreach 1.2s 1.6s both}
.wall.w1{opacity:.35; transform:translateX(-6px) rotate(-1.5deg)}
.slide.on .viz .wcrack{animation:vPop .5s 2.4s both}
.fw{background:#fff; border:1px solid var(--line); border-radius:14px; padding:1rem 1.1rem}
.fwh{font:600 1.1em Fraunces,serif; color:var(--ink); margin-bottom:.6rem}
.pkt{display:flex; justify-content:space-between; align-items:center; padding:.5rem .7rem; border-radius:9px; margin-bottom:.45rem; font-size:clamp(13px,1.2vw,16px); color:var(--ink)}
.pkt b{font-size:.85em; text-transform:uppercase; letter-spacing:.04em; border-radius:6px; padding:.1rem .45rem}
.pkt.ok{background:var(--teal-pale)} .pkt.ok b{color:#fff; background:var(--teal)}
.pkt.no{background:#FBF0EE} .pkt.no b{color:#fff; background:var(--wrong)}
.slide.on .viz .pkt{animation:vIn .45s both}
.slide.on .viz .pkt b{animation:vPop .4s .35s both; display:inline-block}
.viz .nodebox{fill:#fff; stroke:var(--line); stroke-width:2}
.viz .tube{stroke:var(--teal); stroke-width:4; fill:none; stroke-dasharray:10 8}
.viz .pkgbox{fill:var(--gold)} .viz .pkglk{font-size:13px; text-anchor:middle}
.viz .eav{font:600 13px Inter,system-ui,sans-serif; fill:var(--wrong); text-anchor:middle}
@keyframes vTravel{0%{transform:translateX(0)} 100%{transform:translateX(170px)}}
.slide.on .viz .pkg{animation:vTravel 2.4s .5s ease-in-out both}
.viz .pkg{transform:translateX(170px)}
.slide.on .viz .tube{animation:vDash 1s linear infinite}
.slide.on .viz .eav{animation:vIn .45s 2.4s both}
.per{position:relative; padding:1rem}
.perbox{border:3px dashed var(--teal); border-radius:16px; padding:1.4rem 1rem; text-align:center; background:var(--teal-pale)}
.perbox b{display:block; font:600 1.2em Fraunces,serif; color:var(--ink)} .perbox span{color:var(--soft)}
.perout{display:flex; flex-wrap:wrap; justify-content:center; gap:.5rem; margin-top:.8rem}
.perout span{background:#fff; border:1px solid var(--line); border-radius:99px; padding:.3rem .8rem; font-size:clamp(13px,1.2vw,16px); color:var(--ink)}
@keyframes vBlur{0%,40%{border-style:solid; opacity:1} 100%{border-style:dashed; opacity:.75}}
.slide.on .viz .perbox{animation:vBlur 1.6s .3s both}
.slide.on .viz .perout span{animation:vIn .45s both}
.slide.on .viz .po1{animation-delay:.9s} .slide.on .viz .po2{animation-delay:1.3s} .slide.on .viz .po3{animation-delay:1.7s}

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
BASE = "scripts/lecture6_slides_base.html"
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

