# -*- coding: utf-8 -*-
"""Build Lecture 5's deck.

    python scripts/build_lecture5_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/lecture5_slides_base.html and writes lecture5/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the side drawings
added. Always starts from the base, never from the published deck.

Content is Lesson 2-1, Cryptographic Technologies and Authentication, the
English textbook pp. 33-40, and nothing outside the curriculum. Where the
Arabic textbook (pp. 31-37) and the ministry's assessment book go further
than the English book, the deck follows them, because the assessment asks
about it: session keys, the certificate checks (validity, chain of trust,
name), 2FA against MFA, and that a padlock is not a promise about content.

The helpers, port_lightbox(), the exam-code gate, the video and reveal code
and the build block are lecture 4's, unchanged. The Arabic follows the
Arabic textbook's lesson 2-1 point by point, said in Egyptian Arabic, with
the book's own terms kept as they are.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "lecture5/slides/index.html"


# --------------------------------------------------------------------------
# diagrams -- inline SVG, coloured from the page's CSS variables so they follow
# LECTURE_ACCENT. Labels only, never the sentence that explains them (that is
# HTML, where it stays readable when the slide is scaled); no label under 14
# units. The booklet reads these out of this file, so both show one picture.
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

SHOP = '''
<svg viewBox="0 0 900 250" role="img" aria-label="Buying online: HTTPS encryption, the digital certificate, multi-factor login and a digital signature each stop a different threat">
  <g font-size="15">
    <rect x="10" y="12" width="205" height="226" rx="12" fill="#fff" stroke="var(--line)" stroke-width="2"/>
    <circle cx="40" cy="44" r="16" fill="var(--teal)"/><text x="40" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">1</text>
    <text x="112" y="92" text-anchor="middle" font-weight="700" fill="var(--ink)">You open the site</text>
    <text x="112" y="132" text-anchor="middle" font-size="17" font-weight="700" fill="var(--teal)">Encryption</text>
    <text x="112" y="182" text-anchor="middle" fill="var(--soft)">stops</text>
    <text x="112" y="206" text-anchor="middle" font-weight="600" fill="#9C3B2E">eavesdropping</text>

    <rect x="232" y="12" width="205" height="226" rx="12" fill="#fff" stroke="var(--line)" stroke-width="2"/>
    <circle cx="262" cy="44" r="16" fill="var(--teal)"/><text x="262" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">2</text>
    <text x="334" y="92" text-anchor="middle" font-weight="700" fill="var(--ink)">Browser checks it</text>
    <text x="334" y="132" text-anchor="middle" font-size="17" font-weight="700" fill="var(--teal)">Digital certificate</text>
    <text x="334" y="182" text-anchor="middle" fill="var(--soft)">stops</text>
    <text x="334" y="206" text-anchor="middle" font-weight="600" fill="#9C3B2E">a fake site</text>

    <rect x="454" y="12" width="205" height="226" rx="12" fill="#fff" stroke="var(--line)" stroke-width="2"/>
    <circle cx="484" cy="44" r="16" fill="var(--teal)"/><text x="484" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">3</text>
    <text x="556" y="92" text-anchor="middle" font-weight="700" fill="var(--ink)">You log in</text>
    <text x="556" y="124" text-anchor="middle" font-size="17" font-weight="700" fill="var(--teal)">Multi-factor</text>
    <text x="556" y="146" text-anchor="middle" font-size="17" font-weight="700" fill="var(--teal)">authentication</text>
    <text x="556" y="182" text-anchor="middle" fill="var(--soft)">stops</text>
    <text x="556" y="206" text-anchor="middle" font-weight="600" fill="#9C3B2E">unauthorized login</text>

    <rect x="676" y="12" width="214" height="226" rx="12" fill="#fff" stroke="var(--line)" stroke-width="2"/>
    <circle cx="706" cy="44" r="16" fill="var(--teal)"/><text x="706" y="50" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">4</text>
    <text x="783" y="92" text-anchor="middle" font-weight="700" fill="var(--ink)">You send the order</text>
    <text x="783" y="132" text-anchor="middle" font-size="17" font-weight="700" fill="var(--teal)">Digital signature</text>
    <text x="783" y="182" text-anchor="middle" fill="var(--soft)">detects</text>
    <text x="783" y="206" text-anchor="middle" font-weight="600" fill="#9C3B2E">tampering</text>
  </g>
</svg>'''


# ---------------- side visuals ----------------
# A slide whose content fills only the left half of a wide screen gets an
# animated explainer on the right. Each drawing plays once when the slide
# opens and again when tapped. Under 1000px wide the drawing is hidden and
# the slide keeps its one-column layout, because the drawing adds to the
# content and never replaces it. The final frame of every animation is the
# element's own style, so with reduced motion (every animation off) and in
# print the drawing shows complete.

def vcap(en, arabic):
    return '<p class="vcap"><b>%s</b><span dir="rtl">%s</span></p>' % (en, arabic)


def v_padlock():
    return ('<aside class="rise viz">'
            '<svg viewBox="0 0 400 230" role="img" aria-label="An address bar with a padlock that locks">'
            '<rect x="10" y="20" width="380" height="54" rx="27" class="bar0"/>'
            '<g class="lockmini"><rect x="32" y="40" width="20" height="16" rx="3" class="lkbody"/>'
            '<path d="M36 40 v-5 a6 6 0 0 1 12 0 v5" class="lkshackle"/></g>'
            '<text x="66" y="54" class="url">https://</text><text x="138" y="54" class="url host">your-bank&#8230;</text>'
            '<g class="biglock"><path d="M160 128 v-18 a40 40 0 0 1 80 0 v18" class="shackle"/>'
            '<rect x="140" y="128" width="120" height="88" rx="14" class="body"/>'
            '<circle cx="200" cy="164" r="10" class="hole"/><rect x="195" y="168" width="10" height="24" rx="4" class="hole"/></g>'
            '</svg>'
            + vcap("Hide it &#183; prove the site &#183; check the user.",
                   "تخبّي الرسالة، وتثبت الموقع، وتتأكد من المستخدم.")
            + '</aside>')


def v_jobs():
    rows = [("&#128274;", "Messages are scrambled", "no one else can read them"),
            ("&#128196;", "The website proves it is genuine", "not a fake copy"),
            ("&#128100;", "Your identity is checked", "before you are let in")]
    out = []
    for k, (ico, t, why) in enumerate(rows):
        out.append('<div class="drow" style="animation-delay:%.2fs"><span class="dico">%s</span>'
                   '<span class="dt"><b>%s</b><br><small>%s</small></span></div>' % (.5 + .55 * k, ico, t, why))
    return ('<aside class="rise viz">' + "".join(out)
            + vcap("Three hidden jobs, every time you log in.",
                   "تلات حاجات بتحصل في الخفا كل مرة تسجّل دخول.")
            + '</aside>')


def v_threats():
    tiles = [("&#128066;", "Eavesdropping", "someone reads it"),
             ("&#9998;", "Tampering", "someone changes it"),
             ("&#127917;", "Impersonation", "someone pretends"),
             ("&#128682;", "Unauthorized login", "someone gets in")]
    out = "".join('<div class="tile" style="animation-delay:%.2fs"><span>%s</span><b>%s</b><i>%s</i></div>'
                  % (.4 + .45 * k, ico, t, q) for k, (ico, t, q) in enumerate(tiles))
    return ('<aside class="rise viz"><div class="tiles">' + out + '</div>'
            + vcap("Four threats &#8212; no single technology stops them all.",
                   "أربع تهديدات، ومفيش تقنية واحدة بتوقفهم كلهم.")
            + '</aside>')


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


def v_scramble():
    return ('<aside class="rise viz">'
            '<div class="msg plain">PIN 4821</div>'
            '<div class="kk">&#128273; <span>lock with a key</span></div>'
            '<div class="msg cipher"><span class="c0">PIN 4821</span><span class="c1">x9#Lq@7&amp;</span></div>'
            '<div class="kk late">&#128273; <span>unlock with the key</span></div>'
            '<div class="msg plain late2">PIN 4821</div>'
            + vcap("Locked, it is unreadable on the way.",
                   "وهي مقفولة، محدش يقدر يقراها في السكة.")
            + '</aside>')


def v_cert():
    checks = ["Issued by a trusted certificate authority",
              "Still valid &#8212; not expired",
              "Name matches the site you asked for"]
    out = "".join('<div class="ck" style="animation-delay:%.2fs"><b>&#10003;</b>%s</div>' % (.7 + .5 * k, t)
                  for k, t in enumerate(checks))
    return ('<aside class="rise viz"><div class="cert">'
            '<div class="certh">&#128196; Digital certificate</div>'
            '<div class="certn">www.shop&#8230;</div>' + out + '</div>'
            + vcap("The browser checks before it trusts.",
                   "المتصفح بيتأكد قبل ما يثق.")
            + '</aside>')


def v_leak():
    return ('<aside class="rise viz"><div class="leak">'
            '<div class="lk1"><span>&#128273; Password</span><em>LEAKED</em></div>'
            '<div class="lkarrow">&#8595; the attacker types it in</div>'
            '<div class="lk2"><span>&#128241; Code sent to the owner&#8217;s phone</span></div>'
            '<div class="lk3">&#10005; Login blocked &#8212; no phone, no code</div>'
            '</div>'
            + vcap("One factor broken &#8212; the other still holds.",
                   "عامل اتكسر، والتاني لسه حامي الحساب.")
            + '</aside>')


def v_layers():
    items = [("&#128274;", "Encryption", "hides the content"),
             ("&#128196;", "Digital certificate", "proves the site"),
             ("&#9997;", "Digital signature", "detects tampering"),
             ("&#128241;", "Multi-factor authentication", "blocks unauthorized logins")]
    out = "".join('<div class="pchip" style="animation-delay:%.2fs"><span>%s</span><div>%s<small>%s</small></div></div>'
                  % (.5 + .4 * k, ico, t, why) for k, (ico, t, why) in enumerate(items))
    return ('<aside class="rise viz">' + out
            + vcap("Layered, many threats are handled at once.",
                   "لما تتجمع مع بعض، تهديدات كتير بتتعالج في نفس الوقت.")
            + '</aside>')


def v_units():
    rows = [("2-1", "Cryptographic technologies and authentication", True),
            ("2-2", "Network security design", False),
            ("2-3", "Incident response and risk management", False)]
    out = "".join('<div class="ustep2%s" style="animation-delay:%.2fs"><b>%s</b>%s</div>'
                  % (" now" if now else "", .5 + .4 * k, n, t) for k, (n, t, now) in enumerate(rows))
    return ('<aside class="rise viz">' + out
            + vcap("Today: the first of three lessons.",
                   "النهارده أول درس من تلاتة.")
            + '</aside>')


def v_newshop():
    return ('<aside class="rise viz"><div class="shopv">'
            '<div class="sv sv1"><span>&#128100;</span><b>Customer login</b><i>which technology?</i></div>'
            '<div class="sv sv2"><span>&#128179;</span><b>Payment</b><i>which technology?</i></div>'
            '<div class="sv sv3"><span>&#9888;</span><b>One threat that remains</b><i>no technology is absolute</i></div>'
            '</div>'
            + vcap("Two places to protect, and one honest limit.",
                   "مكانين لازم يتحموا، وحد واحد لازم نعترف بيه.")
            + '</aside>')


# heading text (unique to one slide) -> its drawing
VIZ = {
    "Is this connection safe?": v_padlock,
    "Unit 2 &#183; Cybersecurity": v_units,
    "Every login hides three jobs": v_jobs,
    "How do cryptographic technologies and authentication work together": v_threats,
    "Before you read on": v_timer,
    "Locking a message": v_scramble,
    "Who vouches for the website?": v_cert,
    "If a password is leaked": v_timer,
    "One factor is not enough": v_leak,
    "Layers, not one lock": v_layers,
    "A small online shop": v_newshop,
}
VIZ_USED = []


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
    h2("Is this connection safe?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("Every login, every purchase, every padlock in the address bar: hidden technologies are working to keep your information safe. Today: how.",
        "max-width:56ch;margin-top:1rem"),
    ar("كل مرة تسجّل دخول أو تشتري أونلاين أو تشوف القفل في شريط العنوان، فيه تقنيات شغالة في الخفا عشان تحمي بياناتك. النهارده هنفهم بتشتغل إزاي.")))

# 2 where we are -- Unit 2 opens; its three lessons are the contents page
A(s("",
    eyebrow("A new unit"),
    h2("Unit 2 &#183; Cybersecurity", "max-width:22ch"),
    sub("Unit 1 asked what technology does to society. Unit 2 asks how we keep it <b>safe</b>.",
        "max-width:56ch;margin-top:.6rem"),
    '<div class="rise timeline">'
    '<div class="tl"><h3>2-1 &#183; Cryptographic technologies and authentication</h3><p>Today: HTTPS, the two kinds of encryption, certificates, signatures, multi-factor login</p></div>'
    '<div class="tl"><h3>2-2 &#183; Network security design</h3><p>Next: protecting a whole network</p></div>'
    '<div class="tl"><h3>2-3 &#183; Incident response and risk management</h3><p>Then: what to do when something goes wrong</p></div>'
    '</div>',
    ar("الوحدة الأولى كانت عن التكنولوجيا بتعمل إيه في المجتمع. الوحدة التانية — الأمن السيبراني — عن إزاي نحميها. أول درس النهارده: تقنيات التشفير والمصادقة.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("This is already happening"),
    h2("Every login hides three jobs", "max-width:22ch"),
    '<div class="rise fields">'
    '<span class="chip">logging in to a bank app</span>'
    '<span class="chip">buying something online</span>'
    '<span class="chip">a padlock in the address bar</span>'
    '</div>',
    sub("Without these protections, passwords could be <b>stolen</b> and private data could be <b>read</b> by unauthorized people.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> does the padlock mean a website is safe to trust? Remember your answer &#8212; we come back to it.</p></div>',
    ar("لما تسجّل دخول على تطبيق بنك أو تشتري أونلاين أو تفتح موقع بيستخدم HTTPS، فيه كذا تقنية بتحمي الاتصال: TLS بيشفّر البيانات وهي رايحة، والمتصفح بيتأكد من شهادة الموقع واسم النطاق، والخدمة بتتأكد من هويتك قبل ما تدخّلك. دي بتقلل المخاطر — بس مش معناها إن محتوى الموقع موثوق أو إن الحماية مطلقة.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("How do cryptographic technologies and authentication work together to keep online communication and services secure?",
       "max-width:28ch"),
    ar("السؤال الرئيسي: إزاي تقنيات التشفير والمصادقة بتشتغل مع بعض عشان تحافظ على أمان الاتصال والخدمات عبر الإنترنت؟")))

# 5 the map: four technologies, four threats -- p.36 table and point 3(3)
A(s("",
    eyebrow("Today&#8217;s map &#183; four technologies"),
    h2("Each technology stops a different threat", "max-width:26ch"),
    sub("Secure communication depends on <b>combining</b> them &#8212; not on any single technology.",
        "max-width:56ch;margin-top:.6rem"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#128274;</div><div class="role">Part 1&#8211;2 &#183; stops eavesdropping</div>'
    '<h3>Encryption</h3><p>Content cannot be read by third parties</p></div>'
    '<div class="card"><div class="ico">&#128196;</div><div class="role">Part 2 &#183; stops impersonation</div>'
    '<h3>Digital certificate</h3><p>The other side is who it claims to be</p></div>'
    '<div class="card"><div class="ico">&#9997;</div><div class="role">Part 2 &#183; detects tampering</div>'
    '<h3>Digital signature</h3><p>The data was not altered on the way</p></div>'
    '<div class="card"><div class="ico">&#128241;</div><div class="role">Part 3 &#183; stops unauthorized login</div>'
    '<h3>Multi-factor authentication</h3><p>A stolen password is not enough</p></div>'
    '</div>',
    sub("Part 4 puts all four together, in one online purchase.", "margin-top:.6rem;color:var(--soft)"),
    ar("دي خريطة المحاضرة: أربع تقنيات، وكل واحدة بتقف قصاد تهديد: التشفير ← التنصت، الشهادة الرقمية ← انتحال الهوية، التوقيع الرقمي ← التلاعب، المصادقة الثنائية ← الدخول غير المصرح به. وفي الآخر هنجمعهم كلهم في عملية شرا واحدة.")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("You send your password to your bank over the Internet. With your partner, predict: <b>what three things</b> must be true so that no one can <b>read</b> it, <b>change</b> it, or receive it by <b>pretending to be your bank</b>?",
        "max-width:56ch;margin-top:1rem"),
    sub("Keep your answer. Today&#8217;s four parts answer it, one by one.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: انت باعت الباسورد للبنك عبر الإنترنت. توقّعوا: إيه التلات حاجات اللي لازم يتحققوا عشان محدش يقرا الباسورد، ولا يغيّره، ولا ياخده وهو بيضحك عليك إنه البنك؟ خلّوا إجابتكم معاكم.")))

# ---------------- part 1: two kinds of encryption ----------------

A(s("",
    eyebrow("Part 1 &#183; Encryption"),
    h2("Locking a message", "max-width:24ch"),
    '<div class="rise statement"><em>Encryption</em> scrambles a message so that only someone with the right key can read it &#8212; it keeps content private.</div>',
    sub("Every key in this lesson is about one question: <b>who holds the key that unlocks it?</b>",
        "max-width:58ch;margin-top:.9rem"),
    ar("التشفير بيحافظ على خصوصية المحتوى: بيلخبط الرسالة، فمحدش يقدر يقراها غير اللي معاه المفتاح الصح. وكل اللي جاي في الدرس سؤال واحد: مين معاه المفتاح اللي بيفتح؟")))

A(s("",
    eyebrow("1 &#183; Two kinds"),
    h2("One key, or a pair of keys"),
    fig(KEYS),
    ar("التشفير المتماثل (بالمفتاح المشترك): مفتاح واحد بيقفل وبيفتح — سريع في تبادل البيانات، بس الطرفين محتاجين نفس المفتاح. التشفير بالمفتاح العام: زوج من المفاتيح المرتبطة — المفتاح العام بيقفل، ومفتاح خاص تاني بيفتح. المفتاح العام ينفع يتدّي لأي حد، فبيشارك المفتاح بأمان، بس بطيء مع البيانات الكتير.")))

A(s("",
    eyebrow("1 &#183; The one students mix up"),
    h2("Which key does what", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th></th><th>Locks with</th><th>Unlocks with</th></tr>'
    '<tr><td><b>Encryption</b> (public-key)</td><td>the receiver&#8217;s <b>public</b> key</td><td>the receiver&#8217;s <b>private</b> key</td></tr>'
    '<tr><td><b>Digital signature</b></td><td>the sender <b>signs</b> with the <b>private</b> key</td><td>anyone <b>verifies</b> with the <b>public</b> key</td></tr>'
    '</table>',
    sub("In a digital signature the direction reverses. Only the owner has the private key &#8212; so only the owner could have signed.",
        "max-width:60ch;margin-top:.9rem"),
    ar("خلّي بالك: في التشفير، المفتاح العام بيقفل والخاص بيفتح. في التوقيع الرقمي الاتجاه بيتعكس: المفتاح الخاص بيوقّع والعام بيتحقق. وبما إن المفتاح الخاص مع صاحبه بس، يبقى هو بس اللي ممكن يكون وقّع.")))

# ---------------- part 2: HTTPS ----------------

A(s("",
    eyebrow("Part 2 &#183; HTTPS and the TLS handshake"),
    h2("HTTPS &#8212; HTTP with TLS added", "max-width:24ch"),
    '<div class="rise statement"><em>HTTPS</em> (HTTP Secure) &#8212; a communication protocol that adds TLS encryption to HTTP.</div>',
    '<table class="rise" style="margin-top:.9rem">'
    '<tr><th>It provides</th><th>which protects against</th></tr>'
    '<tr><td>Encryption</td><td>Eavesdropping</td></tr>'
    '<tr><td>Detection of tampering</td><td>Tampering</td></tr>'
    '<tr><td>Verification of the communication partner</td><td>Impersonation</td></tr>'
    '</table>',
    sub("The procedure for setting up the secure connection is called the <b>TLS handshake</b>.", "max-width:60ch;margin-top:.8rem"),
    ar("HTTPS: بروتوكول HTTP منقول عبر اتصال TLS مؤمَّن. TLS بيوفّر سرية البيانات وسلامتها وهي بتتنقل، وبيساعد المتصفح يتأكد من هوية الخادم واسم النطاق. وخطوات إنشاء الاتصال الآمن اسمها مصافحة TLS.")))

A(s("",
    eyebrow("2 &#183; How HTTPS communication works"),
    h2("Three stages, two kinds of key"),
    fig(HANDSHAKE),
    ar("① الخادم بيبعت شهادته الرقمية ومفتاحه العام، والمتصفح بيتأكد منها عن طريق جهة إصدار الشهادات. ② المتصفح بيعمل مفتاح مشترك للاتصال، يقفله بالمفتاح العام بتاع الخادم ويبعته، والخادم يفتحه بمفتاحه الخاص. ③ البيانات بتتبادل مقفولة بالمفتاح المشترك ده. المرحلتين الأولانيين بالمفتاح العام، والتالتة بالتشفير المتماثل.")))

A(video("ZghMPWGXexs", "The Internet: Encryption &amp; Public Keys", "Code.org",
        "Watch &#183; the keys in action", "Seeing it work",
        "when does the video use a public key, and when a key both sides share? Match each to stage 1, 2 or 3.",
        "وانتو بتتفرجوا: إمتى الفيديو بيستخدم مفتاح عام، وإمتى مفتاح مشترك بين الطرفين؟ وصّلوا كل واحد بالمرحلة 1 أو 2 أو 3."))

A(s("",
    eyebrow("2 &#183; Exam-style question &#183; 6 marks"),
    h2("Why not use public-key for everything?", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Public-key cryptography</h3><ul>'
    '<li>Used to <b>share keys safely</b></li>'
    '<li>Slow &#8212; exchanging <i>all</i> data with it would be slow</li>'
    '</ul></div>'
    '<div class="pane b"><h3>Common-key cryptography</h3><ul>'
    '<li>Used to <b>exchange large amounts of data quickly</b></li>'
    '<li>Safe once the key has been shared</li>'
    '</ul></div>'
    '</div>',
    '<div class="rise statement" style="margin-top:1rem">This division of roles achieves both <em>security</em> and <em>speed</em>.</div>',
    sub("The common key made for one connection is called a <b>session key</b>. Current versions of TLS agree on it by Diffie-Hellman key agreement instead of sending it locked.",
        "max-width:62ch;margin-top:.8rem;color:var(--soft)"),
    ar("لو استخدمنا التشفير بالمفتاح العام في كل البيانات، الاتصال هيبقى بطيء. عشان كده مصافحة TLS بتستخدم آليات المفتاح العام للمصادقة والاتفاق الآمن على مفاتيح الجلسة، وبعد ما المفاتيح تتعمل، التشفير المتماثل بيحمي بيانات الجلسة بسرعة وكفاءة. الأمان والسرعة مع بعض.")))

A(s("",
    eyebrow("2 &#183; Certificates"),
    h2("Who vouches for the website?", "max-width:24ch"),
    '<div class="rise statement"><em>Digital certificate</em> &#8212; verifies that the communication partner is authentic. A <em>certificate authority (CA)</em> vouches that a site is genuine.</div>',
    sub("During the handshake the browser checks the certificate: is it <b>valid</b>, does it lead back to an authority it trusts (the <b>chain of trust</b>), and does it <b>match the name</b> of the site?",
        "max-width:58ch;margin-top:.9rem"),
    ar("الشهادة الرقمية بتساعد المتصفح يتأكد من هوية الخادم وارتباط الشهادة باسم النطاق اللي بيتصل بيه. أثناء المصافحة الخادم بيبعت شهادته، والمتصفح بيتأكد من صلاحيتها وسلسلة الثقة وملاءمتها لاسم الموقع.")))

A(s("",
    eyebrow("2 &#183; Signatures"),
    h2("Proving who sent it, and that it was not changed", "max-width:26ch"),
    '<div class="rise statement"><em>Digital signature</em> &#8212; detects tampering with the data or impersonation of the sender, and makes it impossible for the sender to deny having sent it: <em>non-repudiation</em>.</div>',
    '<table class="rise" style="margin-top:.9rem">'
    '<tr><th>Digital certificate</th><th>Digital signature</th></tr>'
    '<tr><td>Is the <b>other side</b> genuine?</td><td>Was <b>this data</b> altered, and who sent it?</td></tr>'
    '<tr><td>Stops a fake website</td><td>Detects tampering; gives non-repudiation</td></tr>'
    '</table>',
    ar("التوقيع الرقمي بيكشف التلاعب وانتحال الشخصية، وبيوفّر دليل بيدعم عدم التنصل — يعني اللي بعت الرسالة ميقدرش ينكر إنه بعتها. الشهادة بتجاوب: الطرف التاني حقيقي؟ والتوقيع بيجاوب: البيانات دي اتغيرت؟ ومين بعتها؟")))

A(s("",
    eyebrow("2 &#183; Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">HTTPS communication uses both public-key cryptography and common-key cryptography. <span class="ans">&#8212; <b>true</b>: public-key for the key exchange, common-key for the data.</span></li>'
    '<li class="reveal rv">HTTPS communication exchanges all data using public-key cryptography. <span class="ans">&#8212; <b>false</b>: it would be slow, so common-key is used for the data.</span></li>'
    '<li class="reveal rv tf-t">A padlock shows the connection is encrypted and the site matches its certificate. <span class="ans">&#8212; <b>true</b>: that is what TLS and the certificate check give you.</span></li>'
    '<li class="reveal rv">A padlock means the website&#8217;s content can be trusted completely. <span class="ans">&#8212; <b>false</b>: it reduces risks; it does not make the content trustworthy or the protection absolute.</span></li>'
    '</ul>',
    sub("Tap each one to check. Back to the hands-up question: was the padlock enough?", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: اتصال HTTPS بيستخدم التشفير بالمفتاح العام والتشفير المتماثل — صح. بيبادل كل البيانات بالمفتاح العام — غلط، لأنه هيبقى بطيء. والقفل معناه إن الاتصال متشفّر والموقع مطابق لشهادته — بس مش معناه إن محتوى الموقع موثوق أو إن الحماية مطلقة.")))

# ---------------- part 3: authentication ----------------

A(s("",
    eyebrow("Part 3 &#183; Authentication"),
    h2("Three factors of authentication"),
    fig(FACTORS),
    sub("Every login checks one or more of these. Which factor a method belongs to is what the exam asks.",
        "max-width:60ch;margin-top:.4rem"),
    ar("عوامل المصادقة تلاتة: المعرفة (حاجة بتعرفها زي كلمة المرور أو السؤال السري)، والحيازة (حاجة معاك زي كلمة مرور لمرة واحدة، أو رسالة SMS، أو إشعار على الموبايل، أو بطاقة ذكية)، والسمات الحيوية (بصمة الإصبع أو التعرف على الوجه).")))

A(s("",
    eyebrow("3 &#183; Multi-factor authentication"),
    h2("One factor is not enough", "max-width:24ch"),
    '<div class="rise statement"><em>Multi-factor authentication (MFA)</em> &#8212; combining two or more of the three factors: knowledge, possession, biometric.</div>',
    sub("With one factor, breaking that factor is enough to get in. With several, even if one is broken, another can still stop the attacker.",
        "max-width:58ch;margin-top:.9rem"),
    sub("<b>e.g.</b> A password alone: once it leaks, an unauthorized login is possible. Password <b>plus</b> a notification to a smartphone: without the device, the attacker cannot log in.",
        "max-width:58ch;margin-top:.6rem"),
    ar("المصادقة متعددة العوامل (MFA): استخدام عاملين مستقلين أو أكتر من فئات زي المعرفة والحيازة والسمات الحيوية. لو استخدمت عامل واحد واتكسر، اللي هاجم يدخل. لكن عامل تاني مستقل بيقلل احتمال الدخول غير المصرح به لو كلمة المرور اتكشفت: من غير الموبايل، معرفة كلمة المرور لوحدها مش كفاية.")))

A(s("",
    eyebrow("3 &#183; Two words that sound the same"),
    h2("2FA and MFA", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>Two-factor authentication (2FA)</th><th>Multi-factor authentication (MFA)</th></tr>'
    '<tr><td>Exactly <b>two</b> independent factors</td><td><b>Two or more</b> independent factors</td></tr>'
    '<tr><td>From two <b>different</b> categories</td><td>From different categories &#8212; knowledge, possession, biometric</td></tr>'
    '<tr><td>Password + one-time password</td><td>Password + one-time password + fingerprint</td></tr>'
    '</table>',
    sub("Every 2FA is MFA; not every MFA is 2FA. What both need is <b>different categories</b>.",
        "max-width:58ch;margin-top:.9rem"),
    ar("المصادقة الثنائية (2FA): عاملين مستقلين من فئتين مختلفتين لإثبات الهوية. المصادقة متعددة العوامل (MFA): عاملين مستقلين أو أكتر من فئات مختلفة زي المعرفة والحيازة والسمات الحيوية. الاتنين لازم فئات مختلفة.")))

A(s("",
    eyebrow("3 &#183; In real services"),
    h2("Which factors does each use?"),
    '<table class="rise">'
    '<tr><th>Service</th><th>Authentication used</th><th>Factors</th></tr>'
    '<tr><td>Online banking</td><td>Password + one-time password</td><td class="reveal"><span>knowledge + possession</span></td></tr>'
    '<tr><td>SNS login</td><td>Password + SMS authentication</td><td class="reveal"><span>knowledge + possession</span></td></tr>'
    '<tr><td>Online shopping</td><td>Password + one-time code from 3-D Secure</td><td class="reveal"><span>knowledge + possession</span></td></tr>'
    '<tr><td>Company laptop login</td><td>Smart card + fingerprint authentication</td><td class="reveal"><span>possession + biometric</span></td></tr>'
    '</table>',
    sub("Tap each to check. Then the trap: <b>two passwords</b>?", "margin-top:.7rem;color:var(--soft)"),
    ar("أمثلة من الخدمات: البنك أونلاين: كلمة مرور (معرفة) + كلمة مرور لمرة واحدة (حيازة). السوشيال: كلمة مرور + SMS. التسوق الإلكتروني: كلمة مرور + كود 3-D Secure. وفي الكتاب العربي كمان: الدخول لمبنى مؤمَّن ببطاقة دخول (حيازة) + بصمة إصبع (سمات حيوية).")))

A(s("",
    eyebrow("Exam warning"),
    h2("Two passwords is not multi-factor", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane b"><h3>NOT multi-factor</h3><ul>'
    '<li>Password + a second password</li>'
    '<li>Password + a secret question</li>'
    '</ul><p style="margin-top:.5rem">Both are <b>knowledge</b> &#8212; the same factor twice. This is two-<i>step</i> authentication.</p></div>'
    '<div class="pane a"><h3>Multi-factor</h3><ul>'
    '<li>Password + smartphone notification</li>'
    '<li>Password + SMS authentication</li>'
    '<li>Fingerprint + smart card</li>'
    '</ul><p style="margin-top:.5rem">Two <b>different</b> factors.</p></div>'
    '</div>',
    ar("خلّي بالك: حتى لو حطيت كلمتين مرور، الاتنين من عامل \"المعرفة\"، فده مش مصادقة ثنائية — دي مصادقة متعددة الخطوات بنفس العامل. ونفس الكلام: كلمة مرور + سؤال سري، الاتنين معرفة.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("If a password is leaked, why can a second factor sent to a phone still keep the account safe?",
       "max-width:27ch"),
    ar("وقّف وفكّر: لو كلمة المرور اتسربت، ليه عامل تاني بيتبعت على الموبايل لسه ممكن يحمي الحساب؟")))

# ---------------- part 4: combining ----------------

A(s("",
    eyebrow("Part 4 &#183; Combinations of security technologies"),
    h2("Layers, not one lock", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>Technology</th><th>Effect</th></tr>'
    '<tr><td>Encryption (common-key, public-key)</td><td>Prevents communication content from being read by third parties</td></tr>'
    '<tr><td>Digital signature</td><td>Detects data tampering or impersonation of the sender; non-repudiation</td></tr>'
    '<tr><td>Digital certificate</td><td>Verifies that the communication partner is authentic</td></tr>'
    '<tr><td>Multi-factor authentication</td><td>Prevents unauthorized logins</td></tr>'
    '</table>',
    sub("Safe communication and services come not from a single technology, but from <b>combining</b> several.",
        "max-width:60ch;margin-top:.8rem"),
    ar("الاتصال والخدمات الآمنة مش بتتحقق بتقنية واحدة، لكن بالجمع بين كذا تقنية أمان: التشفير بيمنع قراية المحتوى، والتوقيع الرقمي بيتحقق من سلامة البيانات وهوية الموقّع، والشهادة الرقمية بتتحقق من هوية الخادم، والمصادقة الثنائية بتقلل احتمال الدخول غير المصرح به.")))

A(s("",
    eyebrow("4 &#183; One online purchase"),
    h2("All four, in order"),
    fig(SHOP),
    sub("Eavesdropping, tampering, impersonation and unauthorized login &#8212; handled at the same time. No single one of them blocks every risk absolutely.",
        "max-width:62ch;margin-top:.4rem"),
    ar("مثال الشرا أونلاين: ① تدخل الموقع فيبدأ اتصال HTTPS، والتشفير يمنع حد تالت يقرا. ② المتصفح يتحقق من الشهادة الرقمية واسم النطاق. ③ وانت بتسجّل دخول، المصادقة الثنائية تقلل الدخول غير المصرح به. ④ وانت باعت الطلب، التوقيع الرقمي ممكن يتستخدم عشان أي تلاعب يتكشف. الجمع ده بيقلل مخاطر كذا تهديد، من غير ما نفترض إن أي تقنية بتمنع الخطر منع مطلق.")))

A(s("",
    eyebrow("4 &#183; Your turn"),
    h2("Which technology?"),
    '<table class="rise">'
    '<tr><th>Threat</th><th>Technology</th></tr>'
    '<tr><td>A password is leaked and an unauthorized login occurs</td><td class="reveal"><span>Multi-factor authentication</span></td></tr>'
    '<tr><td>Data is altered during communication</td><td class="reveal"><span>Digital signature</span></td></tr>'
    '<tr><td>A user is led to a fake website</td><td class="reveal"><span>Digital certificate</span></td></tr>'
    '<tr><td>Communication content is intercepted by a third party</td><td class="reveal"><span>Encryption</span></td></tr>'
    '</table>',
    ar("لكل تهديد، أنهي تقنية بتعالجه أساسًا؟ كلمة مرور اتسربت ← المصادقة الثنائية. بيانات اتعدلت أثناء الاتصال ← التوقيع الرقمي. مستخدم اتوجّه لموقع مزيف ← الشهادة الرقمية. محتوى اتعترض من طرف تالت ← التشفير.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Digital signatures are a technology that improves communication speed. <span class="ans">&#8212; <b>false</b>: they detect tampering and impersonation, and give non-repudiation.</span></li>'
    '<li class="reveal rv">One strong technology is enough to protect a service completely. <span class="ans">&#8212; <b>false</b>: security comes from combining several, and none is absolute.</span></li>'
    '<li class="reveal rv">Setting two passwords is an example of multi-factor authentication. <span class="ans">&#8212; <b>false</b>: both are knowledge, the same factor.</span></li>'
    '</ul>',
    ar("خلّي بالك من الجمل دي، كلها غلط: التوقيعات الرقمية بتحسّن سرعة الاتصال — غلط. تقنية واحدة قوية كفاية — غلط. كلمتين مرور يبقوا مصادقة ثنائية — غلط.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("A school portal: how should students log in?", "max-width:26ch"),
    sub("Students will check grades and pay fees online. Password only &#8212; or a password plus a one-time password sent to the phone?",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Collect data.</b> Ask ten classmates which login methods they use and trust. Record a table; find the most common.</li>'
    '<li><b>Analyze the stakeholders.</b> A student, the school, and a student with no smartphone: one benefit and one drawback of a second factor for each.</li>'
    '<li><b>Decide.</b> Recommend one method with two reasons from your survey. In pairs, agree on the single strongest reason.</li>'
    '</ul>',
    sub("Stuck? Start with the user: a password alone fails once it leaks; adding a possession factor still blocks the login.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: مدرسة بتعمل بوابة إلكترونية الطلاب يشوفوا فيها درجاتهم ويدفعوا الرسوم. كلمة مرور بس، ولا كلمة مرور + كلمة مرور لمرة واحدة على الموبايل؟ اجمع بيانات من عشرة من زمايلك، وحلّل أصحاب المصلحة — الطالب، والمدرسة، وطالب معندوش موبايل ذكي — وبعدين قرّر واذكر سببين.")))

A(s("",
    eyebrow("In a new context"),
    h2("A small online shop", "max-width:26ch"),
    sub("It wants to secure both customer login and payment.", "max-width:54ch;margin-top:.7rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li>Name <b>two security technologies</b> it should use.</li>'
    '<li>Say <b>where each one helps</b> &#8212; login, or payment.</li>'
    '<li>Identify <b>one threat that could still remain</b>.</li>'
    '</ul>',
    ar("طبّق اللي اتعلمته: متجر إلكتروني صغير عايز يأمّن تسجيل دخول العملاء والدفع مع بعض. سمّي تقنيتين أمان لازم يستخدمهم وبيّن كل واحدة بتساعد فين، وبعدين حدد تهديد واحد ممكن يفضل موجود.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 2-1"),
    h2("Share the key safely, move the data quickly", "max-width:28ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> does the padlock mean a website is safe to trust? What does it <i>actually</i> tell you?</p>'
    '<div class="rise statement">HTTPS uses <em>public-key cryptography</em> to share a key safely and <em>common-key cryptography</em> to move data quickly. Services stay safe by <em>layering</em> encryption, certificates, signatures and multi-factor authentication.</div>',
    ar("افتكر: مصافحة HTTPS بتستخدم آليات المفتاح العام للمصادقة والاتفاق الآمن على مفاتيح الجلسة، وبعدين بيانات الجلسة بتتحمي بالتشفير المتماثل بسرعة. والخدمات بتفضل آمنة بتكديس التشفير والشهادات والتوقيعات والمصادقة الثنائية.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 5"),
    # Covered until the teacher reveals it (press E, or the dashboard switch),
    # so the code is not handed to a class in advance.
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 5 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers this lesson. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس ده. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))


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
BASE = "scripts/lecture5_slides_base.html"
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

