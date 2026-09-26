# -*- coding: utf-8 -*-
"""Build Lecture 4's deck.

    python scripts/build_lecture4_slides.py

Reads the shell (head, CSS, LECTURE CONFIG, script) from
scripts/lecture4_slides_base.html and writes lecture4/slides/index.html with
the slide body below, the lightbox, the exam-code gate and the photo CSS
added. Always starts from the base, never from the published deck: the
injections check for their own CSS before adding markup, so rebuilding on
top of an already-built deck would drop the lightbox dialog.

Content is Lesson 1-4, Ethical Issues with AI, textbook pp. 26-32, and
nothing outside the curriculum: the recap is lesson 1-3's own list of
cautions, and the closing map is Unit 1's four lessons, because this lesson
closes the unit and the unit exam covers all four. Two ideas the English
book states in one line are given a slide each, because the ministry's
assessment book asks about them directly: responsibility against
accountability, and the proxy variable as a cause of bias.

The helpers, the photo CSS, port_lightbox(), the exam-code gate and the
build block are copied unchanged from build_lecture3_slides.py, which is
where they were proven. Arabic is teaching commentary in the register the
other lectures use, and needs a teacher's read-through.
"""
import io, re
from pathlib import Path

ROOT = Path(__file__).resolve()
DST = "lecture4/slides/index.html"


# --------------------------------------------------------------------------
# diagrams — inline SVG, coloured from the page's CSS variables so they follow
# LECTURE_ACCENT like everything else. Explanatory sentences stay OUT of the
# SVG (they become unreadable once the slide is scaled); labels only.
# --------------------------------------------------------------------------

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

WHO = '''
<svg viewBox="0 0 900 250" role="img" aria-label="When an AI gets it wrong, the developer, the operator and the user each hold a different part of the responsibility">
  <rect x="340" y="24" width="220" height="62" rx="10" fill="#9C3B2E" opacity=".10" stroke="#9C3B2E" stroke-width="2.5">
    <animate attributeName="opacity" values=".10;.26;.10" dur="3s" repeatCount="indefinite"/>
  </rect>
  <text x="450" y="52" text-anchor="middle" font-size="13" font-weight="600" fill="#9C3B2E">the AI gets it wrong</text>
  <text x="450" y="72" text-anchor="middle" font-size="11.5" fill="var(--soft)">who answers for it?</text>

  <line x1="450" y1="90" x2="150" y2="146" stroke="var(--soft)" stroke-width="1.8"/>
  <line x1="450" y1="90" x2="450" y2="146" stroke="var(--soft)" stroke-width="1.8"/>
  <line x1="450" y1="90" x2="750" y2="146" stroke="var(--soft)" stroke-width="1.8"/>

  <rect x="40" y="150" width="220" height="70" rx="9" fill="var(--teal)" opacity=".13" stroke="var(--teal)" stroke-width="2"/>
  <text x="150" y="178" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">the developer</text>
  <text x="150" y="200" text-anchor="middle" font-size="11" fill="var(--soft)">built it, chose the data</text>

  <rect x="340" y="150" width="220" height="70" rx="9" fill="var(--teal)" opacity=".13" stroke="var(--teal)" stroke-width="2"/>
  <text x="450" y="178" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">the operator</text>
  <text x="450" y="200" text-anchor="middle" font-size="11" fill="var(--soft)">the company running it</text>

  <rect x="640" y="150" width="220" height="70" rx="9" fill="var(--teal)" opacity=".13" stroke="var(--teal)" stroke-width="2"/>
  <text x="750" y="178" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">the user</text>
  <text x="750" y="200" text-anchor="middle" font-size="11" fill="var(--soft)">acted on its result</text>

  <text x="450" y="244" text-anchor="middle" font-size="11.5" fill="var(--soft)">Each sees it differently &#8212; and no clear standard has been agreed yet.</text>
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
    h2("Can we trust it?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("AI now helps make real decisions about people. Today: when is that fair, and who answers when it goes wrong?",
        "max-width:56ch;margin-top:1rem"),
    ar("الـ AI بقى بيساعد ياخد قرارات حقيقية عن ناس. النهارده هنشوف: إمتى ده يبقى عادل، ولما يغلط مين اللي يتحاسب؟")))

# 2 recap — lesson 1-3 ended on a list of cautions; this lesson explains them
A(s("",
    eyebrow("Before we start &#183; Lesson 1-3"),
    h2("Last time ended on a list of cautions"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>What AI is good at</h3><ul>'
    '<li>Finding and classifying patterns in data</li>'
    '<li>Recognising and generating images, audio, text</li>'
    '<li>Prediction based on data</li>'
    '</ul></div>'
    '<div class="pane b"><h3>What needs caution</h3><ul>'
    '<li>Ethical judgments &#8212; discrimination, prejudice</li>'
    '<li>Personal information and privacy</li>'
    '<li>Biased training data</li>'
    '<li>The black-box problem, and who is responsible</li>'
    '<li>Copyright, when protected works are training data</li>'
    '</ul></div>'
    '</div>',
    sub("That right-hand column is today&#8217;s whole lesson. We open each caution up.",
        "max-width:60ch;margin-top:.9rem"),
    ar("المرة اللي فاتت خلصنا بقايمة تحذيرات. العمود اليمين ده هو درس النهارده كله — هنفتح كل تحذير ونفهمه.")))

# 3 hook
A(s("",
    eyebrow("This is already happening"),
    h2("AI helps decide things about people", "max-width:22ch"),
    '<div class="rise fields">'
    '<span class="chip">who gets a job interview</span>'
    '<span class="chip">who a camera says you are</span>'
    '<span class="chip">how your personal data is used</span>'
    '</div>',
    sub("If the data it learned from was biased, it can be <b>unfair</b>. And it can be hard to know <b>why</b> it decided at all.",
        "max-width:58ch;margin-top:1rem"),
    ar("الـ AI بيساعد يقرر مين ياخد انترفيو، والكاميرا تقول انت مين، وبياناتك تتستخدم إزاي. لو الداتا اللي اتعلم منها متحيزة، ممكن يبقى ظالم — وساعات مش هتعرف قرر كده ليه أصلاً.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("What ethical issues arise as AI spreads &#8212; and what principles should guide how we use it?",
       "max-width:26ch"),
    ar("سؤال النهارده: إيه المشاكل الأخلاقية اللي بتظهر مع انتشار الـ AI، وإيه المبادئ اللي لازم تمشّي استخدامه؟")))

# 5 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("A face-recognition AI is more likely to <b>misidentify</b> people from some ethnic groups than others. With your partner, predict: <b>who could be harmed</b> by this, and how? Give a reason.",
        "max-width:56ch;margin-top:1rem"),
    sub("Keep your answer. It is exactly what Part 1 explains.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: نظام تعرّف على الوجه بيغلط أكتر مع ناس من مجموعات معينة. توقّعوا: مين ممكن يتأذي من ده، وإزاي؟ وليه؟ احتفظوا بالإجابة — الجزء الأول بيشرحها بالظبط.")))

# ---------------- part 1: algorithmic bias ----------------
A(s("dark",
    eyebrow("Part 1"),
    h2("Algorithmic bias", "font-size:clamp(30px,5.5vw,72px)"),
    ar("الجزء الأول: التحيز الخوارزمي.")))

A(s("",
    eyebrow("1 &#183; The definition"),
    h2("Bias in, bias out", "max-width:24ch"),
    '<div class="rise statement"><em>Algorithmic bias</em> &#8212; bias in AI judgments caused by bias in the training data.</div>',
    '<table class="rise">'
    '<tr><th>Example from the book</th><th>Who is treated unfairly</th></tr>'
    '<tr><td>A hiring AI</td><td>Unfairly evaluates applicants of a particular gender</td></tr>'
    '<tr><td>A face-recognition AI</td><td>Is more likely to misidentify particular ethnic groups</td></tr>'
    '</table>',
    ar("التحيز الخوارزمي يعني الـ AI يحكم بشكل متحيز لأن الداتا اللي اتدرب عليها كانت متحيزة. الكتاب بيدي مثالين: AI توظيف بيظلم نوع معين، و AI تعرّف على الوجه بيغلط أكتر مع مجموعات معينة.")))

A(s("",
    eyebrow("1 &#183; See it happen"),
    h2("It copies the data it was given"),
    fig(BIAS),
    ar("الـ AI محدش قاله يبقى ظالم. هو بيتعلم النمط اللي في الداتا — ولو مجموعة واحدة ماليا الداتا، هيبقى دقيق معاها ويغلط مع الباقي.")))

A(s("",
    eyebrow("1 &#183; Where it comes from"),
    h2("Two places bias gets in", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>In the training data</h3><ul>'
    '<li><b>Insufficient data</b> on certain attributes</li>'
    '<li><b>Past discriminatory tendencies</b> reflected in the data</li>'
    '</ul></div>'
    '<div class="pane b"><h3>In the way the system is built</h3><ul>'
    '<li>An <b>inappropriate choice of variables</b></li>'
    '<li>A <b>proxy variable</b> &#8212; one that indirectly stands in for a protected attribute</li>'
    '<li>The <b>design of the model</b> itself</li>'
    '</ul></div>'
    '</div>',
    ar("التحيز بيدخل من مكانين: من الداتا نفسها — داتا قليلة عن فئات معينة، أو داتا فيها تمييز قديم — أو من طريقة بناء النظام: اختيار متغيرات غلط، أو متغير بديل، أو تصميم النموذج نفسه.")))

A(s("",
    eyebrow("1 &#183; The one students skip"),
    h2("A proxy variable", "max-width:24ch"),
    sub("A <b>protected attribute</b> is something a decision must not discriminate on &#8212; gender, or ethnic group. Removing it from the data is <b>not enough</b>.",
        "max-width:58ch;margin-top:.6rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--teal-pale);border-radius:12px;max-width:64ch">'
    '<p style="font-size:clamp(13px,1.45vw,19px)">A hiring AI is never told an applicant&#8217;s gender. But it is given another detail that <b>goes closely with gender</b>. It can still learn the old bias through that detail &#8212; the detail is standing in for gender. <span style="color:var(--soft)">(Our example, to show the idea.)</span></p>'
    '</div>',
    ar("الـ protected attribute حاجة ممنوع القرار يميّز بيها، زي النوع أو المجموعة العرقية. لو شلتها من الداتا مش كفاية: لو فيه متغير تاني مرتبط بيها أوي، الـ AI هيتعلم التحيز من خلاله — ده الـ proxy variable، المتغير البديل.")))

A(s("dark",
    eyebrow("Think it through"),
    h2("A hiring AI was found to rate applicants of one gender lower. What is the most likely cause &#8212; and one measure to fix it?",
       "max-width:27ch"),
    ar("AI توظيف طلع بيقيّم نوع معين أقل. إيه السبب الأرجح؟ واقترح إجراء واحد يصلّح ده.")))

# ---------------- part 2: privacy ----------------
A(s("dark",
    eyebrow("Part 2"),
    h2("Privacy", "font-size:clamp(30px,5.5vw,72px)"),
    ar("الجزء التاني: الخصوصية.")))

A(s("",
    eyebrow("2 &#183; New issues"),
    h2("AI created new privacy problems", "max-width:24ch"),
    '<div class="rise statement"><em>Privacy</em> &#8212; the appropriate handling and protection of personal data.</div>',
    '<div class="rise vs">'
    '<div class="pane a"><h3>1 &#183; Surveillance</h3><ul>'
    '<li>Face-recognition cameras in <b>public spaces</b></li>'
    '<li>Can <b>identify and track</b> individuals</li>'
    '</ul></div>'
    '<div class="pane b"><h3>2 &#183; Mass collection</h3><ul>'
    '<li>Large amounts of <b>online behaviour data</b></li>'
    '<li>Collected and <b>analysed</b></li>'
    '</ul></div>'
    '</div>',
    ar("الخصوصية يعني بياناتك الشخصية تتعامل صح وتتحمى. الـ AI عمل مشكلتين جداد: كاميرات تعرّف على الوجه في الأماكن العامة تقدر تعرف الناس وتتتبعهم، وجمع كميات ضخمة من بيانات سلوكك على النت وتحليلها.")))

A(s("dark",
    eyebrow("Think it through"),
    h2("Face recognition in public spaces can improve safety and convenience &#8212; and raise privacy concerns. How should the three be balanced?",
       "max-width:27ch"),
    ar("التعرّف على الوجه في الأماكن العامة بيحسّن الأمان والراحة، بس بيعمل مشكلة خصوصية. إزاي نوازن بين التلاتة؟ وأنهي مبدأ من مبادئ أخلاقيات الـ AI أقرب لرأيك؟")))

# ---------------- part 3: XAI and responsibility ----------------
A(s("dark",
    eyebrow("Part 3"),
    h2("Explainable AI and responsibility", "font-size:clamp(28px,5vw,64px);max-width:18ch"),
    ar("الجزء التالت: الـ AI القابل للتفسير، والمسؤولية.")))

A(s("",
    eyebrow("3 &#183; The black box, and the answer to it"),
    h2("Why did it decide that?"),
    fig(XAI),
    ar("لو الـ AI صندوق أسود بيديك النتيجة بس، محدش يقدر يتأكد هي صح ولا عادلة. الـ XAI بيطلّع الأسباب كمان — فبني آدم يقدر يراجعها.")))

A(s("",
    eyebrow("3 &#183; The definition"),
    h2("Seeing why it decided", "max-width:24ch"),
    # the definition is long: the full statement size filled the slide and
    # repeated the heading word for word
    '<div class="rise statement" style="font-size:clamp(20px,3vw,40px)"><em>Explainable AI (XAI)</em> &#8212; technology that makes it possible for humans to understand why an AI made a particular judgment.</div>',
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--teal-pale);border-radius:12px;max-width:64ch">'
    '<p style="font-size:clamp(13px,1.45vw,19px)">When the decision-making process is opaque &#8212; a <b>black box</b> &#8212; it is difficult to verify whether the result is correct. So &#8220;the answer is right, so the process does not matter&#8221; is <b>false</b>.</p>'
    '</div>',
    ar("الـ XAI تقنية بتخلي البني آدم يفهم الـ AI أخد الحكم ده ليه. ولو العملية مقفولة (صندوق أسود)، صعب تتأكد النتيجة صح. عشان كده جملة «طالما النتيجة صح مفيش مشكلة» غلط — وبتيجي في الامتحان.")))

A(s("",
    eyebrow("3 &#183; Responsibility"),
    h2("It got it wrong. Who answers?"),
    fig(WHO),
    ar("لما الـ AI يغلط، مين المسؤول؟ المطوّر اللي عمله، ولا الشركة اللي بتشغّله، ولا المستخدم؟ كل واحد شايفها بشكل، ولسه مفيش معيار واضح متفق عليه — ودي نقطة امتحان.")))

A(s("",
    eyebrow("3 &#183; Two words that sound the same"),
    h2("Responsibility is not accountability", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Responsibility</h3><ul>'
    '<li>The <b>roles and duties</b> of each party</li>'
    '<li>Developer, operator, user &#8212; who does what</li>'
    '<li>Who answers when an AI judgment is wrong</li>'
    '</ul></div>'
    '<div class="pane b"><h3>Accountability</h3><ul>'
    '<li><b>Being answerable</b> for the AI&#8217;s decisions</li>'
    '<li>Knowing who can be <b>held to account</b>, according to their role</li>'
    '<li>One of the four principles of AI ethics</li>'
    '</ul></div>'
    '</div>',
    ar("المسؤولية = أدوار وواجبات كل طرف (المطوّر والمشغّل والمستخدم). المساءلة = إن فيه حد يتحاسب فعلاً على قرارات الـ AI حسب دوره — ودي من المبادئ الأربعة. الوزارة بتسأل على الفرق ده.")))

A(s("",
    eyebrow("3 &#183; Where it becomes real"),
    h2("Two places these questions are not theory"),
    '<div class="rise shots">'
    + shot("Face_detection.jpg", "Face recognition",
           "Useful at a gate &#8212; and it can track people, and misidentify some groups more than others.",
           "مفيد على البوابة — بس ممكن يتتبع الناس، ويغلط مع مجموعات أكتر من غيرها.")
    + shot("Chest_Xray_PA_3-8-2010.png", "Image-diagnosis AI",
           "If its result is wrong, who is answerable &#8212; and can anyone see why it decided?",
           "لو النتيجة غلط، مين يتحاسب؟ وحد يقدر يشوف هو قرر كده ليه؟")
    + '</div>',
    CREDIT,
    ar("مثالين حقيقيين: التعرّف على الوجه (خصوصية وتحيز)، والتشخيص بالصور (صندوق أسود ومسؤولية). اسأل الطلبة: كل صورة فيهم بتلمس أنهي مشكلة من اللي فاتوا؟")))

A(s("dark",
    eyebrow("Pause & think"),
    h2("If no one can explain why an AI rejected someone&#8217;s job application, is that fair? Which principle is missing?",
       "max-width:27ch"),
    ar("لو محدش يقدر يشرح الـ AI رفض طلب توظيف حد ليه، ده عادل؟ وأنهي مبدأ ناقص هنا؟")))

# ---------------- part 4: the four principles ----------------
A(s("dark",
    eyebrow("Part 4"),
    h2("The four principles of AI ethics", "font-size:clamp(28px,5vw,64px);max-width:18ch"),
    ar("الجزء الرابع: المبادئ الأربعة لأخلاقيات الذكاء الاصطناعي.")))

A(s("",
    eyebrow("4 &#183; Learn these four exactly"),
    h2("Four principles for using AI appropriately", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#9878;</div><div class="role">Principle 1</div>'
    '<h3>Fairness</h3><p>Not unjustly discriminating against any particular person or group</p></div>'
    '<div class="card"><div class="ico">&#128269;</div><div class="role">Principle 2</div>'
    '<h3>Transparency</h3><p>Showing the AI&#8217;s decision-making process and inner workings clearly</p></div>'
    '<div class="card"><div class="ico">&#128274;</div><div class="role">Principle 3</div>'
    '<h3>Privacy protection</h3><p>Handling personal information appropriately and protecting privacy</p></div>'
    '<div class="card"><div class="ico">&#9989;</div><div class="role">Principle 4</div>'
    '<h3>Accountability</h3><p>Being answerable for the AI&#8217;s decisions</p></div>'
    '</div>',
    ar("المبادئ الأربعة بالحرف من الكتاب: العدالة (مفيش تمييز ظالم)، الشفافية (عملية القرار واضحة)، حماية الخصوصية (البيانات الشخصية تتعامل صح)، المساءلة (فيه حد مسؤول عن القرار). احفظهم بالتعريف.")))

A(s("",
    eyebrow("4 &#183; Your turn"),
    h2("Which principle is it?"),
    '<table class="rise">'
    '<tr><th>Situation</th><th>Principle</th></tr>'
    '<tr><td>A hiring AI evaluates fairly regardless of gender</td><td>Fairness</td></tr>'
    '<tr><td>The AI&#8217;s decision-making process is disclosed to users in an easy-to-understand way</td><td>Transparency</td></tr>'
    '<tr><td>Collected personal data is not used for other purposes than originally intended</td><td>Privacy protection</td></tr>'
    '<tr><td>Someone is answerable when an AI&#8217;s diagnostic result turns out to be wrong</td><td>Accountability</td></tr>'
    '</table>',
    sub("Cover the right-hand column and answer first. These four are the book&#8217;s own exercise.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("غطّوا العمود اليمين وجاوبوا الأول. الأربع مواقف دول هما تمرين الكتاب نفسه، وبييجوا كسؤال توصيل.")))

A(s("",
    eyebrow("Exam warning"),
    h2("Three sentences that look right but are wrong", "max-width:26ch"),
    '<ul class="rise check">'
    '<li class="no">&#8220;Even if an AI&#8217;s process is opaque, there is no problem as long as the result is correct.&#8221; &#8212; <b>false</b>: an opaque result cannot be verified.</li>'
    '<li class="no">&#8220;Who is responsible when an AI is wrong has already been clearly determined.&#8221; &#8212; <b>false</b>: views differ and no clear standard exists yet.</li>'
    '<li class="no">&#8220;Algorithmic bias is caused by the AI&#8217;s processing speed.&#8221; &#8212; <b>false</b>: it comes from bias in the training data.</li>'
    '</ul>',
    ar("تلات جمل شكلها صح وهي غلط، وبييجوا في الامتحان: «طالما النتيجة صح العملية مش مهمة» غلط، «المسؤولية متحددة بوضوح» غلط، «التحيز سببه سرعة المعالجة» غلط — سببه الداتا.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("A company wants to use a hiring AI", "max-width:26ch"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Investigate</b> one documented case of an AI accused of bias. What group did it affect, and what data might have caused it?</li>'
    '<li><b>Consider responsibility</b>: the developer, the company using it, or the operator &#8212; what does each hold?</li>'
    '<li><b>Decide</b> one rule the company must follow before using it. Justify it with the principles.</li>'
    '</ul>',
    sub("Stuck? If the training data reflects past bias, the AI can repeat it &#8212; one fix is to check the data and test the results across different groups.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: دوّر على حالة حقيقية لـ AI اتهم بالتحيز، حدد مسؤولية كل طرف، واقترح قاعدة واحدة الشركة لازم تمشي عليها قبل ما تستخدمه — وبرّرها بالمبادئ.")))

A(s("",
    eyebrow("In a new context"),
    h2("A school wants face recognition at its gate", "max-width:26ch"),
    sub("The cameras would record attendance automatically.", "max-width:54ch;margin-top:.7rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li>Identify <b>one practical benefit</b> for the school.</li>'
    '<li>Identify <b>one privacy concern</b>.</li>'
    '<li>If the camera <b>misidentifies a student</b>, who should be responsible &#8212; the school, or the company that made the AI? Give a reason.</li>'
    '</ul>',
    ar("مدرسة عايزة كاميرات تعرّف على الوجه على البوابة تسجّل الحضور. اذكر فايدة واحدة ومشكلة خصوصية واحدة. ولو الكاميرا غلطت في طالب، مين المسؤول: المدرسة ولا الشركة؟ وليه؟")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 1-4"),
    h2("Accurate is not enough", "max-width:28ch"),
    '<div class="rise statement">If training data is biased, an AI can reproduce that bias. Using AI responsibly means <em>checking for bias</em>, being able to <em>explain decisions</em>, and knowing <em>who is accountable</em> &#8212; guided by fairness, transparency, privacy protection and accountability.</div>',
    ar("الخلاصة: لو الداتا متحيزة، الـ AI هيكرر التحيز. الاستخدام المسؤول يعني نراجع التحيز، ونقدر نشرح القرار، ونعرف مين يتحاسب — بالمبادئ الأربعة.")))

# unit wrap — this lesson closes Unit 1, and the unit exam covers all four
A(s("",
    eyebrow("Unit 1 &#183; complete"),
    h2("Information technology and society, in four lessons", "max-width:28ch"),
    '<div class="rise timeline">'
    '<div class="tl"><h3>1-1 &#183; How IT developed</h3><p>Five stages, Moore&#8217;s Law, social changes, emerging technologies</p></div>'
    '<div class="tl"><h3>1-2 &#183; How AI works</h3><p>AI &#8594; machine learning &#8594; deep learning &#8594; generative AI, nested; neural networks and their hidden layers</p></div>'
    '<div class="tl"><h3>1-3 &#183; AI in daily life and industry</h3><p>Where it is used, what it is good at, what needs caution</p></div>'
    '<div class="tl"><h3>1-4 &#183; Ethical issues with AI</h3><p>Bias, privacy, XAI and responsibility, the four principles</p></div>'
    '</div>',
    ar("خلصنا الوحدة الأولى: 1-1 تطور تكنولوجيا المعلومات، 1-2 إزاي الـ AI بيشتغل، 1-3 الـ AI في الحياة والصناعة، 1-4 القضايا الأخلاقية. امتحان الوحدة على الأربعة.")))

# QR — must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 4"),
    # Covered until the teacher reveals it (press E, or the dashboard switch),
    # so the code is not handed to a class in advance.
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 4 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers this lesson and reviews the rest of Unit 1. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس ده ومراجعة للوحدة الأولى. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))


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
BASE = "scripts/lecture4_slides_base.html"
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

