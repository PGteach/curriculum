SLIDES = []
A = SLIDES.append

# 1 title
A(s("dark",
    '<div class="rise eyebrow" id="lectureBadge">Programming &amp; Artificial Intelligence</div>',
    h2("When something goes wrong", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("Even a well-protected system can be attacked. Today: how to respond, in the right order &#8212; and how to decide which risks to fix first.",
        "max-width:56ch;margin-top:1rem"),
    ar("حتى النظام المحمي كويس ممكن يتهاجم. النهارده: إزاي نستجيب بالترتيب الصح — وإزاي نقرر نعالج أنهي خطر الأول.")))

# 2 recap -- lesson 2-2, and the Arabic book's bridge into this lesson
A(s("",
    eyebrow("Before we start &#183; Lesson 2-2"),
    h2("Last time: layers, and verify every access"),
    '<table class="rise">'
    '<tr><th>Layer</th><th>Measure</th></tr>'
    '<tr><td>1 &#183; Network entry</td><td>Firewall</td></tr>'
    '<tr><td>2 &#183; Communication path</td><td>VPN</td></tr>'
    '<tr><td>3 &#183; Server placement</td><td>DMZ</td></tr>'
    '<tr><td>4 &#183; Endpoints</td><td>Antivirus, an updated OS</td></tr>'
    '</table>',
    sub("Defense in depth makes a breach less likely &#8212; not impossible. Today moves from <b>prevention</b> to <b>response</b>.",
        "max-width:60ch;margin-top:.9rem"),
    ar("حتى مع تقنيات الحماية والدفاع في العمق، ممكن يحصل حادث أمني؛ عشان كده الدرس ده بينقلنا من الوقاية للاستجابة وإدارة المخاطر.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("This is already happening"),
    h2("A rushed reaction makes it worse", "max-width:22ch"),
    '<div class="rise fields">'
    '<span class="chip">data leaked</span>'
    '<span class="chip">files tampered with</span>'
    '<span class="chip">a service knocked offline</span>'
    '</div>',
    sub("Organizations follow a clear, ordered response, so that damage is contained, the cause is removed, and the same problem does not return. And they decide in advance which risks to guard against first &#8212; no team can fix everything at once.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> ransomware has locked the school&#8217;s files. Would you restore from the backup straight away? Remember your answer.</p></div>',
    ar("حتى النظام المحمي كويس ممكن يتعرض لحادث أمني، زي تسرب بيانات، أو التلاعب بالملفات، أو تعطل خدمة. عشان كده المؤسسات بتستخدم خطة منظمة: توقف انتشار المشكلة، وتشيل التهديد، وترجّع الخدمة، وبعدين تتعلم من الحادث. وبتقيّم المخاطر عشان تحدد الأولويات، لأن الفريق مش هيقدر يعالج كل حاجة في نفس الوقت.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("When a security incident happens, how should an organization respond in order &#8212; and how does it decide which risks to address first?",
       "max-width:28ch"),
    ar("السؤال الرئيسي: لما يحصل حادث أمني، المؤسسة المفروض تنظّم استجابتها إزاي بالترتيب — وإزاي تقرر أنهي مخاطر تعالجها الأول؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map &#183; three parts"),
    h2("What happened, what to do, what to fix first", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#9888;</div><div class="role">Part 1</div>'
    '<h3>Security incident</h3><p>When real damage occurs</p></div>'
    '<div class="card"><div class="ico">&#128221;</div><div class="role">Part 2</div>'
    '<h3>Six stages</h3><p>The response, in order</p></div>'
    '<div class="card"><div class="ico">&#128202;</div><div class="role">Part 3</div>'
    '<h3>Risk assessment</h3><p>Impact &#215; likelihood</p></div>'
    '</div>',
    ar("خريطة المحاضرة: الجزء الأول: يعني إيه حادث أمني. الجزء التاني: المراحل الست للاستجابة بالترتيب. الجزء التالت: تقييم المخاطر — التأثير × الاحتمالية.")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("A school computer is infected with malware that is <b>spreading</b>. With your partner, put these four actions in order: <b>restore the files from a backup</b> &#183; <b>unplug it from the network</b> &#183; <b>find out how it got in</b> &#183; <b>remove the malware</b>.",
        "max-width:56ch;margin-top:1rem"),
    sub("Keep your order. Part 2 gives the book&#8217;s.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: جهاز في المدرسة اتصاب ببرمجية خبيثة وبتنتشر. رتّبوا الأربع خطوات دول: نرجّع الملفات من نسخة احتياطية، نفصله عن الشبكة، نعرف دخلت إزاي، نشيل البرمجية الخبيثة.")))

# ---------------- part 1: security incidents ----------------

A(s("",
    eyebrow("Part 1 &#183; What is a security incident"),
    h2("What is a security incident?", "max-width:24ch"),
    '<div class="rise statement def"><em>Security incident</em> &#8212; a situation in which actual damage occurs due to an information security problem.</div>',
    '<table class="rise" style="margin-top:.9rem">'
    '<tr><th>Type</th><th>Description</th></tr>'
    '<tr><td>Information leak</td><td>Personal or confidential information is leaked to the outside</td></tr>'
    '<tr><td>Data tampering</td><td>Data within a system is altered without authorization</td></tr>'
    '<tr><td>Service outage</td><td>A service becomes unavailable due to attacks on the server, etc.</td></tr>'
    '</table>',
    ar("الحادث الأمني: حدث بيأثر على سرية المعلومات أو سلامتها أو توافرها، أو بيهددها بجدية، أو بيخالف سياسة أمنية. أمثلة: تسرب المعلومات للخارج، والتلاعب بالبيانات من غير تصريح، وانقطاع الخدمة بسبب هجوم على الخادم.")))

A(video("AuYNXgO_f3Y", "The Internet: Cybersecurity &amp; Crime", "Code.org",
        "Watch &#183; incidents in the real world", "What does an attack look like?",
        "which of the three incident types &#8212; leak, tampering, outage &#8212; does each attack in the video cause?",
        "وانتو بتتفرجوا: كل هجوم في الفيديو بيعمل أنهي نوع من الحوادث التلاتة — تسرب، ولا تلاعب، ولا انقطاع خدمة؟"))

A(s("",
    eyebrow("1 &#183; Your turn"),
    h2("Which is NOT a security incident?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">Data was encrypted by a ransomware infection. <span class="ans">&#8212; <b>an incident</b>: real damage.</span></li>'
    '<li class="reveal rv tf-t">Customer information was leaked to the outside through unauthorized access. <span class="ans">&#8212; <b>an incident</b>: an information leak.</span></li>'
    '<li class="reveal rv">A software update was performed to add new features. <span class="ans">&#8212; <b>NOT an incident</b>: nothing was damaged.</span></li>'
    '<li class="reveal rv tf-t">A web service became unavailable due to an attack on the server. <span class="ans">&#8212; <b>an incident</b>: a service outage.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("أنهي واحد مش حادث أمني؟ تحديث برنامج عشان يضيف مميزات جديدة — ده مفيهوش أي ضرر، فمش حادث.")))

# ---------------- part 2: the six stages ----------------

A(s("",
    eyebrow("Part 2 &#183; The flow of incident response"),
    h2("Six stages, in order"),
    fig(STAGES),
    sub("When a security incident occurs, the response proceeds through these six stages &#8212; <b>in order</b>.",
        "max-width:62ch;margin-top:.3rem"),
    ar("لما يحصل حادث أمني، الاستجابة بتمشي في المراحل الست دي بالترتيب: التحضير، الاكتشاف، الاحتواء، إزالة التهديد (الاستئصال)، الاستعادة، الدروس المستفادة والتحسين.")))

A(s("",
    eyebrow("2 &#183; What each stage does"),
    h2("What happens at each stage"),
    '<table class="rise">'
    '<tr><th>Stage</th><th>What happens</th></tr>'
    '<tr><td>1 Preparation</td><td>Establish response procedures and structures in advance, in preparation for incidents</td></tr>'
    '<tr><td>2 Detection</td><td>Discover and confirm that an incident has occurred</td></tr>'
    '<tr><td>3 Containment</td><td>Limit the scope of impact so that damage does not spread further</td></tr>'
    '<tr><td>4 Eradication</td><td>Remove the cause of the incident (e.g. remove malware)</td></tr>'
    '<tr><td>5 Recovery</td><td>Return systems and services to their normal state</td></tr>'
    '<tr><td>6 Prevention of recurrence</td><td>Analyze the cause and take measures so that the same incident does not occur again</td></tr>'
    '</table>',
    ar("1 التحضير: إجراءات وهياكل استجابة مسبقًا. 2 الاكتشاف: نكتشف ونتأكد إن فيه حادث. 3 الاحتواء: نحدد نطاق التأثير عشان الضرر ميتنشرش. 4 إزالة التهديد (الاستئصال): نشيل التهديد ومسبباته زي البرمجيات الخبيثة ونعالج الثغرة. 5 الاستعادة: نرجّع الأنظمة لحالة تشغيل آمنة، وممكن من نسخة احتياطية سليمة. 6 الدروس المستفادة والتحسين: نحلل اللي حصل ونوثّق الدروس ونحسّن الضوابط.")))

A(s("",
    eyebrow("2 &#183; Two names, one stage"),
    h2("Stage 6 has two names", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>English book</h3><ul>'
    '<li><b>Prevention of recurrence</b></li>'
    '<li>Analyze the cause and take measures so the same incident does not occur again</li>'
    '</ul></div>'
    '<div class="pane b"><h3>Arabic book and ministry</h3><ul>'
    '<li><b>Lessons learned and improvement</b> &#8212; الدروس المستفادة والتحسين</li>'
    '<li>Analyze what happened, document the lessons, and improve the controls</li>'
    '</ul></div>'
    '</div>',
    sub("Learn both names: the exam can use either. They are the same last stage.", "max-width:60ch;margin-top:.9rem"),
    ar("خلّي بالك: المرحلة السادسة اسمها في الكتاب الإنجليزي \"منع التكرار\"، وفي الكتاب العربي وامتحانات الوزارة \"الدروس المستفادة والتحسين\". الاتنين نفس المرحلة: نحلل اللي حصل، ونوثّق الدروس، ونحسّن الضوابط.")))

A(s("",
    eyebrow("2 &#183; The order matters"),
    h2("Contain first, then remove the cause", "max-width:24ch"),
    '<div class="rise statement def"><em>Containment</em> limits the spread of damage. <em>Eradication</em> removes the cause. Containment comes <em>first</em>.</div>',
    sub("Disconnecting an infected computer from the network is containment; removing the malware is eradication. And if recovery is performed without removing the cause, <b>the same incident may occur again</b>.",
        "max-width:58ch;margin-top:.9rem"),
    ar("الاحتواء: الحد من انتشار الضرر. الاستئصال: إزالة السبب. الاحتواء بييجي الأول. ولو عملنا استعادة قبل ما نشيل السبب، نفس الحادث ممكن يتكرر.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("Why must containment come before eradication in the six-stage response?",
       "max-width:27ch"),
    ar("وقّف وفكّر: ليه الاحتواء لازم ييجي قبل الاستئصال في الاستجابة ذات المراحل الست؟")))

A(s("",
    eyebrow("2 &#183; In practice"),
    h2("The order is a guide, not a cage", "max-width:24ch"),
    sub("The six stages give the general sequence. In a real response some activities can <b>overlap</b> or <b>repeat</b>.",
        "max-width:58ch;margin-top:.6rem"),
    '<div class="rise statement def" style="margin-top:.9rem"><em>e.g.</em> Recovery can reveal traces of the threat that are still there &#8212; and then the team goes back to containment or eradication.</div>',
    sub("So: follow the order, and be ready to step back.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("ترتيب المراحل بيساعدنا نفهم التسلسل العام، بس الاستجابة الفعلية ممكن يحصل فيها تداخل أو تكرار بين بعض الأنشطة. مثلًا، الاسترداد ممكن يكشف بقايا للتهديد، فنضطر نرجع للاحتواء أو إزالة التهديد.")))

A(s("",
    eyebrow("2 &#183; Your turn &#183; worked example"),
    h2("Which stage is it?"),
    '<table class="rise">'
    '<tr><th>Action</th><th>Stage</th></tr>'
    '<tr><td>Establishing response procedures in advance, in preparation for incidents</td><td class="reveal"><span>Preparation</span></td></tr>'
    '<tr><td>Discovering and confirming that an incident has occurred</td><td class="reveal"><span>Detection</span></td></tr>'
    '<tr><td>Disconnecting a malware-infected computer from the network</td><td class="reveal"><span>Containment</span></td></tr>'
    '<tr><td>Removing the malware infection</td><td class="reveal"><span>Eradication</span></td></tr>'
    '<tr><td>Restoring a clean system from a backup</td><td class="reveal"><span>Recovery</span></td></tr>'
    '<tr><td>Analyzing the cause and taking measures so it does not occur again</td><td class="reveal"><span>Prevention of recurrence</span></td></tr>'
    '</table>',
    ar("لكل إجراء، أنهي مرحلة؟ الإجراءات المسبقة ← التحضير. التأكد إن فيه حادث ← الاكتشاف. فصل الجهاز المصاب عن الشبكة ← الاحتواء. إزالة البرمجية الخبيثة ← الاستئصال. الرجوع من نسخة احتياطية سليمة ← الاستعادة. تحليل السبب ← الدروس المستفادة والتحسين.")))

A(s("",
    eyebrow("2 &#183; Exam-style question &#183; 6 marks"),
    h2("Why must the six stages go in order?", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane b"><h3>Recover first</h3><ul>'
    '<li>The system is back, but the cause is <b>still there</b></li>'
    '<li>The same incident can happen again</li>'
    '</ul></div>'
    '<div class="pane a"><h3>Eradicate, then recover</h3><ul>'
    '<li>The cause is removed first</li>'
    '<li>Recovery returns a <b>clean</b> system</li>'
    '</ul></div>'
    '</div>',
    sub("Use recovery and eradication as the example, and say what happens if the cause is not removed.", "max-width:60ch;margin-top:.9rem"),
    ar("سؤال على نمط الامتحان: اشرح ليه المراحل الست لازم تتنفذ بالترتيب، مستخدمًا الاستعادة والاستئصال كمثال. استعن بـ: إيه اللي بيحصل لو السبب متشالش.")))

# ---------------- part 3: risk assessment ----------------

A(s("",
    eyebrow("Part 3 &#183; The concept of risk assessment"),
    h2("Risk = impact &#215; likelihood"),
    '<div class="rise statement def"><em>Risk</em> &#8212; the possibility of an information security problem occurring in the future, and its impact.</div>',
    '<table class="rise" style="margin-top:.9rem">'
    '<tr><th>Factor</th><th>Meaning</th></tr>'
    '<tr><td>Impact</td><td>How much damage occurs if the risk actually materializes</td></tr>'
    '<tr><td>Likelihood</td><td>How high the probability is that the risk will actually materialize</td></tr>'
    '</table>',
    sub("<b>Risk size = Impact &#215; Likelihood.</b> Not impact alone, and not likelihood alone.", "max-width:58ch;margin-top:.8rem"),
    ar("الخطر: احتمال إن يحصل حدث بيسبب ضرر، مع مراعاة احتمال وقوعه وحجم أثره. درجة الخطر = درجة التأثير × درجة الاحتمالية. التأثير: حجم الضرر لو الحدث وقع. الاحتمالية: مدى احتمال وقوع الحدث.")))

A(s("",
    eyebrow("3 &#183; Risk evaluation matrix"),
    h2("Fix the worst first"),
    fig(MATRIX),
    sub("Risks with both <b>high impact and high likelihood</b> are addressed first. It is difficult to address every risk at the same time, so priorities are set and measures taken systematically.",
        "max-width:62ch;margin-top:.3rem"),
    ar("المخاطر اللي تأثيرها عالي واحتماليتها عالية هي أعلى أولوية. أما ترتيب باقي الحالات فبيعتمد على درجات المصفوفة والسياق والضوابط المتاحة. مثلًا: تأثير كبير واحتمالية منخفضة = 3، يعني خطورة متوسطة.")))

A(s("",
    eyebrow("3 &#183; Your turn"),
    h2("Put the risks in order", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>Risk</th><th>Impact</th><th>Likelihood</th><th>Size</th></tr>'
    '<tr><td>a</td><td>large (3)</td><td>high (3)</td><td class="reveal"><span>9 &#8212; 1st</span></td></tr>'
    '<tr><td>b</td><td>small (1)</td><td>high (3)</td><td class="reveal"><span>3 &#8212; 3rd</span></td></tr>'
    '<tr><td>c</td><td>large (3)</td><td>medium (2)</td><td class="reveal"><span>6 &#8212; 2nd</span></td></tr>'
    '<tr><td>d</td><td>small (1)</td><td>low (1)</td><td class="reveal"><span>1 &#8212; 4th</span></td></tr>'
    '</table>',
    sub("Multiply each row, rank the sizes from biggest to smallest &#8212; then tap each size to check.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("رتّب المخاطر من الأعلى أولوية للأقل: اضرب التأثير × الاحتمالية لكل خطر، وبعدين رتّب الدرجات من الأكبر للأصغر.")))

A(s("",
    eyebrow("Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">A security incident is a situation in which actual damage occurs due to an information security problem. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv tf-t">In incident response, it is important first to prevent the spread of damage before removing the cause. <span class="ans">&#8212; <b>true</b>: containment before eradication.</span></li>'
    '<li class="reveal rv">The size of a risk can be determined by impact alone. <span class="ans">&#8212; <b>false</b>: by impact and likelihood.</span></li>'
    '<li class="reveal rv tf-t">The final stage of incident response is prevention of recurrence. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: تعريف الحادث الأمني — صح. منع انتشار الضرر قبل إزالة السبب — صح. حجم المخاطرة بالتأثير وحده — غلط. المرحلة الأخيرة الدروس المستفادة والتحسين — صح.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">It is enough to address only risks with large impact. <span class="ans">&#8212; <b>false</b>: likelihood counts too.</span></li>'
    '<li class="reveal rv">It is enough to address only risks with high likelihood. <span class="ans">&#8212; <b>false</b>: impact counts too.</span></li>'
    '<li class="reveal rv">All risks must be addressed simultaneously. <span class="ans">&#8212; <b>false</b>: set priorities.</span></li>'
    '<li class="reveal rv">Detection &#8594; Eradication &#8594; Containment &#8594; Recovery is the right order. <span class="ans">&#8212; <b>false</b>: containment comes before eradication.</span></li>'
    '</ul>',
    ar("خلّي بالك، كل الجمل دي غلط: نعالج المخاطر الكبيرة في التأثير بس — غلط. الاحتمالية العالية بس — غلط. كل المخاطر مع بعض — غلط. الاستئصال قبل الاحتواء — غلط.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("Ransomware hits the school&#8217;s records", "max-width:26ch"),
    sub("Files are encrypted and staff cannot log in. You lead the response. Restore from backup immediately &#8212; or follow the six stages in order?",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Respond from here.</b> The incident has just been detected. List the stages still to carry out, and what each means for this incident.</li>'
    '<li><b>Assess the risks.</b> (i) another ransomware attack, (ii) a brief power cut: estimate impact and likelihood, and say which to address first.</li>'
    '<li><b>Decide.</b> The first three actions, and one reason why order matters. In pairs, agree on the single most important first step.</li>'
    '</ul>',
    sub("Stuck? If you recover before you eradicate the cause, the malware is still there &#8212; and the same incident can happen again.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: نظام سجلات الطلاب في مدرسة اتهاجم ببرمجية فدية: الملفات اتشفرت والموظفين مش قادرين يدخلوا. اذكر المراحل اللي لسه هتتنفذ من دلوقتي، وقيّم مخاطرتين (فدية تانية، وانقطاع كهربا قصير)، وقرّر أول تلات إجراءات.")))

A(s("",
    eyebrow("In a new context"),
    h2("An online shop finds its customer data leaked", "max-width:26ch"),
    sub("The leak has just been detected.", "max-width:54ch;margin-top:.7rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li>Name the <b>next two stages</b> it should carry out, and why.</li>'
    '<li>Using risk assessment, identify <b>one risk to prioritize</b> afterward.</li>'
    '</ul>',
    ar("طبّق اللي اتعلمته: متجر إلكتروني لسه مكتشف إن بيانات العملاء اتسربت. باستخدام المراحل الست وتقييم المخاطر، حدد المرحلتين الجايين وليه، وحدد خطر واحد لازم ياخد الأولوية بعد كده.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 2-3"),
    h2("Respond in order; fix the worst first", "max-width:28ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> restore the school&#8217;s files from the backup straight away? What comes first?</p>'
    '<div class="rise statement">Follow the six stages in order &#8212; <em>prepare, detect, contain, eradicate, recover, prevent</em> &#8212; and prioritize risks by <em>impact &#215; likelihood</em>.</div>',
    ar("افتكر: اتبع التسلسل العام للمراحل الست (تحضير ← اكتشاف ← احتواء ← استئصال ← استعادة ← الدروس المستفادة والتحسين) مع إمكانية التداخل أو الرجوع لمرحلة سابقة، وحدد أولويات المخاطر بالتأثير × الاحتمالية.")))

# unit wrap -- this lesson closes Unit 2
A(s("",
    eyebrow("Unit 2 &#183; complete"),
    h2("Cybersecurity, in three lessons", "max-width:28ch"),
    '<div class="rise timeline">'
    '<div class="tl"><h3>2-1 &#183; Cryptographic technologies and authentication</h3><p>HTTPS, common-key and public-key, certificates, signatures, multi-factor login</p></div>'
    '<div class="tl"><h3>2-2 &#183; Network security design</h3><p>Firewall, VPN, DMZ, defense in depth, zero trust</p></div>'
    '<div class="tl"><h3>2-3 &#183; Incident response and risk management</h3><p>Security incidents, the six stages, risk = impact &#215; likelihood</p></div>'
    '</div>',
    ar("خلصنا الوحدة التانية: 2-1 تقنيات التشفير والمصادقة، 2-2 تصميم أمان الشبكات، 2-3 الاستجابة للحوادث وإدارة المخاطر.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 7"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 7 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers this lesson. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس ده. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))
