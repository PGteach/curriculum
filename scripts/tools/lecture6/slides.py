SLIDES = []
A = SLIDES.append

# 1 title
A(s("dark",
    '<div class="rise eyebrow" id="lectureBadge">Programming &amp; Artificial Intelligence</div>',
    h2("What if one wall falls?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("Last lesson protected a message and an account. Today: how to design a whole network so that one breach does not expose everything.",
        "max-width:56ch;margin-top:1rem"),
    ar("الدرس اللي فات حمينا الرسالة والحساب. النهارده: إزاي نصمم الشبكة كلها بحيث لو دفاع واحد اتخرق، النظام كله ميتكشفش.")))

# 2 recap -- lesson 2-1, and the Arabic book's bridge into this lesson
A(s("",
    eyebrow("Before we start &#183; Lesson 2-1"),
    h2("Last time: four technologies, one connection"),
    '<table class="rise">'
    '<tr><th>Technology</th><th>What it protects</th></tr>'
    '<tr><td>Encryption</td><td>The content, from being read</td></tr>'
    '<tr><td>Digital certificate</td><td>That the other side is genuine</td></tr>'
    '<tr><td>Digital signature</td><td>The data, from being altered</td></tr>'
    '<tr><td>Multi-factor authentication</td><td>The account, from unauthorized login</td></tr>'
    '</table>',
    sub("All four protect one connection or one account. Today we widen it to the <b>network itself</b>.",
        "max-width:60ch;margin-top:.9rem"),
    ar("في الدرس 2-1 اتعلمت إزاي تقنيات التشفير والمصادقة بتحمي الاتصال والحسابات. في الدرس ده هنوسّع الحماية لتصميم الشبكة نفسها.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("This is already happening"),
    h2("One lock on the front door is not enough", "max-width:22ch"),
    '<div class="rise fields">'
    '<span class="chip">customer records</span>'
    '<span class="chip">financial files</span>'
    '<span class="chip">private messages</span>'
    '</div>',
    sub("An organization&#8217;s network holds confidential data, and attackers constantly look for a way in. If the single lock is picked, <b>everything inside is exposed</b>.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> if a company has a strong firewall, is its data safe? Remember your answer &#8212; we come back to it.</p></div>',
    ar("شبكات المؤسسات فيها بيانات وخدمات مهمة ممكن مهاجم يحاول يوصلها. ووسيلة حماية واحدة مش كفاية: لو فشلت، موارد تانية ممكن تبقى في خطر. عشان كده بنستخدم الدفاع في العمق — طبقات كتير بتقلل احتمال الاختراق وبتحد من أثره.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("How can an organization design its network so that, even if one defense is breached, the system stays protected?",
       "max-width:28ch"),
    ar("السؤال الرئيسي: إزاي مؤسسة تقدر تصمم شبكتها بحيث، حتى لو دفاع واحد اتخرق، النظام يفضل محمي؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map &#183; five ideas"),
    h2("Four layers, and one rule", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#129521;</div><div class="role">Part 1 &#183; network entry</div>'
    '<h3>Firewall</h3><p>Allows or denies by rules</p></div>'
    '<div class="card"><div class="ico">&#128274;</div><div class="role">Part 2 &#183; communication path</div>'
    '<h3>VPN</h3><p>An encrypted private line</p></div>'
    '<div class="card"><div class="ico">&#127970;</div><div class="role">Part 3 &#183; server placement</div>'
    '<h3>DMZ</h3><p>Public servers kept apart</p></div>'
    '<div class="card"><div class="ico">&#128269;</div><div class="role">Part 5 &#183; the rule</div>'
    '<h3>Zero trust</h3><p>Verify every access</p></div>'
    '</div>',
    sub("Part 4 puts the layers together: <b>defense in depth</b>.", "margin-top:.6rem;color:var(--soft)"),
    ar("دي خريطة المحاضرة: جدار الحماية عند مدخل الشبكة، والشبكة الافتراضية الخاصة لمسار الاتصال، والمنطقة المعزولة لوضع الخوادم — وده كله اسمه الدفاع في العمق. وفي الآخر نهج انعدام الثقة: اتأكد من كل عملية وصول.")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("A company has a <b>public website</b>, staff who <b>work from home</b>, and a <b>customer database</b>. With your partner, predict: where would an attacker try to get in &#8212; and if you could build only one wall, where would you put it?",
        "max-width:56ch;margin-top:1rem"),
    sub("Keep your answer. By Part 4 you will want more than one wall.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: شركة عندها موقع عام، وموظفين بيشتغلوا من البيت، وقاعدة بيانات عملاء. توقّعوا: المهاجم هيحاول يدخل منين؟ ولو هتبني حيطة واحدة بس، هتحطها فين؟")))

# ---------------- part 1: the firewall ----------------

A(s("",
    eyebrow("Part 1 &#183; The role of firewalls"),
    h2("The firewall: rules at the door", "max-width:24ch"),
    '<div class="rise statement def"><em>Firewall</em> &#8212; a system installed at the entry/exit point of a network that allows or denies communication based on rules set in advance.</div>',
    sub("<b>e.g.</b> Allow access to the web server, but deny direct external access to the database server.",
        "max-width:58ch;margin-top:.9rem"),
    ar("جدار الحماية: نظام أو برنامج بيراقب حركة مرور الشبكة وبيسمح بيها أو يمنعها حسب قواعد أمنية. ممكن يكون عند حدود الشبكة، أو بين أجزائها، أو على جهاز مضيف. مثال: نسمح بالوصول لخادم الويب ونمنع الوصول الخارجي المباشر لقاعدة البيانات.")))

# ---------------- part 2: VPN ----------------

A(s("",
    eyebrow("Part 2 &#183; VPN (Virtual Private Network)"),
    h2("A private line through a public network", "max-width:24ch"),
    '<div class="rise statement def"><em>VPN</em> &#8212; a technology that creates an encrypted virtual private line (a tunnel) over the Internet, allowing safe connection to a network from a remote location.</div>',
    '<table class="rise" style="margin-top:.9rem">'
    '<tr><th>Main use</th><th>What it means</th></tr>'
    '<tr><td>Remote work</td><td>Connecting safely to the organization&#8217;s network from home or while away</td></tr>'
    '<tr><td>Connecting branches</td><td>Connecting offices in different locations safely</td></tr>'
    '</table>',
    sub("Because the content is encrypted, the risk of <b>eavesdropping</b> is reduced &#8212; even on public Wi-Fi.",
        "max-width:58ch;margin-top:.8rem"),
    ar("الشبكة الافتراضية الخاصة (VPN): اتصال أو شبكة منطقية خاصة عبر شبكة عامة زي الإنترنت، بتستخدم التشفير وتقنيات النفق عشان تحمي البيانات بين الطرفين. استخداماتها: الشغل عن بُعد، وربط الفروع. ولأن المحتوى متشفّر، مخاطر التنصت بتقل حتى على Wi-Fi عام.")))

A(s("",
    eyebrow("2 &#183; Your turn"),
    h2("Which is NOT a use of a VPN?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">Connecting safely from home to an organization&#8217;s network <span class="ans">&#8212; <b>a use</b>: remote work.</span></li>'
    '<li class="reveal rv tf-t">Connecting offices in different locations safely <span class="ans">&#8212; <b>a use</b>: connecting branches.</span></li>'
    '<li class="reveal rv">Automatically deleting files infected with viruses <span class="ans">&#8212; <b>NOT a use</b>: that is antivirus software, on the endpoints.</span></li>'
    '<li class="reveal rv tf-t">Encrypting communication content on public Wi-Fi <span class="ans">&#8212; <b>a use</b>: it reduces eavesdropping.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("أنهي واحد مش استخدام مناسب للـ VPN؟ الحذف التلقائي للملفات المصابة بالفيروسات — ده شغل برنامج مكافحة الفيروسات، مش الـ VPN.")))

# ---------------- part 3: DMZ ----------------

A(s("",
    eyebrow("Part 3 &#183; DMZ (Demilitarized Zone)"),
    h2("Keep public servers in their own zone"),
    '<div class="rise statement def"><em>DMZ</em> &#8212; an area where servers exposed to the external network (web servers, mail servers, etc.) are placed separately from the internal network.</div>',
    fig(DMZ),
    sub("If a public-facing server is attacked, damage to the internal network can be prevented.",
        "max-width:60ch;margin-top:.2rem"),
    ar("المنطقة المعزولة (DMZ): منطقة بتتحط فيها الخوادم المعرّضة للشبكة الخارجية — خوادم الويب والبريد — منفصلة عن الشبكة الداخلية. فصلها بيقلل احتمال إن الهجوم يوصل منها للشبكة الداخلية لو واحد منها اتخرق.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("Why is it safer to place a public web server in a DMZ rather than inside the internal network?",
       "max-width:27ch"),
    ar("وقّف وفكّر: ليه حط خادم ويب عام في المنطقة المعزولة أأمن من حطه جوه الشبكة الداخلية؟")))

# ---------------- part 4: defense in depth ----------------

A(s("",
    eyebrow("Part 4 &#183; Defense in depth"),
    h2("If one layer falls, the next holds"),
    '<div class="rise statement def"><em>Defense in depth</em> &#8212; layering multiple security measures so that, even if one is breached, the next can still protect the system.</div>',
    fig(LAYERS),
    ar("الدفاع في العمق: استخدام طبقات كتير من الضوابط الأمنية، بحيث لو طبقة فشلت، الطبقات التانية تقلل الخطر وتحد من أثر الاختراق. الطبقة 1 مدخل الشبكة: جدار الحماية. الطبقة 2 مسار الاتصال: VPN. الطبقة 3 وضع الخوادم: DMZ. الطبقة 4 الأجهزة الطرفية: برنامج مكافحة فيروسات وتحديث نظام التشغيل.")))

A(s("",
    eyebrow("4 &#183; Your turn"),
    h2("Which layer does each belong to?"),
    '<table class="rise">'
    '<tr><th>Security measure</th><th>Layer</th></tr>'
    '<tr><td>Blocking unauthorized communication with a firewall</td><td class="reveal"><span>1 &#183; Network entry</span></td></tr>'
    '<tr><td>Encrypting communication with a VPN</td><td class="reveal"><span>2 &#183; Communication path</span></td></tr>'
    '<tr><td>Installing antivirus software</td><td class="reveal"><span>4 &#183; Endpoints</span></td></tr>'
    '<tr><td>Separating public-facing servers from the internal network using a DMZ</td><td class="reveal"><span>3 &#183; Server placement</span></td></tr>'
    '</table>',
    ar("لكل إجراء، أنهي طبقة من طبقات الدفاع في العمق؟ جدار الحماية ← مدخل الشبكة. الـ VPN ← مسار الاتصال. مكافحة الفيروسات ← الأجهزة الطرفية. الـ DMZ ← وضع الخوادم.")))

A(s("",
    eyebrow("4 &#183; Exam-style question &#183; 6 marks"),
    h2("Why is layering better than a firewall alone?", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane b"><h3>A firewall alone</h3><ul>'
    '<li>One barrier</li>'
    '<li>If it is breached, <b>everything inside</b> is exposed</li>'
    '</ul></div>'
    '<div class="pane a"><h3>Defense in depth</h3><ul>'
    '<li>Several layers, each with its own measure</li>'
    '<li>If one is breached, <b>the next still protects</b> the system</li>'
    '</ul></div>'
    '</div>',
    sub("Refer to what happens if one measure is breached &#8212; that is the whole answer.", "max-width:60ch;margin-top:.9rem"),
    ar("سؤال على نمط الامتحان: اشرح ليه تكديس إجراءات أمنية في طبقات بيحمي المؤسسة أحسن من الاعتماد على جدار الحماية لوحده. استعن بـ: إيه اللي بيحصل لو إجراء واحد اتخرق.")))

# ---------------- part 5: zero trust ----------------

A(s("",
    eyebrow("Part 5 &#183; The perimeter"),
    h2("The perimeter has blurred", "max-width:24ch"),
    '<div class="rise statement def"><em>Perimeter</em> &#8212; the old boundary built on the idea that &#8220;inside the organization&#8217;s network is safe, and outside is dangerous&#8221;.</div>',
    sub("With cloud services and remote work, the line between <b>inside</b> and <b>outside</b> has blurred, and designs that protect only the perimeter are no longer enough.",
        "max-width:58ch;margin-top:.9rem"),
    ar("أمان الشبكات التقليدي اتصمم أساسًا حوالين حماية المحيط الأمني، على أساس إن \"جوه شبكة المؤسسة آمن، وبرّه خطر\". بس مع انتشار الخدمات السحابية والشغل عن بُعد، الحدود بين \"الداخل\" و\"الخارج\" بقت مش واضحة، والتصاميم اللي بتحمي المحيط بس بقت مش كفاية.")))

A(s("",
    eyebrow("5 &#183; Zero trust"),
    h2("Trust nothing automatically"),
    '<div class="rise statement def"><em>Zero trust</em> &#8212; the system does not trust any communication, including from within the organization&#8217;s network, and always verifies it.</div>',
    fig(TRUST),
    sub("<b>e.g.</b> Even for access from inside the organization, identity verification and access-permission checks are performed every time.",
        "max-width:62ch;margin-top:.2rem"),
    ar("نهج انعدام الثقة: نهج أمني مش بيدّي ثقة تلقائية لمستخدم أو جهاز لمجرد إنه جوه الشبكة أو ملك المؤسسة. الهوية والصلاحيات والسياق بيتفحصوا عند طلب الوصول للموارد، حسب سياسة المؤسسة.")))

A(s("",
    eyebrow("Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">A firewall allows or denies communication based on rules set in advance. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv tf-t">Using a VPN can reduce the risk of eavesdropping even on public Wi-Fi. <span class="ans">&#8212; <b>true</b>: the content is encrypted.</span></li>'
    '<li class="reveal rv">A DMZ is a system that exposes all servers to the outside. <span class="ans">&#8212; <b>false</b>: it keeps public-facing servers apart from the internal network.</span></li>'
    '<li class="reveal rv tf-t">Defense in depth is the concept of layering multiple security measures. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: جدار الحماية بيسمح أو يمنع حسب قواعد — صح. الـ VPN بتقلل التنصت على Wi-Fi عام — صح. المنطقة المعزولة بتعرّض كل الخوادم — غلط. الدفاع في العمق تكديس إجراءات — صح.")))

A(s("",
    eyebrow("Your turn"),
    h2("Which term is it?"),
    '<table class="rise">'
    '<tr><th>Description</th><th>Term</th></tr>'
    '<tr><td>An encrypted virtual private line over the Internet for safe connection from a remote location</td><td class="reveal"><span>VPN</span></td></tr>'
    '<tr><td>An area where servers exposed to the outside are placed separately from the internal network</td><td class="reveal"><span>DMZ</span></td></tr>'
    '<tr><td>A system that allows or denies communication based on rules set in advance</td><td class="reveal"><span>Firewall</span></td></tr>'
    '<tr><td>The old boundary that assumes inside is safe, blurred by cloud and remote work</td><td class="reveal"><span>Perimeter</span></td></tr>'
    '<tr><td>No access is trusted automatically; every request is verified</td><td class="reveal"><span>Zero trust</span></td></tr>'
    '</table>',
    ar("طابق كل وصف بالمصطلح: الخط الخاص الافتراضي المشفر ← VPN. منطقة الخوادم المعزولة ← DMZ. نظام بيسمح أو يمنع ← جدار الحماية. الحدود القديمة ← المحيط الأمني. التحقق من كل وصول ← نهج انعدام الثقة.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Access from within the organization&#8217;s network is safe, so verification is unnecessary. <span class="ans">&#8212; <b>false</b>: zero trust verifies inside access too.</span></li>'
    '<li class="reveal rv">A firewall alone is sufficient to protect the network. <span class="ans">&#8212; <b>false</b>: if it is breached, nothing else stands.</span></li>'
    '<li class="reveal rv">A DMZ is provided to improve communication speed. <span class="ans">&#8212; <b>false</b>: it protects the internal network if a public server is attacked.</span></li>'
    '<li class="reveal rv">Only access from outside needs to be monitored. <span class="ans">&#8212; <b>false</b>: every access is verified.</span></li>'
    '</ul>',
    ar("خلّي بالك، كل الجمل دي غلط: الوصول من جوه آمن فمش محتاج تحقق — غلط. جدار الحماية لوحده كفاية — غلط. الـ DMZ لتحسين السرعة — غلط. نراقب الوصول من برّه بس — غلط.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("Advise a company on its office network", "max-width:26ch"),
    sub("It has a public website, staff who work from home, and confidential customer data. A firewall only &#8212; or a layered design that also verifies every access?",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Collect data.</b> List the three assets (website, remote staff, customer database) and the main threat to each.</li>'
    '<li><b>Rank the layers.</b> Rank network entry, communication path, server placement and endpoints for this company; justify your top choice.</li>'
    '<li><b>Decide.</b> Recommend a design with two reasons why layering is safer. In pairs, agree on the strongest reason.</li>'
    '</ul>',
    sub("Stuck? Start with the most exposed asset &#8212; the public website &#8212; and place it in a DMZ, so an attack there cannot reach the database.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: شركة بتجهز شبكة مكتبها، عندها موقع عام، وموظفين من البيت، وبيانات عملاء سرية. اذكر الأصول التلاتة والتهديد الرئيسي لكل واحد، واربط كل واحد بطبقة الحماية، وبعدين أوصِ بتصميم بسببين. تلميح: حط الخادم العام في المنطقة المعزولة، ومتعتمدش على العزل لوحده.")))

A(s("",
    eyebrow("In a new context"),
    h2("A hospital moves its records to the cloud", "max-width:26ch"),
    sub("Doctors will open patient records from home.", "max-width:54ch;margin-top:.7rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li>Using <b>zero trust</b> and <b>defense in depth</b>, suggest <b>two measures</b>.</li>'
    '<li>Say <b>where each one helps</b>.</li>'
    '<li>Identify <b>one risk that could still remain</b>.</li>'
    '</ul>',
    ar("طبّق اللي اتعلمته: مستشفى بينقل سجلات المرضى لخدمة سحابية، وبيسمح للدكاترة يفتحوها من البيت. باستخدام نهج انعدام الثقة والدفاع في العمق، اقترح إجراءين وبيّن كل واحد بيساعد فين، وحدد خطر واحد ممكن يفضل موجود.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 2-2"),
    h2("Layer your defenses", "max-width:28ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> is a company with a strong firewall safe? What else does it need?</p>'
    '<div class="rise statement">Layer your defenses &#8212; <em>firewall, VPN, DMZ, endpoints</em> &#8212; and verify every access (<em>zero trust</em>). One breach is then far less likely to expose the whole network.</div>',
    ar("افتكر: كدّس دفاعاتك — جدار الحماية، والشبكة الافتراضية الخاصة، والمنطقة المعزولة، والأجهزة الطرفية — واتأكد من كل عملية وصول (نهج انعدام الثقة). ساعتها خرق واحد مش هيكشف الشبكة كلها.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 6"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 6 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers this lesson. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس ده. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))
