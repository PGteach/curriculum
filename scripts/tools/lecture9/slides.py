SLIDES = []
A = SLIDES.append

# 1 title
A(s("dark",
    '<div class="rise eyebrow" id="lectureBadge">Programming &amp; Artificial Intelligence</div>',
    h2("What happens when you click?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("You search YouTube, buy something online, open your e-mail. Behind one simple screen, three parts work together. Today: what they are &#8212; and, on the platform, functions that add and compare values.",
        "max-width:58ch;margin-top:1rem"),
    ar("بتدوّر على يوتيوب، بتشتري أونلاين، بتفتح الإيميل. ورا الشاشة البسيطة دي فيه تلات أجزاء شغالين مع بعض. النهارده هنعرف هما إيه — وعلى المنصة: دوال بتجمع وبتقارن القيم.")))

# 2 unit 3 opens
A(s("",
    eyebrow("Unit 3 &#183; Web applications"),
    h2("A new unit: how the web works", "max-width:24ch"),
    '<div class="rise timeline">'
    '<div class="tl"><h3>3-1 &#183; The overall structure of web applications</h3><p>Today: the three tiers, and how they cooperate</p></div>'
    '<div class="tl"><h3>3-2 &#183; Web application communication methods</h3><p>How the parts talk to each other</p></div>'
    '<div class="tl"><h3>3-3 &#183; Fundamentals of frontend technology</h3><p>HTML, CSS and JavaScript &#8212; what you write on the platform</p></div>'
    '</div>',
    sub("Unit 2 was about protecting systems. Unit 3 asks how the services you use every day are built.", "max-width:58ch;margin-top:.9rem"),
    ar("الوحدة التالتة: تطبيقات الويب. 3-1 البنية العامة لتطبيقات الويب (النهارده)، 3-2 طرق اتصال تطبيقات الويب، 3-3 أساسيات تكنولوجيا الواجهة الأمامية.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("This is already in your hand"),
    h2("Every time you go online", "max-width:22ch"),
    '<div class="rise fields">'
    '<span class="chip">&#9654; search on YouTube</span>'
    '<span class="chip">&#128722; buy on Amazon</span>'
    '<span class="chip">&#9993; open Gmail</span>'
    '<span class="chip">&#128506; find a place on Google Maps</span>'
    '</div>',
    sub("&#8230; you are using a <b>web application</b> &#8212; a program you use through your browser. Behind the simple screen, three tiers work together: the page you touch, a hidden server that processes your request, and a database that holds all the data.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> when you search YouTube, where do you think the videos are kept &#8212; on your phone, or somewhere else? Remember your answer.</p></div>',
    ar("لما بتدوّر في موقع فيديو، أو بتتسوق أونلاين، أو بتستخدم إيميل على الويب، إنت بتستخدم تطبيق ويب. وورا اللي بتشوفه فيه أجزاء مختلفة شغالة مع بعض.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("How is a web application structured, and how do its three tiers work together to respond to what a user does?",
       "max-width:28ch"),
    ar("السؤال الرئيسي: إزاي بيتبني تطبيق الويب، وإزاي طبقاته التلاتة بتشتغل مع بعض عشان تستجيب للي المستخدم بيعمله؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map &#183; four parts"),
    h2("Three parts from the book, one on the platform", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#127760;</div><div class="role">Part 1</div>'
    '<h3>Web application</h3><p>What it is</p></div>'
    '<div class="card"><div class="ico">&#127970;</div><div class="role">Part 2</div>'
    '<h3>Three tiers</h3><p>Frontend, backend, database</p></div>'
    '<div class="card"><div class="ico">&#128260;</div><div class="role">Part 3</div>'
    '<h3>Working together</h3><p>From your click to the result</p></div>'
    '<div class="card"><div class="ico">&#129380;</div><div class="role">Part 4 &#183; Qureo</div>'
    '<h3>Functions (4)</h3><p>Add and compare values</p></div>'
    '</div>',
    ar("خريطة المحاضرة: 1 يعني إيه تطبيق ويب. 2 الطبقات التلاتة. 3 إزاي بيتعاونوا من ضغطتك لحد النتيجة. 4 على المنصة: الدوال (4).")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("You type <b>red shoes</b> in the search box of a shopping site and press Enter. A second later, a page of red shoes appears.",
        "max-width:56ch;margin-top:1rem"),
    sub("With your partner: <b>who read your words? who found the shoes? where were the shoes kept?</b> Write three guesses.",
        "max-width:56ch;margin-top:.8rem"),
    sub("Keep your guesses. Part 3 shows the book&#8217;s answer, step by step.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: كتبت «red shoes» في موقع تسوق ودوست Enter، وبعد ثانية ظهرت صفحة جزم حمرا. مين قرا الكلام؟ ومين لقى الجزم؟ والجزم كانت متخزنة فين؟ اكتبوا تلات تخمينات.")))

# ---------------- part 1: what is a web application ----------------

A(s("",
    eyebrow("Part 1 &#183; What is a web application?"),
    h2("What is a web application?", "max-width:24ch"),
    '<div class="rise statement def"><em>Web application</em> &#8212; an application used through a web browser. You can use it as long as you have a browser, without installing dedicated software.</div>',
    sub("<i>e.g.</i> YouTube, Amazon, Gmail, Google Maps.", "max-width:58ch;margin-top:.8rem"),
    sub("The Arabic book adds: some web applications can <b>also</b> be installed on the device.", "max-width:58ch;margin-top:.5rem;color:var(--soft)"),
    ar("تطبيق الويب: تطبيق بيتستخدم عادةً من خلال متصفح الويب، وبعض تطبيقات الويب ممكن كمان تتثبت على الجهاز. أمثلة: خدمات الفيديو والتسوق والبريد والخرائط على الويب.")))

A(s("",
    eyebrow("1 &#183; Your turn"),
    h2("Which one is a web application?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">A video player on the device <span class="ans">&#8212; <b>no</b>: it runs on the device, not through a browser.</span></li>'
    '<li class="reveal rv">A maps website on the Internet <span class="ans">&#8212; <b>yes</b>: you use it through the browser.</span></li>'
    '<li class="reveal rv">A calculator app on the desktop <span class="ans">&#8212; <b>no</b>: installed on the computer.</span></li>'
    '<li class="reveal rv">A photo-editing program <span class="ans">&#8212; <b>no</b>: installed software.</span></li>'
    '</ul>',
    sub("Think first, then tap each one.", "margin-top:.7rem;color:var(--soft)"),
    ar("أنهي واحد تطبيق ويب؟ موقع خرائط على الإنترنت — لأنه بيتستخدم من خلال المتصفح. الباقي برامج متثبتة على الجهاز.")))

# ---------------- part 2: the three tiers ----------------

A(s("",
    eyebrow("Part 2 &#183; The three tiers of a web application"),
    h2("Three tiers, one application"),
    fig(TIERS),
    sub("A web application is broadly built from <b>three tiers</b>: the <b>frontend</b>, the <b>backend</b> and the <b>database</b>. This is called the <b>three-tier architecture</b>.",
        "max-width:62ch;margin-top:.3rem"),
    ar("في النموذج التعليمي ده، بنقسم تطبيق الويب لتلات أجزاء رئيسية: الواجهة الأمامية، والواجهة الخلفية، وقاعدة البيانات — ودي اسمها بنية الطبقات الثلاث.")))

A(s("",
    eyebrow("2 &#183; What each tier does"),
    h2("Who does what?"),
    '<table class="rise">'
    '<tr><th>Tier</th><th>Role</th><th>Examples</th></tr>'
    '<tr><td><b>Frontend</b></td><td>The screen users see directly. It runs on the browser and accepts user input.</td><td>Search screen, product listing pages, input forms</td></tr>'
    '<tr><td><b>Backend</b></td><td>The server-side processing users do not see. It processes data and makes decisions.</td><td>Searching for products that match, login authentication</td></tr>'
    '<tr><td><b>Database</b></td><td>Organizes, stores and manages data. It retrieves data when needed and records new data.</td><td>Product information, user information, order history</td></tr>'
    '</table>',
    ar("الواجهة الأمامية: الجزء اللي المستخدم بيشوفه ويتعامل معاه في المتصفح؛ بتعرض المحتوى وبتستقبل اللي بيكتبه. الواجهة الخلفية: الجزء اللي بيشتغل على الخادم، وبيعالج الطلبات ويطبق قواعد التطبيق. قاعدة البيانات: طبقة بتحفظ البيانات وتوفرها وقت الحاجة.")))

A(s("",
    eyebrow("2 &#183; A way to remember"),
    h2("A way to remember: a restaurant", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>In a restaurant</th><th>In a web application</th></tr>'
    '<tr><td>&#129333; The <b>waiter</b> you talk to: takes your order, brings your plate</td><td><b>Frontend</b> &#8212; shows and collects</td></tr>'
    '<tr><td>&#128104;&#8205;&#127859; The <b>kitchen</b> you never see: decides and cooks</td><td><b>Backend</b> &#8212; decides and processes</td></tr>'
    '<tr><td>&#129482; The <b>storeroom</b>: keeps the food, hands it over</td><td><b>Database</b> &#8212; stores and retrieves</td></tr>'
    '</table>',
    sub("The restaurant is ours, not the book&#8217;s. The three phrases on the right are the book&#8217;s &#8212; learn those.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر في مطعم: الجرسون اللي بتكلمه = الواجهة الأمامية (بتعرض وتجمع). المطبخ اللي مش بتشوفه = الواجهة الخلفية (بتقرر وتعالج). المخزن = قاعدة البيانات (بتخزن وتسترجع).")))

A(s("",
    eyebrow("2 &#183; Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">The frontend is the screen component that users see directly. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv">The backend is the part that runs on the browser. <span class="ans">&#8212; <b>false</b>: it runs on the server.</span></li>'
    '<li class="reveal rv tf-t">A database is a system that organizes, stores and manages data. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv">A web application operates with the frontend alone. <span class="ans">&#8212; <b>false</b>: it needs all three tiers.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: الواجهة الأمامية الشاشة اللي بنشوفها — صح. الواجهة الخلفية بتشتغل على المتصفح — غلط، على الخادم. قاعدة البيانات بتنظم وتخزن وتدير البيانات — صح. تطبيق الويب بيشتغل بالواجهة الأمامية لوحدها — غلط.")))

A(s("",
    eyebrow("2 &#183; Exam-style question"),
    h2("Match each description with a tier"),
    '<table class="rise">'
    '<tr><th>Description</th><th>Tier</th></tr>'
    '<tr><td>a &#183; The part responsible for server-side processing that users do not see</td><td class="reveal"><span>B &#183; Backend</span></td></tr>'
    '<tr><td>b &#183; The screen component that users interact with directly</td><td class="reveal"><span>A &#183; Frontend</span></td></tr>'
    '<tr><td>c &#183; A system that organizes, stores and manages data</td><td class="reveal"><span>C &#183; Database</span></td></tr>'
    '</table>',
    sub("Choices: <b>A</b> Frontend &#183; <b>B</b> Backend &#183; <b>C</b> Database. Answer, then tap.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("اربط كل وصف بالمصطلح المناسب: المعالجة من جانب الخادم = الواجهة الخلفية. الشاشة اللي بنتعامل معاها = الواجهة الأمامية. تخزين البيانات وإدارتها = قاعدة البيانات.")))

# ---------------- part 3: how the tiers cooperate ----------------

A(s("",
    eyebrow("Part 3 &#183; The flow of how the three tiers cooperate"),
    h2("Watch a search travel", "max-width:24ch"),
    sub("Searching for a product on an online shopping site. Press <b>Next step</b>:", "max-width:60ch;margin-top:.4rem"),
    flow([
        {"t": "fe", "msg": "red shoes", "en": "① The frontend receives the search keywords entered by the user.",
         "ar": "① الواجهة الأمامية بتستقبل كلمات البحث اللي المستخدم كتبها."},
        {"t": "be", "msg": "keywords: red shoes", "en": "② The frontend sends the search keywords to the backend.",
         "ar": "② الواجهة الأمامية بتبعت كلمات البحث للواجهة الخلفية."},
        {"t": "db", "msg": "find: red shoes", "en": "③ The backend searches the database for products that match the criteria.",
         "ar": "③ الواجهة الخلفية بتطلب من طبقة البيانات المنتجات اللي بتطابق البحث."},
        {"t": "be", "msg": "3 matching products", "en": "④ The database returns the data of the matching products to the backend.",
         "ar": "④ طبقة البيانات بترجّع النتايج المطلوبة للواجهة الخلفية."},
        {"t": "fe", "msg": "organized results", "en": "⑤ The backend organizes the search results and returns them to the frontend.",
         "ar": "⑤ الواجهة الخلفية بتجهز النتايج وتبعتها للواجهة الأمامية."},
        {"t": "fe", "msg": "on your screen", "en": "⑥ The frontend displays the search results on the user's screen.",
         "ar": "⑥ الواجهة الأمامية بتعرض نتايج البحث على شاشة المستخدم."},
    ]),
    ar("الطلب بينزل عبر الطبقات، والرد بيرجع تاني. دوس Next step وتابع الطلب خطوة خطوة.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("When you type in a search box and see results, which tier collected your input, and which tier found the answer?",
       "max-width:28ch"),
    '<ul class="rise check" style="margin-top:1rem">'
    '<li class="reveal rv">Collected your input <span class="ans">&#8212; the <b>frontend</b>.</span></li>'
    '<li class="reveal rv">Found the answer <span class="ans">&#8212; the <b>backend</b> searched the <b>database</b>, which held the data.</span></li>'
    '</ul>',
    ar("وقّف وفكّر: لما بتكتب في مربع البحث وتشوف النتايج، أنهي طبقة جمعت المدخلات، وأنهي طبقة لقت الإجابة؟")))

A(s("",
    eyebrow("3 &#183; Familiar web application configurations"),
    h2("Every service, the same three tiers", "max-width:26ch"),
    '<table class="rise">'
    '<tr><th>Service</th><th>Frontend (display, interaction)</th><th>Backend (processing, control)</th><th>Database (storage, management)</th></tr>'
    '<tr><td><b>Video sharing</b></td><td>Video playback and search screens</td><td>Choosing recommended videos; counting views</td><td>Video data, user information, viewing history</td></tr>'
    '<tr><td><b>SNS</b></td><td>Timeline and post screens; sending what you type</td><td>Deciding who sees a post; push notifications</td><td>Posts, follow relationships, messages</td></tr>'
    '<tr><td><b>E-commerce</b></td><td>Product listings and cart screens; taking orders</td><td>Checking stock; running payments</td><td>Products, order history, customer information</td></tr>'
    '</table>',
    sub("<b>Pause and think:</b> every service uses the same three tiers &#8212; what changes from one service to the next?", "max-width:62ch;margin-top:.8rem"),
    ar("تقريبًا كل خدمة على الإنترنت — الفيديو، والتواصل الاجتماعي، والتسوق — مبنية على نفس الطبقات التلاتة: واجهة أمامية بتعرض وتجمع، وواجهة خلفية بتقرر وتعالج، وقاعدة بيانات بتخزن وتسترجع.")))

A(s("",
    eyebrow("3 &#183; Your turn"),
    h2("An e-commerce site: which tier?"),
    '<table class="rise">'
    '<tr><th>Part of the site</th><th>Tier</th></tr>'
    '<tr><td>a &#183; Product listing page</td><td class="reveal"><span>A &#183; Frontend</span></td></tr>'
    '<tr><td>b &#183; Stock checking</td><td class="reveal"><span>B &#183; Backend</span></td></tr>'
    '<tr><td>c &#183; Storage of customer information</td><td class="reveal"><span>C &#183; Database</span></td></tr>'
    '<tr><td>d &#183; Cart screen</td><td class="reveal"><span>A &#183; Frontend</span></td></tr>'
    '<tr><td>e &#183; Payment processing</td><td class="reveal"><span>B &#183; Backend</span></td></tr>'
    '<tr><td>f &#183; Storage of order history</td><td class="reveal"><span>C &#183; Database</span></td></tr>'
    '</table>',
    sub("A screen &#8594; frontend. Processing &#8594; backend. Storage &#8594; database.", "max-width:58ch;margin-top:.7rem;color:var(--soft)"),
    ar("لكل جزء من موقع التجارة الإلكترونية، حدد الطبقة: شاشة ← واجهة أمامية. معالجة ← واجهة خلفية. تخزين ← قاعدة بيانات.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">The frontend has the role of storing and managing data. <span class="ans">&#8212; <b>false</b>: that is the database.</span></li>'
    '<li class="reveal rv">The backend is the part users interact with directly on the browser. <span class="ans">&#8212; <b>false</b>: that is the frontend.</span></li>'
    '<li class="reveal rv">The database has the role of displaying screens to users. <span class="ans">&#8212; <b>false</b>: the frontend displays.</span></li>'
    '<li class="reveal rv tf-t">When you search a shop, the <b>backend</b> sends the request to the database. <span class="ans">&#8212; <b>true</b>: the frontend never asks the database itself.</span></li>'
    '</ul>',
    ar("خلّي بالك: الواجهة الأمامية مش بتخزن البيانات. الواجهة الخلفية مش اللي بنتعامل معاها في المتصفح. قاعدة البيانات مش بتعرض شاشات. واللي بيبعت الطلب لقاعدة البيانات هي الواجهة الخلفية.")))

A(s("",
    eyebrow("3 &#183; Exam-style question &#183; 6 marks"),
    h2("Posting a photo on a social media app", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Explain&#8230;</h3><ul>'
    '<li>how the <b>three tiers</b> cooperate when a user posts a photo</li>'
    '<li>refer to the role of the <b>frontend</b>, the <b>backend</b> and the <b>database</b></li>'
    '</ul></div>'
    '<div class="pane b"><h3>A plan for your answer</h3><ul>'
    '<li>frontend: takes the photo and the caption, sends them</li>'
    '<li>backend: checks it, decides who sees it</li>'
    '<li>database: stores it &#8212; then the reply comes back</li>'
    '</ul></div>'
    '</div>',
    ar("سؤال على نمط الامتحان: اشرح إزاي الطبقات التلاتة لتطبيق الويب بتتعاون لما المستخدم ينشر صورة على تطبيق تواصل اجتماعي. أشِر إلى: دور الواجهة الأمامية، والواجهة الخلفية، وقاعدة البيانات.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("A clinic wants a booking app", "max-width:26ch"),
    sub("Patients book appointments, check which time slots are free, and see their past visits. You plan its three tiers.",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Assign the work.</b> The booking form, checking free time slots, storing past visits: which tier does each, and why?</li>'
    '<li><b>Diagnose a fault.</b> The booking page opens, but no free slots appear. Which tier is clearly working, and which has probably failed?</li>'
    '<li><b>Decide.</b> Should the clinic separate its app into three tiers? Two reasons. In pairs, agree where checking free slots belongs.</li>'
    '</ul>',
    sub("Stuck? The frontend shows and collects; the backend decides and processes; the database stores and retrieves.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: عيادة عايزة تطبيق ويب للحجز. وزّع المهام على الطبقات، وشخّص العطل: صفحة الحجز بتفتح بس مفيش مواعيد بتظهر. وقرّر: نفصل الطبقات ولا لأ، بسببين.")))

A(s("",
    eyebrow("In a new context"),
    h2("A weather app", "max-width:26ch"),
    sub("Users type a city and see the forecast.", "max-width:54ch;margin-top:.7rem"),
    '<table class="rise">'
    '<tr><th>Job</th><th>Tier</th></tr>'
    '<tr><td>Taking the city name</td><td class="reveal"><span>Frontend</span></td></tr>'
    '<tr><td>Looking up the forecast data</td><td class="reveal"><span>Backend</span></td></tr>'
    '<tr><td>Storing past forecasts</td><td class="reveal"><span>Database</span></td></tr>'
    '</table>',
    sub("And one job the frontend <b>cannot</b> do on its own? Discuss, then compare.", "max-width:58ch;margin-top:.8rem"),
    ar("طبّق اللي اتعلمته: تطبيق طقس بيخليك تكتب اسم مدينة وتشوف التوقعات. سمّي أنهي طبقة بتعمل كل مهمة، وحدد مهمة واحدة الواجهة الأمامية متقدرش تعملها لوحدها.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 3-1"),
    h2("Show, decide, store", "max-width:24ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> where are the YouTube videos kept? On your phone &#8212; or in a database, reached through the backend?</p>'
    '<div class="rise statement">The frontend <em>shows and collects</em>, the backend <em>decides and processes</em>, the database <em>stores and retrieves</em> &#8212; three tiers cooperating make a web application work.</div>',
    sub("The Arabic book adds: this is a simplified teaching model. Real applications can be built differently.", "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("افتكر: الواجهة الأمامية بتعرض وتجمع، والواجهة الخلفية بتقرر وتعالج، وقاعدة البيانات بتخزن وتسترجع — تلات طبقات متعاونة بتخلي تطبيق الويب يشتغل. وده نموذج تعليمي مبسط، والبنية الفعلية ممكن تختلف.")))

# ---------------- part 4: Qureo chapter 31, Functions (4) ----------------

A(s("dark",
    '<div class="rise part">4</div>',
    h2("On the platform: Functions (4)"),
    sub("Qureo chapter 31: a function that adds two values, one that adds three, and one that compares three.", "max-width:56ch"),
    ar("الجزء الرابع على المنصة: الفصل 31 — الدوال (4): دالة بتجمع قيمتين، ودالة بتجمع تلاتة، ودالة بتقارن بين تلاتة.")))

A(s("",
    eyebrow("4 &#183; Remember"),
    h2("A function is a small machine", "max-width:22ch"),
    '<div class="rise code">' + K("function") + " " + F("name") + "(argumentName) {\n  <span class=\"c\">// processing</span>\n  " + K("return") + " result;\n}</div>",
    '<table class="rise">'
    '<tr><th>Word</th><th>Meaning</th></tr>'
    '<tr><td><b>argument</b></td><td>the value you pass <b>into</b> the function</td></tr>'
    '<tr><td><b>return value</b></td><td>the value the function gives <b>back</b> with <span class="codeline">return</span></td></tr>'
    '</table>',
    sub("Like the tiers: <b>receive</b> &#8594; <b>process</b> &#8594; <b>give back</b>.", "max-width:56ch;margin-top:.7rem"),
    ar("الدالة زي ماكينة العصير: بتحط فيها فاكهة (الوسيط)، بتشتغل جوّه (المعالجة)، وبتطلّع عصير (القيمة المرجعة) بـ return. ونفس فكرة الطبقات: تستقبل ← تعالج ← ترجّع.")))

ADD_LINES = [K("function") + " " + F("add") + "(a, b) {",
             "  " + K("return") + " a + b;",
             "}",
             "",
             LOG + "(" + F("add") + "(" + Nn("3") + ", " + Nn("5") + "));"]
A(s("",
    eyebrow("4 &#183; A function to add two values"),
    h2("add(3, 5): watch it run"),
    tracer(ADD_LINES, ["a", "b", "return"], [
        {"ln": 4, "en": "The program reaches the call add(3, 5). The function above only runs when it is called.",
         "ar": "البرنامج وصل لاستدعاء add(3, 5). الدالة اللي فوق مش بتشتغل غير لما تتنادى."},
        {"ln": 0, "set": {"a": "3", "b": "5"}, "en": "The arguments go in: a = 3 and b = 5.",
         "ar": "الوسائط بتدخل: a = 3 و b = 5."},
        {"ln": 1, "set": {"return": "8"}, "en": "a + b is 3 + 5 = 8, and return sends 8 back.",
         "ar": "‏a + b يعني 3 + 5 = 8، و return بترجّع 8."},
        {"ln": 4, "out": "8", "en": "add(3, 5) becomes its return value, 8, and console.log prints it.",
         "ar": "‏add(3, 5) بتتحول لقيمتها المرجعة 8، و console.log بيطبعها."},
    ]),
    ar("دوس Next step: الوسائط بتدخل، الدالة بتجمع، و return بترجّع النتيجة لمكان الاستدعاء.")))

A(s("",
    eyebrow("4 &#183; A function that adds three values"),
    h2("Three arguments, one return value"),
    '<div class="rise code">' + K("function") + " " + F("add3") + "(a, b, c) {\n  " + K("return") + " a + b + c;\n}\n\n"
    + LOG + "(" + F("add3") + "(" + Nn("2") + ", " + Nn("4") + ", " + Nn("6") + "));\n"
    + LOG + "(" + F("add3") + "(" + Nn("10") + ", " + Nn("20") + ", " + Nn("30") + "));</div>",
    '<ul class="rise check">'
    '<li class="reveal rv">The first line prints&#8230; <span class="ans">&#8212; <b>12</b> (2 + 4 + 6)</span></li>'
    '<li class="reveal rv">The second line prints&#8230; <span class="ans">&#8212; <b>60</b> (10 + 20 + 30)</span></li>'
    '<li class="reveal rv">How many arguments does add3 take? <span class="ans">&#8212; <b>three</b>, separated by commas.</span></li>'
    '</ul>',
    ar("نفس الفكرة بتلات وسائط مفصولين بفواصل. فكّر الأول، وبعدين دوس على كل سطر.")))

BIG_LINES = [K("function") + " " + F("biggest") + "(a, b, c) {",
             "  " + K("let") + " big = a;",
             "  " + K("if") + " (b > big) {",
             "    big = b;",
             "  }",
             "  " + K("if") + " (c > big) {",
             "    big = c;",
             "  }",
             "  " + K("return") + " big;",
             "}",
             "",
             LOG + "(" + F("biggest") + "(" + Nn("4") + ", " + Nn("9") + ", " + Nn("7") + "));"]
A(s("",
    eyebrow("4 &#183; A function that compares three values"),
    h2("Which is the biggest?"),
    tracer(BIG_LINES, ["a", "b", "c", "big", "return"], [
        {"ln": 11, "en": "The call biggest(4, 9, 7) starts the function.", "ar": "الاستدعاء biggest(4, 9, 7) بيشغّل الدالة."},
        {"ln": 0, "set": {"a": "4", "b": "9", "c": "7"}, "en": "The arguments go in: a = 4, b = 9, c = 7.", "ar": "الوسائط بتدخل: a = 4 و b = 9 و c = 7."},
        {"ln": 1, "set": {"big": "4"}, "en": "Start by saying the first one is the biggest: big = 4.", "ar": "نبدأ ونقول إن الأولاني هو الأكبر: big = 4."},
        {"ln": 2, "en": "Is b > big? 9 > 4 is true, so go inside.", "ar": "هل b > big؟ ‏9 > 4 صح، فندخل جوّه."},
        {"ln": 3, "set": {"big": "9"}, "en": "big becomes 9.", "ar": "‏big بقت 9."},
        {"ln": 5, "en": "Is c > big? 7 > 9 is false, so skip it.", "ar": "هل c > big؟ ‏7 > 9 غلط، فنعدّيها."},
        {"ln": 8, "set": {"return": "9"}, "en": "return sends back big, which is 9.", "ar": "‏return بترجّع big، اللي هي 9."},
        {"ln": 11, "out": "9", "en": "console.log prints 9, the biggest of the three.", "ar": "‏console.log بيطبع 9، أكبر واحد في التلاتة."},
    ]),
    ar("الدالة بتقارن التلات قيم بـ if — زي اللي اتعلمناه في المحاضرة 8 — وبترجّع الأكبر.")))

A(s("",
    eyebrow("4 &#183; A shortcut you already know"),
    h2("Math.max can take three values"),
    '<div class="rise code">' + LOG + "(" + F("Math.max") + "(" + Nn("4") + ", " + Nn("9") + ", " + Nn("7") + "));\n"
    + LOG + "(" + F("Math.min") + "(" + Nn("4") + ", " + Nn("9") + ", " + Nn("7") + "));</div>",
    '<ul class="rise check">'
    '<li class="reveal rv">Math.max(4, 9, 7) prints&#8230; <span class="ans">&#8212; <b>9</b>, the same as biggest.</span></li>'
    '<li class="reveal rv">Math.min(4, 9, 7) prints&#8230; <span class="ans">&#8212; <b>4</b>, the smallest.</span></li>'
    '</ul>',
    sub("Qureo chapter 12 used Math.max(A, B) with two values. It works with three too. Writing biggest yourself shows <b>how</b> it decides.",
        "max-width:58ch;margin-top:.7rem;color:var(--soft)"),
    ar("اتعلمنا Math.max و Math.min على قيمتين في الفصل 12، وهما بيشتغلوا على تلاتة كمان. بس لما تكتب biggest بنفسك بتفهم بتقرر إزاي.")))

A(s("",
    eyebrow("4 &#183; Watch out"),
    h2("A function with no return", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>&#10060; Forgot return</h3>'
    '<div class="code" style="font-size:clamp(11px,1.35vw,16px)">' + K("function") + " " + F("add") + "(a, b) {\n  a + b;\n}\n" + LOG + "(" + F("add") + "(" + Nn("3") + ", " + Nn("5") + "));</div></div>"
    '<div class="pane b"><h3>&#9989; With return</h3>'
    '<div class="code" style="font-size:clamp(11px,1.35vw,16px)">' + K("function") + " " + F("add") + "(a, b) {\n  " + K("return") + " a + b;\n}\n" + LOG + "(" + F("add") + "(" + Nn("3") + ", " + Nn("5") + "));</div></div>"
    '</div>',
    '<ul class="rise check">'
    '<li class="reveal rv">What does the left one print? <span class="ans">&#8212; <b>undefined</b>: it added, but gave nothing back. A juice machine with no cup.</span></li>'
    '</ul>',
    ar("خلّي بالك: من غير return الدالة بتحسب بس مش بترجّع حاجة، فبيطبع undefined — زي ماكينة عصير من غير كوباية.")))

A(s("dark",
    eyebrow("Remember these"),
    h2("What we learned"),
    '<ul class="rise check">'
    '<li>A <b>web application</b> is used through a browser.</li>'
    '<li><b>Frontend</b> shows and collects; <b>backend</b> decides and processes; <b>database</b> stores and retrieves.</li>'
    '<li>A request flows down the tiers, and the reply comes back up.</li>'
    '<li>A <b>function</b> takes <b>arguments</b>, processes them, and gives back a <b>return value</b> &#8212; two values, three, or the biggest of three.</li>'
    '</ul>',
    ar("تطبيق الويب بيتستخدم من المتصفح • تلات طبقات: تعرض وتجمع، تقرر وتعالج، تخزن وتسترجع • الطلب بينزل والرد بيطلع • الدالة بتاخد وسائط وترجّع قيمة.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 9"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 9 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers lesson 3-1 and Qureo chapter 31. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس 3-1 والفصل 31 على المنصة. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))