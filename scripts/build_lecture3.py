#!/usr/bin/env python3
"""Generate Lecture 3 printed material from the shared A4 template and exercise data."""
import io,json,re
from html import escape as esc
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'lecture3/_teacher/exercises.json').read_text(encoding='utf-8'))
EX={x['n']:x for x in DATA['SHEET']['parts'][0]['exercises']}
IN_CLASS=[1,2,3,4]
HOMEWORK=[5,6,7,8,9,10,11,12,13]
EXTRA_CSS='''
.namebox{display:flex;gap:5mm;margin:0 0 6mm}.namebox>div{flex:1;display:flex;align-items:flex-end;gap:2mm}.namebox span{font-size:9pt;color:var(--soft);font-weight:600}.namebox i{flex:1;border-bottom:1px solid var(--rule);height:6mm}.ex{margin:0 0 5mm;break-inside:avoid}.exhead{display:flex;gap:3mm;align-items:baseline;margin-bottom:1.5mm}.exn{flex:0 0 auto;width:6.5mm;height:6.5mm;border-radius:50%;background:var(--teal);color:#fff;font-size:9pt;font-weight:600;display:flex;align-items:center;justify-content:center}.exq{font-size:10.5pt;font-weight:600}.src{font-size:8pt;color:var(--soft);font-style:italic;margin:0 0 1.5mm 9.5mm}.passage{font-size:10pt;line-height:1.8;background:#FCFCFA;border:1px solid var(--line);padding:3mm}.marks{font-size:9pt;font-weight:600;color:var(--gold);margin:2mm 0}.key{margin-left:9.5mm;font-size:10pt}.teacherwarn{background:#FBF0EE;border-left:3px solid #9C3B2E;padding:3mm}.summary.hw{background:var(--teal-pale)}'''
def shell():
 t=(ROOT/'templates/handout-template.html').read_text(encoding='utf-8').replace('</style>',EXTRA_CSS+'</style>',1)
 t=t.replace('__LECTURE_NUM__','3').replace('__TITLE_HTML__','How does it learn?').replace('__TITLE_JS__','How does it learn?').replace('__TOPIC_HTML__','Programming &amp; Artificial Intelligence').replace('__TOPIC_JS__','Programming & Artificial Intelligence').replace('__ACCENT__','#1D6FA5')
 head=t[:t.index('<div id="pagesTop"></div>')+len('<div id="pagesTop"></div>')];tail=t[t.index('<script>'):]
 qr=re.search(r'<section class="sheet">.*?id="qr".*?</section>',t,re.S).group(0)
 return head,tail,qr
def foot():return '<div class="foot"><span>Prepared by: Mr. Eissa Islam</span><span class="pageno"></span></div>'
def page(x):return '<section class="sheet">'+x+foot()+'</section>'
def masthead(sub):return '<div class="brand" id="brand">Programming &amp; Artificial Intelligence</div><h1 id="docTitle">How does it learn?</h1><div class="docsub">'+sub+' &middot; Lecture 3</div><div class="namebox"><div><span>Name</span><i></i></div><div><span>Class</span><i></i></div><div><span>Date</span><i></i></div></div>'
def rules(n=2):return ''.join('<div class="rule tight"></div>' for _ in range(n))
def exercise(n):
 x=EX[n];typ=x['type'];body=rules(3)
 if typ=='truefalse':body='<table class="tftbl"><tr><th>✓ / ✕</th><th>Statement</th></tr>'+''.join('<tr><td class="blank"></td><td>'+esc(a)+'</td></tr>' for a in x['statements'])+'</table>'
 elif typ=='match':body='<table class="matchtbl">'+''.join('<tr><td>'+esc(a)+'</td><td class="blank"></td></tr>' for a in x['left'])+'</table><p>Options: '+', '.join(esc(a) for a in x['right'])+'</p>'
 elif typ=='table':body='<table><tr>'+''.join('<th>'+esc(a)+'</th>' for a in x['head'])+'</tr>'+''.join('<tr>'+''.join('<td>'+esc(a)+'</td>' for a in r)+'</tr>' for r in x['rows'])+'</table>'
 elif typ=='sort':body='<div class="fields">'+''.join('<span class="chip">'+esc(a)+'</span>' for a in x['items'])+'</div><table><tr>'+''.join('<th>'+esc(a)+'</th>' for a in x['columns'])+'</tr><tr>'+''.join('<td class="blank" style="height:25mm"></td>' for a in x['columns'])+'</tr></table>'
 elif typ=='category':body='<table class="cattbl">'+''.join('<tr><td class="blank"></td><td>'+esc(a)+'</td></tr>' for a in x['items'])+'</table>'
 elif typ=='fill':body='<p class="passage">'+esc(x['passage'])+'</p>'+rules(4)
 elif typ=='extended':body='<div class="marks">['+str(x.get('marks',6))+' marks]</div>'+rules(x.get('lines',7))
 return '<div class="ex"><div class="exhead"><span class="exn">'+str(n)+'</span><span class="exq">'+esc(x['prompt'])+'</span></div><p class="ar">'+esc(x['promptAr'])+'</p><div class="src">'+esc(x['src'])+'</div>'+body+'</div>'
def term(h,p,ar):return '<div class="term"><h4>'+h+'</h4><p>'+p+'</p><p class="ar">'+ar+'</p></div>'
def booklet(head,tail,qr):
 p=[]
 p.append(page(masthead('Student Booklet')+'<h2>What is AI?</h2><p class="lead">AI is a general term for technologies that reproduce or perform intelligent human behavior on a computer.</p><p class="ar">AI ده اسم واسع لتقنيات بتعمل سلوك ذكي على الكمبيوتر.</p><table><tr><th>Everyday example</th><th>What it does</th></tr><tr><td>Speech recognition</td><td>Recognises speech</td></tr><tr><td>Image recognition</td><td>Recognises images</td></tr><tr><td>Translation</td><td>Changes one language into another</td></tr></table><div class="summary"><p><b>Important:</b> today’s AI is narrow — expert at one task only.</p><p class="ar">خلي بالك: AI النهارده شاطر في مهمة محددة، مش فاهم كل حاجة زي الإنسان.</p></div>'))
 p.append(page('<h2>The spine of the lesson</h2><p>The technologies are nested categories, becoming more specialised at each layer.</p><p class="ar">دي دوائر جوه بعض، كل دايرة أضيق وأكتر تحديدًا.</p><table><tr><th>Layer</th><th>What it does</th></tr><tr><td class="k">AI</td><td>Broad term for intelligent behavior on a computer</td></tr><tr><td class="k">Machine learning</td><td>Learns patterns from data</td></tr><tr><td class="k">Deep learning</td><td>Uses neural networks and large-scale data</td></tr><tr><td class="k">Generative AI</td><td>Uses deep learning to generate new data</td></tr></table><p class="ar">احفظ الترتيب ده؛ هو أساس كل أسئلة الدرس.</p>'))
 p.append(page('<h2>Machine learning</h2>'+term('Machine learning','A learning technology that makes AI work: it learns patterns from data to make predictions and judgments.','بدل ما نكتب rules بإيدنا، بيتعلم pattern من أمثلة.')+'<div class="stages"><div class="stage"><div class="n">1</div><h4>Data</h4><p>Examples are provided.</p></div><div class="stage"><div class="n">2</div><h4>Pattern</h4><p>The system learns a pattern.</p></div><div class="stage"><div class="n">3</div><h4>Judgment</h4><p>It makes a prediction or judgment.</p></div></div><p>Examples: spam filters and product recommendations.</p><p class="ar">spam filter و product recommendation مهمتين مختلفتين، لكن الاتنين بيتعلموا من data.</p>'))
 p.append(page('<h2>Deep learning and neural networks</h2>'+term('Deep learning','An advanced technology within machine learning that uses neural networks and large-scale data to learn complex patterns.','Deep learning نوع متقدم جوه machine learning وبيحتاج بيانات كتير.')+term('Neural network','A system modeled after the workings of the nerve cells of the human brain. Connected components learn from data and make complex judgments.','الـ neural network متصممة على فكرة خلايا المخ، بس هي نظام على الكمبيوتر.')+'<div class="summary"><p><b>Pause and think.</b> If an AI has rarely seen something in its data, why might it struggle to judge it?</p><p class="ar">لو الحاجة نادرة في data، غالبًا الـ AI مش هيكون اتعلم نمطها كويس.</p></div>'))
 p.append(page('<h2>Generative AI</h2>'+term('Generative AI','AI technology that uses deep learning to generate new data: text, images, audio and programs.','كلمة generate معناها يطلع حاجة جديدة: text أو image أو صوت.')+'<table><tr><th>Classify / predict</th><th>Generate</th></tr><tr><td>Spam filter sorts email</td><td>ChatGPT generates text</td></tr><tr><td>Product recommendation predicts an interest</td><td>Image AI generates an image</td></tr></table><p class="ar">دي أكتر حاجة الطلبة بيلخبطوا فيها: spam filter بيصنّف، مش generative AI.</p>'))
 p.append(page('<h2>Exam warning: fluent is not always correct</h2><div class="summary"><p>Generative AI can produce text that sounds plausible but is factually incorrect: a <b>hallucination</b>.</p><p class="ar">لو الكلام شكله مقنع مش معناه إنه صح؛ ده ممكن يكون hallucination.</p></div><p>Do not use output as the answer to a school report as-is. Check it first.</p><p class="ar">استخدمه يساعدك، بس راجع المعلومة قبل ما تحطها في report.</p><h2>Key takeaway</h2><div class="summary"><p>AI is the broad field; machine learning sits inside it; deep learning sits inside machine learning; generative AI is built on deep learning.</p><p class="ar">الخلاصة: AI ثم machine learning ثم deep learning ثم generative AI.</p></div>'))
 p += [page('<h2>Class work · Part A</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'+exercise(1)+exercise(2)),page('<h2>Class work · Part B</h2><p class="ar">كمّل مع زميلك وبص على الكلمات المفتاح.</p>'+exercise(3)+exercise(4))]
 panel=qr.replace('<h2>Session Summary</h2>','<h2>Test yourself online</h2>').replace('<h2>My Notes</h2>','<h2>My notes</h2>').replace('Three or four one-line takeaways from the session.','Scan the code to open the Lecture 3 quiz.').replace('One per line, in the order they were taught.','Review the nested layers and key terms first.').replace('Explain the first idea here.','').replace('A term worth its own block','').replace('First Section','').replace('Second Section','').replace('First question?','').replace('Second question?','').replace('First term','').replace('Second term','').replace('Its definition','').replace('My answer','').replace('الشرح بالعربي','').replace('سطر المقدمة بالعربي','')
 return head+''.join(p)+panel+tail
def homework(head,tail,qr):
 p=[]
 for i,n in enumerate(HOMEWORK):p.append(page((masthead('Homework')+'<div class="summary hw"><p>Everything here was taught in the session. Bring this sheet to the next class.</p><p class="ar">كل ده اتشرح في الحصة. هات الورقة المرة الجاية.</p></div>' if i==0 else '<h2>Homework</h2><p class="ar">كمّل بهدوء وراجع الكتيّب لو احتجت.</p>')+exercise(n)))
 panel=qr.replace('<h2>Session Summary</h2>','<h2>Check your work online</h2>').replace('Three or four one-line takeaways from the session.','Use the quiz after completing the homework.').replace('One per line, in the order they were taught.','Bring your questions to the next session.').replace('Explain the first idea here.','').replace('A term worth its own block','').replace('First Section','').replace('Second Section','').replace('First question?','').replace('Second question?','').replace('First term','').replace('Second term','').replace('Its definition','').replace('My answer','').replace('الشرح بالعربي','').replace('سطر المقدمة بالعربي','')
 return head+''.join(p)+panel+tail
def key(head,tail):
 b='<section class="sheet">'+masthead('Teacher Answer Key')+'<div class="teacherwarn">Teacher copy — do not hand this to students.</div>'
 for n in IN_CLASS+HOMEWORK:b+='<div class="ex"><div class="exhead"><span class="exn">'+str(n)+'</span><span class="exq">'+esc(EX[n]['prompt'])+'</span></div><div class="key">'+esc(str(DATA['ANSWERS'][str(n)]))+'</div></div>'
 return head+b+foot()+'</section>'+tail
head,tail,qr=shell()
for path,html in [(ROOT/'lecture3/handout/index.html',booklet(head,tail,qr)),(ROOT/'lecture3/homework/index.html',homework(head,tail,qr)),(ROOT/'lecture3/_teacher/answer-key.html',key(head,tail))]:
 # the template ships author instructions in HTML comments; they are not ours
 # to publish, and lecture2's generated pages carry none.
 html=re.sub(r'<!--.*?-->','',html,flags=re.DOTALL)
 with io.open(path,'w',encoding='utf-8',newline='\n') as f:f.write(html)
 print(path.relative_to(ROOT))
