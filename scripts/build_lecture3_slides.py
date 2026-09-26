# -*- coding: utf-8 -*-
"""Build Lecture 3's deck.

    python scripts/build_lecture3_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/lecture3_slides_base.html and writes lecture3/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the photo CSS
added. Always starts from the base, never from the published deck: the
injections check for their own CSS before adding markup, so rebuilding on
top of an already-built deck would drop the lightbox dialog.

Former description: rebuild Lecture 3's deck with real diagrams.

Replaces only the slide body of lecture3/slides/index.html; the head, CSS,
LECTURE CONFIG and script are left exactly as they are, so everything the
checker and the behavioural harness rely on stays put.

Content is Lesson 1-2, textbook pages 13-19. Arabic is teaching commentary
in the register the other lectures use.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "lecture3/slides/index.html"

# --------------------------------------------------------------------------
# diagrams — inline SVG, coloured from the page's own CSS variables so they
# follow LECTURE_ACCENT like everything else
# --------------------------------------------------------------------------

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

RULES_VS_LEARNED = '''
<svg viewBox="0 0 880 270" role="img" aria-label="Traditional programming follows written rules; machine learning works out the rules from examples">
  <text x="30" y="24" font-size="13" font-weight="600" fill="var(--ink)">Traditional programming</text>
  <rect x="30" y="38" width="150" height="46" rx="6" fill="none" stroke="var(--soft)" stroke-width="2"/>
  <text x="105" y="60" text-anchor="middle" font-size="11.5" fill="var(--ink)">rules you</text>
  <text x="105" y="76" text-anchor="middle" font-size="11.5" fill="var(--ink)">write by hand</text>
  <line x1="186" y1="61" x2="238" y2="61" stroke="var(--soft)" stroke-width="2"/>
  <polygon points="238,61 230,56 230,66" fill="var(--soft)"/>
  <rect x="244" y="38" width="120" height="46" rx="6" fill="var(--soft)" opacity=".13" stroke="var(--soft)" stroke-width="2"/>
  <text x="304" y="66" text-anchor="middle" font-size="11.5" fill="var(--ink)">the program</text>
  <line x1="370" y1="61" x2="422" y2="61" stroke="var(--soft)" stroke-width="2"/>
  <polygon points="422,61 414,56 414,66" fill="var(--soft)"/>
  <text x="432" y="66" font-size="11.5" fill="var(--soft)">answer</text>

  <line x1="30" y1="112" x2="850" y2="112" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="5 5"/>

  <text x="30" y="146" font-size="13" font-weight="600" fill="var(--teal)">Machine learning</text>
  <rect x="30" y="160" width="150" height="62" rx="6" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"><animate attributeName="opacity" values=".12;.30;.12" dur="3.2s" begin="0s" repeatCount="indefinite"/></rect>
  <text x="105" y="184" text-anchor="middle" font-size="11.5" fill="var(--ink)">lots of examples</text>
  <text x="105" y="202" text-anchor="middle" font-size="11.5" fill="var(--ink)">already answered</text>
  <line x1="186" y1="191" x2="238" y2="191" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="238,191 230,186 230,196" fill="var(--teal)"/>
  <rect x="244" y="160" width="150" height="62" rx="6" fill="var(--teal)" opacity=".22" stroke="var(--teal)" stroke-width="2.5"><animate attributeName="opacity" values=".22;.46;.22" dur="3.2s" begin="1.1s" repeatCount="indefinite"/></rect>
  <text x="319" y="184" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--ink)">it works out</text>
  <text x="319" y="202" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--ink)">the rules itself</text>
  <line x1="400" y1="191" x2="452" y2="191" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="452,191 444,186 444,196" fill="var(--teal)"/>
  <text x="462" y="196" font-size="11.5" fill="var(--soft)">answer for something new</text>

  <text x="30" y="252" font-size="11.5" fill="var(--soft)">Nobody wrote a rule for every spam email. It learned what spam looks like.</text>
</svg>'''

NEURAL = '''
<svg viewBox="0 0 980 340" role="img" aria-label="A photograph is broken into pixels, the pixels are fed into a neural network, and the network outputs a judgment">
  <text x="30" y="34" font-size="13" font-weight="600" fill="var(--soft)">A photo is only numbers. The network reads the numbers, not the picture.</text>
  <g>
  <rect x="40" y="92" width="22" height="22" fill="#C9963B"/>
  <rect x="62" y="92" width="22" height="22" fill="#EDEAE3"/>
  <rect x="84" y="92" width="22" height="22" fill="#EDEAE3"/>
  <rect x="106" y="92" width="22" height="22" fill="#EDEAE3"/>
  <rect x="128" y="92" width="22" height="22" fill="#C9963B"/>
  <rect x="40" y="114" width="22" height="22" fill="#C9963B"/>
  <rect x="62" y="114" width="22" height="22" fill="#C9963B"/>
  <rect x="84" y="114" width="22" height="22" fill="#C9963B"/>
  <rect x="106" y="114" width="22" height="22" fill="#C9963B"/>
  <rect x="128" y="114" width="22" height="22" fill="#C9963B"/>
  <rect x="40" y="136" width="22" height="22" fill="#C9963B"/>
  <rect x="62" y="136" width="22" height="22" fill="#16233F"/>
  <rect x="84" y="136" width="22" height="22" fill="#C9963B"/>
  <rect x="106" y="136" width="22" height="22" fill="#16233F"/>
  <rect x="128" y="136" width="22" height="22" fill="#C9963B"/>
  <rect x="40" y="158" width="22" height="22" fill="#C9963B"/>
  <rect x="62" y="158" width="22" height="22" fill="#C9963B"/>
  <rect x="84" y="158" width="22" height="22" fill="#D98C8C"/>
  <rect x="106" y="158" width="22" height="22" fill="#C9963B"/>
  <rect x="128" y="158" width="22" height="22" fill="#C9963B"/>
  <rect x="40" y="180" width="22" height="22" fill="#EDEAE3"/>
  <rect x="62" y="180" width="22" height="22" fill="#C9963B"/>
  <rect x="84" y="180" width="22" height="22" fill="#C9963B"/>
  <rect x="106" y="180" width="22" height="22" fill="#C9963B"/>
  <rect x="128" y="180" width="22" height="22" fill="#EDEAE3"/>
  <g stroke="#fff" stroke-width="1.4" opacity="0">
  <line x1="40" y1="92" x2="40" y2="202"/>
  <line x1="40" y1="92" x2="150" y2="92"/>
  <line x1="62" y1="92" x2="62" y2="202"/>
  <line x1="40" y1="114" x2="150" y2="114"/>
  <line x1="84" y1="92" x2="84" y2="202"/>
  <line x1="40" y1="136" x2="150" y2="136"/>
  <line x1="106" y1="92" x2="106" y2="202"/>
  <line x1="40" y1="158" x2="150" y2="158"/>
  <line x1="128" y1="92" x2="128" y2="202"/>
  <line x1="40" y1="180" x2="150" y2="180"/>
  <line x1="150" y1="92" x2="150" y2="202"/>
  <line x1="40" y1="202" x2="150" y2="202"/>
  <animate attributeName="opacity" values="0;0;1;1;1;0" keyTimes="0;0.10;0.20;0.75;0.90;1" dur="12s" begin="0s" repeatCount="indefinite"/></g>
  </g>
  <text x="95" y="228" text-anchor="middle" font-size="12" font-weight="600" fill="var(--ink)">the photo</text>
  <text x="95" y="245" text-anchor="middle" font-size="10.5" fill="var(--soft)">25 pixels, each a number</text>
  <rect width="22" height="22" rx="2" fill="#16233F" opacity="0">
  <animate attributeName="x" values="40;40;319;319" keyTimes="0;0.28;0.44;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  <animate attributeName="y" values="136;136;85;85" keyTimes="0;0.28;0.44;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.28;0.31;0.42;0.45;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  </rect>
  <rect width="22" height="22" rx="2" fill="#16233F" opacity="0">
  <animate attributeName="x" values="106;106;319;319" keyTimes="0;0.31;0.47;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  <animate attributeName="y" values="136;136;157;157" keyTimes="0;0.31;0.47;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.31;0.34;0.45;0.48;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  </rect>
  <rect width="22" height="22" rx="2" fill="#D98C8C" opacity="0">
  <animate attributeName="x" values="84;84;319;319" keyTimes="0;0.34;0.50;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  <animate attributeName="y" values="158;158;229;229" keyTimes="0;0.34;0.50;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.34;0.37;0.48;0.51;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  </rect>
  <g stroke="var(--line)" stroke-width="1.2">
  <line x1="330" y1="96" x2="520" y2="80"/>
  <line x1="330" y1="96" x2="520" y2="168"/>
  <line x1="330" y1="96" x2="520" y2="256"/>
  <line x1="330" y1="168" x2="520" y2="80"/>
  <line x1="330" y1="168" x2="520" y2="168"/>
  <line x1="330" y1="168" x2="520" y2="256"/>
  <line x1="330" y1="240" x2="520" y2="80"/>
  <line x1="330" y1="240" x2="520" y2="168"/>
  <line x1="330" y1="240" x2="520" y2="256"/>
  <line x1="520" y1="80" x2="680" y2="120"/>
  <line x1="520" y1="80" x2="680" y2="216"/>
  <line x1="520" y1="168" x2="680" y2="120"/>
  <line x1="520" y1="168" x2="680" y2="216"/>
  <line x1="520" y1="256" x2="680" y2="120"/>
  <line x1="520" y1="256" x2="680" y2="216"/>
  <line x1="680" y1="120" x2="840" y2="168"/>
  <line x1="680" y1="216" x2="840" y2="168"/>
  </g>
  <circle cx="330" cy="96" r="15" fill="var(--teal)" opacity=".45"><animate attributeName="opacity" values=".45;.45;1;.45;.45" keyTimes="0;0.42;0.47;0.55;1" dur="12s" begin="0s" repeatCount="indefinite"/></circle>
  <circle cx="330" cy="168" r="15" fill="var(--teal)" opacity=".45"><animate attributeName="opacity" values=".45;.45;1;.45;.45" keyTimes="0;0.43;0.48;0.56;1" dur="12s" begin="0s" repeatCount="indefinite"/></circle>
  <circle cx="330" cy="240" r="15" fill="var(--teal)" opacity=".45"><animate attributeName="opacity" values=".45;.45;1;.45;.45" keyTimes="0;0.44;0.49;0.57;1" dur="12s" begin="0s" repeatCount="indefinite"/></circle>
  <circle cx="520" cy="80" r="15" fill="var(--teal)" opacity=".35"><animate attributeName="opacity" values=".35;.35;.95;.35;.35" keyTimes="0;0.52;0.57;0.65;1" dur="12s" begin="0s" repeatCount="indefinite"/></circle>
  <circle cx="520" cy="168" r="15" fill="var(--teal)" opacity=".35"><animate attributeName="opacity" values=".35;.35;.95;.35;.35" keyTimes="0;0.53;0.58;0.66;1" dur="12s" begin="0s" repeatCount="indefinite"/></circle>
  <circle cx="520" cy="256" r="15" fill="var(--teal)" opacity=".35"><animate attributeName="opacity" values=".35;.35;.95;.35;.35" keyTimes="0;0.54;0.59;0.67;1" dur="12s" begin="0s" repeatCount="indefinite"/></circle>
  <circle cx="680" cy="120" r="15" fill="var(--teal)" opacity=".35"><animate attributeName="opacity" values=".35;.35;.95;.35;.35" keyTimes="0;0.62;0.67;0.75;1" dur="12s" begin="0s" repeatCount="indefinite"/></circle>
  <circle cx="680" cy="216" r="15" fill="var(--teal)" opacity=".35"><animate attributeName="opacity" values=".35;.35;.95;.35;.35" keyTimes="0;0.63;0.68;0.76;1" dur="12s" begin="0s" repeatCount="indefinite"/></circle>
  <circle cx="840" cy="168" r="19" fill="var(--gold)" opacity=".35"><animate attributeName="opacity" values=".35;.35;1;.35;.35" keyTimes="0;0.72;0.77;0.85;1" dur="12s" begin="0s" repeatCount="indefinite"/></circle>
  <text x="330" y="300" text-anchor="middle" font-size="12" font-weight="600" fill="var(--ink)">what goes in</text>
  <text x="600" y="300" text-anchor="middle" font-size="12" font-weight="600" fill="var(--ink)">many simple parts, connected</text>
  <text x="600" y="317" text-anchor="middle" font-size="10.5" fill="var(--soft)">each passes a small judgment along</text>
  <g opacity="0">
  <rect x="786" y="206" width="112" height="46" rx="7" fill="var(--gold)" opacity=".22" stroke="var(--gold)" stroke-width="2"/>
  <text x="842" y="228" text-anchor="middle" font-size="14" font-weight="600" fill="var(--ink)">&#8220;a cat&#8221;</text>
  <text x="842" y="245" text-anchor="middle" font-size="10.5" fill="var(--soft)">the judgment</text>
  <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.76;0.82;0.93;1" dur="12s" begin="0s" repeatCount="indefinite"/>
  </g>
  </svg>'''

CLASSIFY_VS_GENERATE = '''
<svg viewBox="0 0 880 250" role="img" aria-label="Classifying picks a label from a list; generating produces something new">
  <text x="30" y="24" font-size="13" font-weight="600" fill="var(--teal)">Classify &#8212; choose from what exists</text>
  <rect x="30" y="38" width="118" height="52" rx="6" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>
  <text x="89" y="70" text-anchor="middle" font-size="11.5" fill="var(--ink)">an email</text>
  <line x1="154" y1="64" x2="206" y2="64" stroke="var(--teal)" stroke-width="2"/>
  <polygon points="206,64 198,59 198,69" fill="var(--teal)"/>
  <rect x="212" y="38" width="150" height="52" rx="6" fill="none" stroke="var(--teal)" stroke-width="2"/>
  <text x="287" y="62" text-anchor="middle" font-size="11.5" fill="var(--ink)">spam</text>
  <text x="287" y="80" text-anchor="middle" font-size="11.5" fill="var(--soft)">or not spam</text>
  <text x="380" y="68" font-size="11" fill="var(--soft)">one of two answers, both already known</text>

  <line x1="30" y1="120" x2="850" y2="120" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="5 5"/>

  <text x="30" y="154" font-size="13" font-weight="600" fill="#8A6420">Generate &#8212; make something that was not there</text>
  <rect x="30" y="168" width="118" height="52" rx="6" fill="var(--gold)" opacity=".18" stroke="var(--gold)" stroke-width="2"/>
  <text x="89" y="200" text-anchor="middle" font-size="11.5" fill="var(--ink)">a prompt</text>
  <line x1="154" y1="194" x2="206" y2="194" stroke="var(--gold)" stroke-width="2"/>
  <polygon points="206,194 198,189 198,199" fill="var(--gold)"/>
  <rect x="212" y="168" width="150" height="52" rx="6" fill="var(--gold)" opacity=".28" stroke="var(--gold)" stroke-width="2.5"><animate attributeName="opacity" values=".28;.55;.28" dur="2.6s" begin="0s" repeatCount="indefinite"/></rect>
  <text x="287" y="192" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--ink)">a new paragraph</text>
  <text x="287" y="210" text-anchor="middle" font-size="11.5" fill="var(--soft)">nobody wrote before</text>
  <text x="380" y="198" font-size="11" fill="var(--soft)">not picked from a list &#8212; produced</text>
</svg>'''

RARE_CASES = '''
<svg viewBox="0 0 860 250" role="img" aria-label="A model sees common cases many times and rare cases almost never">
  <text x="30" y="24" font-size="12.5" font-weight="600" fill="var(--soft)">what the training data actually contained</text>

  <text x="30" y="66" font-size="12.5" fill="var(--ink)">an ordinary car</text>
  <g fill="var(--teal)">
    <rect x="200" y="50" width="22" height="22" rx="3"/><rect x="230" y="50" width="22" height="22" rx="3"/>
    <rect x="260" y="50" width="22" height="22" rx="3"/><rect x="290" y="50" width="22" height="22" rx="3"/>
    <rect x="320" y="50" width="22" height="22" rx="3"/><rect x="350" y="50" width="22" height="22" rx="3"/>
    <rect x="380" y="50" width="22" height="22" rx="3"/><rect x="410" y="50" width="22" height="22" rx="3"/>
    <rect x="440" y="50" width="22" height="22" rx="3"/><rect x="470" y="50" width="22" height="22" rx="3"/>
    <rect x="500" y="50" width="22" height="22" rx="3"/><rect x="530" y="50" width="22" height="22" rx="3"/>
  </g>
  <text x="566" y="66" font-size="11.5" fill="var(--soft)">seen thousands of times</text>

  <text x="30" y="132" font-size="12.5" fill="var(--ink)">a horse and cart at night</text>
  <rect x="200" y="116" width="22" height="22" rx="3" fill="var(--wrong)"><animate attributeName="opacity" values="1;.18;1" dur="1.6s" begin="0s" repeatCount="indefinite"/></rect>
  <text x="240" y="132" font-size="11.5" fill="var(--wrong)">seen almost never</text>

  <rect x="30" y="170" width="800" height="54" rx="8" fill="var(--gold)" opacity=".16" stroke="var(--gold)" stroke-width="2"/>
  <text x="50" y="194" font-size="12.5" font-weight="600" fill="var(--ink)">It did not learn a rule for &#8220;vehicle&#8221;. It learned what it was shown.</text>
  <text x="50" y="213" font-size="11.5" fill="var(--soft)">So the thing it has barely seen is the thing it gets wrong &#8212; and it is confident anyway.</text>
</svg>'''

NARROW = '''
<svg viewBox="0 0 860 210" role="img" aria-label="Each AI is expert at one task only and cannot do the others">
  <g>
    <rect x="30" y="40" width="180" height="88" rx="10" fill="var(--teal)" opacity=".14" stroke="var(--teal)" stroke-width="2"/>
    <text x="120" y="72" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">translation app</text>
    <text x="120" y="94" text-anchor="middle" font-size="11" fill="var(--soft)">brilliant at translating</text>
    <text x="120" y="113" text-anchor="middle" font-size="11" fill="var(--wrong)">cannot recognise a face</text>
  </g>
  <g>
    <rect x="240" y="40" width="180" height="88" rx="10" fill="var(--teal)" opacity=".14" stroke="var(--teal)" stroke-width="2"/>
    <text x="330" y="72" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">spam filter</text>
    <text x="330" y="94" text-anchor="middle" font-size="11" fill="var(--soft)">brilliant at spotting spam</text>
    <text x="330" y="113" text-anchor="middle" font-size="11" fill="var(--wrong)">cannot translate a word</text>
  </g>
  <g>
    <rect x="450" y="40" width="180" height="88" rx="10" fill="var(--teal)" opacity=".14" stroke="var(--teal)" stroke-width="2"/>
    <text x="540" y="72" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">speech recognition</text>
    <text x="540" y="94" text-anchor="middle" font-size="11" fill="var(--soft)">brilliant at hearing words</text>
    <text x="540" y="113" text-anchor="middle" font-size="11" fill="var(--wrong)">cannot drive a car</text>
  </g>
  <g>
    <rect x="660" y="40" width="170" height="88" rx="10" fill="none" stroke="var(--line)" stroke-width="2" stroke-dasharray="6 5"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" begin="0s" repeatCount="indefinite"/></rect>
    <text x="745" y="80" text-anchor="middle" font-size="12.5" fill="var(--soft)">one AI that</text>
    <text x="745" y="100" text-anchor="middle" font-size="12.5" fill="var(--soft)">does all of it</text>
    <text x="745" y="119" text-anchor="middle" font-size="11" font-weight="600" fill="var(--wrong)">does not exist yet</text>
  </g>
  <text x="30" y="172" font-size="12" fill="var(--soft)">This is what &#8220;narrow&#8221; means: expert at one task, useless at the one next to it.</text>
</svg>'''



PHOTO_CSS = """
/* ---------- photo slides ---------- */
.shots{display:grid; gap:.85rem; margin:1rem 0 .35rem}
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


FOURTASKS = '''
<svg viewBox="0 0 980 470" role="img" aria-label="The same photograph put through classification, detection, recognition and generation, and what each one returns">
  <text x="30" y="24" font-size="13" font-weight="600" fill="var(--soft)">The same photo. Four different questions. Four different answers.</text>

  <!-- ROW 1 -->
  <g>
    <text x="30" y="58" font-size="13" font-weight="600" fill="var(--teal)">1 &#183; Classification &#8212; WHAT is this?</text>
    <rect x="30" y="70" width="96" height="72" rx="5" fill="#EDEAE3" stroke="var(--line)" stroke-width="1.5"/>
    <circle cx="62" cy="100" r="12" fill="#C9963B"/><rect x="82" y="94" width="28" height="32" rx="4" fill="#9BB7A6"/>
    <line x1="134" y1="106" x2="172" y2="106" stroke="var(--teal)" stroke-width="2"/>
    <polygon points="172,106 164,101 164,111" fill="var(--teal)"/>
    <rect x="180" y="84" width="130" height="44" rx="6" fill="var(--teal)" opacity=".16" stroke="var(--teal)" stroke-width="2"/>
    <text x="245" y="111" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">&#8220;a cat&#8221;</text>
    <text x="30" y="164" font-size="11.5" fill="var(--soft)">one label for the whole picture &#8212; it never says where</text>
  </g>

  <g>
    <text x="520" y="58" font-size="13" font-weight="600" fill="#8A6420">3 &#183; Recognition &#8212; WHICH ONE is it?</text>
    <rect x="520" y="70" width="96" height="72" rx="5" fill="#EDEAE3" stroke="var(--line)" stroke-width="1.5"/>
    <circle cx="556" cy="100" r="14" fill="#D9B08C"/>
    <circle cx="551" cy="97" r="2" fill="#16233F"/><circle cx="562" cy="97" r="2" fill="#16233F"/>
    <rect x="539" y="83" width="35" height="35" fill="none" stroke="var(--gold)" stroke-width="2.5"/>
    <line x1="624" y1="106" x2="662" y2="106" stroke="var(--gold)" stroke-width="2"/>
    <polygon points="662,106 654,101 654,111" fill="var(--gold)"/>
    <rect x="670" y="84" width="150" height="44" rx="6" fill="var(--gold)" opacity=".22" stroke="var(--gold)" stroke-width="2"/>
    <text x="745" y="111" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">&#8220;this is Sara&#8221;</text>
    <text x="520" y="164" font-size="11.5" fill="var(--soft)">detection finds A face. Recognition says WHOSE face.</text>
  </g>

  <line x1="30" y1="186" x2="950" y2="186" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="5 5"/>

  <!-- ROW 2 -->
  <g>
    <text x="30" y="218" font-size="13" font-weight="600" fill="var(--teal)">2 &#183; Detection &#8212; WHAT, and WHERE?</text>
    <rect x="30" y="230" width="96" height="72" rx="5" fill="#EDEAE3" stroke="var(--line)" stroke-width="1.5"/>
    <circle cx="62" cy="260" r="12" fill="#C9963B"/><rect x="82" y="254" width="28" height="32" rx="4" fill="#9BB7A6"/>
    <rect x="48" y="246" width="28" height="28" fill="none" stroke="#C9963B" stroke-width="2.5"/>
    <rect x="79" y="250" width="34" height="40" fill="none" stroke="#3F7D3A" stroke-width="2.5"/>
    <line x1="134" y1="266" x2="172" y2="266" stroke="var(--teal)" stroke-width="2"/>
    <polygon points="172,266 164,261 164,271" fill="var(--teal)"/>
    <rect x="180" y="240" width="170" height="52" rx="6" fill="var(--teal)" opacity=".16" stroke="var(--teal)" stroke-width="2"/>
    <text x="265" y="261" text-anchor="middle" font-size="12" font-weight="600" fill="var(--ink)">cat &#8212; box here</text>
    <text x="265" y="280" text-anchor="middle" font-size="12" font-weight="600" fill="var(--ink)">chair &#8212; box there</text>
    <text x="30" y="324" font-size="11.5" fill="var(--soft)">every object found, and its position</text>
    <text x="30" y="342" font-size="11.5" fill="var(--soft)">this is what a self-driving car needs</text>
  </g>

  <g>
    <text x="520" y="218" font-size="13" font-weight="600" fill="#8A6420">4 &#183; Generation &#8212; MAKE one that did not exist</text>
    <rect x="520" y="230" width="124" height="52" rx="6" fill="var(--gold)" opacity=".14" stroke="var(--gold)" stroke-width="2" stroke-dasharray="5 4"/>
    <text x="582" y="253" text-anchor="middle" font-size="11.5" fill="var(--ink)">&#8220;a cat on a</text>
    <text x="582" y="270" text-anchor="middle" font-size="11.5" fill="var(--ink)">chair, painted&#8221;</text>
    <line x1="652" y1="256" x2="690" y2="256" stroke="var(--gold)" stroke-width="2"/>
    <polygon points="690,256 682,251 682,261" fill="var(--gold)"/>
    <rect x="698" y="230" width="96" height="72" rx="5" fill="#F3E6CE" stroke="var(--gold)" stroke-width="2">
      <animate attributeName="opacity" values=".25;1;1;.25" keyTimes="0;0.25;0.8;1" dur="5s" repeatCount="indefinite"/>
    </rect>
    <g>
      <circle cx="730" cy="260" r="12" fill="#C9963B"/><rect x="750" y="254" width="28" height="32" rx="4" fill="#9BB7A6"/>
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.3;0.8;1" dur="5s" repeatCount="indefinite"/>
    </g>
    <text x="520" y="324" font-size="11.5" fill="var(--soft)">no photograph went in at all</text>
    <text x="520" y="342" font-size="11.5" fill="var(--soft)">the picture itself is the answer</text>
  </g>

  <rect x="30" y="374" width="920" height="72" rx="8" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="2"/>
  <text x="50" y="402" font-size="12.5" font-weight="600" fill="var(--ink)">The first three take a picture IN and give a label OUT. Only the fourth gives a picture out.</text>
  <text x="50" y="426" font-size="11.5" fill="var(--soft)">Every AI example in this lesson, and in the exam, is one of these four.</text>
</svg>'''


def s(cls, *parts):
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


SLIDES = []
A = SLIDES.append

# 1 title
A(s("dark",
    '<div class="rise eyebrow" id="lectureBadge">Programming &amp; Artificial Intelligence</div>',
    h2("How does it learn?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("AI is not one thing. Today we open it up, layer by layer, and find out what is actually doing the learning.",
        "max-width:56ch;margin-top:1rem"),
    ar("النهارده هنفك كلمة AI ونشوف الطبقات اللي جواها واحدة واحدة — مين بالظبط اللي بيتعلّم.")))

# 2 recap
A(s("",
    eyebrow("Before we start &#183; Lecture 2"),
    h2("Where we got to"),
    '<div class="rise stats">'
    '<div class="stat"><b>5</b><span>stages of IT, from a room-sized computer to the cloud</span></div>'
    '<div class="stat"><b>&#215;2</b><span>transistors about every two years &#8212; Moore&#8217;s Law</span></div>'
    '<div class="stat"><b>2010s</b><span>cloud computing made large-scale data and AI possible</span></div>'
    '</div>',
    sub("That last one is the door into today. The cloud gave us the data and the computing power &#8212; this lesson is about what we did with them.",
        "max-width:60ch;margin-top:.9rem"),
    ar("آخر مرحلة — السحابة — هي اللي فتحت الباب للدرس ده: داتا كتير وقدرة حوسبة كبيرة. النهارده هنشوف عملنا بيهم إيه.")))

# 3 hook
A(s("",
    eyebrow("Right now, in your pocket"),
    h2("You used AI four times before breakfast"),
    '<div class="rise fields">'
    '<span class="chip">a spam filter sorted your email</span>'
    '<span class="chip">a store recommended a product</span>'
    '<span class="chip">an app translated a sentence</span>'
    '<span class="chip">ChatGPT wrote you a paragraph</span>'
    '</div>',
    sub("All four are AI. <b>None of them work the same way.</b> By the end of this lesson you will be able to say which is which.",
        "max-width:58ch;margin-top:1rem"),
    ar("الأربعة دول كلهم AI، بس شغالين بطرق مختلفة خالص. في آخر الحصة هتعرف تفرق بينهم.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("What is AI &#8212; and how do machine learning, deep learning and generative AI fit inside it?",
       "max-width:26ch"),
    ar("سؤال النهارده: إيه هو الـ AI أصلاً، وإزاي الـ machine learning والـ deep learning والـ generative AI بيدخلوا جواه؟")))

# 5 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("With your partner, list <b>three</b> things your phone does that seem to need intelligence. For each one predict: does it follow rules somebody wrote, or did it <b>learn from examples</b>? Give one reason.",
        "max-width:56ch;margin-top:1rem"),
    sub("Keep your answers. We come back to them at the end.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: اكتبوا تلات حاجات موبايلكم بيعملها وشكلها محتاج ذكاء. ولكل واحدة توقّعوا: بيتبع قواعد حد كتبها، ولا اتعلّم من أمثلة؟ وليه؟ احتفظوا بالإجابات، هنرجعلها في الآخر.")))

# 6 part 1 divider
A(s("dark",
    eyebrow("Part 1"),
    h2("What is AI?", "font-size:clamp(30px,5.5vw,72px)"),
    ar("الجزء الأول: يعني إيه ذكاء اصطناعي.")))

# 7 AI definition
A(s("",
    eyebrow("1 &#183; The definition"),
    h2("AI is a general term, not one machine", "max-width:24ch"),
    '<div class="rise statement"><em>Artificial Intelligence</em> &#8212; a general term for technologies that '
    'reproduce or perform intelligent human behaviour &#8212; learning, reasoning, judgment &#8212; on a computer.</div>',
    sub("It is the name of a whole field. Saying &#8220;an AI&#8221; is a bit like saying &#8220;a vehicle&#8221;: true, but it does not tell you whether you are looking at a bicycle or a lorry.",
        "max-width:58ch;margin-top:.9rem"),
    ar("AI اسم لمجال كامل مش لجهاز معيّن. لما تقول &#8220;ده AI&#8221; ده زي ما تقول &#8220;دي عربية&#8221; — صح، بس ماقلتش عجلة ولا تريلا.")))

# 8 three examples
A(s("",
    eyebrow("1 &#183; The book&#8217;s three examples"),
    h2("Where you meet it"),
    "<table>"
    "<tr><th>Example</th><th>What the machine is doing</th></tr>"
    "<tr><td><b>Speech recognition</b></td><td>Turning the sound of your voice into words</td></tr>"
    "<tr><td><b>Image recognition</b></td><td>Deciding what is in a photograph</td></tr>"
    "<tr><td><b>Translation</b></td><td>Changing one language into another</td></tr>"
    "</table>",
    sub("Learn these three &#8212; they are the examples the textbook gives for AI itself, and they come up in questions.",
        "margin-top:.8rem;color:var(--soft)"),
    ar("التلاتة دول هما الأمثلة اللي الكتاب بيديها للـ AI نفسه. احفظهم، بييجوا في الأسئلة.")))

# 9 narrow AI + diagram
A(s("",
    eyebrow("1 &#183; The limit that matters"),
    h2("Today&#8217;s AI is narrow"),
    fig(NARROW),
    ar("كل AI شاطر في حاجة واحدة بس. اللي بيترجم مايعرفش يشوف وش، واللي بيمسك السبام مايعرفش يترجم. والـ AI اللي يعمل كل حاجة لسه مش موجود.")))

# photos: the same three, for real
A(s("",
    eyebrow("1 &#183; The same three, photographed"),
    h2("AI you can point at"),
    '<div class="rise shots three">'
    + shot("Google_Home_Mini.jpg", "Speech recognition",
           "It turns the sound of a voice into words, and does nothing else.",
           "ده بيحوّل الصوت لكلام — وبس. مابيعرفش يترجم ولا يشوف.")
    + shot("MnistExamples.png", "Image recognition",
           "Thousands of handwritten digits. This is what &#8220;learning from examples&#8221; looks like.",
           "أرقام مكتوبة بخط اليد. دي شكل التعلّم من الأمثلة على الحقيقة.")
    + shot("Waymo_self-driving_car_front_view.gk.jpg", "A car that reads the road",
           "The book&#8217;s own example of deep learning: image analysis for autonomous driving.",
           "مثال الكتاب نفسه على الـ deep learning: تحليل صور القيادة الذاتية.")
    + '</div>',
    CREDIT,
    ar("التلات صور دي نفس أمثلة الكتاب بس على الحقيقة. خلي الطلبة يقولوا كل واحدة شغالة إزاي قبل ما تقول.")))

# 10 think it through
A(s("dark",
    eyebrow("Think it through"),
    h2("A spam filter and a shop&#8217;s recommendations do completely different jobs. What do they have in common <i>underneath</i>?",
       "max-width:26ch"),
    sub("Two minutes with your partner. Answer in one sentence.", "margin-top:1rem;color:var(--soft)"),
    ar("فلتر السبام وترشيحات المتجر بيعملوا حاجتين مختلفتين تمامًا. إيه اللي مشترك بينهم من جوه؟ دقيقتين مع زميلك، وإجابة في سطر واحد.")))

# ---- interlude: the four words, not in the book but worth the time ----

A(s("dark",
    eyebrow("Not in the book &#183; worth five minutes"),
    h2("Four words people mix up", "font-size:clamp(28px,5vw,64px);max-width:20ch"),
    sub("The textbook does not separate these, but every example in this lesson "
        "&#8212; and every one in the exam &#8212; is one of the four. Get these "
        "straight and the rest of the lesson is easy.",
        "max-width:56ch;margin-top:1rem"),
    ar("الأربع كلمات دول مش في الكتاب، بس كل مثال في الدرس وكل سؤال في الامتحان واحد منهم. "
       "لو مسكتهم صح، الباقي كله هيبقى سهل عليك.")))

A(s("",
    eyebrow("Classification &#183; detection &#183; recognition &#183; generation"),
    h2("The same photo, four questions"),
    fig(FOURTASKS),
    ar("نفس الصورة بالظبط، أربع أسئلة مختلفة، أربع إجابات مختلفة. التلاتة الأولانيين "
       "بياخدوا صورة ويطلّعوا كلام. الرابع بس هو اللي بيطلّع صورة.")))

A(s("",
    eyebrow("The same four, for real"),
    h2("What each one actually looks like"),
    '<div class="rise shots four">'
    + shot("MnistExamples.png", "Classification",
           "Each digit gets one label: 0 to 9. One answer for the whole image.",
           "كل رقم بياخد تصنيف واحد من 0 لـ 9 — إجابة واحدة للصورة كلها.")
    + shot("Detected-with-YOLO-Schreibtisch-mit-Objekten.jpg", "Detection",
           "Boxes drawn round every object found, each with its own label and place.",
           "مربعات حوالين كل حاجة اتلاقت، وكل واحدة بإسمها ومكانها.")
    + shot("Face_detection.jpg", "Recognition",
           "Detection finds that there IS a face. Recognition says whose it is.",
           "الـ detection بيلاقي إن فيه وش. الـ recognition بيقول الوش ده بتاع مين.")
    + shot("A_photograph_of_an_astronaut_riding_a_horse_2022-08-28.png", "Generation",
           "Nothing went in but a sentence. The picture itself is the answer.",
           "مدخلش غير جملة. الصورة نفسها هي الناتج.")
    + '</div>',
    CREDIT,
    ar("خلي الطلبة يقولوا كل صورة دي أنهي نوع قبل ما تقرا العناوين — دي أسرع طريقة تعرف مين فهم.")))

A(s("",
    eyebrow("Why it matters for the exam"),
    h2("Where each one shows up later", "max-width:26ch"),
    "<table>"
    "<tr><th>Task</th><th>Question it answers</th><th>Where it appears in this lesson</th></tr>"
    "<tr><td><b>Classification</b></td><td>What is this?</td><td>Spam filter; sorting photos</td></tr>"
    "<tr><td><b>Detection</b></td><td>What, and where?</td><td>A self-driving car reading the road</td></tr>"
    "<tr><td><b>Recognition</b></td><td>Which one is it?</td><td>Unlocking a phone; reading an X-ray</td></tr>"
    "<tr><td><b>Generation</b></td><td>Make a new one</td><td>ChatGPT; image-generation AI</td></tr>"
    "</table>",
    sub("The first three are all <b>machine learning</b> doing different jobs. Only the last "
        "one needs <b>generative AI</b>.", "margin-top:.8rem;max-width:56ch"),
    ar("التلاتة الأولانيين كلهم machine learning بيعمل شغلانات مختلفة. الرابع بس هو اللي "
       "محتاج generative AI. وده بيربط الكلام ده بالطبقات اللي جاية.")))

# 11 part 2 divider
A(s("dark",
    eyebrow("Part 2"),
    h2("The nested layers", "font-size:clamp(30px,5.5vw,72px)"),
    ar("الجزء التاني: الطبقات اللي جوه بعض.")))

# 12 NESTED DIAGRAM — the spine
A(s("",
    eyebrow("2 &#183; The one picture to remember"),
    h2("Boxes inside boxes"),
    fig(NESTED),
    ar("دي أهم صورة في الدرس: الـ AI هو الأوسع، وجواه machine learning، وجواه deep learning، وجواه generative AI. مش أربع حاجات جنب بعض — دول جوه بعض.")))

# 13 machine learning definition
A(s("",
    eyebrow("2 &#183; Machine learning"),
    h2("It learns patterns from data", "max-width:22ch"),
    '<div class="rise statement"><em>Machine learning</em> &#8212; one of the learning technologies that makes AI work. '
    'It learns <b>patterns from data</b> to make predictions and judgments.</div>',
    sub("Examples the book gives: <b>spam filters</b> and <b>product recommendations</b>. That is the answer to the question you just discussed &#8212; different jobs, same underlying method.",
        "max-width:58ch;margin-top:.9rem"),
    ar("الـ machine learning بيتعلّم أنماط من الداتا عشان يتنبأ ويحكم. وأمثلة الكتاب: فلتر السبام وترشيح المنتجات — دي إجابة السؤال اللي لسه سألناه.")))

# 14 RULES VS LEARNED DIAGRAM
A(s("",
    eyebrow("2 &#183; The difference that matters"),
    h2("Rules you write, or rules it works out"),
    fig(RULES_VS_LEARNED),
    ar("الفرق الأساسي: في البرمجة العادية انت بتكتب القواعد بإيدك. في الـ machine learning بتديله أمثلة متحلولة وهو يستنتج القاعدة لوحده.")))

# 15 deep learning
A(s("",
    eyebrow("2 &#183; Deep learning"),
    h2("A more advanced kind of machine learning", "max-width:24ch"),
    '<div class="rise statement"><em>Deep learning</em> &#8212; an advanced technology <b>within</b> machine learning '
    'that uses <b>neural networks</b>. It learns complex patterns using <b>large-scale data</b>.</div>',
    "<table style='margin-top:.9rem'>"
    "<tr><th>Example</th><th>What it handles</th></tr>"
    "<tr><td><b>Image analysis for autonomous driving</b></td><td>Reading a whole road scene at once</td></tr>"
    "<tr><td><b>Speech synthesis</b></td><td>Producing a voice that sounds human</td></tr>"
    "</table>",
    ar("الـ deep learning نوع متقدم جوه الـ machine learning، بيستخدم الشبكات العصبية ومحتاج داتا ضخمة. أمثلته: تحليل صور القيادة الذاتية، وتوليد الصوت.")))

# 16 NEURAL NETWORK DIAGRAM
A(s("",
    eyebrow("2 &#183; The core technology"),
    h2("A neural network"),
    fig(NEURAL),
    sub("It is the core technology behind the recent jump in what AI can do.",
        "max-width:58ch;margin-top:.5rem"),
    # the layer names are not in the English book, but the ministry's
    # assessments ask for them ("the layers between the input and output
    # layers are called ..."), so they are taught here
    sub("The columns have names: the <b>input layer</b>, the <b>hidden layers</b> in between, and the "
        "<b>output layer</b>. Training changes the <b>weight</b> &#8212; the strength &#8212; of each connection.",
        "max-width:62ch;margin-top:.4rem;font-size:clamp(13px,1.4vw,18px)"),
    ar("طبقة الإدخال، وبعدها الطبقات المخفية (hidden layers)، وبعدها طبقة الإخراج — والتدريب بيغيّر وزن كل وصلة. الشبكة العصبية متصممة على فكرة خلايا المخ. مفيش جزء منها ذكي لوحده — الذكاء بييجي من ربط أجزاء بسيطة كتير مع بعض. ودي التقنية اللي شايلة تقدّم الـ AI الحديث.")))

# 17 RARE CASES DIAGRAM
A(s("",
    eyebrow("2 &#183; Why large-scale data matters"),
    h2("It only knows what it was shown"),
    fig(RARE_CASES),
    ar("الموديل مابيتعلمش قاعدة عامة، بيتعلم اللي اتعرض عليه. فالحاجة النادرة هي بالظبط اللي بيغلط فيها — وبثقة كمان.")))

# 18 pause and think
A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("Deep learning needs large-scale data to learn. So why might an AI struggle with something it has <i>rarely</i> seen?",
       "max-width:26ch"),
    ar("الـ deep learning محتاج داتا ضخمة عشان يتعلم. طب ليه بيتلخبط في حاجة نادرًا ما شافها؟")))

# 19 part 3 divider
A(s("dark",
    eyebrow("Part 3"),
    h2("Generative AI", "font-size:clamp(30px,5.5vw,72px)"),
    ar("الجزء التالت: الذكاء الاصطناعي التوليدي.")))

# 20 generative AI definition
A(s("",
    eyebrow("3 &#183; Generative AI"),
    h2("It makes new data", "max-width:18ch"),
    '<div class="rise statement"><em>Generative AI</em> &#8212; AI technology that uses <b>deep learning</b> '
    'to generate <b>new data</b>: text, images, audio, programs.</div>',
    sub("Examples the book gives: <b>ChatGPT</b> and <b>image-generation AIs</b>. Note where it sits &#8212; it is built <i>on</i> deep learning, which is inside machine learning, which is inside AI.",
        "max-width:58ch;margin-top:.9rem"),
    ar("الـ generative AI بيستخدم الـ deep learning عشان يطلّع داتا جديدة: نص، صور، صوت، برامج. وخلي بالك من مكانه — مبني على الـ deep learning اللي جوه الـ machine learning اللي جوه الـ AI.")))

# 21 CLASSIFY VS GENERATE DIAGRAM
A(s("",
    eyebrow("3 &#183; The word &#8220;generate&#8221;"),
    h2("Choosing an answer, or making one"),
    fig(CLASSIFY_VS_GENERATE),
    ar("الفرق بين إنه يختار من حاجات موجودة، وإنه يطلّع حاجة جديدة محدش كتبها قبل كده. دي معنى كلمة generate.")))

# 22 what it can generate
A(s("",
    eyebrow("3 &#183; What counts as &#8220;new data&#8221;"),
    h2("Four kinds"),
    '<div class="rise fields">'
    '<span class="chip">text</span><span class="chip">images</span>'
    '<span class="chip">audio</span><span class="chip">programs</span>'
    '</div>',
    sub("If a question asks what generative AI produces, these four are the answer. A program counts too &#8212; code is just another kind of text it can write.",
        "max-width:58ch;margin-top:1rem"),
    ar("لو السؤال بيقول الـ generative AI بيطلّع إيه، دي الأربعة. والبرامج منهم — الكود ده برضو نص بيكتبه.")))

# 23 worked example T/F
A(s("",
    eyebrow("Worked example &#183; page 15"),
    h2("True or false?", "max-width:18ch"),
    '<ul class="rise check">'
    '<li>Machine learning is one of the technologies that makes AI work. <b>&#10003; True</b></li>'
    '<li class="no">Deep learning is a completely different technology from machine learning. <b>&#10007; False &#8212; it is <i>inside</i> it</b></li>'
    '<li>Generative AI uses deep learning to generate new data. <b>&#10003; True</b></li>'
    '<li class="no">AI and machine learning have the same meaning. <b>&#10007; False &#8212; AI is the broad field</b></li>'
    '</ul>',
    ar("التمرين ده من الكتاب صفحة 15. لاحظ إن الغلطتين الاتنين سببهم حاجة واحدة: إن الطالب فاكر الطبقات دي جنب بعض مش جوه بعض.")))

# 24 exam warning
A(s("",
    eyebrow("Exam warning"),
    h2("The two sentences students get wrong every year", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane b"><h3>&#10007; &#8220;Deep learning is completely different from machine learning&#8221;</h3>'
    '<ul><li>It is not a different technology</li><li>It is an <b>advanced kind of</b> machine learning</li>'
    '<li>Go back to the nested boxes</li></ul></div>'
    '<div class="pane b"><h3>&#10007; &#8220;AI and machine learning mean the same thing&#8221;</h3>'
    '<ul><li>AI is the <b>broad field</b></li><li>Machine learning is <b>one technology inside it</b></li>'
    '<li>Same trap, other direction</li></ul></div>'
    '</div>',
    ar("الجملتين دول بيتكرروا في الامتحان كل سنة، والسبب واحد: الطالب مش شايف إن الطبقات جوه بعض. ارجع لصورة الصناديق.")))

# 25 fluent but wrong
A(s("",
    eyebrow("Use it carefully"),
    h2("A fluent answer can still be wrong", "max-width:24ch"),
    '<div class="rise quote"><p>Generative AI is built to produce text that <i>reads</i> like a good answer. '
    'Reading well and being correct are not the same thing.</p><cite>Why you check before you hand it in</cite></div>',
    sub("It has no way of knowing it is wrong, so it will not warn you. Check any fact it gives you against the book.",
        "max-width:56ch;margin-top:.9rem"),
    ar("الـ generative AI متصمم يطلّع كلام شكله مقنع. وشكله مقنع مش معناه إنه صح — وهو مش هيحذّرك لأنه أصلاً مش عارف. راجع أي معلومة منه على الكتاب.")))

# 26 new context
A(s("",
    eyebrow("In a new context"),
    h2("A farmer photographs a diseased crop leaf", "max-width:26ch"),
    sub("An app names the disease from the photo, and writes a short treatment plan.",
        "max-width:54ch;margin-top:.7rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li>Which part is <b>image recognition</b>, and which part is <b>generative AI</b>?</li>'
    '<li>If the disease is rare in that region, which part would you trust less &#8212; and why?</li>'
    '</ul>',
    ar("فلاح بيصوّر ورقة زرع مريضة. التطبيق بيحدد المرض وبيكتب خطة علاج. أنهي جزء تعرّف على صور وأنهي جزء توليد؟ ولو المرض نادر في المنطقة دي، هتثق في أنهي جزء أقل؟")))

# photos: inside, and made
A(s("",
    eyebrow("3 &#183; Inside, and made"),
    h2("What the words actually point at"),
    '<div class="rise shots three">'
    + shot("GFPneuron.png", "A real nerve cell",
           "The thing a neural network is modelled on. One of these is not clever either.",
           "دي الخلية العصبية اللي الشبكة متصممة على فكرتها. وهي كمان لوحدها مش ذكية.")
    + shot("Datacenter-telecom.jpg", "Where large-scale data lives",
           "Deep learning needs this much machine. It is why the cloud stage mattered.",
           "الـ deep learning محتاج الكم ده من الأجهزة. عشان كده مرحلة السحابة كانت مهمة.")
    + shot("A_photograph_of_an_astronaut_riding_a_horse_2022-08-28.png",
           "Nobody took this photo",
           "Generated from a sentence. There was never an astronaut, a horse, or a camera.",
           "الصورة دي محدش صوّرها. اتولدت من جملة — مفيش رائد فضاء ولا حصان ولا كاميرا.")
    + '</div>',
    CREDIT,
    ar("قف عند الصورة التالتة واسأل: إزاي نعرف إن دي مش صورة حقيقية؟ دي مقدمة لسلايدة التحذير الجاية.")))

# 27 key takeaway
A(s("",
    eyebrow("Key takeaway"),
    h2("AI is the field. Everything else is a box inside it.", "max-width:30ch"),
    '<div class="rise stats" style="margin-top:1rem">'
    '<div class="stat"><b>AI</b><span>intelligent behaviour on a computer</span></div>'
    '<div class="stat"><b>ML</b><span>learns patterns from data</span></div>'
    '<div class="stat"><b>DL</b><span>neural networks, large data</span></div>'
    '<div class="stat"><b>Gen</b><span>makes new text, images, audio</span></div>'
    '</div>',
    ar("الخلاصة: AI هو المجال كله، وكل واحد بعده صندوق جواه. والترتيب ده هو اللي بيتسأل عليه أكتر حاجة.")))


# ============================ PART 4 · lesson 1-3 ============================

A(s("dark",
    eyebrow("Part 4"),
    h2("Where you actually meet it", "font-size:clamp(30px,5.5vw,72px)"),
    sub("Everything so far was how it works. Now: where it already is, what it is "
        "good at, and where it must not be trusted alone.",
        "max-width:56ch;margin-top:1rem"),
    ar("لغاية دلوقتي شفنا بيشتغل إزاي. دلوقتي: هو موجود فين فعلاً، شاطر في إيه، وفين مينفعش نسيبه لوحده.")))

A(s("",
    eyebrow("4 · Explore · in pairs"),
    h2("Three services you used this week", "max-width:24ch"),
    sub("With your partner, name <b>three</b> services you used this week that you think "
        "used AI. For each, predict <b>what data</b> it needed. Then decide together: "
        "which one would matter most if it got it wrong?",
        "max-width:56ch;margin-top:1rem"),
    ar("مع زميلك: اذكروا تلات خدمات استخدمتوها الأسبوع ده وتفتكروا إن فيها AI. ولكل واحدة توقّعوا محتاجة أنهي بيانات. وبعدين قرروا: لو واحدة فيهم غلطت، أنهي غلطة تفرق أكتر؟")))

A(s("",
    eyebrow("4 · In daily life"),
    h2("Four you already use"),
    "<table>"
    "<tr><th>Service</th><th>What the AI does</th><th>Examples</th></tr>"
    "<tr><td><b>Recommendation system</b></td><td>Predicts your preferences from past behaviour and shows suggestions</td><td>YouTube, Amazon, Spotify</td></tr>"
    "<tr><td><b>Voice assistant</b></td><td>Recognises a voice, understands the command, carries it out</td><td>Siri, Google Assistant</td></tr>"
    "<tr><td><b>Machine translation</b></td><td>Turns text automatically into another language</td><td>Google Translate, DeepL</td></tr>"
    "<tr><td><b>Face recognition</b></td><td>Detects and identifies faces in photographs</td><td>Unlocking a phone</td></tr>"
    "</table>",
    ar("الأربعة دول من الكتاب بالحرف، وبيتسألوا كسؤال مطابقة. خلي بالك من الفرق بين voice assistant و machine translation.")))

A(s("",
    eyebrow("4 · How a recommendation works"),
    h2("It read what you did before"),
    fig(RECSYS),
    ar("نظام الترشيح بياخد سلوكك القديم، يلاقي نمط، ويتوقّع. وده machine learning من الجزء التاني بيشتغل في حاجة بتقابلها كل يوم.")))

A(s("",
    eyebrow("4 · In industry"),
    h2("Four industries"),
    "<table>"
    "<tr><th>Industry</th><th>How AI is used</th></tr>"
    "<tr><td><b>Healthcare</b></td><td>Image-diagnosis AI reads X-ray and CT images; drug-discovery support</td></tr>"
    "<tr><td><b>Agriculture</b></td><td>Predicting harvest timing; detecting pests and diseases</td></tr>"
    "<tr><td><b>Manufacturing</b></td><td>Automatic quality inspection; predictive maintenance</td></tr>"
    "<tr><td><b>Logistics</b></td><td>Optimising delivery routes</td></tr>"
    "</table>",
    sub("<b>Predictive maintenance</b> means predicting a failure <i>before</i> it happens. That term is examined.",
        "margin-top:.8rem;color:var(--soft)"),
    ar("الأربع مجالات دي بيتسألوا كسؤال مطابقة برضو. و predictive maintenance معناها يتوقّع العطل قبل ما يحصل — المصطلح ده بييجي في الامتحان.")))

A(s("",
    eyebrow("4 · The same four, photographed"),
    h2("Where the work actually happens"),
    '<div class="rise shots four">'
    + shot("Chest_Xray_PA_3-8-2010.png", "Healthcare",
           "An image-diagnosis AI reads films like this one and flags what a doctor should look at.",
           "الـ AI بيقرا أفلام زي دي ويحدد للدكتور يبص فين.")
    + shot("Combine_harvester.jpg", "Agriculture",
           "Predicting when to harvest, and spotting pests before they spread.",
           "يتوقّع وقت الحصاد، ويكتشف الآفات قبل ما تنتشر.")
    + shot("KUKA_Industrial_Robots_IR.jpg", "Manufacturing",
           "Quality inspection, and predicting a failure before the machine stops.",
           "فحص الجودة، وتوقّع العطل قبل ما الماكينة تقف.")
    + shot("DHL_delivery_van.jpg", "Logistics",
           "Working out the delivery route that costs the least time and fuel.",
           "يحسب أحسن خط توصيل يوفّر وقت ووقود.")
    + '</div>',
    CREDIT,
    ar("خلي الطلبة يوصلوا كل صورة بالمجال بتاعها قبل ما تقرا العناوين.")))

A(s("",
    eyebrow("4 · The honest summary"),
    h2("Good at, and not to be trusted alone", "max-width:26ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>What AI is good at</h3><ul>'
    '<li>Finding and classifying <b>patterns</b> in complex data — images, text</li>'
    '<li><b>Recognition and generation</b> of images, audio and text</li>'
    '<li><b>Probabilistic prediction</b> based on data</li>'
    '</ul></div>'
    '<div class="pane b"><h3>What needs caution</h3><ul>'
    '<li><b>Ethical judgments</b> — can carry discrimination or prejudice</li>'
    '<li>Anything touching <b>personal data and privacy</b></li>'
    '<li><b>Final decisions</b> — who is responsible for the result?</li>'
    '<li><b>Biased training data</b> makes judgments inaccurate</li>'
    '<li><b>Hallucination</b>, and the <b>black-box problem</b></li>'
    '<li><b>Copyright</b> &#8212; rights issues when copyrighted works are used as training data</li>'
    '</ul></div>'
    '</div>',
    ar("العمود الشمال بييجي سؤال 'اختر اللي الـ AI شاطر فيه'، واليمين بييجي 'اختر اللي مش من دواعي الحذر'. ذاكرهم مقابل بعض.")))

A(s("",
    eyebrow("4 · The one that needs a picture"),
    h2("The black-box problem"),
    fig(BLACKBOX),
    ar("انت شايف اللي دخل واللي طلع، بس مش شايف قرر كده ليه — ولا حتى اللي عملوه شايفين. عشان كده الدكتور هو اللي بيمضي التشخيص.")))

A(s("dark",
    eyebrow("Think it through"),
    h2("A hospital wants image-diagnosis AI to read X-rays. Why should a <i>human doctor</i> still confirm the final diagnosis?",
       "max-width:27ch"),
    ar("مستشفى عايزة تستخدم AI يقرا أشعة. ليه لازم دكتور بني آدم يأكد التشخيص النهائي؟")))

A(s("dark",
    eyebrow("Pause & think"),
    h2("These services hold what you watch, buy and say. Why is that a privacy problem — and who should decide how your data is used?",
       "max-width:27ch"),
    ar("الخدمات دي شايلة اللي بتتفرج عليه وبتشتريه وبتقوله. ليه دي مشكلة خصوصية؟ ومين اللي يقرر بياناتك تتستخدم إزاي؟")))

A(s("",
    eyebrow("In a new context"),
    h2("A school library wants AI to recommend books", "max-width:26ch"),
    sub("It would suggest books to a student based on what they borrowed before.",
        "max-width:54ch;margin-top:.7rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li>Explain <b>how it would work</b>, using what you know about recommendation systems.</li>'
    '<li>Identify <b>one caution</b> the school should think about first.</li>'
    '</ul>',
    ar("مكتبة مدرسة عايزة AI يرشّح كتب للطالب حسب اللي استعاره قبل كده. اشرح هيشتغل إزاي، وحدد تحذير واحد لازم المدرسة تفكر فيه.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 1-3"),
    h2("It is already here, and it still needs you", "max-width:28ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Where it is</h3><ul>'
    '<li>Daily life: recommendations, voice, translation, face recognition</li>'
    '<li>Industry: healthcare, agriculture, manufacturing, logistics</li>'
    '</ul></div>'
    '<div class="pane b"><h3>What it cannot be left to do</h3><ul>'
    '<li>Ethical judgments, and anything touching private data</li>'
    '<li>The final decision &#8212; somebody has to be responsible</li>'
    '</ul></div>'
    '</div>',
    ar("الخلاصة: الـ AI موجود فعلاً حواليك في الحياة والصناعة، بس القرار الأخير والأحكام الأخلاقية وأي حاجة فيها بيانات شخصية لسه محتاجة بني آدم.")))

# 28 QR — must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lectures 1, 2 and 3"),
    # The code stays hidden until the teacher reveals it, so a student reading
    # the deck at home the night before cannot sit the exam with an AI. Press
    # E, or click the panel, when it is time.
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 3 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers this session and the ones before it. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على المحاضرات التلاتة. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))


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


body = "\n\n".join(SLIDES)
BASE = "scripts/lecture3_slides_base.html"
src = io.open(BASE, encoding="utf-8").read()
start = src.index('<div id="stage">') + len('<div id="stage">')
end = src.index('<div id="nav">')
# keep whatever closes the stage div
tail = src[end - 20:end]
close = "\n</div>\n\n" if "</div>" in tail else "\n"
out = src[:start] + "\n\n" + body + close + src[end:]
out = port_lightbox(out)
out = gate_js(out)
if ".qrgate{" not in out:
    out = out.replace("</style>", GATE_CSS.strip() + chr(10) + "</style>", 1)
if ".shots{" not in out:
    out = out.replace("</style>", PHOTO_CSS.strip() + chr(10) + "</style>", 1)

# never let a Liquid delimiter into the page
assert not re.search(r"\{[%{]", out), "Liquid delimiter in generated slides"
io.open(DST, "w", encoding="utf-8", newline="\n").write(out)
print("slides written:", len(SLIDES), "slides,", len(out), "bytes")
