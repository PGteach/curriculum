# -*- coding: utf-8 -*-
"""Build Lecture 10's deck.

    python scripts/build_lecture10_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/lecture10_slides_base.html and writes lecture10/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the side drawings
added. Always starts from the base, never from the published deck.

Two parts, as the ministry's plan pairs a book lesson with the Japanese
platform each week. Part one is Lesson 3-2, Web Application Communication
Methods, the English textbook pp. 62-67, and nothing outside the curriculum.
Where the Arabic textbook and the ministry's assessment book go further, the
deck follows them: HTTPS also protects integrity and authenticates the
server; a 500 does not say the detailed cause; reading a key and a value in
JSON. Part two is Qureo chapters 32 and 33: Flowchart, and the comprehension
check on chapters 31-32. Qureo's own lesson text for these chapters is locked
on the platform, so the flowchart part teaches the standard symbols and how a
flowchart becomes an if statement, from the chapter's description and lesson
titles ("if + Operations", "Flowchart (1)", "Flowchart (2)").

Everything but the content is lecture 5's builder, unchanged -- this file was
derived from it. The Arabic follows the Arabic textbook's lesson 3-2 point by
point, said in Egyptian Arabic, with the book's own terms kept as they are.
The step-by-step players (the request flow and the flowchart player) are
this lecture's own; their script is tools/lecture10/script.js, added to the
page's own script.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "lecture10/slides/index.html"


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
    h2("How do they talk?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("Your phone does not hold the whole website &#8212; it asks for it. Today: the request, the response, and the rules they follow. On the platform: flowcharts.",
        "max-width:58ch;margin-top:1rem"),
    ar("موبايلك مش شايل الموقع كله — هو بيطلبه. النهارده: الطلب، والاستجابة، والقواعد اللي بيمشوا عليها. وعلى المنصة: المخططات الانسيابية.")))

# 2 recap -- lesson 3-1, and the Arabic book's bridge
A(s("",
    eyebrow("Before we start &#183; Lesson 3-1"),
    h2("Last time: three tiers", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>Tier</th><th>Its job</th></tr>'
    '<tr><td><b>Frontend</b></td><td>shows and collects</td></tr>'
    '<tr><td><b>Backend</b></td><td>decides and processes</td></tr>'
    '<tr><td><b>Database</b></td><td>stores and retrieves</td></tr>'
    '</table>',
    sub("They cooperate by sending messages. Today: <b>how</b> those messages travel &#8212; the request and the response.", "max-width:60ch;margin-top:.9rem"),
    ar("في الدرس 3-1 اتعلمت إن الواجهة الأمامية والواجهة الخلفية بيتعاونوا عشان ينفذوا طلب المستخدم. في الدرس ده هتتعلم إزاي الطلبات والاستجابات بتتنقل بين العميل والخادم.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("This happens every time you click"),
    h2("Your device asks, a server answers", "max-width:22ch"),
    sub("When you click a link or press &#8220;search&#8221;, your device does not hold the whole website &#8212; it asks a distant computer for it. Your browser is the <b>client</b> that makes the <b>request</b>; a <b>server</b> somewhere answers with a <b>response</b>. Shared rules called <b>protocols</b> govern the exchange.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> you see a page that says <b>404</b>. Is the Internet broken, is the server broken &#8212; or something else? Remember your answer.</p></div>',
    ar("لما بتدوس على لينك أو بتبدأ بحث، المتصفح غالبًا بيطلب البيانات اللي محتاجها من خدمة على خادم عبر الشبكة. المتصفح هنا عميل (client) بيبعت طلب، والخادم (server) بيرجّع استجابة، وبروتوكولات زي HTTP بتحدد قواعد التبادل ده.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("How do the client and server communicate to make a web application work, and what rules and messages do they use?",
       "max-width:28ch"),
    ar("السؤال الرئيسي: إزاي العميل والخادم بيتواصلوا عشان يشغّلوا تطبيق الويب، وإيه القواعد والرسائل اللي بيستخدموها؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map"),
    h2("Four parts from the book, two on the platform", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#128101;</div><div class="role">Part 1</div><h3>Client and server</h3><p>Who asks, who answers</p></div>'
    '<div class="card"><div class="ico">&#128274;</div><div class="role">Part 2</div><h3>HTTP and HTTPS</h3><p>The rules, and the lock</p></div>'
    '<div class="card"><div class="ico">&#128232;</div><div class="role">Part 3</div><h3>Requests and responses</h3><p>GET, POST, 200, 404, 500</p></div>'
    '<div class="card"><div class="ico">&#128279;</div><div class="role">Part 4</div><h3>API and JSON</h3><p>Programs sharing data</p></div>'
    '<div class="card"><div class="ico">&#128200;</div><div class="role">Qureo 32 &#183; 33</div><h3>Flowcharts</h3><p>Draw a program, then review</p></div>'
    '</div>',
    ar("خريطة المحاضرة: 1 العميل والخادم. 2 HTTP و HTTPS. 3 الطلبات والاستجابات: GET و POST ورموز الحالة. 4 API و JSON. وعلى المنصة: الفصل 32 المخطط الانسيابي، والفصل 33 مراجعة.")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("You open YouTube on your phone and search <b>cats</b>. With your partner, write down:",
        "max-width:56ch;margin-top:1rem"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>What does your phone <b>send</b>?</li>'
    '<li>What comes <b>back</b>?</li>'
    '<li>When you log in, should your password travel as it is &#8212; or locked?</li>'
    '</ul>',
    sub("Keep your answers. Part 3 shows the book&#8217;s, step by step.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: فتحت يوتيوب على الموبايل ودوّرت على cats. موبايلك بيبعت إيه؟ وإيه اللي بيرجع؟ ولما بتسجل دخول، الباسورد يمشي زي ما هو ولا متقفل؟")))

# ---------------- part 1: client and server ----------------

A(s("",
    eyebrow("Part 1 &#183; Client and server"),
    h2("Who asks, who answers"),
    fig(CLIENTSERVER),
    '<table class="rise">'
    '<tr><th>Term</th><th>Meaning</th></tr>'
    '<tr><td><b>Client</b></td><td>The side that requests data or processing from the server. Web browsers and smartphone apps.</td></tr>'
    '<tr><td><b>Server</b></td><td>The side that receives requests from clients, processes them, and returns responses.</td></tr>'
    '</table>',
    ar("العميل: برنامج أو جهاز بيبعت طلب لخدمة تانية، زي متصفح الويب وتطبيق الموبايل. الخادم: الجانب اللي بيستقبل الطلبات من العملاء، ويعالجها، ويرجّع الاستجابات. وكتير من تطبيقات الويب بتعتمد على إن العميل يبعت طلب والخادم يرجّع استجابة.")))

A(s("",
    eyebrow("1 &#183; Your turn"),
    h2("Client or server?"),
    '<table class="rise">'
    '<tr><th>Who is it?</th><th>Answer</th></tr>'
    '<tr><td>Your web browser asking for a page</td><td class="reveal"><span>Client</span></td></tr>'
    '<tr><td>The computer that receives the request, processes it and sends back the page</td><td class="reveal"><span>Server</span></td></tr>'
    '<tr><td>A smartphone app asking for today&#8217;s weather</td><td class="reveal"><span>Client</span></td></tr>'
    '</table>',
    sub("The one that <b>asks</b> is the client; the one that <b>answers</b> is the server. Tap to check.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("اللي بيطلب هو العميل، واللي بيرد هو الخادم. فكّر الأول وبعدين دوس.")))

# ---------------- part 2: HTTP and HTTPS ----------------

A(s("",
    eyebrow("Part 2 &#183; HTTP and HTTPS"),
    h2("A postcard or a sealed envelope", "max-width:24ch"),
    '<div class="rise statement def"><em>HTTP</em> (HyperText Transfer Protocol) &#8212; a communication protocol for exchanging data between clients and servers.</div>',
    '<div class="rise statement def" style="margin-top:.7rem"><em>HTTPS</em> (HTTP Secure) &#8212; HTTP with <em>TLS encryption</em> added. The content is encrypted, so the risk of it being read by others is reduced.</div>',
    sub("Addresses that begin with <span class=\"codeline\">https://</span> use HTTPS. The Arabic book adds: TLS also stops the content being <b>changed</b> on the way, and checks it is the <b>real server</b>.",
        "max-width:58ch;margin-top:.8rem"),
    ar("HTTP: بروتوكول بيستخدم لتبادل الرسائل بين عميل وخادم على الويب. HTTPS: استخدام HTTP عبر اتصال TLS آمن؛ بيحمي سرية الاتصال وسلامته، وبيتحقق من الخادم، فالمتجسس ميقدرش يقرا المحتوى أو يعدّله بسهولة. والمواقع اللي عناوينها بتبدأ بـ https:// بتستخدم HTTPS.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("Why should a login page use HTTPS rather than plain HTTP?", "max-width:24ch"),
    '<ul class="rise check" style="margin-top:1rem">'
    '<li class="reveal rv">Because&#8230; <span class="ans">&#8212; the password is <b>encrypted</b> on the way, so someone listening on the network cannot read it. With plain HTTP it travels as it is.</span></li>'
    '</ul>',
    ar("وقّف وفكّر: ليه صفحة تسجيل الدخول لازم تستخدم HTTPS بدل HTTP العادي؟")))

# ---------------- part 3: requests and responses ----------------

A(s("",
    eyebrow("Part 3 &#183; The request: an HTTP method"),
    h2("GET or POST?"),
    sub("Every request carries an <b>HTTP method</b>: what kind of operation is wanted.", "max-width:58ch;margin-top:.4rem"),
    '<table class="rise">'
    '<tr><th>Method</th><th>Role</th><th>Examples</th></tr>'
    '<tr><td><b>GET</b></td><td>Retrieve data from the server</td><td>Displaying a web page, retrieving search results</td></tr>'
    '<tr><td><b>POST</b></td><td>Send data to the server</td><td>Sending login information, submitting a form</td></tr>'
    '</table>',
    '<table class="rise" style="margin-top:.8rem">'
    '<tr><th>Operation</th><th>Method</th></tr>'
    '<tr><td>a &#183; Displaying a web page</td><td class="reveal"><span>GET</span></td></tr>'
    '<tr><td>b &#183; Submitting an ID and password in a login form</td><td class="reveal"><span>POST</span></td></tr>'
    '<tr><td>c &#183; Displaying search results</td><td class="reveal"><span>GET</span></td></tr>'
    '<tr><td>d &#183; Submitting a contact form</td><td class="reveal"><span>POST</span></td></tr>'
    '</table>',
    ar("كل طلب فيه طريقة طلب HTTP بتوضح نوع العملية المطلوبة. GET بيستخدم عادةً لطلب مورد أو بيانات من الخادم، زي عرض صفحة أو نتايج بحث. POST بيستخدم عادةً لإرسال بيانات يعالجها الخادم، زي تسجيل الدخول أو إرسال نموذج.")))

A(s("",
    eyebrow("3 &#183; The response: a status code"),
    h2("Three numbers to know"),
    sub("Every response carries a <b>status code</b>: a number that reports the result.", "max-width:58ch;margin-top:.4rem"),
    '<table class="rise">'
    '<tr><th>Status code</th><th>Meaning</th></tr>'
    '<tr><td><b>200</b></td><td>Success &#8212; the request was processed successfully</td></tr>'
    '<tr><td><b>404</b></td><td>Page not found &#8212; the requested address does not exist</td></tr>'
    '<tr><td><b>500</b></td><td>Server error &#8212; a problem occurred on the server side</td></tr>'
    '</table>',
    sub("The Arabic book adds: a 500 alone does not say <b>what</b> went wrong &#8212; only that it was on the server.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("الاستجابة فيها رقم بيوضح نتيجة المعالجة اسمه رمز حالة HTTP. 200: نجاح. 404: المورد المطلوب مش موجود بالعنوان ده. 500: خطأ داخلي في الخادم منعه يكمّل الطلب؛ والرمز لوحده مش بيحدد السبب بالتفصيل.")))

A(s("",
    eyebrow("3 &#183; One request, one matching response"),
    h2("Watch a page arrive, then a login", "max-width:26ch"),
    flow([
        {"t": "c", "msg": "GET  /search?q=cats", "en": "① You search 'cats'. The browser (client) sends a request with the GET method: it wants to retrieve data.",
         "ar": "① بتدوّر على cats. المتصفح (العميل) بيبعت طلب بأسلوب GET: عايز يجيب بيانات."},
        {"t": "s", "msg": "processing…", "en": "② The server receives the request and processes it: it finds the results.",
         "ar": "② الخادم بيستقبل الطلب ويعالجه: بيدوّر على النتايج."},
        {"t": "c", "msg": "200 OK  +  the results page", "en": "③ The server returns a response with status code 200 (success) and the page. The browser shows it.",
         "ar": "③ الخادم بيرجّع استجابة برمز حالة 200 (نجاح) ومعاها الصفحة، والمتصفح بيعرضها."},
        {"t": "c", "msg": "POST  /login  (HTTPS 🔒)", "en": "④ Now you log in. Sending data means POST, and over HTTPS the password travels encrypted.",
         "ar": "④ دلوقتي بتسجل دخول. إرسال بيانات يعني POST، ومع HTTPS الباسورد بيمشي متشفر."},
        {"t": "s", "msg": "checking the password…", "en": "⑤ The server receives the login data and checks it.",
         "ar": "⑤ الخادم بيستقبل بيانات الدخول ويتحقق منها."},
        {"t": "c", "msg": "200 OK  +  your account", "en": "⑥ Success: status code 200, and your account page comes back.",
         "ar": "⑥ نجاح: رمز حالة 200، وصفحة حسابك بترجع."},
    ], [("c", "&#128241;", "Client", "your browser"), ("s", "&#128452;", "Server", "far away")]),
    ar("طلب HTTP واحد، واستجابة مطابقة واحدة. دوس Next step وتابع.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("If a browser receives status code 404, what should it tell the user &#8212; and whose side had the problem?",
       "max-width:28ch"),
    '<ul class="rise check" style="margin-top:1rem">'
    '<li class="reveal rv">Tell the user&#8230; <span class="ans">&#8212; &#8220;page not found&#8221;: the address asked for does not exist.</span></li>'
    '<li class="reveal rv">Whose side? <span class="ans">&#8212; the server is working; the <b>requested address</b> is wrong or the page is gone. A server breakdown would be <b>500</b>.</span></li>'
    '</ul>',
    ar("وقّف وفكّر: لو المتصفح استقبل 404، يقول للمستخدم إيه — وأنهي جانب كان فيه المشكلة؟")))

A(s("",
    eyebrow("3 &#183; Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">The client requests data or processing from the server, and the server returns the response. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv tf-t">HTTPS is a communication protocol that adds encryption to HTTP. <span class="ans">&#8212; <b>true</b>: TLS.</span></li>'
    '<li class="reveal rv">The GET method is for sending data to the server. <span class="ans">&#8212; <b>false</b>: GET retrieves; POST sends.</span></li>'
    '<li class="reveal rv tf-t">Status code 404 indicates that the page is not found. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: العميل بيطلب والخادم بيرد — صح. HTTPS بيضيف تشفير لـ HTTP — صح. GET لإرسال البيانات — غلط، ده POST. 404 الصفحة مش موجودة — صح.")))

# ---------------- part 4: API and JSON ----------------

A(s("",
    eyebrow("Part 4 &#183; API (Application Programming Interface)"),
    h2("Programs asking programs"),
    '<div class="rise statement def"><em>API</em> &#8212; a system for exchanging data between different pieces of software.</div>',
    sub("In web applications, the frontend often sends requests to the backend <b>through an API</b> and receives data back. That data is often written in <b>JSON</b> (JavaScript Object Notation): easy for people to read, and for computers to process.",
        "max-width:58ch;margin-top:.8rem"),
    '<div class="rise json">{\n  <span class="key">"city"</span>: <span class="val">"Cairo"</span>,\n  <span class="key">"temperature"</span>: <span class="num">31</span>\n}</div>',
    '<ul class="rise check">'
    '<li class="reveal rv">Name one <b>key</b> and its <b>value</b>. <span class="ans">&#8212; key <b>"city"</b>, value <b>"Cairo"</b> (or key "temperature", value 31).</span></li>'
    '</ul>',
    ar("واجهة برمجة التطبيقات (API): مجموعة قواعد واضحة بتسمح لبرنامج يطلب بيانات أو وظائف من برنامج تاني. وممكن ترجّع بيانات بصيغة JSON، وهي صيغة نصية لتمثيل البيانات المهيكلة. اقرا البيانات دي وحدد مفتاح (key) وقيمته (value).")))

A(s("",
    eyebrow("4 &#183; Exam-style question"),
    h2("Match each description with a term"),
    '<table class="rise">'
    '<tr><th>Description</th><th>Term</th></tr>'
    '<tr><td>a &#183; A communication protocol for exchanging data between web browsers and servers</td><td class="reveal"><span>A &#183; HTTP</span></td></tr>'
    '<tr><td>b &#183; A system for exchanging data between different pieces of software</td><td class="reveal"><span>B &#183; API</span></td></tr>'
    '<tr><td>c &#183; A communication protocol that adds encryption to HTTP</td><td class="reveal"><span>C &#183; HTTPS</span></td></tr>'
    '</table>',
    sub("Choices: <b>A</b> HTTP &#183; <b>B</b> API &#183; <b>C</b> HTTPS.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("اربط كل وصف بالمصطلح: بروتوكول تبادل البيانات بين المتصفح والخادم = HTTP. تبادل البيانات بين برمجيات مختلفة = API. HTTP مع تشفير = HTTPS.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Status code 500 means the request was processed successfully. <span class="ans">&#8212; <b>false</b>: 500 is a server error; success is 200.</span></li>'
    '<li class="reveal rv">An API is a technology for adjusting the appearance of web pages. <span class="ans">&#8212; <b>false</b>: it exchanges data between software.</span></li>'
    '<li class="reveal rv">JSON is used to encrypt the connection. <span class="ans">&#8212; <b>false</b>: JSON is a data format; HTTPS encrypts.</span></li>'
    '<li class="reveal rv tf-t">To send login data, POST is the right method. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    ar("خلّي بالك: 500 مش نجاح — ده خطأ في الخادم. الـ API مش لشكل الصفحة. JSON صيغة بيانات مش تشفير. وبيانات الدخول بتتبعت بـ POST.")))

A(s("",
    eyebrow("Exam-style question &#183; 6 marks"),
    h2("A browser asks for a web page", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Explain, step by step&#8230;</h3><ul>'
    '<li>what happens when a browser requests a web page and the server responds</li>'
    '<li>refer to: <b>client</b>, <b>request</b>, <b>HTTP method</b>, <b>response</b>, <b>status code</b></li>'
    '</ul></div>'
    '<div class="pane b"><h3>A plan for your answer</h3><ul>'
    '<li>the client sends a request &#8212; GET, to retrieve</li>'
    '<li>the server receives and processes it</li>'
    '<li>the response comes back with a status code: 200, 404 or 500</li>'
    '</ul></div>'
    '</div>',
    ar("سؤال على نمط الامتحان: اشرح خطوة بخطوة إيه اللي بيحصل لما المتصفح يطلب صفحة ويب والخادم يستجيب. أشِر إلى: العميل، الطلب، طريقة طلب HTTP، الاستجابة، رمز حالة HTTP.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("A school wants a timetable app", "max-width:26ch"),
    sub("Students log in, view their timetable, and download a PDF. You plan how the client and server communicate.",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Choose the method.</b> Loading a student&#8217;s grade history, submitting the login form, requesting today&#8217;s schedule from another school system: GET or POST? Is an API involved in the last?</li>'
    '<li><b>Choose the protocol.</b> Should the login use HTTP or HTTPS? Why?</li>'
    '<li><b>Decide.</b> Recommend the design, with two reasons. In pairs, agree which action must use POST.</li>'
    '</ul>',
    sub("Stuck? GET retrieves and shows; POST sends data such as a login; HTTPS encrypts so passwords are not intercepted.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: مدرسة عايزة تطبيق ويب الطلاب يسجلوا فيه دخول ويشوفوا جدولهم وينزّلوا PDF. اختار GET ولا POST لكل إجراء، واختار HTTP ولا HTTPS للدخول، وقرّر بسببين.")))

A(s("",
    eyebrow("In a new context"),
    h2("A weather API", "max-width:26ch"),
    sub("A weather service offers an API that returns today&#8217;s forecast when a client sends a request.", "max-width:56ch;margin-top:.7rem"),
    '<table class="rise">'
    '<tr><th>Question</th><th>Answer</th></tr>'
    '<tr><td>Which HTTP method retrieves the forecast?</td><td class="reveal"><span>GET</span></td></tr>'
    '<tr><td>Why should the service use HTTPS?</td><td class="reveal"><span>So the data is encrypted and not changed on the way</span></td></tr>'
    '<tr><td>One advantage of receiving the data as JSON?</td><td class="reveal"><span>Easy for people to read and for programs to process</span></td></tr>'
    '</table>',
    ar("طبّق اللي اتعلمته: خدمة طقس عندها API بترجّع توقعات النهارده. أنهي طريقة طلب هتستخدم؟ وليه HTTPS؟ وميزة واحدة لـ JSON.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 3-2"),
    h2("Ask, answer, by the rules", "max-width:24ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> that <b>404</b> &#8212; Internet broken, server broken, or something else?</p>'
    '<div class="rise statement">Client <em>requests</em>, server <em>responds</em> &#8212; over HTTP/HTTPS, with a method (<em>GET/POST</em>), a <em>status code</em>, and often an <em>API</em> returning <em>JSON</em>.</div>',
    ar("افتكر: العميل بيطلب، والخادم بيستجيب — عبر HTTP/HTTPS، بأسلوب (GET/POST)، ورمز حالة، وغالبًا واجهة برمجة تطبيقات بترجّع بيانات JSON.")))

# ---------------- part 5: Qureo chapter 32, Flowchart ----------------

A(s("dark",
    '<div class="rise part">5</div>',
    h2("On the platform: Flowchart"),
    sub("Qureo chapter 32: plan a program as a drawing first &#8212; then write the code. With if and calculations.", "max-width:56ch"),
    ar("الجزء الخامس على المنصة: الفصل 32 — المخطط الانسيابي: نرسم البرنامج الأول، وبعدين نكتب الكود.")))

A(s("",
    eyebrow("5 &#183; The symbols"),
    h2("Four shapes, joined by arrows"),
    fig(FLOWSYM),
    sub("A <b>flowchart</b> draws a program&#8217;s steps in order. Arrows show which step comes next.", "max-width:60ch;margin-top:.3rem"),
    ar("المخطط الانسيابي بيرسم خطوات البرنامج بالترتيب: البيضاوي للبداية والنهاية، والمستطيل لخطوة معالجة، والمعين لسؤال إجابته نعم أو لا (يعني if)، ومتوازي الأضلاع للإدخال والإخراج (زي console.log). والأسهم بتوضح الخطوة اللي بعدها.")))

A(s("",
    eyebrow("5 &#183; if + operations"),
    h2("Follow the arrows"),
    chart(PRICE, ["price", "total"], [
        {"el": "start", "en": "Start here.", "ar": "نبدأ من هنا."},
        {"el": "p0", "set": {"price": "40"}, "en": "A process: price = 40.", "ar": "خطوة معالجة: price = 40."},
        {"el": "p1", "set": {"total": "120"}, "en": "A process with an operation: total = 40 * 3 = 120.", "ar": "خطوة فيها عملية حسابية: total = 40 * 3 = 120."},
        {"el": "d", "en": "A decision: is 120 > 100? Yes.", "ar": "سؤال: هل 120 > 100؟ أيوه."},
        {"el": "yes", "out": "Too expensive", "en": "Follow the Yes arrow: show \"Too expensive\".", "ar": "نمشي على سهم Yes: نعرض \"Too expensive\"."},
        {"el": "end", "en": "End. The No branch was never used.", "ar": "النهاية. فرع No متستخدمش خالص."},
    ]),
    ar("دوس Next step وامشي مع الأسهم: المستطيل بيحسب، والمعين بيسأل، وبنمشي في فرع واحد بس.")))

A(s("",
    eyebrow("5 &#183; From the drawing to the code"),
    h2("Every shape becomes a line"),
    '<div class="rise twocol"><div class="fcfig">' + PRICE.strip() + '</div><div>'
    '<div class="code" style="font-size:clamp(12px,1.45vw,19px)">' + K("let") + " price = " + Nn("40") + ";\n"
    + K("let") + " total = price * " + Nn("3") + ";\n\n" + K("if") + " (total > " + Nn("100") + ") {\n  "
    + LOG + "(" + S_('"Too expensive"') + ");\n} " + K("else") + " {\n  " + LOG + "(" + S_('"Buy it"') + ");\n}</div>"
    '<table><tr><th>Shape</th><th>In the code</th></tr>'
    '<tr><td>Rectangle (process)</td><td class="reveal"><span>let &#8230; = &#8230;; a calculation</span></td></tr>'
    '<tr><td>Diamond (decision)</td><td class="reveal"><span>if ( &#8230; )</span></td></tr>'
    '<tr><td>Yes / No arrows</td><td class="reveal"><span>the if { } and the else { }</span></td></tr>'
    '<tr><td>Parallelogram (output)</td><td class="reveal"><span>console.log( &#8230; )</span></td></tr>'
    '</table></div></div>',
    ar("كل شكل بيتحول لسطر: المستطيل = let أو عملية حسابية، المعين = if، سهم Yes = جوّه if، سهم No = else، ومتوازي الأضلاع = console.log.")))

A(s("",
    eyebrow("5 &#183; Your turn"),
    h2("Write the code for this flowchart", "max-width:24ch"),
    '<div class="rise twocol"><div class="fcfig">' + AB.strip() + '</div><div>'
    '<ul class="check">'
    '<li class="reveal rv">What does it show? <span class="ans">&#8212; <b>8</b>: 8 &gt; 5 is true, so the Yes branch shows a.</span></li>'
    '<li class="reveal rv">The code: <span class="ans"><span class="mono" style="white-space:pre;display:block;font-size:.92em">let a = 8;\nlet b = 5;\nif (a &gt; b) {\n  console.log(a);\n} else {\n  console.log(b);\n}</span></span></li>'
    '<li class="reveal rv">What would it show if b were 11? <span class="ans">&#8212; <b>11</b>: 8 &gt; 11 is false, so the No branch.</span></li>'
    '</ul></div></div>',
    ar("اكتب الكود للمخطط ده. فكّر الأول، وبعدين دوس على كل سطر. ده نفس فكرة مقارنة القيم في المحاضرة 9.")))

A(s("",
    eyebrow("5 &#183; Watch out"),
    h2("Rules of a good flowchart", "max-width:24ch"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">A diamond has only one way out. <span class="ans">&#8212; <b>false</b>: two, labelled <b>Yes</b> and <b>No</b>.</span></li>'
    '<li class="reveal rv tf-t">A flowchart begins at Start and finishes at End. <span class="ans">&#8212; <b>true</b>: ovals.</span></li>'
    '<li class="reveal rv">A calculation such as total = price * 3 goes in a diamond. <span class="ans">&#8212; <b>false</b>: a calculation is a process, a rectangle.</span></li>'
    '<li class="reveal rv tf-t">The arrows show the order the steps run in. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    ar("خلّي بالك: المعين ليه مخرجين Yes و No. بنبدأ بـ Start ونخلص بـ End. الحساب في مستطيل مش معين. والأسهم بتوضح الترتيب.")))

# ---------------- part 6: Qureo chapter 33, comprehension check ----------------

A(s("dark",
    '<div class="rise part">6</div>',
    h2("Comprehension check: chapters 31 and 32"),
    sub("Qureo chapter 33 reviews functions and flowcharts. Today, together: a function inside a flowchart.", "max-width:56ch"),
    ar("الجزء السادس: الفصل 33 — مراجعة الفصلين 31 و 32: الدوال والمخطط الانسيابي، مع بعض.")))

A(s("",
    eyebrow("6 &#183; A function in a flowchart"),
    h2("add3, then decide"),
    '<div class="rise code" style="font-size:clamp(12px,1.4vw,18px)">' + K("function") + " " + F("add3") + "(a, b, c) {\n  " + K("return") + " a + b + c;\n}</div>",
    chart(REVIEW, ["total"], [
        {"el": "start", "en": "Start.", "ar": "البداية."},
        {"el": "p0", "set": {"total": "12"}, "en": "A process that calls a function: add3(2, 4, 6) returns 12, so total = 12.", "ar": "خطوة بتنادي دالة: add3(2, 4, 6) بترجّع 12، يعني total = 12."},
        {"el": "d", "en": "A decision: is 12 > 10? Yes.", "ar": "سؤال: هل 12 > 10؟ أيوه."},
        {"el": "yes", "out": "Big total", "en": "Yes branch: show \"Big total\".", "ar": "فرع Yes: نعرض \"Big total\"."},
        {"el": "end", "en": "End.", "ar": "النهاية."},
    ]),
    ar("الدالة بترجّع قيمة، والمخطط بيقرر بيها. دوس Next step.")))

A(s("",
    eyebrow("6 &#183; Review &#183; your turn"),
    h2("Functions and flowcharts"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">add3(1, 1, 1) returns&#8230; <span class="ans">&#8212; <b>3</b>.</span></li>'
    '<li class="reveal rv">In the flowchart above, with add3(1, 2, 3), what is shown? <span class="ans">&#8212; <b>Small total</b>: 6 &gt; 10 is false.</span></li>'
    '<li class="reveal rv">Which shape would hold <span class="mono">if (total &gt; 10)</span>? <span class="ans">&#8212; the <b>diamond</b>.</span></li>'
    '<li class="reveal rv">A function without <span class="mono">return</span> gives back&#8230; <span class="ans">&#8212; <b>undefined</b>.</span></li>'
    '</ul>',
    ar("مراجعة: فكّر في كل سطر الأول، وبعدين دوس عليه.")))

A(s("dark",
    eyebrow("Remember these"),
    h2("What we learned"),
    '<ul class="rise check">'
    '<li>The <b>client</b> requests, the <b>server</b> responds.</li>'
    '<li><b>HTTP</b> carries the messages; <b>HTTPS</b> adds TLS encryption.</li>'
    '<li><b>GET</b> retrieves, <b>POST</b> sends. Status codes: <b>200</b> success, <b>404</b> not found, <b>500</b> server error.</li>'
    '<li>An <b>API</b> lets programs exchange data, often as <b>JSON</b>.</li>'
    '<li>A <b>flowchart</b>: oval start/end, rectangle process, diamond decision (if), parallelogram output.</li>'
    '</ul>',
    ar("العميل بيطلب والخادم بيرد • HTTP بينقل و HTTPS بيشفّر • GET بيجيب و POST بيبعت • 200 و 404 و 500 • API و JSON • والمخطط الانسيابي: بيضاوي، مستطيل، معين، متوازي أضلاع.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 10"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 10 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers lesson 3-2 and Qureo chapters 32 and 33. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس 3-2 والفصلين 32 و 33 على المنصة. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))


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

/* lecture 10's drawings */
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
@media print{.tbtns{display:none}}/* the flowchart player and the flowcharts */
.stepper.chartp{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.fcwrap svg,.fcfig svg{width:100%; max-width:440px; height:auto; display:block; margin:0 auto}
.fcwrap{max-height:62vh}
.fcwrap svg{max-height:62vh}
.fc [data-id] .shp{transition:fill .3s,stroke .3s}
.fc [data-id].on .shp{fill:var(--gold-pale); stroke:var(--gold); stroke-width:5}
.chartp .tcons{margin-top:.8rem}
.fcfig{background:#fff; border:1px solid var(--line); border-radius:12px; padding:.6rem}
.twocol{display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1.1fr); gap:clamp(14px,2vw,30px); align-items:start; margin-top:.6rem}
@media(max-width:760px){.twocol{grid-template-columns:1fr}}
.json{display:block; background:var(--ink); color:#E6EDF3; border-radius:12px; padding:clamp(12px,1.6vw,20px); font-family:"JetBrains Mono",monospace; font-size:clamp(14px,1.8vw,24px); line-height:1.6; white-space:pre; margin:.8rem 0 .4rem}
.json .key{color:#9DC7FF} .json .val{color:#8FE3D6} .json .num{color:#F7C66B}
@media(max-width:760px){.stepper.chartp{grid-template-columns:1fr} .fcwrap,.fcwrap svg{max-height:none}}

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
BASE = "scripts/lecture10_slides_base.html"
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
LECTURE_JS = '/* ---- the step-by-step players (lectures 9 and 10) ---------------------------------\n   .stepper[data-kind=flow]: lights one tier per step and shows what is\n   passed on. .stepper[data-kind=code]: lights a code line, fills the value\n   boxes and prints to the console; in a flowchart (.chartp) it lights the\n   shape whose data-id is the step\'s el. Next step, Play all, Again. Space and\n   Enter on the buttons must not also turn the slide, so they stop here. */\n(function(){\n  if(!document.querySelectorAll) return;\n  document.querySelectorAll(\'.stepper\').forEach(function(box){\n    var steps = JSON.parse(box.getAttribute(\'data-steps\'));\n    var kind = box.getAttribute(\'data-kind\');\n    var en = box.querySelector(\'.tstat .en\'), ar = box.querySelector(\'.tstat .ar\');\n    var nx = box.querySelector(\'.nx\'), pl = box.querySelector(\'.pl\'), rs = box.querySelector(\'.rs\');\n    var lines = box.querySelectorAll(\'.ln\'), cons = box.querySelector(\'.tcons\');\n    var tiers = box.querySelectorAll(\'.tier\'), packet = box.querySelector(\'.packet\');\n    var nodes = box.querySelectorAll(\'[data-id]\');\n    var i = 0, timer = null;\n\n    function stop(){ if(timer){ clearInterval(timer); timer = null; } }\n    /* In an Arabic (right-to-left) line, \'12 > 10\' shows mirrored as \'12 < 10\'.\n       Each run of code is wrapped in a left-to-right isolate (U+2066 ... U+2069)\n       so it reads exactly as typed. */\n    function iso(t){\n      return String(t || \'\').replace(/[A-Za-z0-9_"\'(][A-Za-z0-9_ .,*+\\-<>=!"\'()\\/%]*[A-Za-z0-9_"\')]/g, function(m){\n        return /[<>=*+]/.test(m) ? \'\\u2066\' + m + \'\\u2069\' : m;\n      });\n    }\n    function say(e, a){ en.textContent = e || \'\'; ar.textContent = iso(a); }\n    function reset(){\n      stop(); i = 0;\n      for(var j = 0; j < lines.length; j++) lines[j].classList.remove(\'hot\');\n      for(var t = 0; t < tiers.length; t++) tiers[t].classList.remove(\'on\');\n      for(var q = 0; q < nodes.length; q++) nodes[q].classList.remove(\'on\');\n      if(packet) packet.textContent = \'\';\n      if(cons) cons.querySelectorAll(\'.line\').forEach(function(l){ l.remove(); });\n      box.querySelectorAll(\'.box b\').forEach(function(b){ b.textContent = \'?\'; b.classList.remove(\'pop\'); });\n      nx.disabled = false; pl.disabled = false;\n      say(\'Press Next step to start.\', \'اضغط Next step عشان تبدأ.\');\n    }\n    function next(){\n      if(i >= steps.length) return;\n      var s = steps[i++];\n      if(kind === \'flow\'){\n        for(var t = 0; t < tiers.length; t++) tiers[t].classList.toggle(\'on\', tiers[t].getAttribute(\'data-t\') === s.t);\n        packet.textContent = \'\';\n        if(s.msg){ var p = document.createElement(\'span\'); p.textContent = s.msg; packet.appendChild(p); }\n      } else {\n        for(var j = 0; j < lines.length; j++) lines[j].classList.toggle(\'hot\', j === s.ln);\n        for(var q = 0; q < nodes.length; q++) nodes[q].classList.toggle(\'on\', nodes[q].getAttribute(\'data-id\') === s.el);\n        if(s.set) Object.keys(s.set).forEach(function(k){\n          var b = box.querySelector(\'.box[data-k="\' + k + \'"] b\');\n          if(!b) return;\n          b.textContent = s.set[k];\n          b.classList.remove(\'pop\'); void b.offsetWidth; b.classList.add(\'pop\');\n        });\n        if(s.out !== undefined){\n          var l = document.createElement(\'span\'); l.className = \'line\'; l.textContent = s.out; cons.appendChild(l);\n        }\n      }\n      say(s.en, s.ar);\n      if(i >= steps.length){ stop(); nx.disabled = true; pl.disabled = true; }\n    }\n    nx.addEventListener(\'click\', function(){ stop(); next(); });\n    pl.addEventListener(\'click\', function(){\n      if(timer) return;\n      if(i >= steps.length) reset();\n      pl.disabled = true; next(); timer = setInterval(next, 1500);\n    });\n    rs.addEventListener(\'click\', reset);\n    box.addEventListener(\'keydown\', function(e){\n      if(e.target.tagName === \'BUTTON\' && (e.key === \' \' || e.key === \'Enter\')) e.stopPropagation();\n    });\n    reset();\n  });\n})();'
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

