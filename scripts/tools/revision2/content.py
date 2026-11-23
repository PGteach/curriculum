# --------------------------------------------------------------------------
# diagrams -- inline SVG, reused from lectures 5, 6 and 7, so the
# revision shows the picture each lesson was taught with. The booklet
# reads these out of this file.
# --------------------------------------------------------------------------

KEYS = '''
<svg viewBox="0 0 900 300" role="img" aria-label="Common-key cryptography uses one key to lock and unlock; public-key cryptography locks with a public key and unlocks with a different private key">
  <rect x="20" y="16" width="420" height="268" rx="12" fill="var(--teal)" opacity=".08" stroke="var(--teal)" stroke-width="2"/>
  <text x="230" y="48" text-anchor="middle" font-size="19" font-weight="700" fill="var(--ink)">Common-key cryptography</text>
  <text x="230" y="72" text-anchor="middle" font-size="14" fill="var(--soft)">also called symmetric-key</text>
  <g transform="translate(70,98)">
    <circle cx="22" cy="22" r="16" fill="none" stroke="var(--teal)" stroke-width="6"/>
    <rect x="36" y="18" width="70" height="9" rx="3" fill="var(--teal)"/>
    <rect x="88" y="27" width="8" height="13" fill="var(--teal)"/><rect x="100" y="27" width="6" height="9" fill="var(--teal)"/>
  </g>
  <text x="190" y="122" font-size="16" fill="var(--ink)">one key</text>
  <text x="190" y="144" font-size="16" fill="var(--ink)">locks <tspan font-weight="700">and</tspan> unlocks</text>
  <line x1="40" y1="176" x2="420" y2="176" stroke="var(--line)" stroke-width="1.5"/>
  <text x="44" y="206" font-size="16" fill="var(--ink)"><tspan font-weight="700" fill="var(--teal)">+</tspan> fast &#8212; exchanges data quickly</text>
  <text x="44" y="238" font-size="16" fill="var(--ink)"><tspan font-weight="700" fill="#9C3B2E">&#8722;</tspan> both sides need the same key:</text>
  <text x="64" y="262" font-size="16" fill="var(--ink)">how do you share it safely?</text>

  <rect x="460" y="16" width="420" height="268" rx="12" fill="var(--gold)" opacity=".10" stroke="var(--gold)" stroke-width="2"/>
  <text x="670" y="48" text-anchor="middle" font-size="19" font-weight="700" fill="var(--ink)">Public-key cryptography</text>
  <text x="670" y="72" text-anchor="middle" font-size="14" fill="var(--soft)">a pair of linked keys</text>
  <g transform="translate(490,90)">
    <circle cx="18" cy="18" r="13" fill="none" stroke="var(--gold)" stroke-width="5"/>
    <rect x="29" y="15" width="54" height="7" rx="3" fill="var(--gold)"/>
    <rect x="70" y="22" width="6" height="10" fill="var(--gold)"/>
  </g>
  <text x="590" y="113" font-size="16" fill="var(--ink)"><tspan font-weight="700">public key</tspan> locks</text>
  <g transform="translate(490,132)">
    <circle cx="18" cy="18" r="13" fill="none" stroke="var(--ink)" stroke-width="5"/>
    <rect x="29" y="15" width="54" height="7" rx="3" fill="var(--ink)"/>
    <rect x="70" y="22" width="6" height="10" fill="var(--ink)"/>
  </g>
  <text x="590" y="155" font-size="16" fill="var(--ink)"><tspan font-weight="700">private key</tspan> unlocks</text>
  <line x1="480" y1="176" x2="860" y2="176" stroke="var(--line)" stroke-width="1.5"/>
  <text x="484" y="206" font-size="16" fill="var(--ink)"><tspan font-weight="700" fill="var(--teal)">+</tspan> the public key can be given to anyone</text>
  <text x="484" y="230" font-size="16" fill="var(--ink)"><tspan font-weight="700" fill="var(--teal)">+</tspan> shares a key safely</text>
  <text x="484" y="262" font-size="16" fill="var(--ink)"><tspan font-weight="700" fill="#9C3B2E">&#8722;</tspan> slow for large amounts of data</text>
</svg>'''

HANDSHAKE = '''
<svg viewBox="0 0 900 360" role="img" aria-label="HTTPS in three stages: the server sends its certificate and public key, the browser sends a common key locked with that public key, then data flows locked with the common key">
  <rect x="20" y="10" width="170" height="52" rx="10" fill="#fff" stroke="var(--ink)" stroke-width="2"/>
  <text x="105" y="43" text-anchor="middle" font-size="18" font-weight="700" fill="var(--ink)">Browser</text>
  <rect x="710" y="10" width="170" height="52" rx="10" fill="var(--ink)"/>
  <text x="795" y="43" text-anchor="middle" font-size="18" font-weight="700" fill="#fff">Web server</text>
  <line x1="105" y1="62" x2="105" y2="350" stroke="var(--line)" stroke-width="2" stroke-dasharray="5 6"/>
  <line x1="795" y1="62" x2="795" y2="350" stroke="var(--line)" stroke-width="2" stroke-dasharray="5 6"/>

  <circle cx="40" cy="112" r="15" fill="var(--teal)"/><text x="40" y="118" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">1</text>
  <text x="450" y="94" text-anchor="middle" font-size="16" font-weight="700" fill="var(--ink)">digital certificate + public key</text>
  <line x1="780" y1="112" x2="124" y2="112" stroke="var(--gold)" stroke-width="3"/>
  <polygon points="118,112 130,105 130,119" fill="var(--gold)"/>
  <text x="450" y="138" text-anchor="middle" font-size="14" fill="var(--soft)">the browser checks the certificate with a certificate authority (CA)</text>

  <circle cx="40" cy="202" r="15" fill="var(--teal)"/><text x="40" y="208" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">2</text>
  <text x="450" y="184" text-anchor="middle" font-size="16" font-weight="700" fill="var(--ink)">common key, locked with the server&#8217;s public key</text>
  <line x1="120" y1="202" x2="776" y2="202" stroke="var(--gold)" stroke-width="3"/>
  <polygon points="782,202 770,195 770,209" fill="var(--gold)"/>
  <text x="450" y="228" text-anchor="middle" font-size="14" fill="var(--soft)">the server unlocks it with its private key &#8212; now both have the common key</text>

  <circle cx="40" cy="292" r="15" fill="var(--teal)"/><text x="40" y="298" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">3</text>
  <text x="450" y="274" text-anchor="middle" font-size="16" font-weight="700" fill="var(--ink)">data, locked with the shared common key</text>
  <line x1="124" y1="292" x2="776" y2="292" stroke="var(--teal)" stroke-width="3"/>
  <polygon points="118,292 130,285 130,299" fill="var(--teal)"/><polygon points="782,292 770,285 770,299" fill="var(--teal)"/>
  <text x="450" y="318" text-anchor="middle" font-size="14" fill="var(--soft)">fast, in both directions, for the rest of the session</text>

  <rect x="230" y="334" width="190" height="22" rx="6" fill="var(--gold)" opacity=".25"/>
  <text x="325" y="350" text-anchor="middle" font-size="14" font-weight="600" fill="var(--ink)">1&#8211;2 public-key</text>
  <rect x="480" y="334" width="190" height="22" rx="6" fill="var(--teal)" opacity=".18"/>
  <text x="575" y="350" text-anchor="middle" font-size="14" font-weight="600" fill="var(--ink)">3 common-key</text>
</svg>'''

FACTORS = '''
<svg viewBox="0 0 900 230" role="img" aria-label="The three factors of authentication: knowledge, possession and biometric, with the book's examples of each">
  <rect x="20" y="14" width="270" height="200" rx="12" fill="var(--teal)" opacity=".09" stroke="var(--teal)" stroke-width="2"/>
  <text x="155" y="50" text-anchor="middle" font-size="20" font-weight="700" fill="var(--ink)">Knowledge</text>
  <text x="155" y="76" text-anchor="middle" font-size="14" fill="var(--soft)">something the user knows</text>
  <text x="155" y="122" text-anchor="middle" font-size="16" fill="var(--ink)">password</text>
  <text x="155" y="150" text-anchor="middle" font-size="16" fill="var(--ink)">secret question</text>

  <rect x="315" y="14" width="270" height="200" rx="12" fill="var(--gold)" opacity=".12" stroke="var(--gold)" stroke-width="2"/>
  <text x="450" y="50" text-anchor="middle" font-size="20" font-weight="700" fill="var(--ink)">Possession</text>
  <text x="450" y="76" text-anchor="middle" font-size="14" fill="var(--soft)">something the user has</text>
  <text x="450" y="114" text-anchor="middle" font-size="16" fill="var(--ink)">one-time password</text>
  <text x="450" y="140" text-anchor="middle" font-size="16" fill="var(--ink)">SMS code &#183; phone notification</text>
  <text x="450" y="166" text-anchor="middle" font-size="16" fill="var(--ink)">smart card &#183; IC card</text>

  <rect x="610" y="14" width="270" height="200" rx="12" fill="var(--ink)" opacity=".07" stroke="var(--ink)" stroke-width="2"/>
  <text x="745" y="50" text-anchor="middle" font-size="20" font-weight="700" fill="var(--ink)">Biometric</text>
  <text x="745" y="76" text-anchor="middle" font-size="14" fill="var(--soft)">a feature of the user&#8217;s body</text>
  <text x="745" y="122" text-anchor="middle" font-size="16" fill="var(--ink)">fingerprint</text>
  <text x="745" y="150" text-anchor="middle" font-size="16" fill="var(--ink)">face recognition</text>
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
# None in a revision deck: every slide is full width.
VIZ = {}
VIZ_USED = []


# ---------------- the revision data ----------------
# data.py beside this file holds one record per lesson; the deck, the
# booklet and the flashcards all read it.
import importlib.util as _ilu, os as _os, html as _html, json as _json
_spec = _ilu.spec_from_file_location("revdata", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "tools", "revision2", "data.py"))
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
