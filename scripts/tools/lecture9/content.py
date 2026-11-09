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