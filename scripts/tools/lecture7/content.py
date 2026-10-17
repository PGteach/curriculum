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
