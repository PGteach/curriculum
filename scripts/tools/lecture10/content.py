# --------------------------------------------------------------------------
# diagrams -- inline SVG, coloured from the page's CSS variables so they follow
# LECTURE_ACCENT. Labels only, never the sentence that explains them; no label
# under 14 units. Fills are #fff, never var(--white): the booklet template
# does not define --white. The booklet reads these out of this file. The
# flowcharts give each shape a data-id, which the chart player lights.
# --------------------------------------------------------------------------

CLIENTSERVER = '''
<svg viewBox="0 0 900 270" role="img" aria-label="Several clients, a browser, a phone app and a tablet, send requests to one server; the server returns a response to each">
  <g font-size="15" text-anchor="middle">
    <rect x="20" y="20" width="200" height="62" rx="12" fill="#fff" stroke="var(--teal)" stroke-width="3"/>
    <text x="70" y="60" font-size="26">&#128187;</text><text x="140" y="57" font-weight="700" fill="var(--ink)">Web browser</text>
    <rect x="20" y="104" width="200" height="62" rx="12" fill="#fff" stroke="var(--teal)" stroke-width="3"/>
    <text x="70" y="144" font-size="26">&#128241;</text><text x="140" y="141" font-weight="700" fill="var(--ink)">Phone app</text>
    <rect x="20" y="188" width="200" height="62" rx="12" fill="#fff" stroke="var(--teal)" stroke-width="3"/>
    <text x="70" y="228" font-size="26">&#128421;</text><text x="140" y="225" font-weight="700" fill="var(--ink)">Another program</text>
    <text x="120" y="12" font-size="14" font-weight="700" fill="var(--teal)">CLIENTS &#8212; request</text>
    <rect x="660" y="60" width="220" height="150" rx="14" fill="#fff" stroke="var(--gold)" stroke-width="3"/>
    <text x="770" y="112" font-size="34">&#128452;</text>
    <text x="770" y="150" font-size="20" font-weight="700" fill="var(--ink)">Server</text>
    <text x="770" y="174" fill="var(--soft)">processes and responds</text>
    <line x1="226" y1="44" x2="646" y2="104" stroke="var(--teal)" stroke-width="3"/><polygon points="654,105 641,97 640,112" fill="var(--teal)"/>
    <line x1="226" y1="135" x2="646" y2="135" stroke="var(--teal)" stroke-width="3"/><polygon points="654,135 642,128 642,142" fill="var(--teal)"/>
    <line x1="654" y1="166" x2="234" y2="228" stroke="var(--gold)" stroke-width="3"/><polygon points="226,229 239,221 240,236" fill="var(--gold)"/>
    <text x="440" y="62" font-weight="600" fill="var(--teal)">request (HTTP method: GET / POST)</text>
    <text x="440" y="236" font-weight="600" fill="var(--gold)">response (status code + data)</text>
  </g>
</svg>'''

FLOWSYM = '''
<svg viewBox="0 0 900 200" role="img" aria-label="The four flowchart symbols: an oval for start and end, a rectangle for a process, a diamond for a decision, a parallelogram for input and output">
  <g font-size="15" text-anchor="middle">
    <ellipse cx="110" cy="70" rx="85" ry="34" fill="#fff" stroke="var(--teal)" stroke-width="3"/>
    <text x="110" y="76" font-weight="700" fill="var(--ink)">Start / End</text>
    <rect x="245" y="36" width="180" height="68" rx="4" fill="#fff" stroke="var(--teal)" stroke-width="3"/>
    <text x="335" y="76" font-weight="700" fill="var(--ink)">Process</text>
    <polygon points="565,22 655,70 565,118 475,70" fill="#fff" stroke="var(--gold)" stroke-width="3"/>
    <text x="565" y="76" font-weight="700" fill="var(--ink)">Decision</text>
    <polygon points="725,36 885,36 855,104 695,104" fill="#fff" stroke="var(--teal)" stroke-width="3"/>
    <text x="790" y="76" font-weight="700" fill="var(--ink)">Input / Output</text>
    <text x="110" y="150" fill="var(--soft)">where the program</text><text x="110" y="170" fill="var(--soft)">begins and ends</text>
    <text x="335" y="150" fill="var(--soft)">a step: calculate,</text><text x="335" y="170" fill="var(--soft)">give a value</text>
    <text x="565" y="150" fill="var(--soft)">a question: Yes / No</text><text x="565" y="170" fill="var(--soft)">&#8594; an if statement</text>
    <text x="790" y="150" fill="var(--soft)">take in or show</text><text x="790" y="170" fill="var(--soft)">&#8594; console.log</text>
  </g>
</svg>'''

PRICE = '''
<svg class="fc" viewBox="0 0 520 478" role="img" aria-label="Flowchart: start; price = 40; total = price * 3; is total greater than 100? Yes: show Too expensive. No: show Buy it. End">
  <g font-size="17" text-anchor="middle">
    <g data-id="start"><ellipse class="shp" cx="200" cy="30" rx="70" ry="24" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="36" font-weight="700" fill="var(--ink)">Start</text></g>
    <line x1="200" y1="54" x2="200" y2="78" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,80 193,68 207,68" fill="var(--ink)"/>
    <g data-id="p0"><rect class="shp" x="95" y="80" width="210" height="46" rx="4" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="109" font-family="JetBrains Mono,monospace" fill="var(--ink)">price = 40</text></g>
    <line x1="200" y1="126" x2="200" y2="150" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,152 193,140 207,140" fill="var(--ink)"/>
    <g data-id="p1"><rect class="shp" x="95" y="152" width="210" height="46" rx="4" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="181" font-family="JetBrains Mono,monospace" fill="var(--ink)">total = price * 3</text></g>
    <line x1="200" y1="198" x2="200" y2="222" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,224 193,212 207,212" fill="var(--ink)"/>
    <g data-id="d"><polygon class="shp" points="200,222 310,272 200,322 90,272" fill="#fff" stroke="var(--gold)" stroke-width="3"/><text x="200" y="278" font-family="JetBrains Mono,monospace" fill="var(--ink)">total &gt; 100 ?</text></g>
    <line x1="310" y1="272" x2="410" y2="272" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="410" y1="272" x2="410" y2="346" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="410,348 403,336 417,336" fill="var(--ink)"/>
    <text x="350" y="262" font-weight="700" fill="var(--teal)">Yes</text>
    <line x1="200" y1="322" x2="200" y2="346" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,348 193,336 207,336" fill="var(--ink)"/>
    <text x="222" y="342" font-weight="700" fill="#9C3B2E">No</text>
    <g data-id="yes"><polygon class="shp" points="335,346 505,346 485,392 315,392" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="410" y="375" font-family="JetBrains Mono,monospace" fill="var(--ink)">&quot;Too expensive&quot;</text></g>
    <g data-id="no"><polygon class="shp" points="125,346 295,346 275,392 105,392" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="375" font-family="JetBrains Mono,monospace" fill="var(--ink)">&quot;Buy it&quot;</text></g>
    <line x1="200" y1="392" x2="200" y2="444" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="200" y1="444" x2="228" y2="444" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="230,444 218,437 218,451" fill="var(--ink)"/>
    <line x1="410" y1="392" x2="410" y2="444" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="410" y1="444" x2="372" y2="444" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="370,444 382,437 382,451" fill="var(--ink)"/>
    <g data-id="end"><ellipse class="shp" cx="300" cy="444" rx="70" ry="24" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="300" y="450" font-weight="700" fill="var(--ink)">End</text></g>
  </g>
</svg>'''

AB = '''
<svg class="fc" viewBox="0 0 520 406" role="img" aria-label="Flowchart: start; a = 8 and b = 5; is a greater than b? Yes: show a. No: show b. End">
  <g font-size="17" text-anchor="middle">
    <g data-id="start"><ellipse class="shp" cx="200" cy="30" rx="70" ry="24" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="36" font-weight="700" fill="var(--ink)">Start</text></g>
    <line x1="200" y1="54" x2="200" y2="78" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,80 193,68 207,68" fill="var(--ink)"/>
    <g data-id="p0"><rect class="shp" x="95" y="80" width="210" height="46" rx="4" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="109" font-family="JetBrains Mono,monospace" fill="var(--ink)">a = 8, b = 5</text></g>
    <line x1="200" y1="126" x2="200" y2="150" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,152 193,140 207,140" fill="var(--ink)"/>
    <g data-id="d"><polygon class="shp" points="200,150 310,200 200,250 90,200" fill="#fff" stroke="var(--gold)" stroke-width="3"/><text x="200" y="206" font-family="JetBrains Mono,monospace" fill="var(--ink)">a &gt; b ?</text></g>
    <line x1="310" y1="200" x2="410" y2="200" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="410" y1="200" x2="410" y2="274" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="410,276 403,264 417,264" fill="var(--ink)"/>
    <text x="350" y="190" font-weight="700" fill="var(--teal)">Yes</text>
    <line x1="200" y1="250" x2="200" y2="274" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,276 193,264 207,264" fill="var(--ink)"/>
    <text x="222" y="270" font-weight="700" fill="#9C3B2E">No</text>
    <g data-id="yes"><polygon class="shp" points="335,274 505,274 485,320 315,320" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="410" y="303" font-family="JetBrains Mono,monospace" fill="var(--ink)">a</text></g>
    <g data-id="no"><polygon class="shp" points="125,274 295,274 275,320 105,320" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="303" font-family="JetBrains Mono,monospace" fill="var(--ink)">b</text></g>
    <line x1="200" y1="320" x2="200" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="200" y1="372" x2="228" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="230,372 218,365 218,379" fill="var(--ink)"/>
    <line x1="410" y1="320" x2="410" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="410" y1="372" x2="372" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="370,372 382,365 382,379" fill="var(--ink)"/>
    <g data-id="end"><ellipse class="shp" cx="300" cy="372" rx="70" ry="24" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="300" y="378" font-weight="700" fill="var(--ink)">End</text></g>
  </g>
</svg>'''

AGE = '''
<svg class="fc" viewBox="0 0 520 406" role="img" aria-label="Flowchart: start; age = 15; is age at least 12? Yes: show Ticket OK. No: show Too young. End">
  <g font-size="17" text-anchor="middle">
    <g data-id="start"><ellipse class="shp" cx="200" cy="30" rx="70" ry="24" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="36" font-weight="700" fill="var(--ink)">Start</text></g>
    <line x1="200" y1="54" x2="200" y2="78" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,80 193,68 207,68" fill="var(--ink)"/>
    <g data-id="p0"><rect class="shp" x="95" y="80" width="210" height="46" rx="4" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="109" font-family="JetBrains Mono,monospace" fill="var(--ink)">age = 15</text></g>
    <line x1="200" y1="126" x2="200" y2="150" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,152 193,140 207,140" fill="var(--ink)"/>
    <g data-id="d"><polygon class="shp" points="200,150 310,200 200,250 90,200" fill="#fff" stroke="var(--gold)" stroke-width="3"/><text x="200" y="206" font-family="JetBrains Mono,monospace" fill="var(--ink)">age &gt;= 12 ?</text></g>
    <line x1="310" y1="200" x2="410" y2="200" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="410" y1="200" x2="410" y2="274" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="410,276 403,264 417,264" fill="var(--ink)"/>
    <text x="350" y="190" font-weight="700" fill="var(--teal)">Yes</text>
    <line x1="200" y1="250" x2="200" y2="274" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,276 193,264 207,264" fill="var(--ink)"/>
    <text x="222" y="270" font-weight="700" fill="#9C3B2E">No</text>
    <g data-id="yes"><polygon class="shp" points="335,274 505,274 485,320 315,320" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="410" y="303" font-family="JetBrains Mono,monospace" fill="var(--ink)">&quot;Ticket OK&quot;</text></g>
    <g data-id="no"><polygon class="shp" points="125,274 295,274 275,320 105,320" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="303" font-family="JetBrains Mono,monospace" fill="var(--ink)">&quot;Too young&quot;</text></g>
    <line x1="200" y1="320" x2="200" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="200" y1="372" x2="228" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="230,372 218,365 218,379" fill="var(--ink)"/>
    <line x1="410" y1="320" x2="410" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="410" y1="372" x2="372" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="370,372 382,365 382,379" fill="var(--ink)"/>
    <g data-id="end"><ellipse class="shp" cx="300" cy="372" rx="70" ry="24" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="300" y="378" font-weight="700" fill="var(--ink)">End</text></g>
  </g>
</svg>'''

REVIEW = '''
<svg class="fc" viewBox="0 0 520 406" role="img" aria-label="Flowchart: start; total = add3(2, 4, 6); is total greater than 10? Yes: show Big total. No: show Small total. End">
  <g font-size="17" text-anchor="middle">
    <g data-id="start"><ellipse class="shp" cx="200" cy="30" rx="70" ry="24" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="36" font-weight="700" fill="var(--ink)">Start</text></g>
    <line x1="200" y1="54" x2="200" y2="78" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,80 193,68 207,68" fill="var(--ink)"/>
    <g data-id="p0"><rect class="shp" x="75" y="80" width="250" height="46" rx="4" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="109" font-family="JetBrains Mono,monospace" fill="var(--ink)">total = add3(2, 4, 6)</text></g>
    <line x1="200" y1="126" x2="200" y2="150" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,152 193,140 207,140" fill="var(--ink)"/>
    <g data-id="d"><polygon class="shp" points="200,150 310,200 200,250 90,200" fill="#fff" stroke="var(--gold)" stroke-width="3"/><text x="200" y="206" font-family="JetBrains Mono,monospace" fill="var(--ink)">total &gt; 10 ?</text></g>
    <line x1="310" y1="200" x2="410" y2="200" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="410" y1="200" x2="410" y2="274" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="410,276 403,264 417,264" fill="var(--ink)"/>
    <text x="350" y="190" font-weight="700" fill="var(--teal)">Yes</text>
    <line x1="200" y1="250" x2="200" y2="274" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="200,276 193,264 207,264" fill="var(--ink)"/>
    <text x="222" y="270" font-weight="700" fill="#9C3B2E">No</text>
    <g data-id="yes"><polygon class="shp" points="335,274 505,274 485,320 315,320" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="410" y="303" font-family="JetBrains Mono,monospace" fill="var(--ink)">&quot;Big total&quot;</text></g>
    <g data-id="no"><polygon class="shp" points="125,274 295,274 275,320 105,320" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="200" y="303" font-family="JetBrains Mono,monospace" fill="var(--ink)">&quot;Small total&quot;</text></g>
    <line x1="200" y1="320" x2="200" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="200" y1="372" x2="228" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="230,372 218,365 218,379" fill="var(--ink)"/>
    <line x1="410" y1="320" x2="410" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <line x1="410" y1="372" x2="372" y2="372" stroke="var(--ink)" stroke-width="2.5"/>
    <polygon points="370,372 382,365 382,379" fill="var(--ink)"/>
    <g data-id="end"><ellipse class="shp" cx="300" cy="372" rx="70" ry="24" fill="#fff" stroke="var(--teal)" stroke-width="3"/><text x="300" y="378" font-weight="700" fill="var(--ink)">End</text></g>
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


def v_envelope():
    rows = [("&#9993;", "HTTP", "a postcard: anyone on the way can read it", "readable"),
            ("&#128274;", "HTTPS", "a sealed envelope: TLS encrypts it", "encrypted")]
    out = "".join('<div class="drow" style="animation-delay:%.2fs"><span class="dico">%s</span>'
                  '<span class="dt"><b>%s</b><br><small>%s</small></span>'
                  '<span class="darrow">&#8594;</span><span class="dai">%s</span></div>'
                  % (.4 + .6 * k, ico, t, why, tag) for k, (ico, t, why, tag) in enumerate(rows))
    return ('<aside class="rise viz">' + out
            + vcap("Same message, but only one is sealed.",
                   "نفس الرسالة، بس واحدة بس متقفلة.")
            + '</aside>')


def v_codes():
    tiles = [("&#9989;", "200", "success"), ("&#128269;", "404", "not found"), ("&#128165;", "500", "server error")]
    out = "".join('<div class="tile" style="animation-delay:%.2fs"><span>%s</span><b>%s</b><i>%s</i></div>'
                  % (.3 + .35 * k, ico, n, t) for k, (ico, n, t) in enumerate(tiles))
    return ('<aside class="rise viz"><div class="tiles">' + out + '</div>'
            + vcap("The server's answer, as a number.",
                   "رد الخادم، في شكل رقم.")
            + '</aside>')


def v_school():
    return ('<aside class="rise viz"><div class="shopv">'
            '<div class="sv sv1"><span>&#128218;</span><b>Grade history</b><i>GET or POST?</i></div>'
            '<div class="sv sv2"><span>&#128272;</span><b>Login form</b><i>GET or POST? HTTP or HTTPS?</i></div>'
            '<div class="sv sv3"><span>&#127979;</span><b>Another school&#8217;s timetable</b><i>is an API involved?</i></div>'
            '</div>'
            + vcap("Choose a method for each action.",
                   "اختار الأسلوب المناسب لكل إجراء.")
            + '</aside>')


# heading text (unique to one slide) -> its drawing
VIZ = {
    "Before you read on": v_timer,
    "A postcard or a sealed envelope": v_envelope,
    "Three numbers to know": v_codes,
    "A school wants a timetable app": v_school,
}
VIZ_USED = []


# ---------------- the step-by-step players ----------------
# All three are plain data: the builder writes the steps into data-steps,
# and script.js (added to the page's own script) plays them one press at a
# time. flow: boxes light in turn with what is passed on. tracer: a code
# line lights and values fill. chart: a flowchart shape lights.

def _steps_attr(steps):
    import html as _h, json as _j
    return _h.escape(_j.dumps(steps, ensure_ascii=False), quote=True)


def _buttons():
    return ('<div class="tbtns"><button type="button" class="nx">Next step &#9654;</button>'
            '<button type="button" class="alt pl">Play all</button>'
            '<button type="button" class="alt rs">&#8634; Again</button></div>')


def flow(steps, tiers):
    """A message travelling between boxes. tiers: (key, icon, name, note).
    Each step lights one box and shows what is passed on:
    {"t": key, "msg", "en", "ar"}."""
    return ('<div class="rise stepper flowcol" data-kind="flow" data-steps="%s">'
            '<div class="tiers" style="grid-template-columns:repeat(%d,1fr)">%s</div><p class="packet"></p>'
            '<p class="tstat"><span class="en"></span><span class="ar"></span></p>%s</div>'
            % (_steps_attr(steps), len(tiers),
               "".join('<div class="tier" data-t="%s"><div class="ti">%s</div><b>%s</b><small>%s</small></div>'
                       % (k, ico, n, d) for k, ico, n, d in tiers),
               _buttons()))


def chart(svg, boxes, steps, boxlabel="The values"):
    """A flowchart player. svg: a chart whose shapes carry data-id. Each step
    may light a shape ("el"), set values ("set"), print a line ("out"), and
    says what happened ("en", "ar")."""
    return ('<div class="rise stepper chartp" data-kind="code" data-steps="%s">'
            '<div class="fcwrap">%s</div>'
            '<div><div class="tlbl">%s</div><div class="boxes">%s</div>'
            '<div class="tcons"><span class="lbl">Output &#8212; what is shown</span></div>'
            '<p class="tstat"><span class="en"></span><span class="ar"></span></p>%s</div></div>'
            % (_steps_attr(steps), svg.strip(), boxlabel,
               "".join('<div class="box" data-k="%s"><span>%s =</span><b>?</b></div>' % (b, b) for b in boxes),
               _buttons()))


def K(t): return '<span class="k">%s</span>' % t
def S_(t): return '<span class="s">%s</span>' % t
def Nn(t): return '<span class="n">%s</span>' % t
def F(t): return '<span class="f">%s</span>' % t
LOG = F("console.log")
