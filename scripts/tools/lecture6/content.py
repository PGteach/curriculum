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
