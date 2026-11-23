# -*- coding: utf-8 -*-
"""Build the Chapter 2 Revision's deck.

    python scripts/build_revision2_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/revision2_slides_base.html and writes revision/chapter2/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the side drawings
added. Always starts from the base, never from the published deck.

A revision of Unit 2, Cybersecurity (lessons 2-1 to 2-3), one lesson at a time, at the teacher's request. Nothing
here is new: every line comes from the lessons as they were taught in
lectures 5 to 7. The data is tools/revision2/data.py -- per lesson, the book's
key takeaway, its key terms, the exam traps, and the lesson's exam-style
question with the marking points from that lecture's answer key. The
diagrams are the ones the lessons were taught with.

Each lesson gets a divider with its key takeaway, its picture, flashcards
of its key terms, true-or-false exam traps, and its exam question with the
marking points to reveal one by one. The flashcards are this lecture's own;
their script is tools/revision2/script.js, added to the page's own script.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "revision/chapter2/slides/index.html"


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

# ---- this revision ----
CH = 2
UNIT = "Cybersecurity"
UNIT_AR = "الوحدة التانية: الأمن السيبراني"
LECTURES = "lectures 5 to 7"
SECOND = {"2-1": "HANDSHAKE", "2-2": "DMZ", "2-3": "MATRIX"}
CORE_HEAD = {"2-1": "Two keys, two jobs", "2-2": "Four layers of defense",
             "2-3": "Six stages, in order"}
SECOND_HEAD = {"2-1": "The three stages of HTTPS", "2-2": "Why a DMZ", "2-3": "Fix the worst risk first"}

LS = D.LESSONS
SVG = globals()

# 1 title
A(s("dark",
    '<div class="rise eyebrow" id="lectureBadge">Programming &amp; Artificial Intelligence</div>',
    h2("Ready for Chapter %d?" % CH, "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("A revision of Unit %d, %s: %d lessons, one at a time. For each one: the big idea, the key terms on flashcards, the exam traps, and one exam-style question with its marking points."
        % (CH, UNIT, len(LS)), "max-width:60ch;margin-top:1rem"),
    ar("مراجعة %s، درس درس: الفكرة الأساسية، والمصطلحات على كروت، وفخاخ الامتحان، وسؤال على نمط الامتحان بنقط التصحيح." % UNIT_AR)))

# 2 how to revise
A(s("",
    eyebrow("How to revise today"),
    h2("Three steps for every lesson", "max-width:24ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#127183;</div><div class="role">Step 1</div><h3>Flashcards</h3><p>Say the meaning out loud, then flip. Be honest: &#8220;Not yet&#8221; brings it back.</p></div>'
    '<div class="card"><div class="ico">&#9888;</div><div class="role">Step 2</div><h3>Exam traps</h3><p>True or false? Decide before you tap.</p></div>'
    '<div class="card"><div class="ico">&#128221;</div><div class="role">Step 3</div><h3>Exam question</h3><p>Plan your answer, then reveal the marking points one by one.</p></div>'
    '</div>',
    ar("لكل درس: كروت المصطلحات — قول المعنى بصوتك وبعدين اقلب. وبعدين فخاخ الامتحان: صح ولا غلط. وفي الآخر سؤال امتحان: خطّط إجابتك وبعدين اكشف نقط التصحيح.")))

# 3 the unit at a glance
A(s("",
    eyebrow("Unit %d at a glance" % CH),
    h2("%d lessons" % len(LS), "max-width:28ch"),
    '<div class="rise timeline">'
    + "".join('<div class="tl"><h3>%s &#183; %s</h3><p>%s</p></div>' % (L["id"], L["title"], L["remember"]) for L in LS)
    + '</div>',
    ar(" • ".join(L["id"] for L in LS) + " — كل درس وفكرته الأساسية في سطر.")))

for L in LS:
    lid = L["id"]
    # the lesson's own divider, with the book's key takeaway
    A(s("dark",
        '<div class="rise part">%s</div>' % lid,
        h2(L["title"], "max-width:26ch"),
        '<div class="rise remember">&#8220;%s&#8221;</div>' % L["remember"],
        ar(L["remember_ar"])))
    # the picture the lesson was taught with
    A(s("",
        eyebrow("%s &#183; In one picture" % lid),
        h2(CORE_HEAD[lid]),
        fig(SVG[L["svg"]]),
        ar("نفس الرسمة اللي اتشرح بيها الدرس %s. اشرح كل جزء فيها بكلامك." % lid)))
    if SECOND.get(lid):
        A(s("",
            eyebrow("%s &#183; One more picture" % lid),
            h2(SECOND_HEAD[lid]),
            fig(SVG[SECOND[lid]]),
            ar("اشرح الرسمة دي لزميلك في دقيقة.")))
    # flashcards
    A(s("",
        eyebrow("%s &#183; Key terms &#183; %d cards" % (lid, len(L["terms"]))),
        h2("Say it, then flip", "max-width:22ch"),
        cards(L["terms"]),
        ar("قول التعريف بصوت عالي الأول، وبعدين اقلب الكارت. لو عرفته دوس I knew it، ولو لأ دوس Not yet وهيرجعلك تاني.")))
    # exam traps
    A(s("",
        eyebrow("%s &#183; Exam traps" % lid),
        h2("True or false?"),
        '<ul class="rise check" style="margin-top:.6rem">'
        + "".join('<li class="reveal rv%s">%s <span class="ans">&#8212; <b>%s</b>: %s</span></li>'
                  % (" tf-t" if ok else "", st, "true" if ok else "false", why) for st, ok, why in L["traps"])
        + '</ul>',
        sub("Decide first, then tap.", "margin-top:.7rem;color:var(--soft)"),
        ar("قرّر الأول صح ولا غلط، وبعدين دوس. الجمل دي من الكتاب وكتاب التقييمات.")))
    # the lesson's exam-style question, with its marking points
    ex = L["exam"]
    A(s("",
        eyebrow("%s &#183; Exam-style question &#183; %d marks" % (lid, ex["marks"])),
        h2("Plan it, then check the points", "max-width:24ch"),
        sub(ex["q"], "max-width:62ch;margin-top:.4rem"),
        '<ul class="rise check plan" style="margin-top:.7rem">'
        + "".join('<li class="reveal rv">Point %d <span class="ans">&#8212; %s</span></li>' % (k + 1, p)
                  for k, p in enumerate(D.POINTS[lid]))
        + '</ul>',
        sub("Source: %s. Each point is about one mark." % ex["src"], "margin-top:.6rem;color:var(--soft)"),
        ar("اكتب خطة إجابتك في كشكولك الأول، وبعدين اكشف نقط التصحيح واحدة واحدة وقارن.")))

# mixed quick-fire
A(s("",
    eyebrow("All %d lessons &#183; quick-fire" % len(LS)),
    h2("Mixed questions"),
    '<ul class="rise check" style="margin-top:.6rem">'
    + "".join('<li class="reveal rv">%s <span class="ans">&#8212; %s</span></li>' % (q, a) for q, a in D.QUICK)
    + '</ul>',
    ar("أسئلة من كل الدروس متلخبطة — زي الامتحان. فكّر وبعدين دوس.")))

# exam tips
A(s("",
    eyebrow("Before the exam"),
    h2("Four habits that score marks", "max-width:24ch"),
    '<table class="rise"><tr><th>Habit</th><th>Why</th></tr>'
    + "".join('<tr><td><b>%s</b></td><td>%s</td></tr>' % (t, w) for t, w, _ in D.EXAM_TIPS)
    + '</table>',
    ar(" ".join(a for _, _, a in D.EXAM_TIPS))))

# checklist
A(s("dark",
    eyebrow("Can you&#8230;?"),
    h2("Your checklist"),
    '<ul class="rise check">'
    + "".join('<li><b>%s</b> &#8212; define %s.</li>' % (L["id"], ", ".join(t[0] for t in L["terms"][:4])) for L in LS)
    + '<li>Explain each lesson&#8217;s exam question in about six points.</li>'
    + '</ul>',
    ar("لو تقدر تعمل كل ده، انت جاهز. ولو لأ، ارجع لكروت الدرس ده.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Chapter %d Revision" % CH),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Chapter %d Revision quiz" width="250" height="250">' % CH
    + '<div class="txt"><p class="sub">A mixed revision exam on all of Unit %d, drawn from %s. ' % (CH, LECTURES)
    + 'At the end it shows you, lesson by lesson, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان مراجعة على الوحدة كلها. في الآخر هيوضحلك انت ضعيف في أنهي درس بالظبط.")))


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

/* the Chapter 2 Revision's drawings */
.statement.def{font-size:clamp(18px,2.15vw,30px); line-height:1.28; max-width:46ch}
/* code cards, as lecture 8; no ligatures, so >= reads as typed */
.code{display:block; background:var(--ink); color:#E6EDF3; text-align:left; padding:clamp(12px,1.7vw,22px); border-radius:12px; margin:.9rem 0 .4rem; font-family:"JetBrains Mono",monospace; font-size:clamp(13px,1.6vw,21px); line-height:1.6; white-space:pre; overflow-x:auto; max-width:100%}
.code .k,.tcode .k{color:#FF9D7A} .code .s,.tcode .s{color:#8FE3D6} .code .n,.tcode .n{color:#F7C66B} .code .f,.tcode .f{color:#9DC7FF} .code .c,.tcode .c{color:#7C8B99}
.code,.tcode,.mono,.codeline,code,.qcode{font-variant-ligatures:none; font-feature-settings:"liga" 0,"calt" 0}
.codeline{display:inline-block; background:var(--ink); color:#8FE3D6; padding:.25em .6em; border-radius:7px; font-family:"JetBrains Mono",monospace; font-size:.9em}
.part{font:600 clamp(40px,8vw,110px)/1 Fraunces,serif; color:var(--gold)}
.remember{font-family:Fraunces,serif; font-weight:600; font-size:clamp(19px,2.4vw,32px); line-height:1.3; max-width:44ch; margin-top:1rem}
.remember em{font-style:normal; color:var(--gold)}
.tbtns{display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.6rem}
.tbtns button{font:inherit; font-size:clamp(13px,1.35vw,17px); font-weight:600; border-radius:9px; padding:.5em 1em; cursor:pointer; background:var(--teal); color:#fff; border:1px solid var(--teal)}
.tbtns button.alt{background:#fff; color:var(--ink); border-color:var(--line)}
.tbtns button:disabled{opacity:.4; cursor:default}
/* flashcards */
.fcards{margin-top:.8rem; max-width:760px}
.fcard{position:relative; min-height:clamp(150px,24vh,230px); border-radius:16px; cursor:pointer; background:#fff; border:2px solid var(--line); box-shadow:0 10px 24px rgba(22,35,63,.08); display:flex; align-items:center; justify-content:center; text-align:center; padding:1rem 1.4rem; transition:transform .35s, border-color .3s}
.fcard:focus-visible{outline:3px solid var(--gold); outline-offset:3px}
.fcard .ff{font:600 clamp(24px,3.6vw,46px)/1.15 Fraunces,serif; color:var(--ink)}
.fcard .fb{display:none; font-size:clamp(15px,1.9vw,24px); line-height:1.45; color:var(--ink)}
.fcard .fb .ar{display:block; margin-top:.5rem; color:var(--soft); font-size:.88em}
.fcard.flipped{border-color:var(--teal); background:var(--teal-pale); transform:rotateX(6deg)}
.fcard.flipped .ff{display:none} .fcard.flipped .fb{display:block}
.fcard.done{border-color:var(--gold); background:var(--gold-pale)}
.fprog{margin-top:.6rem; color:var(--soft); font-size:clamp(13px,1.4vw,17px)}
/* the answer plan for an exam question: one reveal per marking point */
.plan li{margin-bottom:.45rem}
.mark{display:inline-block; background:var(--gold); color:#fff; font-weight:700; border-radius:99px; padding:.05em .6em; font-size:.85em; margin-left:.3em}
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
BASE = "scripts/revision2_slides_base.html"
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
LECTURE_JS = '/* ---- flashcards (revision lectures 12 and 13) --------------------------------\n   .fcards: the term on the front; Flip (or tap the card) shows the definition,\n   in English and Arabic. "I knew it" takes the card out of the pile; "Not\n   yet" sends it to the back, so it comes round again. Space and Enter on the\n   card or a button stay here, so they do not also turn the slide. */\n(function(){\n  if(!document.querySelectorAll) return;\n  document.querySelectorAll(\'.fcards\').forEach(function(box){\n    var all = JSON.parse(box.getAttribute(\'data-cards\'));\n    var card = box.querySelector(\'.fcard\'), front = box.querySelector(\'.ff\');\n    var en = box.querySelector(\'.fb .en\'), ar = box.querySelector(\'.fb .ar\'), prog = box.querySelector(\'.fprog\');\n    var fl = box.querySelector(\'.fl\'), kn = box.querySelector(\'.kn\'), ny = box.querySelector(\'.ny\'), rs = box.querySelector(\'.rs\');\n    var pile = [], known = 0;\n\n    function show(){\n      card.classList.remove(\'flipped\');\n      if(!pile.length){\n        front.textContent = \'All \' + all.length + \' known!\';\n        en.textContent = \'\'; ar.textContent = \'\';\n        prog.textContent = \'Well done — press Start again to go through them once more.\';\n        fl.disabled = kn.disabled = ny.disabled = true;\n        card.classList.add(\'done\');\n        return;\n      }\n      card.classList.remove(\'done\');\n      var c = all[pile[0]];\n      front.textContent = c[0];\n      en.textContent = c[1]; ar.textContent = c[2] || \'\';\n      prog.textContent = \'Known \' + known + \' of \' + all.length + \' · \' + pile.length + \' left · say the meaning, then flip\';\n      fl.disabled = kn.disabled = ny.disabled = false;\n    }\n    function flip(){ if(pile.length) card.classList.toggle(\'flipped\'); }\n    function start(){\n      pile = all.map(function(_, k){ return k; });\n      known = 0;\n      show();\n    }\n    fl.addEventListener(\'click\', flip);\n    card.addEventListener(\'click\', flip);\n    kn.addEventListener(\'click\', function(){ if(!pile.length) return; pile.shift(); known++; show(); });\n    ny.addEventListener(\'click\', function(){ if(!pile.length) return; pile.push(pile.shift()); show(); });\n    rs.addEventListener(\'click\', start);\n    box.addEventListener(\'keydown\', function(e){\n      if(e.key !== \' \' && e.key !== \'Enter\') return;\n      var t = e.target;\n      if(t === card){ e.preventDefault(); e.stopPropagation(); flip(); }\n      else if(t.tagName === \'BUTTON\') e.stopPropagation();\n    });\n    start();\n  });\n})();'
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

