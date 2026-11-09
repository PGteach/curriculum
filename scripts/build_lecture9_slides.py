# -*- coding: utf-8 -*-
"""Build Lecture 9's deck.

    python scripts/build_lecture9_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/lecture9_slides_base.html and writes lecture9/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the side drawings
added. Always starts from the base, never from the published deck.

Two parts, as the ministry's plan pairs a book lesson with the Japanese
platform each week. Part one is Lesson 3-1, The Overall Structure of Web
Applications, the English textbook pp. 56-61, and nothing outside the
curriculum. Where the Arabic textbook and the ministry's assessment book go
further, the deck follows them: the three tiers are a simplified teaching
model and real structures can differ; some web applications can also be
installed; which tier sends the request to the database. Part two is Qureo
chapter 31, Functions (4): a function that adds two values, adds three, and
compares three, in Qureo's own terms (argument, return value).

Everything but the content is lecture 5's builder, unchanged -- this file was
derived from it. The Arabic follows the Arabic textbook's lesson 3-1 point by
point, said in Egyptian Arabic, with the book's own terms kept as they are.
The two step-by-step players (the request flow and the code tracer) are this
lecture's own; their script is tools/lecture9/script.js, added to the page's own script.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "lecture9/slides/index.html"


# --------------------------------------------------------------------------
# diagrams -- inline SVG, coloured from the page's CSS variables so they follow
# LECTURE_ACCENT. Labels only, never the sentence that explains them; no label
# under 14 units. Fills are #fff, never var(--white): the booklet template
# does not define --white. The booklet reads these out of this file.
# --------------------------------------------------------------------------

TIERS = '''
<svg viewBox="0 0 900 250" role="img" aria-label="The three tiers of a web application: the frontend, the backend and the database. A request goes from the frontend to the backend to the database, and the reply comes back the other way">
  <g font-size="15" text-anchor="middle">
    <rect x="20" y="40" width="230" height="150" rx="14" fill="#fff" stroke="var(--teal)" stroke-width="3"/>
    <text x="135" y="88" font-size="30">&#128187;</text>
    <text x="135" y="122" font-size="20" font-weight="700" fill="var(--ink)">Frontend</text>
    <text x="135" y="146" fill="var(--soft)">runs on the browser</text>
    <text x="135" y="170" font-weight="600" fill="var(--teal)">shows and collects</text>
    <rect x="335" y="40" width="230" height="150" rx="14" fill="#fff" stroke="var(--gold)" stroke-width="3"/>
    <text x="450" y="88" font-size="30">&#9881;</text>
    <text x="450" y="122" font-size="20" font-weight="700" fill="var(--ink)">Backend</text>
    <text x="450" y="146" fill="var(--soft)">runs on the server</text>
    <text x="450" y="170" font-weight="600" fill="var(--gold)">decides and processes</text>
    <rect x="650" y="40" width="230" height="150" rx="14" fill="#fff" stroke="var(--ink)" stroke-width="3"/>
    <text x="765" y="88" font-size="30">&#128451;</text>
    <text x="765" y="122" font-size="20" font-weight="700" fill="var(--ink)">Database</text>
    <text x="765" y="146" fill="var(--soft)">organizes the data</text>
    <text x="765" y="170" font-weight="600" fill="var(--ink)">stores and retrieves</text>
    <line x1="256" y1="92" x2="322" y2="92" stroke="var(--teal)" stroke-width="3"/><polygon points="330,92 318,85 318,99" fill="var(--teal)"/>
    <line x1="571" y1="92" x2="637" y2="92" stroke="var(--teal)" stroke-width="3"/><polygon points="645,92 633,85 633,99" fill="var(--teal)"/>
    <line x1="329" y1="140" x2="264" y2="140" stroke="var(--gold)" stroke-width="3"/><polygon points="256,140 268,133 268,147" fill="var(--gold)"/>
    <line x1="644" y1="140" x2="579" y2="140" stroke="var(--gold)" stroke-width="3"/><polygon points="571,140 583,133 583,147" fill="var(--gold)"/>
    <text x="293" y="80" font-size="14" fill="var(--teal)">request</text>
    <text x="293" y="164" font-size="14" fill="var(--gold)">reply</text>
    <text x="608" y="80" font-size="14" fill="var(--teal)">request</text>
    <text x="608" y="164" font-size="14" fill="var(--gold)">reply</text>
    <text x="450" y="232" font-weight="600" fill="var(--ink)">three tiers cooperating = one web application</text>
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


def v_apps():
    tiles = [("&#9654;", "Video sharing", "watch and search"), ("&#128722;", "Online shop", "buy and pay"),
             ("&#9993;", "Web e-mail", "read and send"), ("&#128506;", "Web maps", "find the way")]
    out = "".join('<div class="tile" style="animation-delay:%.2fs"><span>%s</span><b>%s</b><i>%s</i></div>'
                  % (.3 + .3 * k, ico, t, i) for k, (ico, t, i) in enumerate(tiles))
    return ('<aside class="rise viz"><div class="tiles">' + out + '</div>'
            + vcap("All used through a browser.",
                   "كلها بنستخدمها من خلال المتصفح.")
            + '</aside>')


def v_restaurant():
    rows = [("&#129333;", "Waiter", "takes your order, brings the plate", "Frontend"),
            ("&#128104;&#8205;&#127859;", "Kitchen", "hidden; decides and cooks", "Backend"),
            ("&#129482;", "Storeroom", "keeps the food, hands it over", "Database")]
    out = "".join('<div class="drow" style="animation-delay:%.2fs"><span class="dico">%s</span>'
                  '<span class="dt"><b>%s</b><br><small>%s</small></span>'
                  '<span class="darrow">&#8594;</span><span class="dai">%s</span></div>'
                  % (.4 + .5 * k, ico, t, why, tier) for k, (ico, t, why, tier) in enumerate(rows))
    return ('<aside class="rise viz">' + out
            + vcap("A way to remember the three tiers.",
                   "طريقة تفتكر بيها الطبقات التلاتة.")
            + '</aside>')


def v_clinic():
    return ('<aside class="rise viz"><div class="shopv">'
            '<div class="sv sv1"><span>&#128197;</span><b>Booking form</b><i>which tier?</i></div>'
            '<div class="sv sv2"><span>&#9200;</span><b>Free time slots</b><i>which tier checks?</i></div>'
            '<div class="sv sv3"><span>&#128451;</span><b>Past visits</b><i>which tier stores?</i></div>'
            '</div>'
            + vcap("Give each job to one tier.",
                   "ادّي كل مهمة لطبقة.")
            + '</aside>')


def v_machine():
    return ('<aside class="rise viz"><div class="shopv">'
            '<div class="sv sv1"><span>&#127822;</span><b>In: the arguments</b><i>the values you give it</i></div>'
            '<div class="sv sv2"><span>&#9881;</span><b>Inside: the processing</b><i>the code between { }</i></div>'
            '<div class="sv sv3"><span>&#129380;</span><b>Out: the return value</b><i>what return sends back</i></div>'
            '</div>'
            + vcap("A function is a juice machine.",
                   "الدالة زي ماكينة العصير.")
            + '</aside>')


# heading text (unique to one slide) -> its drawing
VIZ = {
    "Before you read on": v_timer,
    "What is a web application?": v_apps,
    "A way to remember: a restaurant": v_restaurant,
    "A clinic wants a booking app": v_clinic,
    "A function is a small machine": v_machine,
}
VIZ_USED = []


# ---------------- the step-by-step players ----------------
# Both are plain data: the builder writes the steps into data-steps, and
# script.js (added to the page's own script) plays them one press at a time.

def _steps_attr(steps):
    import html as _h, json as _j
    return _h.escape(_j.dumps(steps, ensure_ascii=False), quote=True)


def _buttons():
    return ('<div class="tbtns"><button type="button" class="nx">Next step &#9654;</button>'
            '<button type="button" class="alt pl">Play all</button>'
            '<button type="button" class="alt rs">&#8634; Again</button></div>')


def flow(steps):
    """The request flow across the three tiers. Each step lights one tier
    and shows what is passed on: {"t": "fe"|"be"|"db", "msg", "en", "ar"}."""
    tiers = [("fe", "&#128187;", "Frontend", "the screen"), ("be", "&#9881;", "Backend", "the server"),
             ("db", "&#128451;", "Database", "the data")]
    return ('<div class="rise stepper flowcol" data-kind="flow" data-steps="%s">'
            '<div class="tiers">%s</div><p class="packet"></p>'
            '<p class="tstat"><span class="en"></span><span class="ar"></span></p>%s</div>'
            % (_steps_attr(steps),
               "".join('<div class="tier" data-t="%s"><div class="ti">%s</div><b>%s</b><small>%s</small></div>'
                       % (k, ico, n, d) for k, ico, n, d in tiers),
               _buttons()))


def tracer(lines, boxes, steps, boxlabel="The values inside"):
    """A code tracer. lines: the code, already coloured, one string a line.
    boxes: the names whose values are shown. Each step may light a line
    ("ln", counted from 0), set values ("set"), print a line ("out"), and
    says what happened ("en", "ar")."""
    return ('<div class="rise stepper" data-kind="code" data-steps="%s">'
            '<div><div class="tcode">%s</div><div class="tcons"><span class="lbl">Console &#8212; what prints</span></div></div>'
            '<div><div class="tlbl">%s</div><div class="boxes">%s</div>'
            '<p class="tstat"><span class="en"></span><span class="ar"></span></p>%s</div></div>'
            % (_steps_attr(steps),
               "".join('<span class="ln">%s</span>' % (l if l else " ") for l in lines),
               boxlabel,
               "".join('<div class="box" data-k="%s"><span>%s =</span><b>?</b></div>' % (b, b) for b in boxes),
               _buttons()))




def K(t): return '<span class="k">%s</span>' % t
def S_(t): return '<span class="s">%s</span>' % t
def Nn(t): return '<span class="n">%s</span>' % t
def F(t): return '<span class="f">%s</span>' % t
LOG = F("console.log")


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
    h2("What happens when you click?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("You search YouTube, buy something online, open your e-mail. Behind one simple screen, three parts work together. Today: what they are &#8212; and, on the platform, functions that add and compare values.",
        "max-width:58ch;margin-top:1rem"),
    ar("بتدوّر على يوتيوب، بتشتري أونلاين، بتفتح الإيميل. ورا الشاشة البسيطة دي فيه تلات أجزاء شغالين مع بعض. النهارده هنعرف هما إيه — وعلى المنصة: دوال بتجمع وبتقارن القيم.")))

# 2 unit 3 opens
A(s("",
    eyebrow("Unit 3 &#183; Web applications"),
    h2("A new unit: how the web works", "max-width:24ch"),
    '<div class="rise timeline">'
    '<div class="tl"><h3>3-1 &#183; The overall structure of web applications</h3><p>Today: the three tiers, and how they cooperate</p></div>'
    '<div class="tl"><h3>3-2 &#183; Web application communication methods</h3><p>How the parts talk to each other</p></div>'
    '<div class="tl"><h3>3-3 &#183; Fundamentals of frontend technology</h3><p>HTML, CSS and JavaScript &#8212; what you write on the platform</p></div>'
    '</div>',
    sub("Unit 2 was about protecting systems. Unit 3 asks how the services you use every day are built.", "max-width:58ch;margin-top:.9rem"),
    ar("الوحدة التالتة: تطبيقات الويب. 3-1 البنية العامة لتطبيقات الويب (النهارده)، 3-2 طرق اتصال تطبيقات الويب، 3-3 أساسيات تكنولوجيا الواجهة الأمامية.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("This is already in your hand"),
    h2("Every time you go online", "max-width:22ch"),
    '<div class="rise fields">'
    '<span class="chip">&#9654; search on YouTube</span>'
    '<span class="chip">&#128722; buy on Amazon</span>'
    '<span class="chip">&#9993; open Gmail</span>'
    '<span class="chip">&#128506; find a place on Google Maps</span>'
    '</div>',
    sub("&#8230; you are using a <b>web application</b> &#8212; a program you use through your browser. Behind the simple screen, three tiers work together: the page you touch, a hidden server that processes your request, and a database that holds all the data.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> when you search YouTube, where do you think the videos are kept &#8212; on your phone, or somewhere else? Remember your answer.</p></div>',
    ar("لما بتدوّر في موقع فيديو، أو بتتسوق أونلاين، أو بتستخدم إيميل على الويب، إنت بتستخدم تطبيق ويب. وورا اللي بتشوفه فيه أجزاء مختلفة شغالة مع بعض.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("How is a web application structured, and how do its three tiers work together to respond to what a user does?",
       "max-width:28ch"),
    ar("السؤال الرئيسي: إزاي بيتبني تطبيق الويب، وإزاي طبقاته التلاتة بتشتغل مع بعض عشان تستجيب للي المستخدم بيعمله؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map &#183; four parts"),
    h2("Three parts from the book, one on the platform", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#127760;</div><div class="role">Part 1</div>'
    '<h3>Web application</h3><p>What it is</p></div>'
    '<div class="card"><div class="ico">&#127970;</div><div class="role">Part 2</div>'
    '<h3>Three tiers</h3><p>Frontend, backend, database</p></div>'
    '<div class="card"><div class="ico">&#128260;</div><div class="role">Part 3</div>'
    '<h3>Working together</h3><p>From your click to the result</p></div>'
    '<div class="card"><div class="ico">&#129380;</div><div class="role">Part 4 &#183; Qureo</div>'
    '<h3>Functions (4)</h3><p>Add and compare values</p></div>'
    '</div>',
    ar("خريطة المحاضرة: 1 يعني إيه تطبيق ويب. 2 الطبقات التلاتة. 3 إزاي بيتعاونوا من ضغطتك لحد النتيجة. 4 على المنصة: الدوال (4).")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("You type <b>red shoes</b> in the search box of a shopping site and press Enter. A second later, a page of red shoes appears.",
        "max-width:56ch;margin-top:1rem"),
    sub("With your partner: <b>who read your words? who found the shoes? where were the shoes kept?</b> Write three guesses.",
        "max-width:56ch;margin-top:.8rem"),
    sub("Keep your guesses. Part 3 shows the book&#8217;s answer, step by step.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: كتبت «red shoes» في موقع تسوق ودوست Enter، وبعد ثانية ظهرت صفحة جزم حمرا. مين قرا الكلام؟ ومين لقى الجزم؟ والجزم كانت متخزنة فين؟ اكتبوا تلات تخمينات.")))

# ---------------- part 1: what is a web application ----------------

A(s("",
    eyebrow("Part 1 &#183; What is a web application?"),
    h2("What is a web application?", "max-width:24ch"),
    '<div class="rise statement def"><em>Web application</em> &#8212; an application used through a web browser. You can use it as long as you have a browser, without installing dedicated software.</div>',
    sub("<i>e.g.</i> YouTube, Amazon, Gmail, Google Maps.", "max-width:58ch;margin-top:.8rem"),
    sub("The Arabic book adds: some web applications can <b>also</b> be installed on the device.", "max-width:58ch;margin-top:.5rem;color:var(--soft)"),
    ar("تطبيق الويب: تطبيق بيتستخدم عادةً من خلال متصفح الويب، وبعض تطبيقات الويب ممكن كمان تتثبت على الجهاز. أمثلة: خدمات الفيديو والتسوق والبريد والخرائط على الويب.")))

A(s("",
    eyebrow("1 &#183; Your turn"),
    h2("Which one is a web application?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">A video player on the device <span class="ans">&#8212; <b>no</b>: it runs on the device, not through a browser.</span></li>'
    '<li class="reveal rv">A maps website on the Internet <span class="ans">&#8212; <b>yes</b>: you use it through the browser.</span></li>'
    '<li class="reveal rv">A calculator app on the desktop <span class="ans">&#8212; <b>no</b>: installed on the computer.</span></li>'
    '<li class="reveal rv">A photo-editing program <span class="ans">&#8212; <b>no</b>: installed software.</span></li>'
    '</ul>',
    sub("Think first, then tap each one.", "margin-top:.7rem;color:var(--soft)"),
    ar("أنهي واحد تطبيق ويب؟ موقع خرائط على الإنترنت — لأنه بيتستخدم من خلال المتصفح. الباقي برامج متثبتة على الجهاز.")))

# ---------------- part 2: the three tiers ----------------

A(s("",
    eyebrow("Part 2 &#183; The three tiers of a web application"),
    h2("Three tiers, one application"),
    fig(TIERS),
    sub("A web application is broadly built from <b>three tiers</b>: the <b>frontend</b>, the <b>backend</b> and the <b>database</b>. This is called the <b>three-tier architecture</b>.",
        "max-width:62ch;margin-top:.3rem"),
    ar("في النموذج التعليمي ده، بنقسم تطبيق الويب لتلات أجزاء رئيسية: الواجهة الأمامية، والواجهة الخلفية، وقاعدة البيانات — ودي اسمها بنية الطبقات الثلاث.")))

A(s("",
    eyebrow("2 &#183; What each tier does"),
    h2("Who does what?"),
    '<table class="rise">'
    '<tr><th>Tier</th><th>Role</th><th>Examples</th></tr>'
    '<tr><td><b>Frontend</b></td><td>The screen users see directly. It runs on the browser and accepts user input.</td><td>Search screen, product listing pages, input forms</td></tr>'
    '<tr><td><b>Backend</b></td><td>The server-side processing users do not see. It processes data and makes decisions.</td><td>Searching for products that match, login authentication</td></tr>'
    '<tr><td><b>Database</b></td><td>Organizes, stores and manages data. It retrieves data when needed and records new data.</td><td>Product information, user information, order history</td></tr>'
    '</table>',
    ar("الواجهة الأمامية: الجزء اللي المستخدم بيشوفه ويتعامل معاه في المتصفح؛ بتعرض المحتوى وبتستقبل اللي بيكتبه. الواجهة الخلفية: الجزء اللي بيشتغل على الخادم، وبيعالج الطلبات ويطبق قواعد التطبيق. قاعدة البيانات: طبقة بتحفظ البيانات وتوفرها وقت الحاجة.")))

A(s("",
    eyebrow("2 &#183; A way to remember"),
    h2("A way to remember: a restaurant", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>In a restaurant</th><th>In a web application</th></tr>'
    '<tr><td>&#129333; The <b>waiter</b> you talk to: takes your order, brings your plate</td><td><b>Frontend</b> &#8212; shows and collects</td></tr>'
    '<tr><td>&#128104;&#8205;&#127859; The <b>kitchen</b> you never see: decides and cooks</td><td><b>Backend</b> &#8212; decides and processes</td></tr>'
    '<tr><td>&#129482; The <b>storeroom</b>: keeps the food, hands it over</td><td><b>Database</b> &#8212; stores and retrieves</td></tr>'
    '</table>',
    sub("The restaurant is ours, not the book&#8217;s. The three phrases on the right are the book&#8217;s &#8212; learn those.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر في مطعم: الجرسون اللي بتكلمه = الواجهة الأمامية (بتعرض وتجمع). المطبخ اللي مش بتشوفه = الواجهة الخلفية (بتقرر وتعالج). المخزن = قاعدة البيانات (بتخزن وتسترجع).")))

A(s("",
    eyebrow("2 &#183; Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">The frontend is the screen component that users see directly. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv">The backend is the part that runs on the browser. <span class="ans">&#8212; <b>false</b>: it runs on the server.</span></li>'
    '<li class="reveal rv tf-t">A database is a system that organizes, stores and manages data. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv">A web application operates with the frontend alone. <span class="ans">&#8212; <b>false</b>: it needs all three tiers.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: الواجهة الأمامية الشاشة اللي بنشوفها — صح. الواجهة الخلفية بتشتغل على المتصفح — غلط، على الخادم. قاعدة البيانات بتنظم وتخزن وتدير البيانات — صح. تطبيق الويب بيشتغل بالواجهة الأمامية لوحدها — غلط.")))

A(s("",
    eyebrow("2 &#183; Exam-style question"),
    h2("Match each description with a tier"),
    '<table class="rise">'
    '<tr><th>Description</th><th>Tier</th></tr>'
    '<tr><td>a &#183; The part responsible for server-side processing that users do not see</td><td class="reveal"><span>B &#183; Backend</span></td></tr>'
    '<tr><td>b &#183; The screen component that users interact with directly</td><td class="reveal"><span>A &#183; Frontend</span></td></tr>'
    '<tr><td>c &#183; A system that organizes, stores and manages data</td><td class="reveal"><span>C &#183; Database</span></td></tr>'
    '</table>',
    sub("Choices: <b>A</b> Frontend &#183; <b>B</b> Backend &#183; <b>C</b> Database. Answer, then tap.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("اربط كل وصف بالمصطلح المناسب: المعالجة من جانب الخادم = الواجهة الخلفية. الشاشة اللي بنتعامل معاها = الواجهة الأمامية. تخزين البيانات وإدارتها = قاعدة البيانات.")))

# ---------------- part 3: how the tiers cooperate ----------------

A(s("",
    eyebrow("Part 3 &#183; The flow of how the three tiers cooperate"),
    h2("Watch a search travel", "max-width:24ch"),
    sub("Searching for a product on an online shopping site. Press <b>Next step</b>:", "max-width:60ch;margin-top:.4rem"),
    flow([
        {"t": "fe", "msg": "red shoes", "en": "① The frontend receives the search keywords entered by the user.",
         "ar": "① الواجهة الأمامية بتستقبل كلمات البحث اللي المستخدم كتبها."},
        {"t": "be", "msg": "keywords: red shoes", "en": "② The frontend sends the search keywords to the backend.",
         "ar": "② الواجهة الأمامية بتبعت كلمات البحث للواجهة الخلفية."},
        {"t": "db", "msg": "find: red shoes", "en": "③ The backend searches the database for products that match the criteria.",
         "ar": "③ الواجهة الخلفية بتطلب من طبقة البيانات المنتجات اللي بتطابق البحث."},
        {"t": "be", "msg": "3 matching products", "en": "④ The database returns the data of the matching products to the backend.",
         "ar": "④ طبقة البيانات بترجّع النتايج المطلوبة للواجهة الخلفية."},
        {"t": "fe", "msg": "organized results", "en": "⑤ The backend organizes the search results and returns them to the frontend.",
         "ar": "⑤ الواجهة الخلفية بتجهز النتايج وتبعتها للواجهة الأمامية."},
        {"t": "fe", "msg": "on your screen", "en": "⑥ The frontend displays the search results on the user's screen.",
         "ar": "⑥ الواجهة الأمامية بتعرض نتايج البحث على شاشة المستخدم."},
    ]),
    ar("الطلب بينزل عبر الطبقات، والرد بيرجع تاني. دوس Next step وتابع الطلب خطوة خطوة.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("When you type in a search box and see results, which tier collected your input, and which tier found the answer?",
       "max-width:28ch"),
    '<ul class="rise check" style="margin-top:1rem">'
    '<li class="reveal rv">Collected your input <span class="ans">&#8212; the <b>frontend</b>.</span></li>'
    '<li class="reveal rv">Found the answer <span class="ans">&#8212; the <b>backend</b> searched the <b>database</b>, which held the data.</span></li>'
    '</ul>',
    ar("وقّف وفكّر: لما بتكتب في مربع البحث وتشوف النتايج، أنهي طبقة جمعت المدخلات، وأنهي طبقة لقت الإجابة؟")))

A(s("",
    eyebrow("3 &#183; Familiar web application configurations"),
    h2("Every service, the same three tiers", "max-width:26ch"),
    '<table class="rise">'
    '<tr><th>Service</th><th>Frontend (display, interaction)</th><th>Backend (processing, control)</th><th>Database (storage, management)</th></tr>'
    '<tr><td><b>Video sharing</b></td><td>Video playback and search screens</td><td>Choosing recommended videos; counting views</td><td>Video data, user information, viewing history</td></tr>'
    '<tr><td><b>SNS</b></td><td>Timeline and post screens; sending what you type</td><td>Deciding who sees a post; push notifications</td><td>Posts, follow relationships, messages</td></tr>'
    '<tr><td><b>E-commerce</b></td><td>Product listings and cart screens; taking orders</td><td>Checking stock; running payments</td><td>Products, order history, customer information</td></tr>'
    '</table>',
    sub("<b>Pause and think:</b> every service uses the same three tiers &#8212; what changes from one service to the next?", "max-width:62ch;margin-top:.8rem"),
    ar("تقريبًا كل خدمة على الإنترنت — الفيديو، والتواصل الاجتماعي، والتسوق — مبنية على نفس الطبقات التلاتة: واجهة أمامية بتعرض وتجمع، وواجهة خلفية بتقرر وتعالج، وقاعدة بيانات بتخزن وتسترجع.")))

A(s("",
    eyebrow("3 &#183; Your turn"),
    h2("An e-commerce site: which tier?"),
    '<table class="rise">'
    '<tr><th>Part of the site</th><th>Tier</th></tr>'
    '<tr><td>a &#183; Product listing page</td><td class="reveal"><span>A &#183; Frontend</span></td></tr>'
    '<tr><td>b &#183; Stock checking</td><td class="reveal"><span>B &#183; Backend</span></td></tr>'
    '<tr><td>c &#183; Storage of customer information</td><td class="reveal"><span>C &#183; Database</span></td></tr>'
    '<tr><td>d &#183; Cart screen</td><td class="reveal"><span>A &#183; Frontend</span></td></tr>'
    '<tr><td>e &#183; Payment processing</td><td class="reveal"><span>B &#183; Backend</span></td></tr>'
    '<tr><td>f &#183; Storage of order history</td><td class="reveal"><span>C &#183; Database</span></td></tr>'
    '</table>',
    sub("A screen &#8594; frontend. Processing &#8594; backend. Storage &#8594; database.", "max-width:58ch;margin-top:.7rem;color:var(--soft)"),
    ar("لكل جزء من موقع التجارة الإلكترونية، حدد الطبقة: شاشة ← واجهة أمامية. معالجة ← واجهة خلفية. تخزين ← قاعدة بيانات.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">The frontend has the role of storing and managing data. <span class="ans">&#8212; <b>false</b>: that is the database.</span></li>'
    '<li class="reveal rv">The backend is the part users interact with directly on the browser. <span class="ans">&#8212; <b>false</b>: that is the frontend.</span></li>'
    '<li class="reveal rv">The database has the role of displaying screens to users. <span class="ans">&#8212; <b>false</b>: the frontend displays.</span></li>'
    '<li class="reveal rv tf-t">When you search a shop, the <b>backend</b> sends the request to the database. <span class="ans">&#8212; <b>true</b>: the frontend never asks the database itself.</span></li>'
    '</ul>',
    ar("خلّي بالك: الواجهة الأمامية مش بتخزن البيانات. الواجهة الخلفية مش اللي بنتعامل معاها في المتصفح. قاعدة البيانات مش بتعرض شاشات. واللي بيبعت الطلب لقاعدة البيانات هي الواجهة الخلفية.")))

A(s("",
    eyebrow("3 &#183; Exam-style question &#183; 6 marks"),
    h2("Posting a photo on a social media app", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Explain&#8230;</h3><ul>'
    '<li>how the <b>three tiers</b> cooperate when a user posts a photo</li>'
    '<li>refer to the role of the <b>frontend</b>, the <b>backend</b> and the <b>database</b></li>'
    '</ul></div>'
    '<div class="pane b"><h3>A plan for your answer</h3><ul>'
    '<li>frontend: takes the photo and the caption, sends them</li>'
    '<li>backend: checks it, decides who sees it</li>'
    '<li>database: stores it &#8212; then the reply comes back</li>'
    '</ul></div>'
    '</div>',
    ar("سؤال على نمط الامتحان: اشرح إزاي الطبقات التلاتة لتطبيق الويب بتتعاون لما المستخدم ينشر صورة على تطبيق تواصل اجتماعي. أشِر إلى: دور الواجهة الأمامية، والواجهة الخلفية، وقاعدة البيانات.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("A clinic wants a booking app", "max-width:26ch"),
    sub("Patients book appointments, check which time slots are free, and see their past visits. You plan its three tiers.",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Assign the work.</b> The booking form, checking free time slots, storing past visits: which tier does each, and why?</li>'
    '<li><b>Diagnose a fault.</b> The booking page opens, but no free slots appear. Which tier is clearly working, and which has probably failed?</li>'
    '<li><b>Decide.</b> Should the clinic separate its app into three tiers? Two reasons. In pairs, agree where checking free slots belongs.</li>'
    '</ul>',
    sub("Stuck? The frontend shows and collects; the backend decides and processes; the database stores and retrieves.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: عيادة عايزة تطبيق ويب للحجز. وزّع المهام على الطبقات، وشخّص العطل: صفحة الحجز بتفتح بس مفيش مواعيد بتظهر. وقرّر: نفصل الطبقات ولا لأ، بسببين.")))

A(s("",
    eyebrow("In a new context"),
    h2("A weather app", "max-width:26ch"),
    sub("Users type a city and see the forecast.", "max-width:54ch;margin-top:.7rem"),
    '<table class="rise">'
    '<tr><th>Job</th><th>Tier</th></tr>'
    '<tr><td>Taking the city name</td><td class="reveal"><span>Frontend</span></td></tr>'
    '<tr><td>Looking up the forecast data</td><td class="reveal"><span>Backend</span></td></tr>'
    '<tr><td>Storing past forecasts</td><td class="reveal"><span>Database</span></td></tr>'
    '</table>',
    sub("And one job the frontend <b>cannot</b> do on its own? Discuss, then compare.", "max-width:58ch;margin-top:.8rem"),
    ar("طبّق اللي اتعلمته: تطبيق طقس بيخليك تكتب اسم مدينة وتشوف التوقعات. سمّي أنهي طبقة بتعمل كل مهمة، وحدد مهمة واحدة الواجهة الأمامية متقدرش تعملها لوحدها.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 3-1"),
    h2("Show, decide, store", "max-width:24ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> where are the YouTube videos kept? On your phone &#8212; or in a database, reached through the backend?</p>'
    '<div class="rise statement">The frontend <em>shows and collects</em>, the backend <em>decides and processes</em>, the database <em>stores and retrieves</em> &#8212; three tiers cooperating make a web application work.</div>',
    sub("The Arabic book adds: this is a simplified teaching model. Real applications can be built differently.", "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("افتكر: الواجهة الأمامية بتعرض وتجمع، والواجهة الخلفية بتقرر وتعالج، وقاعدة البيانات بتخزن وتسترجع — تلات طبقات متعاونة بتخلي تطبيق الويب يشتغل. وده نموذج تعليمي مبسط، والبنية الفعلية ممكن تختلف.")))

# ---------------- part 4: Qureo chapter 31, Functions (4) ----------------

A(s("dark",
    '<div class="rise part">4</div>',
    h2("On the platform: Functions (4)"),
    sub("Qureo chapter 31: a function that adds two values, one that adds three, and one that compares three.", "max-width:56ch"),
    ar("الجزء الرابع على المنصة: الفصل 31 — الدوال (4): دالة بتجمع قيمتين، ودالة بتجمع تلاتة، ودالة بتقارن بين تلاتة.")))

A(s("",
    eyebrow("4 &#183; Remember"),
    h2("A function is a small machine", "max-width:22ch"),
    '<div class="rise code">' + K("function") + " " + F("name") + "(argumentName) {\n  <span class=\"c\">// processing</span>\n  " + K("return") + " result;\n}</div>",
    '<table class="rise">'
    '<tr><th>Word</th><th>Meaning</th></tr>'
    '<tr><td><b>argument</b></td><td>the value you pass <b>into</b> the function</td></tr>'
    '<tr><td><b>return value</b></td><td>the value the function gives <b>back</b> with <span class="codeline">return</span></td></tr>'
    '</table>',
    sub("Like the tiers: <b>receive</b> &#8594; <b>process</b> &#8594; <b>give back</b>.", "max-width:56ch;margin-top:.7rem"),
    ar("الدالة زي ماكينة العصير: بتحط فيها فاكهة (الوسيط)، بتشتغل جوّه (المعالجة)، وبتطلّع عصير (القيمة المرجعة) بـ return. ونفس فكرة الطبقات: تستقبل ← تعالج ← ترجّع.")))

ADD_LINES = [K("function") + " " + F("add") + "(a, b) {",
             "  " + K("return") + " a + b;",
             "}",
             "",
             LOG + "(" + F("add") + "(" + Nn("3") + ", " + Nn("5") + "));"]
A(s("",
    eyebrow("4 &#183; A function to add two values"),
    h2("add(3, 5): watch it run"),
    tracer(ADD_LINES, ["a", "b", "return"], [
        {"ln": 4, "en": "The program reaches the call add(3, 5). The function above only runs when it is called.",
         "ar": "البرنامج وصل لاستدعاء add(3, 5). الدالة اللي فوق مش بتشتغل غير لما تتنادى."},
        {"ln": 0, "set": {"a": "3", "b": "5"}, "en": "The arguments go in: a = 3 and b = 5.",
         "ar": "الوسائط بتدخل: a = 3 و b = 5."},
        {"ln": 1, "set": {"return": "8"}, "en": "a + b is 3 + 5 = 8, and return sends 8 back.",
         "ar": "‏a + b يعني 3 + 5 = 8، و return بترجّع 8."},
        {"ln": 4, "out": "8", "en": "add(3, 5) becomes its return value, 8, and console.log prints it.",
         "ar": "‏add(3, 5) بتتحول لقيمتها المرجعة 8، و console.log بيطبعها."},
    ]),
    ar("دوس Next step: الوسائط بتدخل، الدالة بتجمع، و return بترجّع النتيجة لمكان الاستدعاء.")))

A(s("",
    eyebrow("4 &#183; A function that adds three values"),
    h2("Three arguments, one return value"),
    '<div class="rise code">' + K("function") + " " + F("add3") + "(a, b, c) {\n  " + K("return") + " a + b + c;\n}\n\n"
    + LOG + "(" + F("add3") + "(" + Nn("2") + ", " + Nn("4") + ", " + Nn("6") + "));\n"
    + LOG + "(" + F("add3") + "(" + Nn("10") + ", " + Nn("20") + ", " + Nn("30") + "));</div>",
    '<ul class="rise check">'
    '<li class="reveal rv">The first line prints&#8230; <span class="ans">&#8212; <b>12</b> (2 + 4 + 6)</span></li>'
    '<li class="reveal rv">The second line prints&#8230; <span class="ans">&#8212; <b>60</b> (10 + 20 + 30)</span></li>'
    '<li class="reveal rv">How many arguments does add3 take? <span class="ans">&#8212; <b>three</b>, separated by commas.</span></li>'
    '</ul>',
    ar("نفس الفكرة بتلات وسائط مفصولين بفواصل. فكّر الأول، وبعدين دوس على كل سطر.")))

BIG_LINES = [K("function") + " " + F("biggest") + "(a, b, c) {",
             "  " + K("let") + " big = a;",
             "  " + K("if") + " (b > big) {",
             "    big = b;",
             "  }",
             "  " + K("if") + " (c > big) {",
             "    big = c;",
             "  }",
             "  " + K("return") + " big;",
             "}",
             "",
             LOG + "(" + F("biggest") + "(" + Nn("4") + ", " + Nn("9") + ", " + Nn("7") + "));"]
A(s("",
    eyebrow("4 &#183; A function that compares three values"),
    h2("Which is the biggest?"),
    tracer(BIG_LINES, ["a", "b", "c", "big", "return"], [
        {"ln": 11, "en": "The call biggest(4, 9, 7) starts the function.", "ar": "الاستدعاء biggest(4, 9, 7) بيشغّل الدالة."},
        {"ln": 0, "set": {"a": "4", "b": "9", "c": "7"}, "en": "The arguments go in: a = 4, b = 9, c = 7.", "ar": "الوسائط بتدخل: a = 4 و b = 9 و c = 7."},
        {"ln": 1, "set": {"big": "4"}, "en": "Start by saying the first one is the biggest: big = 4.", "ar": "نبدأ ونقول إن الأولاني هو الأكبر: big = 4."},
        {"ln": 2, "en": "Is b > big? 9 > 4 is true, so go inside.", "ar": "هل b > big؟ ‏9 > 4 صح، فندخل جوّه."},
        {"ln": 3, "set": {"big": "9"}, "en": "big becomes 9.", "ar": "‏big بقت 9."},
        {"ln": 5, "en": "Is c > big? 7 > 9 is false, so skip it.", "ar": "هل c > big؟ ‏7 > 9 غلط، فنعدّيها."},
        {"ln": 8, "set": {"return": "9"}, "en": "return sends back big, which is 9.", "ar": "‏return بترجّع big، اللي هي 9."},
        {"ln": 11, "out": "9", "en": "console.log prints 9, the biggest of the three.", "ar": "‏console.log بيطبع 9، أكبر واحد في التلاتة."},
    ]),
    ar("الدالة بتقارن التلات قيم بـ if — زي اللي اتعلمناه في المحاضرة 8 — وبترجّع الأكبر.")))

A(s("",
    eyebrow("4 &#183; A shortcut you already know"),
    h2("Math.max can take three values"),
    '<div class="rise code">' + LOG + "(" + F("Math.max") + "(" + Nn("4") + ", " + Nn("9") + ", " + Nn("7") + "));\n"
    + LOG + "(" + F("Math.min") + "(" + Nn("4") + ", " + Nn("9") + ", " + Nn("7") + "));</div>",
    '<ul class="rise check">'
    '<li class="reveal rv">Math.max(4, 9, 7) prints&#8230; <span class="ans">&#8212; <b>9</b>, the same as biggest.</span></li>'
    '<li class="reveal rv">Math.min(4, 9, 7) prints&#8230; <span class="ans">&#8212; <b>4</b>, the smallest.</span></li>'
    '</ul>',
    sub("Qureo chapter 12 used Math.max(A, B) with two values. It works with three too. Writing biggest yourself shows <b>how</b> it decides.",
        "max-width:58ch;margin-top:.7rem;color:var(--soft)"),
    ar("اتعلمنا Math.max و Math.min على قيمتين في الفصل 12، وهما بيشتغلوا على تلاتة كمان. بس لما تكتب biggest بنفسك بتفهم بتقرر إزاي.")))

A(s("",
    eyebrow("4 &#183; Watch out"),
    h2("A function with no return", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>&#10060; Forgot return</h3>'
    '<div class="code" style="font-size:clamp(11px,1.35vw,16px)">' + K("function") + " " + F("add") + "(a, b) {\n  a + b;\n}\n" + LOG + "(" + F("add") + "(" + Nn("3") + ", " + Nn("5") + "));</div></div>"
    '<div class="pane b"><h3>&#9989; With return</h3>'
    '<div class="code" style="font-size:clamp(11px,1.35vw,16px)">' + K("function") + " " + F("add") + "(a, b) {\n  " + K("return") + " a + b;\n}\n" + LOG + "(" + F("add") + "(" + Nn("3") + ", " + Nn("5") + "));</div></div>"
    '</div>',
    '<ul class="rise check">'
    '<li class="reveal rv">What does the left one print? <span class="ans">&#8212; <b>undefined</b>: it added, but gave nothing back. A juice machine with no cup.</span></li>'
    '</ul>',
    ar("خلّي بالك: من غير return الدالة بتحسب بس مش بترجّع حاجة، فبيطبع undefined — زي ماكينة عصير من غير كوباية.")))

A(s("dark",
    eyebrow("Remember these"),
    h2("What we learned"),
    '<ul class="rise check">'
    '<li>A <b>web application</b> is used through a browser.</li>'
    '<li><b>Frontend</b> shows and collects; <b>backend</b> decides and processes; <b>database</b> stores and retrieves.</li>'
    '<li>A request flows down the tiers, and the reply comes back up.</li>'
    '<li>A <b>function</b> takes <b>arguments</b>, processes them, and gives back a <b>return value</b> &#8212; two values, three, or the biggest of three.</li>'
    '</ul>',
    ar("تطبيق الويب بيتستخدم من المتصفح • تلات طبقات: تعرض وتجمع، تقرر وتعالج، تخزن وتسترجع • الطلب بينزل والرد بيطلع • الدالة بتاخد وسائط وترجّع قيمة.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 9"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 9 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers lesson 3-1 and Qureo chapter 31. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس 3-1 والفصل 31 على المنصة. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))


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

/* lecture 9's drawings */
.statement.def{font-size:clamp(18px,2.15vw,30px); line-height:1.28; max-width:46ch}
/* code cards, as lecture 8; no ligatures, so >= reads as typed */
.code{display:block; background:var(--ink); color:#E6EDF3; text-align:left; padding:clamp(12px,1.7vw,22px); border-radius:12px; margin:.9rem 0 .4rem; font-family:"JetBrains Mono",monospace; font-size:clamp(13px,1.6vw,21px); line-height:1.6; white-space:pre; overflow-x:auto; max-width:100%}
.code .k,.tcode .k{color:#FF9D7A} .code .s,.tcode .s{color:#8FE3D6} .code .n,.tcode .n{color:#F7C66B} .code .f,.tcode .f{color:#9DC7FF} .code .c,.tcode .c{color:#7C8B99}
.code,.tcode,.mono,.codeline,code,.qcode{font-variant-ligatures:none; font-feature-settings:"liga" 0,"calt" 0}
.codeline{display:inline-block; background:var(--ink); color:#8FE3D6; padding:.25em .6em; border-radius:7px; font-family:"JetBrains Mono",monospace; font-size:.9em}
.part{font:600 clamp(46px,9vw,120px)/1 Fraunces,serif; color:var(--gold)}
/* the step-by-step players: the request flow and the code tracer */
.stepper{display:grid; grid-template-columns:1.15fr 1fr; gap:clamp(12px,1.8vw,26px); margin-top:.9rem; align-items:start}
@media(max-width:760px){.stepper{grid-template-columns:1fr}}
.tcode{background:var(--ink); color:#E6EDF3; border-radius:12px; padding:clamp(10px,1.3vw,16px); font-family:"JetBrains Mono",monospace; font-size:clamp(12px,1.4vw,18px); line-height:1.7; overflow-x:auto}
.tcode .ln{display:block; padding:0 .45em; border-radius:6px; white-space:pre; transition:background .25s,box-shadow .25s}
.tcode .ln.hot{background:rgba(247,198,107,.2); box-shadow:inset 4px 0 0 #F7C66B}
.tcons{margin-top:.6rem; background:#0B1324; color:#7CE38F; border-radius:10px; padding:.55em .9em; font-family:"JetBrains Mono",monospace; font-size:clamp(12px,1.4vw,18px); min-height:3.6em}
.tcons .lbl{display:block; color:#7C8B99; font-size:.72em; margin-bottom:.2em}
.tcons .line{display:block; animation:typeIn .5s steps(16) both}
@keyframes typeIn{from{clip-path:inset(0 100% 0 0)} to{clip-path:inset(0 0 0 0)}}
.tlbl{font-size:clamp(12px,1.25vw,16px); font-weight:600; color:var(--soft); margin-bottom:.3rem}
.boxes{display:flex; gap:.5rem; flex-wrap:wrap}
.box{display:flex; align-items:center; gap:.35em; font-family:"JetBrains Mono",monospace; font-size:clamp(13px,1.55vw,20px)}
.box b{min-width:3.2em; text-align:center; border:2px dashed var(--teal); border-radius:10px; padding:.15em .55em; color:var(--teal); background:var(--teal-pale)}
.box b.pop{animation:revealPop .6s cubic-bezier(.2,.8,.3,1.1) both}
.tstat{margin-top:.7rem; font-size:clamp(13px,1.45vw,19px); min-height:4.6em; line-height:1.45; color:var(--ink)}
.tstat .ar{display:block; margin-top:.25em; color:var(--soft)}
.tbtns{display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.5rem}
.tbtns button{font:inherit; font-size:clamp(13px,1.35vw,17px); font-weight:600; border-radius:9px; padding:.5em 1em; cursor:pointer; background:var(--teal); color:#fff; border:1px solid var(--teal)}
.tbtns button.alt{background:#fff; color:var(--ink); border-color:var(--line)}
.tbtns button:disabled{opacity:.4; cursor:default}
/* the three tiers, for the request flow */
.tiers{display:grid; grid-template-columns:repeat(3,1fr); gap:clamp(8px,1.4vw,18px); margin-top:.4rem}
.tier{position:relative; background:#fff; border:2px solid var(--line); border-radius:14px; padding:.8rem .6rem; text-align:center; transition:border-color .3s,background .3s,transform .3s}
.tier .ti{font-size:clamp(24px,3vw,40px); line-height:1.1}
.tier b{display:block; font-size:clamp(14px,1.5vw,20px); margin-top:.2rem}
.tier small{display:block; color:var(--soft); font-size:clamp(11px,1.1vw,14px)}
.tier.on{border-color:var(--gold); background:var(--gold-pale); transform:translateY(-6px)}
.packet{display:block; margin:.7rem auto 0; text-align:center; font-weight:600; font-size:clamp(13px,1.4vw,18px); color:var(--ink); min-height:1.6em}
.packet span{display:inline-block; background:var(--ink); color:#fff; border-radius:99px; padding:.2em .9em; animation:revealPop .55s cubic-bezier(.2,.8,.3,1.1) both}
.stepper.flowcol{display:block; max-width:860px}
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
BASE = "scripts/lecture9_slides_base.html"
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
LECTURE_JS = '/* ---- the step-by-step players (lecture 9) ---------------------------------\n   .stepper[data-kind=flow]: lights one tier per step and shows what is\n   passed on. .stepper[data-kind=code]: lights a code line, fills the value\n   boxes and prints to the console. Next step, Play all, Again. Space and\n   Enter on the buttons must not also turn the slide, so they stop here. */\n(function(){\n  if(!document.querySelectorAll) return;\n  document.querySelectorAll(\'.stepper\').forEach(function(box){\n    var steps = JSON.parse(box.getAttribute(\'data-steps\'));\n    var kind = box.getAttribute(\'data-kind\');\n    var en = box.querySelector(\'.tstat .en\'), ar = box.querySelector(\'.tstat .ar\');\n    var nx = box.querySelector(\'.nx\'), pl = box.querySelector(\'.pl\'), rs = box.querySelector(\'.rs\');\n    var lines = box.querySelectorAll(\'.ln\'), cons = box.querySelector(\'.tcons\');\n    var tiers = box.querySelectorAll(\'.tier\'), packet = box.querySelector(\'.packet\');\n    var i = 0, timer = null;\n\n    function stop(){ if(timer){ clearInterval(timer); timer = null; } }\n    function say(e, a){ en.textContent = e || \'\'; ar.textContent = a || \'\'; }\n    function reset(){\n      stop(); i = 0;\n      for(var j = 0; j < lines.length; j++) lines[j].classList.remove(\'hot\');\n      for(var t = 0; t < tiers.length; t++) tiers[t].classList.remove(\'on\');\n      if(packet) packet.textContent = \'\';\n      if(cons) cons.querySelectorAll(\'.line\').forEach(function(l){ l.remove(); });\n      box.querySelectorAll(\'.box b\').forEach(function(b){ b.textContent = \'?\'; b.classList.remove(\'pop\'); });\n      nx.disabled = false; pl.disabled = false;\n      say(\'Press Next step to start.\', \'اضغط Next step عشان تبدأ.\');\n    }\n    function next(){\n      if(i >= steps.length) return;\n      var s = steps[i++];\n      if(kind === \'flow\'){\n        for(var t = 0; t < tiers.length; t++) tiers[t].classList.toggle(\'on\', tiers[t].getAttribute(\'data-t\') === s.t);\n        packet.textContent = \'\';\n        if(s.msg){ var p = document.createElement(\'span\'); p.textContent = s.msg; packet.appendChild(p); }\n      } else {\n        for(var j = 0; j < lines.length; j++) lines[j].classList.toggle(\'hot\', j === s.ln);\n        if(s.set) Object.keys(s.set).forEach(function(k){\n          var b = box.querySelector(\'.box[data-k="\' + k + \'"] b\');\n          if(!b) return;\n          b.textContent = s.set[k];\n          b.classList.remove(\'pop\'); void b.offsetWidth; b.classList.add(\'pop\');\n        });\n        if(s.out !== undefined){\n          var l = document.createElement(\'span\'); l.className = \'line\'; l.textContent = s.out; cons.appendChild(l);\n        }\n      }\n      say(s.en, s.ar);\n      if(i >= steps.length){ stop(); nx.disabled = true; pl.disabled = true; }\n    }\n    nx.addEventListener(\'click\', function(){ stop(); next(); });\n    pl.addEventListener(\'click\', function(){\n      if(timer) return;\n      if(i >= steps.length) reset();\n      pl.disabled = true; next(); timer = setInterval(next, 1500);\n    });\n    rs.addEventListener(\'click\', reset);\n    box.addEventListener(\'keydown\', function(e){\n      if(e.target.tagName === \'BUTTON\' && (e.key === \' \' || e.key === \'Enter\')) e.stopPropagation();\n    });\n    reset();\n  });\n})();'
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

