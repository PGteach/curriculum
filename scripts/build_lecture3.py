#!/usr/bin/env python3
"""Generate Lecture 3 printed material from the shared A4 template and exercise data."""
import io,json,re
from html import escape as esc
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'lecture3/_teacher/exercises.json').read_text(encoding='utf-8'))
EX={x['n']:x for x in DATA['SHEET']['parts'][0]['exercises']}
# Class work: two from each lesson, all quick to mark together. The session
# also carries last week's homework correction, but the quiz is taken at home
# so it costs no session time.
IN_CLASS=[1,2,18,19]

# Homework is grouped by lesson so it can be set over two weeks, with the
# book's thinking and research tasks kept separate and optional.
HW_SECTIONS=[
 ("Part 1 &middot; How AI works",
  "الجزء الأول — إزاي الـ AI بيشتغل",
  # the first sheet also carries the masthead and the intro box, so it takes
  # two exercises rather than three
  [[3,4],[5,6,7],[8,9],[13,14],[10,11]]),
 ("Part 2 &middot; AI in daily life and industry",
  "الجزء التاني — الـ AI في الحياة والصناعة",
  [[20,21],[22,25],[23,24]]),
 ("Challenge &middot; optional",
  "تحدي — اختياري",
  [[15,16],[17]]),
]
HOMEWORK=[n for _,_,pages in HW_SECTIONS for g in pages for n in g]
EXTRA_CSS='''
.namebox{display:flex;gap:5mm;margin:0 0 6mm}.namebox>div{flex:1;display:flex;align-items:flex-end;gap:2mm}.namebox span{font-size:9pt;color:var(--soft);font-weight:600}.namebox i{flex:1;border-bottom:1px solid var(--rule);height:6mm}.ex{margin:0 0 5mm;break-inside:avoid}.exhead{display:flex;gap:3mm;align-items:baseline;margin-bottom:1.5mm}.exn{flex:0 0 auto;width:6.5mm;height:6.5mm;border-radius:50%;background:var(--teal);color:#fff;font-size:9pt;font-weight:600;display:flex;align-items:center;justify-content:center}.exq{font-size:10.5pt;font-weight:600}.src{font-size:8pt;color:var(--soft);font-style:italic;margin:0 0 1.5mm 9.5mm}.passage{font-size:10pt;line-height:1.8;background:#FCFCFA;border:1px solid var(--line);padding:3mm}.marks{font-size:9pt;font-weight:600;color:var(--gold);margin:2mm 0}.key{margin-left:9.5mm;font-size:10pt}.teacherwarn{background:#FBF0EE;border-left:3px solid #9C3B2E;padding:3mm}.summary.hw{background:var(--teal-pale)}.keygroup{font-size:9.5pt;color:var(--soft);font-weight:600;text-transform:uppercase;letter-spacing:.04em;margin:5mm 0 2mm}.key ul{margin-left:4mm}.key li{margin-bottom:1mm}.key .note{font-size:9.5pt;color:var(--soft);font-style:italic;margin-top:1.5mm}.keysheet{min-height:auto}ol.blanks{list-style:none;margin:3mm 0 0}ol.blanks li{display:flex;align-items:flex-end;gap:3mm;margin-bottom:4.5mm}ol.blanks li b{flex:0 0 auto;font-size:10.5pt}ol.blanks .rule{flex:1;height:6mm;border-bottom:1px solid var(--rule)}.opt{display:block;margin:1.2mm 0 0 4mm}.srcinline{font-size:8pt;color:var(--soft);font-style:italic;margin-left:2mm}ol.qs li{margin-bottom:3mm}.optlead{font-size:10pt;font-weight:600;margin:2.5mm 0 1.5mm}.fields{display:flex;flex-wrap:wrap;gap:2.5mm;margin:0 0 2mm}.chip{border:1px solid var(--line);border-radius:20mm;padding:1.5mm 4mm;font-size:10pt;background:#FCFCFA}'''
def shell():
 t=(ROOT/'templates/handout-template.html').read_text(encoding='utf-8').replace('</style>',EXTRA_CSS+'</style>',1)
 t=t.replace('__LECTURE_NUM__','3').replace('__TITLE_HTML__','How does it learn?').replace('__TITLE_JS__','How does it learn?').replace('__TOPIC_HTML__','Programming &amp; Artificial Intelligence').replace('__TOPIC_JS__','Programming & Artificial Intelligence').replace('__ACCENT__','#1D6FA5')
 head=t[:t.index('<div id="pagesTop"></div>')+len('<div id="pagesTop"></div>')];tail=t[t.index('<script>'):]
 # Start at the sheet that actually holds the QR, not at the first sheet in the
 # template: the template opens with two demo pages, and anchoring on the first
 # <section> swallowed both into every generated document.
 i=t.index('id="qr"')
 qr=t[t.rindex('<section class="sheet"',0,i):t.index('</section>',i)+len('</section>')]
 return head,tail,qr
def foot():return '<div class="foot"><span>Prepared by: Mr. Eissa Islam</span><span class="pageno"></span></div>'

# Diagrams, identical to the ones in the deck so the booklet a student
# revises from shows the same picture the lesson was taught with.
NESTED='<svg viewBox="0 0 860 300" role="img" aria-label="AI contains machine learning, which contains deep learning, which contains generative AI">\n  <rect x="20" y="20" width="820" height="260" rx="16" fill="var(--teal)" opacity=".07" stroke="var(--teal)" stroke-width="2.5"/>\n  <text x="40" y="48" font-size="15" font-weight="600" fill="var(--teal)">AI</text>\n  <text x="40" y="68" font-size="11" fill="var(--soft)">intelligent behaviour on a computer</text>\n\n  <rect x="150" y="56" width="670" height="204" rx="14" fill="var(--teal)" opacity=".10" stroke="var(--teal)" stroke-width="2"/>\n  <text x="170" y="84" font-size="14" font-weight="600" fill="var(--teal)">Machine learning</text>\n  <text x="170" y="103" font-size="11" fill="var(--soft)">learns from data</text>\n\n  <rect x="300" y="92" width="500" height="148" rx="12" fill="var(--teal)" opacity=".14" stroke="var(--teal)" stroke-width="2"/>\n  <text x="320" y="120" font-size="14" font-weight="600" fill="var(--teal)">Deep learning</text>\n  <text x="320" y="139" font-size="11" fill="var(--soft)">neural networks</text>\n\n  <rect x="470" y="128" width="310" height="92" rx="10" fill="var(--gold)" opacity=".20" stroke="var(--gold)" stroke-width="2.5"/>\n  <text x="492" y="156" font-size="14" font-weight="600" fill="#8A6420">Generative AI</text>\n  <text x="492" y="175" font-size="11" fill="var(--soft)">makes new text, images, audio</text>\n  <text x="492" y="196" font-size="10.5" fill="var(--soft)">e.g. ChatGPT</text>\n\n  <text x="40" y="272" font-size="11.5" fill="var(--soft)">each box is inside the one before it &#8212; not beside it</text>\n</svg>'
RULES='<svg viewBox="0 0 880 270" role="img" aria-label="Traditional programming follows written rules; machine learning works out the rules from examples">\n  <text x="30" y="24" font-size="13" font-weight="600" fill="var(--ink)">Traditional programming</text>\n  <rect x="30" y="38" width="150" height="46" rx="6" fill="none" stroke="var(--soft)" stroke-width="2"/>\n  <text x="105" y="60" text-anchor="middle" font-size="11.5" fill="var(--ink)">rules you</text>\n  <text x="105" y="76" text-anchor="middle" font-size="11.5" fill="var(--ink)">write by hand</text>\n  <line x1="186" y1="61" x2="238" y2="61" stroke="var(--soft)" stroke-width="2"/>\n  <polygon points="238,61 230,56 230,66" fill="var(--soft)"/>\n  <rect x="244" y="38" width="120" height="46" rx="6" fill="var(--soft)" opacity=".13" stroke="var(--soft)" stroke-width="2"/>\n  <text x="304" y="66" text-anchor="middle" font-size="11.5" fill="var(--ink)">the program</text>\n  <line x1="370" y1="61" x2="422" y2="61" stroke="var(--soft)" stroke-width="2"/>\n  <polygon points="422,61 414,56 414,66" fill="var(--soft)"/>\n  <text x="432" y="66" font-size="11.5" fill="var(--soft)">answer</text>\n\n  <line x1="30" y1="112" x2="850" y2="112" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="5 5"/>\n\n  <text x="30" y="146" font-size="13" font-weight="600" fill="var(--teal)">Machine learning</text>\n  <rect x="30" y="160" width="150" height="62" rx="6" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>\n  <text x="105" y="184" text-anchor="middle" font-size="11.5" fill="var(--ink)">lots of examples</text>\n  <text x="105" y="202" text-anchor="middle" font-size="11.5" fill="var(--ink)">already answered</text>\n  <line x1="186" y1="191" x2="238" y2="191" stroke="var(--teal)" stroke-width="2"/>\n  <polygon points="238,191 230,186 230,196" fill="var(--teal)"/>\n  <rect x="244" y="160" width="150" height="62" rx="6" fill="var(--teal)" opacity=".22" stroke="var(--teal)" stroke-width="2.5"/>\n  <text x="319" y="184" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--ink)">it works out</text>\n  <text x="319" y="202" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--ink)">the rules itself</text>\n  <line x1="400" y1="191" x2="452" y2="191" stroke="var(--teal)" stroke-width="2"/>\n  <polygon points="452,191 444,186 444,196" fill="var(--teal)"/>\n  <text x="462" y="196" font-size="11.5" fill="var(--soft)">answer for something new</text>\n\n  <text x="30" y="252" font-size="11.5" fill="var(--soft)">Nobody wrote a rule for every spam email. It learned what spam looks like.</text>\n</svg>'
NEURAL='<svg viewBox="0 0 860 290" role="img" aria-label="A neural network: input nodes connect through hidden layers to an output">\n  <g stroke="var(--line)" stroke-width="1.2">\n    <line x1="140" y1="70"  x2="330" y2="60"/><line x1="140" y1="70"  x2="330" y2="140"/><line x1="140" y1="70"  x2="330" y2="220"/>\n    <line x1="140" y1="145" x2="330" y2="60"/><line x1="140" y1="145" x2="330" y2="140"/><line x1="140" y1="145" x2="330" y2="220"/>\n    <line x1="140" y1="220" x2="330" y2="60"/><line x1="140" y1="220" x2="330" y2="140"/><line x1="140" y1="220" x2="330" y2="220"/>\n    <line x1="330" y1="60"  x2="520" y2="100"/><line x1="330" y1="60"  x2="520" y2="185"/>\n    <line x1="330" y1="140" x2="520" y2="100"/><line x1="330" y1="140" x2="520" y2="185"/>\n    <line x1="330" y1="220" x2="520" y2="100"/><line x1="330" y1="220" x2="520" y2="185"/>\n    <line x1="520" y1="100" x2="690" y2="145"/><line x1="520" y1="185" x2="690" y2="145"/>\n  </g>\n\n  <g fill="var(--teal)">\n    <circle cx="140" cy="70" r="15"/><circle cx="140" cy="145" r="15"/><circle cx="140" cy="220" r="15"/>\n  </g>\n  <g fill="var(--teal)" opacity=".62">\n    <circle cx="330" cy="60" r="15"/><circle cx="330" cy="140" r="15"/><circle cx="330" cy="220" r="15"/>\n    <circle cx="520" cy="100" r="15"/><circle cx="520" cy="185" r="15"/>\n  </g>\n  <circle cx="690" cy="145" r="18" fill="var(--gold)"/>\n\n  <text x="140" y="264" text-anchor="middle" font-size="12" font-weight="600" fill="var(--ink)">what goes in</text>\n  <text x="140" y="281" text-anchor="middle" font-size="10.5" fill="var(--soft)">the photo</text>\n  <text x="425" y="264" text-anchor="middle" font-size="12" font-weight="600" fill="var(--ink)">many simple parts, connected</text>\n  <text x="425" y="281" text-anchor="middle" font-size="10.5" fill="var(--soft)">each one passes a small judgment along</text>\n  <text x="690" y="264" text-anchor="middle" font-size="12" font-weight="600" fill="var(--ink)">the judgment</text>\n  <text x="690" y="281" text-anchor="middle" font-size="10.5" fill="var(--soft)">&#8220;that is a cat&#8221;</text>\n\n  <text x="30" y="26" font-size="12.5" font-weight="600" fill="var(--soft)">modelled on the nerve cells of the brain &#8212; no single part is clever</text>\n</svg>'
GEN='<svg viewBox="0 0 880 250" role="img" aria-label="Classifying picks a label from a list; generating produces something new">\n  <text x="30" y="24" font-size="13" font-weight="600" fill="var(--teal)">Classify &#8212; choose from what exists</text>\n  <rect x="30" y="38" width="118" height="52" rx="6" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>\n  <text x="89" y="70" text-anchor="middle" font-size="11.5" fill="var(--ink)">an email</text>\n  <line x1="154" y1="64" x2="206" y2="64" stroke="var(--teal)" stroke-width="2"/>\n  <polygon points="206,64 198,59 198,69" fill="var(--teal)"/>\n  <rect x="212" y="38" width="150" height="52" rx="6" fill="none" stroke="var(--teal)" stroke-width="2"/>\n  <text x="287" y="62" text-anchor="middle" font-size="11.5" fill="var(--ink)">spam</text>\n  <text x="287" y="80" text-anchor="middle" font-size="11.5" fill="var(--soft)">or not spam</text>\n  <text x="380" y="68" font-size="11" fill="var(--soft)">one of two answers, both already known</text>\n\n  <line x1="30" y1="120" x2="850" y2="120" stroke="var(--line)" stroke-width="1.5" stroke-dasharray="5 5"/>\n\n  <text x="30" y="154" font-size="13" font-weight="600" fill="#8A6420">Generate &#8212; make something that was not there</text>\n  <rect x="30" y="168" width="118" height="52" rx="6" fill="var(--gold)" opacity=".18" stroke="var(--gold)" stroke-width="2"/>\n  <text x="89" y="200" text-anchor="middle" font-size="11.5" fill="var(--ink)">a prompt</text>\n  <line x1="154" y1="194" x2="206" y2="194" stroke="var(--gold)" stroke-width="2"/>\n  <polygon points="206,194 198,189 198,199" fill="var(--gold)"/>\n  <rect x="212" y="168" width="150" height="52" rx="6" fill="var(--gold)" opacity=".28" stroke="var(--gold)" stroke-width="2.5"/>\n  <text x="287" y="192" text-anchor="middle" font-size="11.5" font-weight="600" fill="var(--ink)">a new paragraph</text>\n  <text x="287" y="210" text-anchor="middle" font-size="11.5" fill="var(--soft)">nobody wrote before</text>\n  <text x="380" y="198" font-size="11" fill="var(--soft)">not picked from a list &#8212; produced</text>\n</svg>'
RECSYS='<svg viewBox="0 0 900 250" role="img" aria-label="A recommendation system reads past behaviour, finds a pattern, and suggests something new">\n  <text x="30" y="24" font-size="12.5" font-weight="600" fill="var(--soft)">Nobody told it you like this. It read what you did before.</text>\n\n  <rect x="30" y="52" width="180" height="118" rx="9" fill="var(--teal)" opacity=".12" stroke="var(--teal)" stroke-width="2"/>\n  <text x="120" y="78" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">what you did before</text>\n  <text x="120" y="102" text-anchor="middle" font-size="11" fill="var(--soft)">videos watched</text>\n  <text x="120" y="122" text-anchor="middle" font-size="11" fill="var(--soft)">things bought</text>\n  <text x="120" y="142" text-anchor="middle" font-size="11" fill="var(--soft)">songs skipped</text>\n\n  <line x1="216" y1="111" x2="276" y2="111" stroke="var(--teal)" stroke-width="2"/>\n  <polygon points="276,111 268,106 268,116" fill="var(--teal)"/>\n\n  <rect x="282" y="52" width="200" height="118" rx="9" fill="var(--teal)" opacity=".22" stroke="var(--teal)" stroke-width="2.5">\n    <animate attributeName="opacity" values=".22;.42;.22" dur="3.4s" repeatCount="indefinite"/>\n  </rect>\n  <text x="382" y="86" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">it finds a pattern</text>\n  <text x="382" y="110" text-anchor="middle" font-size="11" fill="var(--soft)">people who liked these</text>\n  <text x="382" y="130" text-anchor="middle" font-size="11" fill="var(--soft)">also liked that</text>\n\n  <line x1="488" y1="111" x2="548" y2="111" stroke="var(--teal)" stroke-width="2"/>\n  <polygon points="548,111 540,106 540,116" fill="var(--teal)"/>\n\n  <rect x="554" y="52" width="200" height="118" rx="9" fill="var(--gold)" opacity=".24" stroke="var(--gold)" stroke-width="2.5">\n    <animate attributeName="opacity" values=".24;.46;.24" dur="3.4s" begin="1.2s" repeatCount="indefinite"/>\n  </rect>\n  <text x="654" y="96" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">&#8220;watch this next&#8221;</text>\n  <text x="654" y="120" text-anchor="middle" font-size="11" fill="var(--soft)">a prediction, not a fact</text>\n\n  <text x="30" y="208" font-size="11.5" fill="var(--soft)">This is machine learning from Part 2, doing a job you meet every day.</text>\n  <text x="30" y="228" font-size="11.5" fill="#9C3B2E">It works because it holds your behaviour &#8212; which is the privacy question.</text>\n</svg>'
BLACKBOX='<svg viewBox="0 0 900 240" role="img" aria-label="The black-box problem: the input and the answer are visible but the reasoning inside is not">\n  <text x="30" y="24" font-size="12.5" font-weight="600" fill="var(--soft)">You can see what went in and what came out. You cannot see why.</text>\n\n  <rect x="30" y="58" width="150" height="90" rx="8" fill="var(--teal)" opacity=".14" stroke="var(--teal)" stroke-width="2"/>\n  <text x="105" y="98" text-anchor="middle" font-size="12" fill="var(--ink)">an X-ray</text>\n  <text x="105" y="120" text-anchor="middle" font-size="11" fill="var(--soft)">you can see this</text>\n\n  <line x1="186" y1="103" x2="244" y2="103" stroke="var(--teal)" stroke-width="2"/>\n  <polygon points="244,103 236,98 236,108" fill="var(--teal)"/>\n\n  <rect x="250" y="44" width="260" height="118" rx="10" fill="var(--ink)" opacity=".88"/>\n  <text x="380" y="92" text-anchor="middle" font-size="15" font-weight="600" fill="#fff">?</text>\n  <text x="380" y="118" text-anchor="middle" font-size="12" fill="#C6CCD9">why it decided that</text>\n  <text x="380" y="138" text-anchor="middle" font-size="11" fill="#8A93A6">not visible, even to its builders</text>\n  <rect x="250" y="44" width="260" height="118" rx="10" fill="none" stroke="#9C3B2E" stroke-width="2.5" stroke-dasharray="7 5">\n    <animate attributeName="opacity" values="1;.3;1" dur="2.2s" repeatCount="indefinite"/>\n  </rect>\n\n  <line x1="516" y1="103" x2="574" y2="103" stroke="var(--teal)" stroke-width="2"/>\n  <polygon points="574,103 566,98 566,108" fill="var(--teal)"/>\n\n  <rect x="580" y="58" width="180" height="90" rx="8" fill="var(--gold)" opacity=".24" stroke="var(--gold)" stroke-width="2"/>\n  <text x="670" y="92" text-anchor="middle" font-size="12.5" font-weight="600" fill="var(--ink)">&#8220;likely disease&#8221;</text>\n  <text x="670" y="116" text-anchor="middle" font-size="11" fill="var(--soft)">you can see this too</text>\n\n  <text x="30" y="204" font-size="11.5" fill="var(--ink)">That gap is the <tspan font-weight="600">black-box problem</tspan> &#8212; and it is why a doctor still signs the diagnosis.</text>\n</svg>'
def dg(x):return '<div class="dg">'+x+'</div>'

def page(x):return '<section class="sheet">'+x+foot()+'</section>'
def masthead(sub):return '<div class="brand" id="brand">Programming &amp; Artificial Intelligence</div><h1 id="docTitle">How does it learn?</h1><div class="docsub">'+sub+' &middot; Lecture 3</div><div class="namebox"><div><span>Name</span><i></i></div><div><span>Class</span><i></i></div><div><span>Date</span><i></i></div></div>'
def rules(n=2):return ''.join('<div class="rule tight"></div>' for _ in range(n))
def mcq(t):
 """A question whose options are written inline as "A: ... B: ... " reads as a
 wall of text on paper. Put each option on its own line."""
 import re as _re
 parts=_re.split(r'\s(?=[A-D]:\s)', esc(t))
 if len(parts)<3:return esc(t)
 return parts[0]+''.join('<span class="opt">'+x+'</span>' for x in parts[1:])

def exercise(n,num=None):
 x=EX[n];num=n if num is None else num;typ=x['type'];body=rules(3)
 if typ=='truefalse':body='<table class="tftbl"><tr><th>✓ / ✕</th><th>Statement</th></tr>'+''.join('<tr><td class="blank"></td><td>'+esc(a)+'</td></tr>' for a in x['statements'])+'</table>'
 elif typ=='match':
  # the options carry letters, so there is something definite to write in the
  # blank; the data keeps them out of step with the descriptions
  opts=''.join('<span class="chip"><b>'+chr(65+i)+'</b> '+esc(a)+'</span>' for i,a in enumerate(x['right']))
  body=('<table class="matchtbl"><tr><th>Description</th><th style="width:18%">Letter</th></tr>'
        +''.join('<tr><td>'+esc(a)+'</td><td class="blank"></td></tr>' for a in x['left'])
        +'</table><p class="optlead">Choose from:</p><div class="fields">'+opts+'</div>')
 elif typ=='table':body='<table><tr>'+''.join('<th>'+esc(a)+'</th>' for a in x['head'])+'</tr>'+''.join('<tr>'+''.join('<td>'+esc(a)+'</td>' for a in r)+'</tr>' for r in x['rows'])+'</table>'
 elif typ=='sort':body='<div class="fields">'+''.join('<span class="chip">'+esc(a)+'</span>' for a in x['items'])+'</div><table><tr>'+''.join('<th>'+esc(a)+'</th>' for a in x['columns'])+'</tr><tr>'+''.join('<td class="blank" style="height:25mm"></td>' for a in x['columns'])+'</tr></table>'
 elif typ=='category':body='<table class="cattbl">'+''.join('<tr><td class="blank"></td><td>'+esc(a)+'</td></tr>' for a in x['items'])+'</table>'
 elif typ=='fill':
  # one labelled line per blank, so the student can see which answer goes where
  ls=[c for c in 'abcdef' if '( '+c+' )' in x['passage']]
  body=('<p class="passage">'+esc(x['passage'])+'</p><ol class="blanks">'
        +''.join('<li><b>( '+c+' )</b><span class="rule tight"></span></li>' for c in ls)
        +'</ol>')
 elif typ=='short':
  # Without this branch a short-answer exercise fell through to the
  # default and printed blank lines with no question on them at all.
  qs=x.get('questions')
  if qs:
   body='<ol class="qs">'+''.join(
     '<li>'+mcq(q['q'])
     +(('<span class="srcinline">'+esc(q['src'])+'</span>') if q.get('src') else '')
     +rules(q.get('lines',1))+'</li>' for q in qs)+'</ol>'
  else:
   body=rules(3)
 elif typ=='extended':body='<div class="marks">['+str(x.get('marks',6))+' marks]</div>'+rules(x.get('lines',7))
 return '<div class="ex"><div class="exhead"><span class="exn">'+str(num)+'</span><span class="exq">'+esc(x['prompt'])+'</span></div><p class="ar">'+esc(x['promptAr'])+'</p><div class="src">'+esc(x['src'])+'</div>'+body+'</div>'
def term(h,p,ar):return '<div class="term"><h4>'+h+'</h4><p>'+p+'</p><p class="ar">'+ar+'</p></div>'
def lastpage(kind):
 """Closing sheet, with no QR and no quiz address on it.

 The exam is meant to be taken in the lesson, not at home the night before
 with an AI to hand, so nothing a student carries home carries the link.
 The code is on the deck, which the teacher projects when it is time."""
 if kind=='booklet':
  head=('<h2>What to revise</h2><div class="summary">'
        '<p>Go back over the nested layers first &mdash; AI, machine learning, deep '
        'learning, generative AI &mdash; then the key terms, then what AI is good at '
        'and what needs caution.</p>'
        '<p class="ar">راجع الطبقات الأول: AI ثم machine learning ثم deep learning ثم '
        'generative AI، وبعدين المصطلحات، وبعدين الـ AI شاطر في إيه ومحتاج حذر في إيه.</p></div>')
 else:
  head=('<h2>Before you hand this in</h2><div class="summary">'
        '<p>Check every answer against the booklet. Bring anything you could not '
        'work out to the next session.</p>'
        '<p class="ar">راجع كل إجابة على الكتيّب. وأي حاجة معرفتش تحلها هاتها معاك المرة الجاية.</p></div>')
 notes='<h2>My notes</h2>'+''.join('<div class="rule"></div>' for _ in range(8))
 exam=('<div class="summary hw"><p><b>The exam is done in class.</b> Your teacher will '
       'show the code to scan during the lesson.</p>'
       '<p class="ar">الامتحان بيتحل في الحصة. المدرّس هيعرض الكود تمسحوه وقتها.</p></div>')
 return page(head+exam+notes)

def booklet(head,tail,qr):
 p=[]
 p.append(page(masthead('Student Booklet')+'<h2>What is AI?</h2><p class="lead">AI is a general term for technologies that reproduce or perform intelligent human behavior on a computer.</p><p class="ar">AI ده اسم واسع لتقنيات بتعمل سلوك ذكي على الكمبيوتر.</p><table><tr><th>Everyday example</th><th>What it does</th></tr><tr><td>Speech recognition</td><td>Recognises speech</td></tr><tr><td>Image recognition</td><td>Recognises images</td></tr><tr><td>Translation</td><td>Changes one language into another</td></tr></table><div class="summary"><p><b>Important:</b> today’s AI is narrow — expert at one task only.</p><p class="ar">خلي بالك: AI النهارده شاطر في مهمة محددة، مش فاهم كل حاجة زي الإنسان.</p></div>'))
 p.append(page('<h2>The spine of the lesson</h2>'+dg(NESTED)+'<p>The technologies are nested categories, becoming more specialised at each layer.</p><p class="ar">دي دوائر جوه بعض، كل دايرة أضيق وأكتر تحديدًا.</p><table><tr><th>Layer</th><th>What it does</th></tr><tr><td class="k">AI</td><td>Broad term for intelligent behavior on a computer</td></tr><tr><td class="k">Machine learning</td><td>Learns patterns from data</td></tr><tr><td class="k">Deep learning</td><td>Uses neural networks and large-scale data</td></tr><tr><td class="k">Generative AI</td><td>Uses deep learning to generate new data</td></tr></table><p class="ar">احفظ الترتيب ده؛ هو أساس كل أسئلة الدرس.</p>'))
 p.append(page('<h2>Machine learning</h2>'+dg(RULES)+''+term('Machine learning','A learning technology that makes AI work: it learns patterns from data to make predictions and judgments.','بدل ما نكتب rules بإيدنا، بيتعلم pattern من أمثلة.')+'<div class="stages"><div class="stage"><div class="n">1</div><h4>Data</h4><p>Examples are provided.</p></div><div class="stage"><div class="n">2</div><h4>Pattern</h4><p>The system learns a pattern.</p></div><div class="stage"><div class="n">3</div><h4>Judgment</h4><p>It makes a prediction or judgment.</p></div></div><p>Examples: spam filters and product recommendations.</p><p class="ar">spam filter و product recommendation مهمتين مختلفتين، لكن الاتنين بيتعلموا من data.</p>'))
 p.append(page('<h2>Deep learning and neural networks</h2>'+dg(NEURAL)+''+term('Deep learning','An advanced technology within machine learning that uses neural networks and large-scale data to learn complex patterns.','Deep learning نوع متقدم جوه machine learning وبيحتاج بيانات كتير.')+term('Neural network','A system modeled after the workings of the nerve cells of the human brain. Connected components learn from data and make complex judgments.','الـ neural network متصممة على فكرة خلايا المخ، بس هي نظام على الكمبيوتر.')+'<div class="summary"><p><b>Pause and think.</b> If an AI has rarely seen something in its data, why might it struggle to judge it?</p><p class="ar">لو الحاجة نادرة في data، غالبًا الـ AI مش هيكون اتعلم نمطها كويس.</p></div>'))
 p.append(page('<h2>Generative AI</h2>'+dg(GEN)+''+term('Generative AI','AI technology that uses deep learning to generate new data: text, images, audio and programs.','كلمة generate معناها يطلع حاجة جديدة: text أو image أو صوت.')+'<table><tr><th>Classify / predict</th><th>Generate</th></tr><tr><td>Spam filter sorts email</td><td>ChatGPT generates text</td></tr><tr><td>Product recommendation predicts an interest</td><td>Image AI generates an image</td></tr></table><p class="ar">دي أكتر حاجة الطلبة بيلخبطوا فيها: spam filter بيصنّف، مش generative AI.</p>'+'<h2>Exam warning: fluent is not always correct</h2><div class="summary"><p>Generative AI can produce text that sounds plausible but is factually incorrect: a <b>hallucination</b>.</p><p class="ar">لو الكلام شكله مقنع مش معناه إنه صح؛ ده ممكن يكون hallucination.</p></div><p>Do not use output as the answer to a school report as-is. Check it first.</p><p class="ar">استخدمه يساعدك، بس راجع المعلومة قبل ما تحطها في report.</p><h2>Key takeaway</h2><div class="summary"><p>AI is the broad field; machine learning sits inside it; deep learning sits inside machine learning; generative AI is built on deep learning.</p><p class="ar">الخلاصة: AI ثم machine learning ثم deep learning ثم generative AI.</p></div>'))
 # ---- lesson 1-3: where you meet it ----
 p.append(page('<h2>AI in daily life</h2>'+dg(RECSYS)+'<table><tr><th>Service</th><th>What the AI does</th><th>Examples</th></tr><tr><td class="k">Recommendation system</td><td>Predicts your preferences from past behaviour and shows suggestions</td><td>YouTube, Amazon, Spotify</td></tr><tr><td class="k">Voice assistant</td><td>Recognises a voice, understands the command, carries it out</td><td>Siri, Google Assistant</td></tr><tr><td class="k">Machine translation</td><td>Turns text automatically into another language</td><td>Google Translate, DeepL</td></tr><tr><td class="k">Face recognition</td><td>Detects and identifies faces in photographs</td><td>Unlocking a phone</td></tr></table><p class="ar">الأربعة دول من الكتاب بالحرف وبيتسألوا كسؤال مطابقة.</p>'))
 p.append(page('<h2>AI in industry</h2>'+'<table><tr><th>Industry</th><th>How AI is used</th></tr><tr><td class="k">Healthcare</td><td>Image-diagnosis AI reads X-ray and CT images; drug-discovery support</td></tr><tr><td class="k">Agriculture</td><td>Predicting harvest timing; detecting pests and diseases</td></tr><tr><td class="k">Manufacturing</td><td>Automatic quality inspection; predictive maintenance</td></tr><tr><td class="k">Logistics</td><td>Optimising delivery routes</td></tr></table>'+term('Predictive maintenance','Predicting that a machine will fail before it does, so it can be serviced in time.','يتوقّع إن الماكينة هتعطل قبل ما تعطل فعلاً، عشان تتصلح في وقتها.')+'<div class="summary"><p><b>Pause and think.</b> These services hold what you watch, buy and say. Why is that a privacy problem, and who should decide how your data is used?</p><p class="ar">الخدمات دي شايلة بياناتك. ليه دي مشكلة خصوصية، ومين يقرر تتستخدم إزاي؟</p></div>'))
 p.append(page('<h2>What AI is good at, and what needs caution</h2>'+'<table><tr><th>Good at</th><th>Needs caution</th></tr><tr><td>Finding and classifying patterns in complex data</td><td>Ethical judgments — can carry discrimination or prejudice</td></tr><tr><td>Recognition and generation of images, audio and text</td><td>Anything involving personal data and privacy</td></tr><tr><td>Probabilistic reasoning and prediction from data</td><td>Final decision-making — who is responsible?</td></tr><tr><td></td><td>Biased training data makes judgments inaccurate</td></tr><tr><td></td><td>Hallucination, and the black-box problem</td></tr></table>'+dg(BLACKBOX)+'<p class="ar">العمود الشمال بييجي سؤال اختر اللي الـ AI شاطر فيه، واليمين اختر اللي مش من دواعي الحذر. ذاكرهم مقابل بعض.</p>'))
 # two pages rather than one: four exercises overflowed a single sheet
 p.append(page('<h2>Class work &middot; how AI works</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
               +exercise(1,1)+exercise(2,2)))
 p.append(page('<h2>Class work &middot; where you meet it</h2><p class="ar">الجزء التاني — كمّل مع زميلك.</p>'
               +exercise(18,3)+exercise(19,4)))
 return head+''.join(p)+lastpage('booklet')+tail
def homework(head,tail,qr):
 p=[]
 # Grouped, not one per sheet: nine exercises on nine near-empty pages is a
 # waste of paper. Verified by rendering that each group fits one A4 page.
 first=True
 for title,titleAr,pages in HW_SECTIONS:
  for j,group in enumerate(pages):
   intro=''
   if first:
    intro=(masthead('Homework')+'<div class="summary hw"><p>Everything here was taught in the session. Bring this sheet to the next class.</p><p class="ar">كل ده اتشرح في الحصة. هات الورقة المرة الجاية.</p></div>')
    first=False
   if j==0:
    intro+='<h2>'+title+'</h2><p class="ar">'+titleAr+'</p>'
   else:
    intro+='<h2>Homework</h2><p class="ar">كمّل بهدوء وراجع الكتيّب لو احتجت.</p>'
   p.append(page(intro+''.join(exercise(n,HOMEWORK.index(n)+1) for n in group)))
 return head+''.join(p)+lastpage('homework')+tail
def answer_html(n):
 """Render one answer readably. The data carries different shapes -- a list of
 lines, a model answer with a marking scheme, a set of lettered blanks -- and
 printing str() of the dict put raw Python in the teacher's hand."""
 a=DATA['ANSWERS'].get(str(n))
 out=[]
 if isinstance(a,list):
  out.append('<ul>'+''.join('<li>'+esc(str(x))+'</li>' for x in a)+'</ul>')
 elif isinstance(a,dict):
  if a.get('marks'):out.append('<div class="marks">['+str(a['marks'])+' marks]</div>')
  if a.get('open'):out.append('<p class="note">Open response &mdash; any reasonable answer, marked on the points below.</p>')
  if a.get('model'):out.append('<p><b>Model answer.</b> '+esc(a['model'])+'</p>')
  if a.get('points'):
   out.append('<p><b>The answer must cover:</b></p><ul>'+''.join('<li>'+esc(x)+'</li>' for x in a['points'])+'</ul>')
  if a.get('example'):out.append('<p><b>Example of a good answer.</b> '+esc(a['example'])+'</p>')
  rest=[(k,v) for k,v in a.items() if k not in ('note','src','marks','open','model','points','example','marking')]
  if rest:
   out.append('<ul>'+''.join('<li><b>'+esc(k)+'</b> &mdash; '+esc(', '.join(v) if isinstance(v,list) else str(v))+'</li>' for k,v in rest)+'</ul>')
  if a.get('marking'):out.append('<p class="note"><b>Marking.</b> '+esc(a['marking'])+'</p>')
  if a.get('note'):out.append('<p class="note">'+esc(a['note'])+'</p>')
  if a.get('src'):out.append('<div class="src">'+esc(a['src'])+'</div>')
 elif a is not None:
  out.append('<p>'+esc(str(a))+'</p>')
 else:
  out.append('<p class="note">Open response &mdash; mark on the points named in the question.</p>')
 return ''.join(out)

def key(head,tail):
 """Teacher copy. Numbers match what the student sees: class work is numbered
 1.. on its sheets, homework 1.. on its own, so 'homework 7' means the same
 thing to both of them."""
 b=[masthead('Teacher Answer Key'),
    '<div class="teacherwarn">Teacher copy &mdash; do not hand this to students.</div>']
 for label,nums in (('Class work &mdash; done in the session',IN_CLASS),
                    ('Homework &mdash; separate sheet',HOMEWORK)):
  b.append('<div class="keygroup">'+label+'</div>')
  for i,n in enumerate(nums,1):
   b.append('<div class="ex"><div class="exhead"><span class="exn">'+str(i)+'</span>'
            '<span class="exq">'+esc(EX[n]['prompt'])+'</span></div>')
   if EX[n].get('src'):b.append('<div class="src">'+esc(EX[n]['src'])+'</div>')
   b.append('<div class="key">'+answer_html(n)+'</div></div>')
 return head+'<section class="sheet keysheet">'+''.join(b)+foot()+'</section>'+tail
head,tail,qr=shell()
for path,html in [(ROOT/'lecture3/handout/index.html',booklet(head,tail,qr)),(ROOT/'lecture3/homework/index.html',homework(head,tail,qr)),(ROOT/'lecture3/_teacher/answer-key.html',key(head,tail))]:
 # the template ships author instructions in HTML comments; they are not ours
 # to publish, and lecture2's generated pages carry none.
 html=re.sub(r'<!--.*?-->','',html,flags=re.DOTALL)
 with io.open(path,'w',encoding='utf-8',newline='\n') as f:f.write(html)
 print(path.relative_to(ROOT))
