# --------------------------------------------------------------------------
# diagrams -- inline SVG, reused from lectures 3 and 4 (lesson 1-1's timeline is new), so the
# revision shows the picture each lesson was taught with. The booklet
# reads these out of this file.
# --------------------------------------------------------------------------

TIMELINE = '''
<svg viewBox="0 0 900 250" role="img" aria-label="The five stages of IT development: the birth of the computer in the 1940s to 60s, personal computers in the 1970s and 80s, the Internet and the Web in the 1990s, smartphones in the 2000s, and cloud computing from the 2010s onward">
  <g font-size="15" text-anchor="middle">
    <line x1="90" y1="70" x2="830" y2="70" stroke="var(--line)" stroke-width="4"/>
    <polygon points="842,70 828,62 828,78" fill="var(--line)"/>
    <circle cx="90" cy="70" r="28" fill="var(--teal)"/><text x="90" y="77" font-size="18" font-weight="700" fill="#fff">1</text>
    <circle cx="275" cy="70" r="28" fill="var(--teal)"/><text x="275" y="77" font-size="18" font-weight="700" fill="#fff">2</text>
    <circle cx="460" cy="70" r="28" fill="var(--teal)"/><text x="460" y="77" font-size="18" font-weight="700" fill="#fff">3</text>
    <circle cx="645" cy="70" r="28" fill="var(--teal)"/><text x="645" y="77" font-size="18" font-weight="700" fill="#fff">4</text>
    <circle cx="830" cy="70" r="28" fill="var(--gold)"/><text x="830" y="77" font-size="18" font-weight="700" fill="#fff">5</text>
    <text x="90" y="24" fill="var(--soft)">1940s-60s</text>
    <text x="275" y="24" fill="var(--soft)">1970s-80s</text>
    <text x="460" y="24" fill="var(--soft)">1990s</text>
    <text x="645" y="24" fill="var(--soft)">2000s</text>
    <text x="830" y="24" fill="var(--soft)">2010s onward</text>
    <text x="90" y="128" font-weight="700" fill="var(--ink)">The computer</text>
    <text x="90" y="150" fill="var(--soft)">ENIAC, vacuum tubes</text>
    <text x="90" y="172" fill="var(--soft)">military, science</text>
    <text x="275" y="128" font-weight="700" fill="var(--ink)">Personal computers</text>
    <text x="275" y="150" fill="var(--soft)">PCs at home</text>
    <text x="275" y="172" fill="var(--soft)">personal use begins</text>
    <text x="460" y="128" font-weight="700" fill="var(--ink)">The Internet, the Web</text>
    <text x="460" y="150" fill="var(--soft)">commercialized</text>
    <text x="460" y="172" fill="var(--soft)">information goes global</text>
    <text x="645" y="128" font-weight="700" fill="var(--ink)">Smartphones</text>
    <text x="645" y="150" fill="var(--soft)">iPhone, etc.</text>
    <text x="645" y="172" fill="var(--soft)">mobile Internet explodes</text>
    <text x="830" y="128" font-weight="700" fill="var(--ink)">Cloud computing</text>
    <text x="830" y="150" fill="var(--soft)">IT as a service</text>
    <text x="830" y="172" fill="var(--soft)">big data and AI</text>
    <rect x="200" y="200" width="500" height="34" rx="8" fill="var(--gold)" opacity=".2"/>
    <text x="450" y="223" font-weight="600" fill="var(--ink)">each stage: a new technology, and a changed society</text>
  </g>
</svg>'''

NESTED = '''
<svg viewBox="0 0 860 300" role="img" aria-label="AI contains machine learning, which contains deep learning, which contains generative AI">
  <rect x="20" y="20" width="820" height="260" rx="16" fill="var(--teal)" opacity=".07" stroke="var(--teal)" stroke-width="2.5"><animate attributeName="opacity" values=".07;.20;.07" dur="8s" begin="0s" repeatCount="indefinite"/></rect>
  <text x="40" y="48" font-size="15" font-weight="600" fill="var(--teal)">AI</text>
  <text x="40" y="68" font-size="11" fill="var(--soft)">intelligent behaviour on a computer</text>

  <rect x="150" y="56" width="670" height="204" rx="14" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="2"><animate attributeName="opacity" values=".10;.24;.10" dur="8s" begin="2s" repeatCount="indefinite"/></rect>
  <text x="170" y="84" font-size="14" font-weight="600" fill="var(--teal)">Machine learning</text>
  <text x="170" y="103" font-size="11" fill="var(--soft)">learns from data</text>

  <rect x="300" y="92" width="500" height="148" rx="12" fill="var(--teal)" opacity=".14" stroke="var(--teal)" stroke-width="2"><animate attributeName="opacity" values=".14;.30;.14" dur="8s" begin="4s" repeatCount="indefinite"/></rect>
  <text x="320" y="120" font-size="14" font-weight="600" fill="var(--teal)">Deep learning</text>
  <text x="320" y="139" font-size="11" fill="var(--soft)">neural networks</text>

  <rect x="470" y="128" width="310" height="92" rx="10" fill="var(--gold)" opacity=".20" stroke="var(--gold)" stroke-width="2.5"><animate attributeName="opacity" values=".20;.42;.20" dur="8s" begin="6s" repeatCount="indefinite"/></rect>
  <text x="492" y="156" font-size="14" font-weight="600" fill="#8A6420">Generative AI</text>
  <text x="492" y="175" font-size="11" fill="var(--soft)">makes new text, images, audio</text>
  <text x="492" y="196" font-size="10.5" fill="var(--soft)">e.g. ChatGPT</text>

  <text x="40" y="272" font-size="11.5" fill="var(--soft)">each box is inside the one before it &#8212; not beside it</text>
</svg>'''

RECSYS = '''
<svg viewBox="0 0 900 250" role="img" aria-label="A recommendation system reads past behaviour, finds a pattern, and suggests something new">
  <text x="30" y="24" font-size="12.5" font-weight="600" fill="var(--soft)">Nobody told it you like this. It read what you did before.</text>

  <rect x="30" y="52" width="180" height="118" rx="9" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>
  <text x="120" y="78" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">what you did before</text>
  <text x="120" y="102" text-anchor="middle" font-size="11" fill="var(--soft)">videos watched</text>
  <text x="120" y="122" text-anchor="middle" font-size="11" fill="var(--soft)">things bought</text>
  <text x="120" y="142" text-anchor="middle" font-size="11" fill="var(--soft)">songs skipped</text>

  <line x1="216" y1="111" x2="276" y2="111" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="276,111 268,106 268,116" fill="var(--teal)"/>

  <rect x="282" y="52" width="200" height="118" rx="9" fill="var(--teal)" opacity=".22" stroke="var(--teal)" stroke-width="2.5">
    <animate attributeName="opacity" values=".22;.42;.22" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <text x="382" y="86" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">it finds a pattern</text>
  <text x="382" y="110" text-anchor="middle" font-size="11" fill="var(--soft)">people who liked these</text>
  <text x="382" y="130" text-anchor="middle" font-size="11" fill="var(--soft)">also liked that</text>

  <line x1="488" y1="111" x2="548" y2="111" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="548,111 540,106 540,116" fill="var(--teal)"/>

  <rect x="554" y="52" width="200" height="118" rx="9" fill="var(--gold)" opacity=".24" stroke="var(--gold)" stroke-width="2.5">
    <animate attributeName="opacity" values=".24;.46;.24" dur="3.4s" begin="1.2s" repeatCount="indefinite"/>
  </rect>
  <text x="654" y="96" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">&#8220;watch this next&#8221;</text>
  <text x="654" y="120" text-anchor="middle" font-size="11" fill="var(--soft)">a prediction, not a fact</text>

  <text x="30" y="208" font-size="11.5" fill="var(--soft)">This is machine learning from Part 2, doing a job you meet every day.</text>
  <text x="30" y="228" font-size="11.5" fill="var(--wrong)">It works because it holds your behaviour &#8212; which is the privacy question.</text>
</svg>'''

BLACKBOX = '''
<svg viewBox="0 0 900 240" role="img" aria-label="The black-box problem: the input and the answer are visible but the reasoning inside is not">
  <text x="30" y="24" font-size="12.5" font-weight="600" fill="var(--soft)">You can see what went in and what came out. You cannot see why.</text>

  <rect x="30" y="58" width="150" height="90" rx="8" fill="var(--teal)" opacity=".14" stroke="var(--teal)" stroke-width="2"/>
  <text x="105" y="98" text-anchor="middle" font-size="12" fill="var(--ink)">an X-ray</text>
  <text x="105" y="120" text-anchor="middle" font-size="11" fill="var(--soft)">you can see this</text>

  <line x1="186" y1="103" x2="244" y2="103" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="244,103 236,98 236,108" fill="var(--teal)"/>

  <rect x="250" y="44" width="260" height="118" rx="10" fill="var(--ink)" opacity=".88"/>
  <text x="380" y="92" text-anchor="middle" font-size="15" font-weight="600" fill="#fff">?</text>
  <text x="380" y="118" text-anchor="middle" font-size="12" fill="#C6CCD9">why it decided that</text>
  <text x="380" y="138" text-anchor="middle" font-size="11" fill="#8A93A6">not visible, even to its builders</text>
  <rect x="250" y="44" width="260" height="118" rx="10" fill="none" stroke="var(--wrong)" stroke-width="2.5" stroke-dasharray="7 5">
    <animate attributeName="opacity" values="1;.3;1" dur="2.2s" repeatCount="indefinite"/>
  </rect>

  <line x1="516" y1="103" x2="574" y2="103" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="574,103 566,98 566,108" fill="var(--teal)"/>

  <rect x="580" y="58" width="180" height="90" rx="8" fill="var(--gold)" opacity=".24" stroke="var(--gold)" stroke-width="2"/>
  <text x="670" y="92" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">&#8220;likely disease&#8221;</text>
  <text x="670" y="116" text-anchor="middle" font-size="11" fill="var(--soft)">you can see this too</text>

  <text x="30" y="204" font-size="11.5" fill="var(--ink)">That gap is the <tspan font-weight="600">black-box problem</tspan> &#8212; and it is why a doctor still signs the diagnosis.</text>
</svg>'''

BIAS = '''
<svg viewBox="0 0 900 250" role="img" aria-label="Lopsided training data produces a lopsided judgment">
  <text x="30" y="24" font-size="12.5" font-weight="600" fill="var(--soft)">It is not told to be unfair. It copies the data it was given.</text>

  <rect x="30" y="46" width="210" height="136" rx="9" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="2"/>
  <text x="135" y="70" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">training data</text>
  <g fill="var(--teal)">
    <circle cx="62" cy="100" r="11"/><circle cx="96" cy="100" r="11"/><circle cx="130" cy="100" r="11"/>
    <circle cx="164" cy="100" r="11"/><circle cx="198" cy="100" r="11"/>
    <circle cx="62" cy="136" r="11"/><circle cx="96" cy="136" r="11"/><circle cx="130" cy="136" r="11"/>
  </g>
  <g fill="var(--gold)"><circle cx="164" cy="136" r="11"/></g>
  <text x="135" y="170" text-anchor="middle" font-size="11" fill="var(--soft)">8 of one group, 1 of another</text>

  <line x1="246" y1="114" x2="304" y2="114" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="304,114 296,109 296,119" fill="var(--teal)"/>

  <rect x="310" y="60" width="200" height="108" rx="10" fill="var(--teal)" opacity=".22" stroke="var(--teal)" stroke-width="2.5">
    <animate attributeName="opacity" values=".22;.40;.22" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <text x="410" y="104" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">the AI learns</text>
  <text x="410" y="126" text-anchor="middle" font-size="11" fill="var(--soft)">whatever pattern is there</text>

  <line x1="516" y1="114" x2="574" y2="114" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="574,114 566,109 566,119" fill="var(--teal)"/>

  <rect x="580" y="46" width="290" height="136" rx="9" fill="#9C3B2E" opacity=".08" stroke="#9C3B2E" stroke-width="2"/>
  <text x="725" y="72" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">its judgment</text>
  <text x="725" y="104" text-anchor="middle" font-size="12" fill="var(--ink)">accurate for the big group</text>
  <text x="725" y="136" text-anchor="middle" font-size="12" font-weight="600" fill="#9C3B2E">misjudges the small one</text>

  <text x="30" y="222" font-size="12" fill="var(--ink)">That is <tspan font-weight="600">algorithmic bias</tspan> &#8212; bias in the judgment, caused by bias in the training data.</text>
</svg>'''

XAI = '''
<svg viewBox="0 0 900 270" role="img" aria-label="A black box shows only the answer; explainable AI also shows the reasons">
  <text x="30" y="26" font-size="13" font-weight="600" fill="#9C3B2E">Black box &#8212; the answer, and nothing else</text>
  <rect x="30" y="40" width="150" height="54" rx="7" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>
  <text x="105" y="72" text-anchor="middle" font-size="12" fill="var(--ink)">a job application</text>
  <line x1="186" y1="67" x2="236" y2="67" stroke="var(--soft)" stroke-width="2"/>
  <polygon points="236,67 228,62 228,72" fill="var(--soft)"/>
  <rect x="242" y="36" width="220" height="62" rx="8" fill="var(--ink)" opacity=".88"/>
  <text x="352" y="74" text-anchor="middle" font-size="16" font-weight="600" fill="#fff">?</text>
  <line x1="468" y1="67" x2="518" y2="67" stroke="var(--soft)" stroke-width="2"/>
  <polygon points="518,67 510,62 510,72" fill="var(--soft)"/>
  <rect x="524" y="40" width="160" height="54" rx="7" fill="#9C3B2E" opacity=".10" stroke="#9C3B2E" stroke-width="2"/>
  <text x="604" y="72" text-anchor="middle" font-size="12.5" font-weight="600" fill="#9C3B2E">&#8220;rejected&#8221;</text>
  <text x="700" y="64" font-size="11" fill="var(--soft)">why? nobody</text>
  <text x="700" y="80" font-size="11" fill="var(--soft)">can check it</text>

  <line x1="30" y1="126" x2="870" y2="126" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="5 5"/>

  <text x="30" y="160" font-size="13" font-weight="600" fill="var(--teal)">Explainable AI (XAI) &#8212; the answer, and why</text>
  <rect x="30" y="174" width="150" height="54" rx="7" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>
  <text x="105" y="206" text-anchor="middle" font-size="12" fill="var(--ink)">a job application</text>
  <line x1="186" y1="201" x2="236" y2="201" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="236,201 228,196 228,206" fill="var(--teal)"/>
  <rect x="242" y="170" width="220" height="62" rx="8" fill="var(--teal)" opacity=".20" stroke="var(--teal)" stroke-width="2.5">
    <animate attributeName="opacity" values=".20;.38;.20" dur="3.4s" repeatCount="indefinite"/>
  </rect>
  <text x="352" y="196" text-anchor="middle" font-size="11.5" fill="var(--ink)">reasons shown:</text>
  <text x="352" y="216" text-anchor="middle" font-size="11.5" fill="var(--ink)">experience, test score</text>
  <line x1="468" y1="201" x2="518" y2="201" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="518,201 510,196 510,206" fill="var(--teal)"/>
  <rect x="524" y="174" width="160" height="54" rx="7" fill="var(--gold)" opacity=".22" stroke="var(--gold)" stroke-width="2"/>
  <text x="604" y="206" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">&#8220;rejected&#8221;</text>
  <text x="700" y="198" font-size="11" fill="var(--soft)">now a person can</text>
  <text x="700" y="214" font-size="11" fill="var(--soft)">check whether it is fair</text>
</svg>'''


# ---------------- side visuals ----------------
# None in a revision deck: every slide is full width.
VIZ = {}
VIZ_USED = []


# ---------------- the revision data ----------------
# data.py beside this file holds one record per lesson; the deck, the
# booklet and the flashcards all read it.
import importlib.util as _ilu, os as _os, html as _html, json as _json
_spec = _ilu.spec_from_file_location("revdata", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "tools", "lecture12", "data.py"))
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
