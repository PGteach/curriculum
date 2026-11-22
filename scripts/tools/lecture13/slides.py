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
    h2("Exam &#8212; Lecture %d" % (11 + CH)),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture %d quiz" width="250" height="250">' % (11 + CH)
    + '<div class="txt"><p class="sub">A mixed revision exam on all of Unit %d, drawn from %s. ' % (CH, LECTURES)
    + 'At the end it shows you, lesson by lesson, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان مراجعة على الوحدة كلها. في الآخر هيوضحلك انت ضعيف في أنهي درس بالظبط.")))
