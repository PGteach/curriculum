# -*- coding: utf-8 -*-
"""Build Lecture 11's deck.

    python scripts/build_lecture11_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/lecture11_slides_base.html and writes lecture11/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the side drawings
added. Always starts from the base, never from the published deck.

Lesson 3-3, Fundamentals of Frontend Technology, the English textbook pp.
68-74, closes Unit 3. Where the Arabic textbook and the ministry's assessment
book go further, the deck follows them: a page need not use all three
technologies; semantic HTML helps search engines understand a page but does
not guarantee a higher ranking, and accessibility needs other practices too;
React is a JavaScript library and Next.js a framework built on it.

A longer lecture, at the teacher's request: three Qureo chapters follow the
lesson -- 34 HTML(2), 35 CSS(2) and 36, the comprehension check on 34-35.
Their own lesson text is locked on the platform; the deck teaches what their
lesson titles name (specifying ranges with div and span, input fields and
buttons, decorating a button, adding borders) in Qureo's words for CSS:
selector, property, value.

Everything but the content is lecture 5's builder, unchanged -- this file was
derived from it. The Arabic follows the Arabic textbook's lesson 3-3 point by
point, said in Egyptian Arabic. The live demos (layers, screen sizes and the
editor) are this lecture's own; their script is tools/lecture11/script.js,
added to the page's own script.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "lecture11/slides/index.html"


# --------------------------------------------------------------------------
# diagrams -- inline SVG, coloured from the page's CSS variables so they follow
# LECTURE_ACCENT. Labels only, never the sentence that explains them; no label
# under 14 units. Fills are #fff, never var(--white): the booklet template
# does not define --white. The booklet reads these out of this file.
# --------------------------------------------------------------------------

LAYERS = '''
<svg viewBox="0 0 900 250" role="img" aria-label="A web page is built like a building: HTML is the frame, CSS the interior and exterior, JavaScript the electrical and plumbing systems">
  <g font-size="15" text-anchor="middle">
    <rect x="20" y="20" width="270" height="200" rx="14" fill="#fff" stroke="var(--teal)" stroke-width="3"/>
    <text x="155" y="78" font-size="40">&#127959;</text>
    <text x="155" y="118" font-size="24" font-weight="700" fill="var(--ink)">HTML</text>
    <text x="155" y="146" font-weight="600" fill="var(--teal)">structure (skeleton)</text>
    <text x="155" y="172" fill="var(--soft)">the frame of a building</text>
    <text x="155" y="196" fill="var(--soft)">headings, paragraphs, links</text>
    <rect x="315" y="20" width="270" height="200" rx="14" fill="#fff" stroke="var(--gold)" stroke-width="3"/>
    <text x="450" y="78" font-size="40">&#127912;</text>
    <text x="450" y="118" font-size="24" font-weight="700" fill="var(--ink)">CSS</text>
    <text x="450" y="146" font-weight="600" fill="var(--gold)">appearance</text>
    <text x="450" y="172" fill="var(--soft)">the interior and exterior</text>
    <text x="450" y="196" fill="var(--soft)">colours, layout, fonts</text>
    <rect x="610" y="20" width="270" height="200" rx="14" fill="#fff" stroke="var(--ink)" stroke-width="3"/>
    <text x="745" y="78" font-size="40">&#128161;</text>
    <text x="745" y="118" font-size="24" font-weight="700" fill="var(--ink)">JavaScript</text>
    <text x="745" y="146" font-weight="600" fill="var(--ink)">behavior</text>
    <text x="745" y="172" fill="var(--soft)">electricity and plumbing</text>
    <text x="745" y="196" fill="var(--soft)">buttons that respond</text>
    <text x="450" y="244" font-weight="600" fill="var(--ink)">each has its own role &#8212; a page uses them in combination</text>
  </g>
</svg>'''

SEMANTIC = '''
<svg viewBox="0 0 900 300" role="img" aria-label="A page built from semantic elements: header at the top, nav for navigation, main for the body, footer at the bottom">
  <g font-size="16" text-anchor="middle">
    <rect x="200" y="10" width="500" height="280" rx="12" fill="#fff" stroke="var(--line)" stroke-width="3"/>
    <rect x="216" y="24" width="468" height="46" rx="6" fill="var(--teal)" opacity=".18" stroke="var(--teal)" stroke-width="2"/>
    <text x="450" y="53" font-family="JetBrains Mono,monospace" font-weight="700" fill="var(--ink)">&lt;header&gt;</text>
    <rect x="216" y="80" width="468" height="34" rx="6" fill="var(--gold)" opacity=".22" stroke="var(--gold)" stroke-width="2"/>
    <text x="450" y="103" font-family="JetBrains Mono,monospace" font-weight="700" fill="var(--ink)">&lt;nav&gt;</text>
    <rect x="216" y="124" width="468" height="104" rx="6" fill="#fff" stroke="var(--ink)" stroke-width="2"/>
    <text x="450" y="182" font-family="JetBrains Mono,monospace" font-weight="700" fill="var(--ink)">&lt;main&gt;</text>
    <rect x="216" y="238" width="468" height="40" rx="6" fill="var(--teal)" opacity=".18" stroke="var(--teal)" stroke-width="2"/>
    <text x="450" y="264" font-family="JetBrains Mono,monospace" font-weight="700" fill="var(--ink)">&lt;footer&gt;</text>
    <text x="100" y="53" fill="var(--soft)">top of the page</text>
    <text x="100" y="103" fill="var(--soft)">navigation</text>
    <text x="100" y="182" fill="var(--soft)">the body</text>
    <text x="100" y="264" fill="var(--soft)">bottom of the page</text>
    <text x="800" y="140" font-weight="700" fill="var(--teal)">screen readers</text>
    <text x="800" y="162" font-weight="700" fill="var(--teal)">and search engines</text>
    <text x="800" y="184" font-weight="700" fill="var(--teal)">understand it</text>
  </g>
</svg>'''


# ---------------- side visuals ----------------
# A slide whose content fills only the left half of a wide screen gets an
# animated explainer on the right. Each drawing plays once when the slide
# opens and again when tapped. Under 1000px wide the drawing is hidden.

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


def v_frameworks():
    tiles = [("&#9883;", "React", "parts that update"), ("&#9993;", "Vue", "start small"),
             ("&#9889;", "Next.js", "built on React"), ("&#129513;", "Ready-made", "no need to start from zero")]
    out = "".join('<div class="tile" style="animation-delay:%.2fs"><span>%s</span><b>%s</b><i>%s</i></div>'
                  % (.3 + .3 * k, ico, t, i) for k, (ico, t, i) in enumerate(tiles))
    return ('<aside class="rise viz"><div class="tiles">' + out + '</div>'
            + vcap("Build from ready-made parts.",
                   "ابني من أجزاء جاهزة.")
            + '</aside>')


def v_club():
    return ('<aside class="rise viz"><div class="shopv">'
            '<div class="sv sv1"><span>&#128197;</span><b>The list of events</b><i>which technology?</i></div>'
            '<div class="sv sv2"><span>&#127912;</span><b>The club&#8217;s colours</b><i>which technology?</i></div>'
            '<div class="sv sv3"><span>&#128290;</span><b>A live sign-up counter</b><i>which technology?</i></div>'
            '</div>'
            + vcap("Give each feature to one technology.",
                   "ادّي كل ميزة للتقنية المناسبة.")
            + '</aside>')


# heading text (unique to one slide) -> its drawing
VIZ = {
    "Before you read on": v_timer,
    "Frameworks: ready-made parts": v_frameworks,
    "A student club wants a page": v_club,
}
VIZ_USED = []


# ---------------- code, shown on a slide ----------------
import html as _html, re as _re


def hl(t):
    """Escape code for a slide and colour it lightly: tags and keywords
    orange, strings green, CSS properties blue."""
    s = _html.escape(t, quote=False)
    # strings first: the spans added after this carry quotes of their own
    s = _re.sub(r'("[^"\n]*")', r'<span class="s">\1</span>', s)
    s = _re.sub(r'(&lt;/?[a-z0-9]+)', r'<span class="k">\1</span>', s)
    s = _re.sub(r'(?<![\w-])(&gt;)', r'<span class="k">\1</span>', s)
    s = _re.sub(r'(?m)^(\s+)([a-z-]+)(:)', r'\1<span class="f">\2</span>\3', s)
    return s


def codebox(t, style=""):
    return '<div class="rise code"%s>%s</div>' % ((' style="%s"' % style) if style else "", hl(t))


# ---------------- the live demos ----------------
# All plain HTML; script.js (added to the page's own script) makes them work.

DEMO_PAGE = ('<div class="dp-head"><b>Science Club</b></div>'
             '<div class="dp-body"><h4>Next event: Robot day</h4>'
             '<p>Thursday, 2 pm, in the lab.</p>'
             '<button type="button" class="dp-btn">I&#8217;m coming</button> '
             '<span class="dp-count">0 signed up</span></div>')


def layers():
    """The same page as HTML only, then with CSS, then with JavaScript."""
    return ('<div class="rise layers" data-stage="html">'
            '<div class="lbtns"><button type="button" data-s="html" class="on">1 &#183; HTML only</button>'
            '<button type="button" data-s="css">2 &#183; + CSS</button>'
            '<button type="button" data-s="js">3 &#183; + JavaScript</button></div>'
            '<div class="dpage">' + DEMO_PAGE + '</div>'
            '<p class="lnote"><span class="en"></span><span class="ar"></span></p></div>')


def resp():
    """One layout, three screen widths."""
    cards = "".join('<div class="rc"><b>%s</b><span>%s</span></div>' % (t, d) for t, d in
                    [("Events", "Robot day"), ("Members", "48 students"), ("Join", "Sign up now")])
    return ('<div class="rise resp" data-w="pc">'
            '<div class="lbtns"><button type="button" data-w="phone">&#128241; Phone</button>'
            '<button type="button" data-w="tablet">Tablet</button>'
            '<button type="button" data-w="pc" class="on">&#128187; PC</button></div>'
            '<div class="rframe"><div class="rhead">Science Club</div><div class="rgrid">' + cards + '</div></div>'
            '<p class="lnote"><span class="en"></span><span class="ar"></span></p></div>')


def live(start, rows=7):
    """A live editor: type HTML (and CSS in a style tag); the preview updates.
    The preview is a sandboxed frame, so nothing typed can run a script."""
    return ('<div class="rise live">'
            '<div class="lcol"><div class="tlbl">Type here &#8212; the result updates</div>'
            '<textarea spellcheck="false" rows="%d" aria-label="HTML and CSS to try">%s</textarea>'
            '<div class="tbtns"><button type="button" class="alt lreset">&#8634; Start again</button></div></div>'
            '<div class="lcol"><div class="tlbl">The result</div>'
            '<iframe class="lprev" sandbox="" title="Result of the code"></iframe></div></div>'
            % (rows, _html.escape(start, quote=False)))


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
    h2("What is a web page made of?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("Every page you open is three technologies working together. Today: what each one does &#8212; and on the platform, you build pages yourself: HTML, then CSS, then a small project.",
        "max-width:58ch;margin-top:1rem"),
    ar("كل صفحة بتفتحها فيها تلات تقنيات شغالين مع بعض. النهارده: كل واحدة بتعمل إيه — وعلى المنصة هتبني صفحات بنفسك: HTML، وبعدين CSS، وبعدين مشروع صغير.")))

# 2 recap -- lesson 3-2
A(s("",
    eyebrow("Before we start &#183; Lesson 3-2"),
    h2("Last time: how they talk", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>Word</th><th>Meaning</th></tr>'
    '<tr><td><b>Client / server</b></td><td>the client requests, the server responds</td></tr>'
    '<tr><td><b>HTTP / HTTPS</b></td><td>the rules for the messages; HTTPS adds TLS encryption</td></tr>'
    '<tr><td><b>GET / POST</b></td><td>retrieve data / send data</td></tr>'
    '<tr><td><b>200 / 404 / 500</b></td><td>success / not found / server error</td></tr>'
    '</table>',
    sub("The page the server sends back is what the <b>frontend</b> shows. Today: what that page is made of.", "max-width:60ch;margin-top:.9rem"),
    ar("المرة اللي فاتت: العميل بيطلب والخادم بيرد. الصفحة اللي الخادم بيرجّعها هي اللي الواجهة الأمامية بتعرضها. النهارده: الصفحة دي معمولة من إيه.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("Open any web page"),
    h2("Three technologies at work", "max-width:22ch"),
    sub("<b>HTML</b> builds the structure &#8212; headings, paragraphs and links, like the frame of a building. <b>CSS</b> adds the appearance &#8212; colours, layout and fonts, like a building&#8217;s interior. <b>JavaScript</b> adds behavior &#8212; search boxes that respond, buttons that count, screens that update.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> you want a page&#8217;s title to turn pink. Which of the three would you change? Remember your answer.</p></div>',
    ar("عند فتح أي صفحة ويب، بتشوف تلات تقنيات شغالين مع بعض: HTML بيبني الهيكل — العناوين والفقرات والروابط — زي هيكل المبنى. و CSS بيضيف المظهر — الألوان والتخطيط والخطوط — زي التصميم الداخلي. و JavaScript بيضيف السلوك التفاعلي — مربعات بحث بتستجيب، وأزرار بتعد، وشاشات بتتحدّث.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("How do HTML, CSS, and JavaScript work together to build a web page, and what makes a modern frontend meaningful, adaptable, and efficient to build?",
       "max-width:30ch"),
    ar("السؤال الرئيسي: إزاي HTML و CSS و JavaScript بيشتغلوا مع بعض عشان يبنوا صفحة ويب، وإيه اللي بيخلي الواجهة الأمامية الحديثة ليها معنى، وقابلة للتكيف، وفعّالة في البناء؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map &#183; a long one"),
    h2("Three parts from the book, three on the platform", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#127959;</div><div class="role">Part 1</div><h3>HTML, CSS, JS</h3><p>Who does what</p></div>'
    '<div class="card"><div class="ico">&#127991;</div><div class="role">Part 2</div><h3>Semantic HTML</h3><p>Tags with meaning</p></div>'
    '<div class="card"><div class="ico">&#128241;</div><div class="role">Part 3</div><h3>Responsive &amp; frameworks</h3><p>Every screen; ready-made parts</p></div>'
    '<div class="card"><div class="ico">&#128221;</div><div class="role">Qureo 34</div><h3>HTML (2)</h3><p>Ranges, inputs, buttons</p></div>'
    '<div class="card"><div class="ico">&#127912;</div><div class="role">Qureo 35</div><h3>CSS (2)</h3><p>Decorate a button, add borders</p></div>'
    '<div class="card"><div class="ico">&#128295;</div><div class="role">Qureo 36</div><h3>Review</h3><p>Build a sign-up card</p></div>'
    '</div>',
    ar("خريطة المحاضرة: 1 أدوار HTML و CSS و JavaScript. 2 HTML الدلالية. 3 التصميم المتجاوب وأطر العمل. وعلى المنصة: الفصل 34 HTML (2)، والفصل 35 CSS (2)، والفصل 36 مراجعة.")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("Think of a page you use often &#8212; YouTube, your school&#8217;s site, a shop. With your partner, point to:",
        "max-width:56ch;margin-top:1rem"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>one thing that is <b>structure</b> &#8212; a heading, a list, a link;</li>'
    '<li>one thing that is <b>style</b> &#8212; a colour, a font, a layout;</li>'
    '<li>one thing that <b>reacts to you</b> when you click or type.</li>'
    '</ul>',
    sub("Keep your three. Part 1 says which technology does each.", "margin-top:.8rem;color:var(--soft)"),
    ar("في صفحة بتستخدمها كتير، إيه الأجزاء اللي بتمثل البنية (HTML)، وإيه اللي بتمثل الشكل (CSS)، وإيه اللي بيتفاعل معاك (JavaScript)؟")))

# ---------------- part 1: the roles of HTML, CSS and JavaScript ----------------

A(s("",
    eyebrow("Part 1 &#183; The roles of HTML, CSS, and JavaScript"),
    h2("A page is built like a building"),
    fig(LAYERS),
    sub("These three technologies each have independent roles, and a web page is created using them in combination.",
        "max-width:60ch;margin-top:.3rem"),
    ar("التقنيات دي بتأدي أدوار مختلفة: HTML بيبني الهيكل، و CSS بيضيف التنسيق، و JS بيضيف السلوك التفاعلي.")))

A(s("",
    eyebrow("1 &#183; Who does what"),
    h2("Structure, appearance, behavior"),
    '<table class="rise">'
    '<tr><th>Technology</th><th>Role</th><th>Analogy</th></tr>'
    '<tr><td><b>HTML</b></td><td>Defines the structure (skeleton): headings, paragraphs, images, links</td><td>The frame of a building</td></tr>'
    '<tr><td><b>CSS</b></td><td>Specifies the appearance: colours, layout, size, fonts</td><td>The interior and exterior</td></tr>'
    '<tr><td><b>JavaScript</b></td><td>Adds behavior and interactivity: responds when buttons are pressed, updates part of the screen</td><td>The electrical and plumbing systems</td></tr>'
    '</table>',
    sub("The Arabic book adds: a page does not have to use all three. It can be HTML alone, or HTML with CSS and JavaScript, depending on what it needs to do.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("HTML بيحدد بنية الصفحة، و CSS بيحدد مظهرها، و JavaScript بيضيف السلوك والتفاعلية. والصفحة ممكن تستخدم HTML لوحده، أو HTML مع CSS و JavaScript حسب الوظايف اللي محتاجاها.")))

A(s("",
    eyebrow("1 &#183; Watch it happen"),
    h2("Switch on the layers, one at a time"),
    layers(),
    ar("دوس 1 وبعدين 2 وبعدين 3: نفس الصفحة بـ HTML بس، وبعدين مع CSS، وبعدين مع JavaScript. جرّب تدوس على الزرار في كل مرحلة.")))

A(s("",
    eyebrow("1 &#183; Your turn"),
    h2("Which technology does each task?"),
    '<table class="rise">'
    '<tr><th>Task</th><th>Technology</th></tr>'
    '<tr><td>a &#183; Describing the structure of headings and paragraphs</td><td class="reveal"><span>A &#183; HTML</span></td></tr>'
    '<tr><td>b &#183; Changing the colour and size of text</td><td class="reveal"><span>B &#183; CSS</span></td></tr>'
    '<tr><td>c &#183; Updating part of the screen when a button is pressed</td><td class="reveal"><span>C &#183; JavaScript</span></td></tr>'
    '<tr><td>d &#183; Placing images and links</td><td class="reveal"><span>A &#183; HTML</span></td></tr>'
    '<tr><td>e &#183; Setting the background colour of the whole page</td><td class="reveal"><span>B &#183; CSS</span></td></tr>'
    '<tr><td>f &#183; Validating what is entered into a form</td><td class="reveal"><span>C &#183; JavaScript</span></td></tr>'
    '</table>',
    ar("لكل مهمة، أنهي تقنية؟ البنية ← HTML، الشكل ← CSS، التفاعل والتحديث ← JavaScript. جاوب الأول وبعدين دوس.")))

A(s("",
    eyebrow("1 &#183; Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">HTML is a technology that defines the structure (skeleton) of a web page. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv">CSS is a technology that adds behavior to a web page. <span class="ans">&#8212; <b>false</b>: CSS is appearance; behavior is JavaScript.</span></li>'
    '<li class="reveal rv tf-t">Responsive design adjusts the layout automatically to different screen sizes. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv tf-t">Using a framework means you do not write all the code from scratch. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: HTML بيحدد البنية — صح. CSS بيضيف السلوك — غلط، ده JavaScript. التصميم المتجاوب بيظبط التخطيط حسب الشاشة — صح. إطار العمل بيوفّر الكتابة من الصفر — صح.")))

A(s("",
    eyebrow("1 &#183; Exam-style question"),
    h2("Match each role with a technology"),
    '<table class="rise">'
    '<tr><th>Role</th><th>Technology</th></tr>'
    '<tr><td>a &#183; Defines the structure of a web page</td><td class="reveal"><span>A &#183; HTML</span></td></tr>'
    '<tr><td>b &#183; Specifies the appearance of a web page</td><td class="reveal"><span>B &#183; CSS</span></td></tr>'
    '<tr><td>c &#183; Adds behavior and interactivity to a web page</td><td class="reveal"><span>C &#183; JavaScript</span></td></tr>'
    '</table>',
    sub("Choices: <b>A</b> HTML &#183; <b>B</b> CSS &#183; <b>C</b> JavaScript.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("اربط كل دور بالتقنية: البنية = HTML، المظهر = CSS، السلوك والتفاعلية = JavaScript.")))

# ---------------- part 2: semantic HTML ----------------

A(s("",
    eyebrow("Part 2 &#183; Semantic HTML"),
    h2("Tags that say what a part is"),
    '<div class="rise statement def"><em>Semantic HTML</em> &#8212; describing each part of a page with element names (tags) that show their meaning.</div>',
    fig(SEMANTIC),
    ar("HTML الدلالي: استخدام عناصر بتوضح وظيفة أجزاء الصفحة، زي <span class='mono' dir='ltr'>&lt;header&gt;</span> في أعلى الصفحة، و <span class='mono' dir='ltr'>&lt;nav&gt;</span> للتنقل، و <span class='mono' dir='ltr'>&lt;main&gt;</span> للمحتوى الرئيسي، و <span class='mono' dir='ltr'>&lt;footer&gt;</span> في أسفل الصفحة.")))

A(s("",
    eyebrow("2 &#183; Why use it?"),
    h2("Two benefits"),
    '<table class="rise">'
    '<tr><th>Benefit</th><th>What it means</th></tr>'
    '<tr><td><b>Accessibility</b></td><td>Screen-reader software can understand the page&#8217;s structure, so information reaches users with visual impairments more easily.</td></tr>'
    '<tr><td><b>SEO</b> (search engine optimization)</td><td>Search engines can understand the content more easily, so it is more likely to be shown properly in results.</td></tr>'
    '</table>',
    sub("The Arabic book is careful: semantic HTML <b>helps</b> search engines, but it does not <b>guarantee</b> a higher ranking &#8212; and accessibility needs other good practices too.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Pause &amp; think: why does a screen reader understand a page better with &lt;header&gt;, &lt;nav&gt; and &lt;main&gt; than with plain boxes? <span class="ans">&#8212; the tag <b>names the part</b>, so it can say &#8220;navigation&#8221; or &#8220;main content&#8221; and let the user jump there.</span></li>'
    '</ul>',
    ar("فوايد HTML الدلالي: إمكانية الوصول — بيساعد قارئ الشاشة يفهم بنية الصفحة ويتنقل فيها، مع الحاجة لممارسات وصول تانية. وفهم محركات البحث للمحتوى — ممكن يساعدها، لكنه مش بيضمن ترتيب أعلى.")))

A(s("",
    eyebrow("2 &#183; The same page, two ways"),
    h2("Plain boxes or meaningful tags?"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Plain boxes</h3>'
    '<div class="code" style="font-size:clamp(11px,1.3vw,16px)">' + hl('<div>Science Club</div>\n<div>Home | Events</div>\n<div>Robot day ...</div>\n<div>© 2026</div>') + '</div>'
    '<p>Works &#8212; but nothing says which part is which.</p></div>'
    '<div class="pane b"><h3>Semantic HTML</h3>'
    '<div class="code" style="font-size:clamp(11px,1.3vw,16px)">' + hl('<header>Science Club</header>\n<nav>Home | Events</nav>\n<main>Robot day ...</main>\n<footer>© 2026</footer>') + '</div>'
    '<p>Same look &#8212; and every part is named.</p></div>'
    '</div>',
    ar("الاتنين ممكن يبانوا نفس الشكل، بس في التاني كل جزء ليه اسم بيوضح وظيفته.")))

A(s("",
    eyebrow("2 &#183; Your turn"),
    h2("Which element is used for&#8230;?"),
    '<table class="rise">'
    '<tr><th>Element</th><th>Used for</th></tr>'
    '<tr><td><b class="mono">&lt;header&gt;</b></td><td class="reveal"><span>the top of the page</span></td></tr>'
    '<tr><td><b class="mono">&lt;nav&gt;</b></td><td class="reveal"><span>navigating between parts of the site</span></td></tr>'
    '<tr><td><b class="mono">&lt;main&gt;</b></td><td class="reveal"><span>the main content</span></td></tr>'
    '<tr><td><b class="mono">&lt;footer&gt;</b></td><td class="reveal"><span>the bottom of the page</span></td></tr>'
    '</table>',
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Which is NOT a semantic element: &lt;header&gt;, &lt;E-mail&gt;, &lt;main&gt;, &lt;footer&gt;? <span class="ans">&#8212; <b>&lt;E-mail&gt;</b>: there is no such element.</span></li>'
    '</ul>',
    ar("العنصر <span class='mono' dir='ltr'>&lt;header&gt;</span> لرأس الصفحة، و <span class='mono' dir='ltr'>&lt;nav&gt;</span> للتنقل، و <span class='mono' dir='ltr'>&lt;main&gt;</span> للمحتوى الرئيسي، و <span class='mono' dir='ltr'>&lt;footer&gt;</span> للتذييل. أسئلة زي دي موجودة في كتاب التقييمات.")))

# ---------------- part 3: responsive design and frameworks ----------------

A(s("",
    eyebrow("Part 3 &#183; Responsive design"),
    h2("One page, every screen"),
    '<div class="rise statement def"><em>Responsive design</em> &#8212; the layout adjusts automatically to different screen sizes: PCs, smartphones and tablets.</div>',
    resp(),
    ar("التصميم المتجاوب: مفهوم تصميمي بيتظبط فيه التخطيط تلقائيًا حسب أحجام الشاشات المختلفة. دوس Phone و Tablet و PC وشوف نفس الصفحة بتتغير.")))

A(s("",
    eyebrow("3 &#183; Mobile first"),
    h2("Why it matters now", "max-width:24ch"),
    sub("Many people use the web on their phones, so developers think about small screens from the very start of the design. This is called <b>mobile-first</b>.",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li class="reveal rv">Why is responsive design needed? <span class="ans">&#8212; because websites are accessed from many devices: PCs, smartphones and tablets.</span></li>'
    '<li class="reveal rv">Does it make the server faster? <span class="ans">&#8212; <b>no</b>: it is about the layout on the screen.</span></li>'
    '<li class="reveal rv">&#8220;Mobile-first&#8221; means designing first for&#8230; <span class="ans">&#8212; <b>small screens such as phones</b>.</span></li>'
    '</ul>',
    ar("ناس كتير بتستخدم الويب من الموبايل، عشان كده المطورين بيراعوا الشاشات الصغيرة من بداية التصميم. وده اسمه نهج الأولوية للجوال.")))

A(s("",
    eyebrow("3 &#183; Frameworks"),
    h2("Frameworks: ready-made parts", "max-width:24ch"),
    '<div class="rise statement def"><em>Framework</em> &#8212; a structure that provides common functions and components in advance, to make web application development more efficient.</div>',
    '<table class="rise" style="margin-top:.8rem">'
    '<tr><th>Name</th><th>What to know</th></tr>'
    '<tr><td><b>React</b></td><td>From Meta (formerly Facebook). Updates only part of the screen; suits large web apps. The Arabic book: a JavaScript library for building interfaces from reusable components.</td></tr>'
    '<tr><td><b>Vue</b></td><td>A simple structure; build an app step by step, starting from small features.</td></tr>'
    '<tr><td><b>Next.js</b></td><td>Built on React; adds ways to show pages faster (routing, rendering on the server and the client).</td></tr>'
    '</table>',
    ar("إطار العمل: بنية بتوفر وظايف ومكونات شائعة مسبقًا، عشان تطوير تطبيقات الويب يبقى أكفأ؛ فمش لازم تكتب الكود كله من الصفر. React مكتبة JavaScript لبناء الواجهات من مكونات بتتعاد، و Vue بنيته بسيطة، و Next.js مبني على React.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Using semantic HTML necessarily makes a page display faster. <span class="ans">&#8212; <b>false</b>: its benefits are accessibility and SEO.</span></li>'
    '<li class="reveal rv">A framework is a language for defining the structure of a page. <span class="ans">&#8212; <b>false</b>: that is HTML.</span></li>'
    '<li class="reveal rv">Responsive design means the page works only on computers. <span class="ans">&#8212; <b>false</b>: it adapts to every screen.</span></li>'
    '<li class="reveal rv tf-t">Next.js is built on React. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    ar("خلّي بالك: HTML الدلالي مش بيسرّع الصفحة بالضرورة. إطار العمل مش لغة لبنية الصفحة. التصميم المتجاوب مش للكمبيوتر بس. و Next.js مبني على React — صح.")))

A(s("",
    eyebrow("Exam-style question &#183; 6 marks"),
    h2("A library page", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Explain&#8230;</h3><ul>'
    '<li>how HTML, CSS and JavaScript each contribute to a library page that <b>lists books</b>, is <b>styled</b>, and <b>filters the results</b> as the user types</li>'
    '<li>refer to: structure, appearance, behavior</li>'
    '</ul></div>'
    '<div class="pane b"><h3>A plan for your answer</h3><ul>'
    '<li>HTML: the list of books, the search box</li>'
    '<li>CSS: colours, fonts, the layout of the list</li>'
    '<li>JavaScript: hides the books that do not match, as you type</li>'
    '</ul></div>'
    '</div>',
    ar("سؤال على نمط الامتحان: اشرح إزاي HTML و CSS و JavaScript بيساهموا في صفحة مكتبة بتعرض قائمة كتب، ومتنسّقة، وبتصفّي النتايج وانت بتكتب. راجع: البنية، المظهر، السلوك.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("A student club wants a page", "max-width:26ch"),
    sub("It lists the club&#8217;s events, uses the club&#8217;s colours, and has a button showing how many people have signed up.",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Observe first.</b> On a page you use, note two things that change when you click or type. Then: the list of events, the club&#8217;s colours and layout, the live sign-up counter &#8212; which technology does each, and why?</li>'
    '<li><b>Make it reach everyone.</b> One change for phones (responsive design), one semantic-HTML choice for a screen reader.</li>'
    '<li><b>Decide.</b> Separate HTML, CSS and JavaScript? Two reasons. In pairs, agree on what the counter needs.</li>'
    '</ul>',
    sub("Stuck? HTML holds the content; CSS styles it; JavaScript makes it react and update.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: نادي طلابي عايز صفحة بتعرض الفعاليات، بألوان النادي، وفيها زرار بيعرض عدد المسجلين. حدد التقنية لكل ميزة، وغيّر حاجة للموبايل وحاجة لقارئ الشاشة، وقرّر بسببين.")))

A(s("",
    eyebrow("In a new context"),
    h2("A news site", "max-width:26ch"),
    sub("It must look good on phones and be found easily by search engines.", "max-width:56ch;margin-top:.7rem"),
    '<table class="rise">'
    '<tr><th>Choice</th><th>What it improves</th></tr>'
    '<tr><td>A responsive-design choice, e.g. one column on a phone</td><td class="reveal"><span>easy to read on any screen</span></td></tr>'
    '<tr><td>A semantic-HTML choice, e.g. &lt;header&gt;, &lt;nav&gt;, &lt;main&gt;</td><td class="reveal"><span>search engines and screen readers understand it</span></td></tr>'
    '</table>',
    ar("طبّق اللي اتعلمته: موقع أخبار لازم يبان كويس على الموبايل ويتلاقي بسهولة في محركات البحث. اذكر اختيار من التصميم المتجاوب واختيار من HTML الدلالي، وكل واحد بيحسّن إيه.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 3-3"),
    h2("Structure, style, behavior", "max-width:24ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> the pink title &#8212; which technology? (CSS: it is appearance.)</p>'
    '<div class="rise statement">HTML <em>structures</em>, CSS <em>styles</em>, JavaScript <em>behaves</em> &#8212; and semantic HTML, responsive design and frameworks make a modern frontend <em>meaningful, adaptable and efficient</em>.</div>',
    ar("افتكر: HTML بيبني، و CSS بينسّق، و JavaScript بيتفاعل — و HTML الدلالي والتصميم المتجاوب وأطر العمل بيخلّوا الواجهة الأمامية الحديثة ليها معنى، وبتتكيف، وفعّالة في البناء.")))

# unit wrap -- this lesson closes Unit 3
A(s("",
    eyebrow("Unit 3 &#183; complete"),
    h2("Web applications, in three lessons", "max-width:28ch"),
    '<div class="rise timeline">'
    '<div class="tl"><h3>3-1 &#183; The overall structure of web applications</h3><p>Frontend, backend, database &#8212; three tiers cooperating</p></div>'
    '<div class="tl"><h3>3-2 &#183; Web application communication methods</h3><p>Client and server, HTTP/HTTPS, GET/POST, status codes, API and JSON</p></div>'
    '<div class="tl"><h3>3-3 &#183; Fundamentals of frontend technology</h3><p>HTML, CSS, JavaScript; semantic HTML, responsive design, frameworks</p></div>'
    '</div>',
    ar("خلصنا الوحدة التالتة: 3-1 البنية العامة لتطبيقات الويب، 3-2 طرق اتصال تطبيقات الويب، 3-3 أساسيات تقنية الواجهة الأمامية.")))

# ---------------- part 4: Qureo 34, HTML (2) ----------------

A(s("dark",
    '<div class="rise part">4</div>',
    h2("On the platform: HTML (2)"),
    sub("Qureo chapter 34: an HTML review, then marking ranges with div and span, then text boxes and buttons. You will type it yourself.", "max-width:56ch"),
    ar("الجزء الرابع على المنصة: الفصل 34 — HTML (2): مراجعة، وبعدين تحديد نطاقات بـ div و span، وبعدين خانات الإدخال والأزرار. وهتكتب بنفسك.")))

A(s("",
    eyebrow("4 &#183; HTML review"),
    h2("An element: a tag, the content, a closing tag", "max-width:28ch"),
    codebox('<h1>Science Club</h1>\n<p>We build robots every Thursday.</p>\n<a href="events.html">See the events</a>'),
    '<table class="rise">'
    '<tr><th>Tag</th><th>Makes</th></tr>'
    '<tr><td><b class="mono">&lt;h1&gt;</b></td><td class="reveal"><span>a big heading</span></td></tr>'
    '<tr><td><b class="mono">&lt;p&gt;</b></td><td class="reveal"><span>a paragraph</span></td></tr>'
    '<tr><td><b class="mono">&lt;a href="..."&gt;</b></td><td class="reveal"><span>a link to another page</span></td></tr>'
    '</table>',
    ar("العنصر = وسم فتح + المحتوى + وسم قفل، زي <span class='mono' dir='ltr'>&lt;p&gt;…&lt;/p&gt;</span>. والوسم بيقول للمتصفح الجزء ده إيه: عنوان، ولا فقرة، ولا رابط.")))

A(s("",
    eyebrow("4 &#183; Try it"),
    h2("Write HTML, see the page"),
    live('<h1>Science Club</h1>\n<p>We build robots every Thursday.</p>\n<p>Next event: Robot day.</p>', 6),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>Change the heading to your own club&#8217;s name.</li>'
    '<li>Add a third paragraph with the day and the time.</li>'
    '<li>Change <span class="codeline">&lt;h1&gt;</span> to <span class="codeline">&lt;h2&gt;</span> &#8212; what happens?</li>'
    '</ul>',
    ar("اكتب في المربع الغامق، والنتيجة بتتحدّث لوحدها. جرّب المهام التلاتة اللي تحت.")))

A(s("",
    eyebrow("4 &#183; Specifying ranges"),
    h2("div for a box, span for a few words"),
    '<div class="rise twocol"><div>'
    + '<div class="code" style="font-size:clamp(11px,1.3vw,17px)">' + hl('<div class="card">\n  <h3>Robot day</h3>\n  <p>Thursday, 2 pm</p>\n</div>\n\n<p>Bring your <span class="hot">own laptop</span>.</p>') + '</div>'
    + '</div><div>'
    '<div class="preview"><div style="border:2px solid var(--teal);border-radius:10px;padding:.6rem .8rem;margin-bottom:.8rem">'
    '<h3 style="margin:0 0 .2rem">Robot day</h3><p style="margin:0">Thursday, 2 pm</p></div>'
    '<p style="margin:0">Bring your <span style="background:var(--gold-pale);color:#9C3B2E;font-weight:700">own laptop</span>.</p></div>'
    '<table style="margin-top:.8rem"><tr><th>Tag</th><th>Marks</th></tr>'
    '<tr><td><b class="mono">&lt;div&gt;</b></td><td>a block: a box that holds several elements</td></tr>'
    '<tr><td><b class="mono">&lt;span&gt;</b></td><td>a range inside a line of text</td></tr></table>'
    '</div></div>',
    ar("<span class='mono' dir='ltr'>&lt;div&gt;</span> بيحدد نطاق كبير — صندوق جوّاه كذا عنصر. و <span class='mono' dir='ltr'>&lt;span&gt;</span> بيحدد نطاق صغير جوّه سطر. ومع class نقدر ننسّق النطاق ده بـ CSS.")))

A(s("",
    eyebrow("4 &#183; Input fields and buttons"),
    h2("Let the user type and press"),
    codebox('<input type="text" placeholder="Your name">\n<button>Sign up</button>', "font-size:clamp(12px,1.45vw,19px)"),
    '<div class="rise preview" style="max-width:520px"><input type="text" placeholder="Your name" style="font:inherit;padding:.35em .6em;margin-right:.4rem"> <button type="button" style="font:inherit;padding:.35em .9em">Sign up</button></div>',
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">What does <span class="codeline">placeholder</span> do? <span class="ans">&#8212; shows a grey hint in the box until the user types.</span></li>'
    '<li class="reveal rv">Does &lt;input&gt; need a closing tag? <span class="ans">&#8212; <b>no</b>: it stands alone. &lt;button&gt; does: &lt;button&gt;Sign up&lt;/button&gt;.</span></li>'
    '</ul>',
    ar("<span class='mono' dir='ltr'>&lt;input&gt;</span> بيعمل خانة يكتب فيها المستخدم، و placeholder تلميح رمادي. و <span class='mono' dir='ltr'>&lt;button&gt;</span> بيعمل زرار. ودوس جرّب تكتب في الخانة اللي فوق.")))

A(s("",
    eyebrow("4 &#183; Try it"),
    h2("Build a sign-up row"),
    live('<h2>Join the club</h2>\n<input type="text" placeholder="Your name">\n<button>Sign up</button>', 5),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>Add a second input with the placeholder <span class="codeline">Your class</span>.</li>'
    '<li>Change the button&#8217;s text to <span class="codeline">Join now</span>.</li>'
    '<li>Put the heading and the two inputs in one <span class="codeline">&lt;div&gt;</span>.</li>'
    '</ul>',
    ar("زوّد خانة تانية، وغيّر كلام الزرار، وحط كله جوّه div واحد.")))

A(s("",
    eyebrow("4 &#183; Your turn"),
    h2("Which tag?"),
    '<table class="rise">'
    '<tr><th>I want&#8230;</th><th>Tag</th></tr>'
    '<tr><td>a box where the user types a name</td><td class="reveal"><span>&lt;input&gt;</span></td></tr>'
    '<tr><td>a box that groups a heading and two paragraphs</td><td class="reveal"><span>&lt;div&gt;</span></td></tr>'
    '<tr><td>to colour two words in the middle of a sentence</td><td class="reveal"><span>&lt;span&gt;</span></td></tr>'
    '<tr><td>something the user can press</td><td class="reveal"><span>&lt;button&gt;</span></td></tr>'
    '<tr><td>a link to another page</td><td class="reveal"><span>&lt;a href="..."&gt;</span></td></tr>'
    '</table>',
    ar("لكل حاجة، أنهي وسم؟ فكّر الأول وبعدين دوس.")))

# ---------------- part 5: Qureo 35, CSS (2) ----------------

A(s("dark",
    '<div class="rise part">5</div>',
    h2("On the platform: CSS (2)"),
    sub("Qureo chapter 35: a CSS review, then decorating a button, then adding borders.", "max-width:56ch"),
    ar("الجزء الخامس على المنصة: الفصل 35 — CSS (2): مراجعة، وبعدين تزيين الزرار، وبعدين إضافة إطارات.")))

A(s("",
    eyebrow("5 &#183; CSS review"),
    h2("Which part, what to change, how"),
    codebox('button {\n  color: white;\n  background-color: green;\n}'),
    '<table class="rise">'
    '<tr><th>Part</th><th>In the example</th><th>It says</th></tr>'
    '<tr><td><b>selector</b></td><td class="mono">button</td><td><b>which</b> part to change</td></tr>'
    '<tr><td><b>property</b></td><td class="mono">background-color</td><td><b>what</b> to change</td></tr>'
    '<tr><td><b>value</b></td><td class="mono">green</td><td><b>how</b> to change it</td></tr>'
    '</table>',
    sub("A class selector starts with a dot: <span class=\"codeline\">.big { &#8230; }</span> styles every element with <span class=\"codeline\">class=\"big\"</span>.", "max-width:60ch;margin-top:.7rem"),
    ar("CSS بيحدد أنهي جزء (المحدِّد selector)، وإيه اللي يتغير (الخاصية property)، وإزاي (القيمة value). ومحدِّد الـ class بيبدأ بنقطة.")))

A(s("",
    eyebrow("5 &#183; Decorating a button (1)"),
    h2("Colours and size"),
    '<div class="rise twocol"><div>'
    '<div class="code" style="font-size:clamp(11px,1.3vw,17px)">' + hl('button {\n  background-color: #2D7A4B;\n  color: white;\n  font-size: 20px;\n}') + '</div></div><div>'
    '<table><tr><th>Before</th><th>After</th></tr><tr>'
    '<td><button type="button" style="font:14px Arial">Sign up</button></td>'
    '<td><button type="button" style="background-color:#2D7A4B;color:#fff;font-size:20px;border:1px solid #2D7A4B">Sign up</button></td></tr></table>'
    '<ul class="check" style="margin-top:.6rem">'
    '<li class="reveal rv"><span class="codeline">color</span> or <span class="codeline">background-color</span> &#8212; which one colours the text? <span class="ans">&#8212; <b>color</b>. background-color fills behind it.</span></li>'
    '</ul></div></div>',
    ar("background-color بيلوّن خلفية الزرار، و color بيلوّن الكلام، و font-size بيكبّر الخط.")))

A(s("",
    eyebrow("5 &#183; Decorating a button (2)"),
    h2("Space inside, round corners"),
    '<div class="rise twocol"><div>'
    '<div class="code" style="font-size:clamp(11px,1.3vw,17px)">' + hl('button {\n  background-color: #2D7A4B;\n  color: white;\n  padding: 12px 28px;\n  border-radius: 30px;\n}') + '</div></div><div>'
    '<table><tr><th>Property</th><th>Result</th></tr>'
    '<tr><td><b class="mono">padding</b></td><td>space <b>inside</b> the button, around the text</td></tr>'
    '<tr><td><b class="mono">border-radius</b></td><td>rounds the corners</td></tr></table>'
    '<div class="preview" style="margin-top:.8rem;text-align:center">'
    '<button type="button" style="background-color:#2D7A4B;color:#fff;padding:12px 28px;border-radius:30px;border:0;font:600 18px Inter,sans-serif">Sign up</button></div>'
    '</div></div>',
    ar("padding بيعمل مسافة جوّه الزرار حوالين الكلام، و border-radius بيدوّر الأركان.")))

A(s("",
    eyebrow("5 &#183; Adding borders"),
    h2("border: width, style, colour"),
    codebox('.card {\n  border: 3px solid #7A3B69;\n  border-radius: 12px;\n  padding: 16px;\n}', "font-size:clamp(12px,1.45vw,19px)"),
    '<div class="rise" style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:.4rem">'
    '<div class="preview" style="border:3px solid #7A3B69;border-radius:12px">solid</div>'
    '<div class="preview" style="border:3px dashed #7A3B69;border-radius:12px">dashed</div>'
    '<div class="preview" style="border:3px dotted #7A3B69;border-radius:12px">dotted</div>'
    '</div>',
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">In <span class="codeline">border: 2px dashed red</span>, what are the three parts? <span class="ans">&#8212; the width <b>2px</b>, the style <b>dashed</b>, the colour <b>red</b>.</span></li>'
    '</ul>',
    ar("border بياخد تلات حاجات: السُمك، والنوع (solid أو dashed أو dotted)، واللون.")))

A(s("",
    eyebrow("5 &#183; Try it"),
    h2("Decorate the button yourself"),
    live('<button>Sign up</button>\n\n<style>\n  button {\n    background-color: green;\n    color: white;\n    font-size: 20px;\n  }\n</style>', 9),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>Add <span class="codeline">padding: 12px 28px;</span></li>'
    '<li>Add <span class="codeline">border-radius: 30px;</span></li>'
    '<li>Add a border: <span class="codeline">border: 3px solid black;</span> &#8212; then try <span class="codeline">dashed</span>.</li>'
    '</ul>',
    ar("زوّد كل سطر جوّه أقواس button وشوف الزرار بيتغير إزاي.")))

A(s("",
    eyebrow("5 &#183; Your turn"),
    h2("Predict, then check"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv"><span class="codeline">color: red;</span> on a button changes&#8230; <span class="ans">&#8212; the colour of its <b>text</b>.</span></li>'
    '<li class="reveal rv"><span class="codeline">padding: 30px;</span> makes the button&#8230; <span class="ans">&#8212; <b>bigger</b>: more space inside.</span></li>'
    '<li class="reveal rv"><span class="codeline">border-radius: 0;</span> gives&#8230; <span class="ans">&#8212; <b>sharp</b> corners.</span></li>'
    '<li class="reveal rv">To style only buttons with <span class="codeline">class="big"</span>, the selector is&#8230; <span class="ans">&#8212; <b>.big</b> (with a dot).</span></li>'
    '</ul>',
    ar("توقّع الأول، وبعدين دوس وشوف.")))

# ---------------- part 6: Qureo 36, comprehension check ----------------

A(s("dark",
    '<div class="rise part">6</div>',
    h2("Comprehension check: chapters 34 and 35"),
    sub("Qureo chapter 36 reviews HTML (2) and CSS (2). Put them together: build a sign-up card.", "max-width:56ch"),
    ar("الجزء السادس: الفصل 36 — مراجعة الفصلين 34 و 35. هنجمعهم ونبني كارت تسجيل.")))

A(s("",
    eyebrow("6 &#183; Mini project"),
    h2("A sign-up card"),
    live('<div class="card">\n  <h2>Science Club</h2>\n  <p>Join us on <span class="hot">Thursday</span>!</p>\n  <input type="text" placeholder="Your name">\n  <button>Sign up</button>\n</div>\n\n<style>\n  .card {\n    border: 3px solid #7A3B69;\n    border-radius: 12px;\n    padding: 16px;\n  }\n</style>', 12),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>Style the button: a background colour, white text, padding, round corners.</li>'
    '<li>Make <span class="codeline">.hot</span> red and bold: <span class="codeline">color: red; font-weight: bold;</span></li>'
    '<li>Give the card a background colour of your own.</li>'
    '</ul>',
    ar("مشروع صغير: كارت تسجيل فيه div و span و input و button، ونسّقه بـ CSS. نفّذ المهام التلاتة.")))

A(s("",
    eyebrow("6 &#183; Review &#183; your turn"),
    h2("HTML and CSS, quick-fire"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">The tag for a text box&#8230; <span class="ans">&#8212; <b>&lt;input&gt;</b>.</span></li>'
    '<li class="reveal rv">The tag that marks a range inside a sentence&#8230; <span class="ans">&#8212; <b>&lt;span&gt;</b>.</span></li>'
    '<li class="reveal rv">In <span class="codeline">p { color: blue; }</span>, the property is&#8230; <span class="ans">&#8212; <b>color</b> (p is the selector, blue the value).</span></li>'
    '<li class="reveal rv">The property that adds space inside a button&#8230; <span class="ans">&#8212; <b>padding</b>.</span></li>'
    '<li class="reveal rv">HTML, CSS or JavaScript: making the button count sign-ups&#8230; <span class="ans">&#8212; <b>JavaScript</b>: that is behavior.</span></li>'
    '</ul>',
    ar("مراجعة سريعة: فكّر في كل سطر الأول، وبعدين دوس عليه.")))

A(s("dark",
    eyebrow("Remember these"),
    h2("What we learned"),
    '<ul class="rise check">'
    '<li><b>HTML</b> structures, <b>CSS</b> styles, <b>JavaScript</b> behaves &#8212; a page uses them in combination.</li>'
    '<li><b>Semantic HTML</b> (&lt;header&gt;, &lt;nav&gt;, &lt;main&gt;, &lt;footer&gt;) helps accessibility and SEO.</li>'
    '<li><b>Responsive design</b> fits every screen; <b>mobile-first</b> starts with phones. <b>Frameworks</b> give ready-made parts.</li>'
    '<li>HTML (2): <b>div</b> and <b>span</b> mark ranges; <b>input</b> and <b>button</b> let the user type and press.</li>'
    '<li>CSS (2): <b>selector { property: value; }</b> &#8212; background-color, color, padding, border-radius, border.</li>'
    '</ul>',
    ar("HTML بيبني، CSS بينسّق، JavaScript بيتفاعل • HTML الدلالي للوصول ومحركات البحث • التصميم المتجاوب وأطر العمل • div و span و input و button • والـ CSS: محدِّد وخاصية وقيمة.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 11"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 11 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers lesson 3-3 and Qureo chapters 34 to 36. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس 3-3 والفصول من 34 لـ 36 على المنصة. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))


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

/* lecture 11's drawings */
.statement.def{font-size:clamp(18px,2.15vw,30px); line-height:1.28; max-width:46ch}
/* code cards, as lecture 8; no ligatures, so >= reads as typed */
.code{display:block; background:var(--ink); color:#E6EDF3; text-align:left; padding:clamp(12px,1.7vw,22px); border-radius:12px; margin:.9rem 0 .4rem; font-family:"JetBrains Mono",monospace; font-size:clamp(13px,1.6vw,21px); line-height:1.6; white-space:pre; overflow-x:auto; max-width:100%}
.code .k,.tcode .k{color:#FF9D7A} .code .s,.tcode .s{color:#8FE3D6} .code .n,.tcode .n{color:#F7C66B} .code .f,.tcode .f{color:#9DC7FF} .code .c,.tcode .c{color:#7C8B99}
.code,.tcode,.mono,.codeline,code,.qcode{font-variant-ligatures:none; font-feature-settings:"liga" 0,"calt" 0}
.codeline{display:inline-block; background:var(--ink); color:#8FE3D6; padding:.25em .6em; border-radius:7px; font-family:"JetBrains Mono",monospace; font-size:.9em}
.part{font:600 clamp(46px,9vw,120px)/1 Fraunces,serif; color:var(--gold)}
.tbtns{display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.5rem}
.tbtns button{font:inherit; font-size:clamp(13px,1.35vw,17px); font-weight:600; border-radius:9px; padding:.5em 1em; cursor:pointer; background:var(--teal); color:#fff; border:1px solid var(--teal)}
.tbtns button.alt{background:#fff; color:var(--ink); border-color:var(--line)}
.tbtns button:disabled{opacity:.4; cursor:default}
@media print{.tbtns{display:none}}.tlbl{font-size:clamp(12px,1.25vw,16px); font-weight:600; color:var(--soft); margin-bottom:.3rem}
/* the live demos */
.lbtns{display:flex; gap:.45rem; flex-wrap:wrap; margin:.5rem 0 .7rem}
.lbtns button{font:inherit; font-size:clamp(13px,1.35vw,17px); font-weight:600; border-radius:9px; padding:.5em 1em; cursor:pointer; background:#fff; color:var(--ink); border:2px solid var(--line)}
.lbtns button.on{border-color:var(--teal); background:var(--teal-pale); color:var(--teal)}
.lnote{margin-top:.7rem; font-size:clamp(13px,1.45vw,19px); min-height:3.2em; line-height:1.45; color:var(--ink)}
.lnote .ar{display:block; margin-top:.25em; color:var(--soft); direction:rtl}
/* layers: the same page, three stages */
.dpage{background:#fff; border:1px solid var(--line); border-radius:12px; overflow:hidden; max-width:640px; min-height:150px; transition:all .4s}
.layers[data-stage="html"] .dpage{font-family:"Times New Roman",Times,serif; color:#000; padding:.6rem .9rem}
.layers[data-stage="html"] .dp-head b{font-size:1.4em}
.layers[data-stage="html"] .dp-body h4{font-size:1.1em; margin:.4rem 0}
.layers[data-stage="html"] .dp-btn{font:13px Arial,sans-serif; padding:2px 6px; border:1px solid #767676; border-radius:2px; background:#EFEFEF; color:#000}
.layers:not([data-stage="html"]) .dpage{font-family:Inter,system-ui,sans-serif}
.layers:not([data-stage="html"]) .dp-head{background:var(--teal); color:#fff; padding:.7rem 1rem; font-size:1.2em}
.layers:not([data-stage="html"]) .dp-body{padding:.8rem 1rem}
.layers:not([data-stage="html"]) .dp-body h4{color:var(--teal); font-size:1.2em; margin-bottom:.3rem}
.layers:not([data-stage="html"]) .dp-body p{color:var(--soft); margin-bottom:.6rem}
.layers:not([data-stage="html"]) .dp-btn{font:inherit; font-weight:700; background:var(--gold); color:#fff; border:0; border-radius:999px; padding:.55em 1.3em; cursor:pointer}
.layers:not([data-stage="html"]) .dp-count{font-weight:600; color:var(--ink); margin-left:.6rem}
.layers[data-stage="js"] .dp-btn{box-shadow:0 0 0 4px var(--gold-pale)}
/* responsive: one layout, three widths */
.rframe{background:#fff; border:2px solid var(--ink); border-radius:16px; padding:.7rem; margin:0 auto; transition:max-width .45s ease}
.resp[data-w="phone"] .rframe{max-width:240px}
.resp[data-w="tablet"] .rframe{max-width:440px}
.resp[data-w="pc"] .rframe{max-width:760px}
.rhead{background:var(--teal); color:#fff; font-weight:700; border-radius:8px; padding:.45rem .7rem; margin-bottom:.6rem}
.rgrid{display:grid; gap:.5rem; grid-template-columns:repeat(3,1fr)}
.resp[data-w="tablet"] .rgrid{grid-template-columns:repeat(2,1fr)}
.resp[data-w="phone"] .rgrid{grid-template-columns:1fr}
.rc{background:var(--teal-pale); border-radius:8px; padding:.6rem; text-align:center}
.rc b{display:block; color:var(--ink)} .rc span{color:var(--soft); font-size:.9em}
/* the live editor */
.live{display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:clamp(12px,1.8vw,24px); margin-top:.7rem; align-items:start}
@media(max-width:760px){.live{grid-template-columns:1fr}}
.live textarea{width:100%; font-family:"JetBrains Mono",monospace; font-size:clamp(12px,1.35vw,17px); line-height:1.55; background:var(--ink); color:#E6EDF3; border:0; border-radius:12px; padding:.8rem; resize:vertical; font-variant-ligatures:none}
.live iframe{width:100%; height:clamp(160px,30vh,300px); background:#fff; border:2px solid var(--line); border-radius:12px}
.twocol{display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:clamp(14px,2vw,30px); align-items:start; margin-top:.6rem}
@media(max-width:760px){.twocol{grid-template-columns:1fr}}
.preview{background:#fff; border:2px solid var(--line); border-radius:12px; padding:.8rem 1rem; font-family:Inter,system-ui,sans-serif}
@media print{.lbtns,.tbtns{display:none}}

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
BASE = "scripts/lecture11_slides_base.html"
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
LECTURE_JS = '/* ---- the live demos (lecture 11) -------------------------------------------\n   .layers: the same small page as HTML only, then with CSS, then with\n   JavaScript (only then does its button count). .resp: one layout at phone,\n   tablet and PC width. .live: an editor whose preview is a sandboxed frame\n   (sandbox="" -- nothing typed there can run a script), redrawn as you type.\n   Keys and swipes inside a demo stay there, so typing a space or an arrow\n   does not also turn the slide. */\n(function(){\n  if(!document.querySelectorAll) return;\n  function keep(el){\n    [\'keydown\', \'touchstart\', \'touchend\'].forEach(function(ev){\n      el.addEventListener(ev, function(e){\n        var t = e.target && e.target.tagName;\n        if(ev !== \'keydown\' || t === \'TEXTAREA\' || (t === \'BUTTON\' && (e.key === \' \' || e.key === \'Enter\'))) e.stopPropagation();\n      }, {passive: true});\n    });\n  }\n  function note(box, en, ar){\n    var n = box.querySelector(\'.lnote\');\n    if(!n) return;\n    n.querySelector(\'.en\').textContent = en;\n    n.querySelector(\'.ar\').textContent = ar;\n  }\n\n  var STAGES = {\n    html: [\'HTML only: the content and its structure — a heading, a paragraph, a button. No colours, and the button does nothing.\',\n           \'HTML بس: المحتوى وبنيته — عنوان وفقرة وزرار. مفيش ألوان، والزرار مش بيعمل حاجة.\'],\n    css:  [\'+ CSS: the same content, now with colours, spacing and a styled button. The button still does nothing.\',\n           \'+ CSS: نفس المحتوى، بس بقى فيه ألوان ومسافات وزرار متنسّق. والزرار لسه مش بيعمل حاجة.\'],\n    js:   [\'+ JavaScript: now the button responds. Press it, and the number goes up.\',\n           \'+ JavaScript: دلوقتي الزرار بيستجيب. دوس عليه والرقم هيزيد.\']\n  };\n  document.querySelectorAll(\'.layers\').forEach(function(box){\n    var count = 0, btn = box.querySelector(\'.dp-btn\'), out = box.querySelector(\'.dp-count\');\n    function set(s){\n      box.setAttribute(\'data-stage\', s);\n      /* without JavaScript the button does nothing, so the count starts over */\n      if(s !== \'js\'){ count = 0; out.textContent = \'0 signed up\'; }\n      box.querySelectorAll(\'.lbtns button\').forEach(function(b){ b.classList.toggle(\'on\', b.getAttribute(\'data-s\') === s); });\n      note(box, STAGES[s][0], STAGES[s][1]);\n    }\n    box.querySelectorAll(\'.lbtns button\').forEach(function(b){\n      b.addEventListener(\'click\', function(){ set(b.getAttribute(\'data-s\')); });\n    });\n    btn.addEventListener(\'click\', function(){\n      if(box.getAttribute(\'data-stage\') !== \'js\') return;\n      count++;\n      out.textContent = count + \' signed up\';\n    });\n    keep(box);\n    set(\'html\');\n  });\n\n  var WIDTHS = {\n    phone:  [\'Phone: the three boxes stack in one column, so nothing is too small to read.\',\n             \'موبايل: الصناديق التلاتة بتترص تحت بعض في عمود واحد، فمفيش حاجة صغيرة أوي.\'],\n    tablet: [\'Tablet: two boxes side by side, the third below.\',\n             \'تابلت: صندوقين جنب بعض، والتالت تحتهم.\'],\n    pc:     [\'PC: there is room for all three boxes in one row.\',\n             \'كمبيوتر: فيه مكان للتلات صناديق في صف واحد.\']\n  };\n  document.querySelectorAll(\'.resp\').forEach(function(box){\n    function set(w){\n      box.setAttribute(\'data-w\', w);\n      box.querySelectorAll(\'.lbtns button\').forEach(function(b){ b.classList.toggle(\'on\', b.getAttribute(\'data-w\') === w); });\n      note(box, WIDTHS[w][0], WIDTHS[w][1]);\n    }\n    box.querySelectorAll(\'.lbtns button\').forEach(function(b){\n      b.addEventListener(\'click\', function(){ set(b.getAttribute(\'data-w\')); });\n    });\n    keep(box);\n    set(\'pc\');\n  });\n\n  var BASE = \'<style>body{font:16px/1.5 Inter,Arial,sans-serif;margin:12px;color:#16233F}</style>\';\n  document.querySelectorAll(\'.live\').forEach(function(box){\n    var ta = box.querySelector(\'textarea\'), fr = box.querySelector(\'iframe\'), timer = null;\n    function draw(){ fr.srcdoc = BASE + ta.value; }\n    ta.addEventListener(\'input\', function(){\n      if(timer) clearTimeout(timer);\n      timer = setTimeout(draw, 250);\n    });\n    box.querySelector(\'.lreset\').addEventListener(\'click\', function(){ ta.value = ta.defaultValue; draw(); });\n    keep(box);\n    draw();\n  });\n})();'
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

