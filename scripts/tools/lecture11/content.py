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
