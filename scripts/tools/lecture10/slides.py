SLIDES = []
A = SLIDES.append

# 1 title
A(s("dark",
    '<div class="rise eyebrow" id="lectureBadge">Programming &amp; Artificial Intelligence</div>',
    h2("How do they talk?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("Your phone does not hold the whole website &#8212; it asks for it. Today: the request, the response, and the rules they follow. On the platform: flowcharts.",
        "max-width:58ch;margin-top:1rem"),
    ar("موبايلك مش شايل الموقع كله — هو بيطلبه. النهارده: الطلب، والاستجابة، والقواعد اللي بيمشوا عليها. وعلى المنصة: المخططات الانسيابية.")))

# 2 recap -- lesson 3-1, and the Arabic book's bridge
A(s("",
    eyebrow("Before we start &#183; Lesson 3-1"),
    h2("Last time: three tiers", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>Tier</th><th>Its job</th></tr>'
    '<tr><td><b>Frontend</b></td><td>shows and collects</td></tr>'
    '<tr><td><b>Backend</b></td><td>decides and processes</td></tr>'
    '<tr><td><b>Database</b></td><td>stores and retrieves</td></tr>'
    '</table>',
    sub("They cooperate by sending messages. Today: <b>how</b> those messages travel &#8212; the request and the response.", "max-width:60ch;margin-top:.9rem"),
    ar("في الدرس 3-1 اتعلمت إن الواجهة الأمامية والواجهة الخلفية بيتعاونوا عشان ينفذوا طلب المستخدم. في الدرس ده هتتعلم إزاي الطلبات والاستجابات بتتنقل بين العميل والخادم.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("This happens every time you click"),
    h2("Your device asks, a server answers", "max-width:22ch"),
    sub("When you click a link or press &#8220;search&#8221;, your device does not hold the whole website &#8212; it asks a distant computer for it. Your browser is the <b>client</b> that makes the <b>request</b>; a <b>server</b> somewhere answers with a <b>response</b>. Shared rules called <b>protocols</b> govern the exchange.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> you see a page that says <b>404</b>. Is the Internet broken, is the server broken &#8212; or something else? Remember your answer.</p></div>',
    ar("لما بتدوس على لينك أو بتبدأ بحث، المتصفح غالبًا بيطلب البيانات اللي محتاجها من خدمة على خادم عبر الشبكة. المتصفح هنا عميل (client) بيبعت طلب، والخادم (server) بيرجّع استجابة، وبروتوكولات زي HTTP بتحدد قواعد التبادل ده.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("How do the client and server communicate to make a web application work, and what rules and messages do they use?",
       "max-width:28ch"),
    ar("السؤال الرئيسي: إزاي العميل والخادم بيتواصلوا عشان يشغّلوا تطبيق الويب، وإيه القواعد والرسائل اللي بيستخدموها؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map"),
    h2("Four parts from the book, two on the platform", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#128101;</div><div class="role">Part 1</div><h3>Client and server</h3><p>Who asks, who answers</p></div>'
    '<div class="card"><div class="ico">&#128274;</div><div class="role">Part 2</div><h3>HTTP and HTTPS</h3><p>The rules, and the lock</p></div>'
    '<div class="card"><div class="ico">&#128232;</div><div class="role">Part 3</div><h3>Requests and responses</h3><p>GET, POST, 200, 404, 500</p></div>'
    '<div class="card"><div class="ico">&#128279;</div><div class="role">Part 4</div><h3>API and JSON</h3><p>Programs sharing data</p></div>'
    '<div class="card"><div class="ico">&#128200;</div><div class="role">Qureo 32 &#183; 33</div><h3>Flowcharts</h3><p>Draw a program, then review</p></div>'
    '</div>',
    ar("خريطة المحاضرة: 1 العميل والخادم. 2 HTTP و HTTPS. 3 الطلبات والاستجابات: GET و POST ورموز الحالة. 4 API و JSON. وعلى المنصة: الفصل 32 المخطط الانسيابي، والفصل 33 مراجعة.")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("You open YouTube on your phone and search <b>cats</b>. With your partner, write down:",
        "max-width:56ch;margin-top:1rem"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>What does your phone <b>send</b>?</li>'
    '<li>What comes <b>back</b>?</li>'
    '<li>When you log in, should your password travel as it is &#8212; or locked?</li>'
    '</ul>',
    sub("Keep your answers. Part 3 shows the book&#8217;s, step by step.", "margin-top:.8rem;color:var(--soft)"),
    ar("مع زميلك: فتحت يوتيوب على الموبايل ودوّرت على cats. موبايلك بيبعت إيه؟ وإيه اللي بيرجع؟ ولما بتسجل دخول، الباسورد يمشي زي ما هو ولا متقفل؟")))

# ---------------- part 1: client and server ----------------

A(s("",
    eyebrow("Part 1 &#183; Client and server"),
    h2("Who asks, who answers"),
    fig(CLIENTSERVER),
    '<table class="rise">'
    '<tr><th>Term</th><th>Meaning</th></tr>'
    '<tr><td><b>Client</b></td><td>The side that requests data or processing from the server. Web browsers and smartphone apps.</td></tr>'
    '<tr><td><b>Server</b></td><td>The side that receives requests from clients, processes them, and returns responses.</td></tr>'
    '</table>',
    ar("العميل: برنامج أو جهاز بيبعت طلب لخدمة تانية، زي متصفح الويب وتطبيق الموبايل. الخادم: الجانب اللي بيستقبل الطلبات من العملاء، ويعالجها، ويرجّع الاستجابات. وكتير من تطبيقات الويب بتعتمد على إن العميل يبعت طلب والخادم يرجّع استجابة.")))

A(s("",
    eyebrow("1 &#183; Your turn"),
    h2("Client or server?"),
    '<table class="rise">'
    '<tr><th>Who is it?</th><th>Answer</th></tr>'
    '<tr><td>Your web browser asking for a page</td><td class="reveal"><span>Client</span></td></tr>'
    '<tr><td>The computer that receives the request, processes it and sends back the page</td><td class="reveal"><span>Server</span></td></tr>'
    '<tr><td>A smartphone app asking for today&#8217;s weather</td><td class="reveal"><span>Client</span></td></tr>'
    '</table>',
    sub("The one that <b>asks</b> is the client; the one that <b>answers</b> is the server. Tap to check.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("اللي بيطلب هو العميل، واللي بيرد هو الخادم. فكّر الأول وبعدين دوس.")))

# ---------------- part 2: HTTP and HTTPS ----------------

A(s("",
    eyebrow("Part 2 &#183; HTTP and HTTPS"),
    h2("A postcard or a sealed envelope", "max-width:24ch"),
    '<div class="rise statement def"><em>HTTP</em> (HyperText Transfer Protocol) &#8212; a communication protocol for exchanging data between clients and servers.</div>',
    '<div class="rise statement def" style="margin-top:.7rem"><em>HTTPS</em> (HTTP Secure) &#8212; HTTP with <em>TLS encryption</em> added. The content is encrypted, so the risk of it being read by others is reduced.</div>',
    sub("Addresses that begin with <span class=\"codeline\">https://</span> use HTTPS. The Arabic book adds: TLS also stops the content being <b>changed</b> on the way, and checks it is the <b>real server</b>.",
        "max-width:58ch;margin-top:.8rem"),
    ar("HTTP: بروتوكول بيستخدم لتبادل الرسائل بين عميل وخادم على الويب. HTTPS: استخدام HTTP عبر اتصال TLS آمن؛ بيحمي سرية الاتصال وسلامته، وبيتحقق من الخادم، فالمتجسس ميقدرش يقرا المحتوى أو يعدّله بسهولة. والمواقع اللي عناوينها بتبدأ بـ https:// بتستخدم HTTPS.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("Why should a login page use HTTPS rather than plain HTTP?", "max-width:24ch"),
    '<ul class="rise check" style="margin-top:1rem">'
    '<li class="reveal rv">Because&#8230; <span class="ans">&#8212; the password is <b>encrypted</b> on the way, so someone listening on the network cannot read it. With plain HTTP it travels as it is.</span></li>'
    '</ul>',
    ar("وقّف وفكّر: ليه صفحة تسجيل الدخول لازم تستخدم HTTPS بدل HTTP العادي؟")))

# ---------------- part 3: requests and responses ----------------

A(s("",
    eyebrow("Part 3 &#183; The request: an HTTP method"),
    h2("GET or POST?"),
    sub("Every request carries an <b>HTTP method</b>: what kind of operation is wanted.", "max-width:58ch;margin-top:.4rem"),
    '<table class="rise">'
    '<tr><th>Method</th><th>Role</th><th>Examples</th></tr>'
    '<tr><td><b>GET</b></td><td>Retrieve data from the server</td><td>Displaying a web page, retrieving search results</td></tr>'
    '<tr><td><b>POST</b></td><td>Send data to the server</td><td>Sending login information, submitting a form</td></tr>'
    '</table>',
    '<table class="rise" style="margin-top:.8rem">'
    '<tr><th>Operation</th><th>Method</th></tr>'
    '<tr><td>a &#183; Displaying a web page</td><td class="reveal"><span>GET</span></td></tr>'
    '<tr><td>b &#183; Submitting an ID and password in a login form</td><td class="reveal"><span>POST</span></td></tr>'
    '<tr><td>c &#183; Displaying search results</td><td class="reveal"><span>GET</span></td></tr>'
    '<tr><td>d &#183; Submitting a contact form</td><td class="reveal"><span>POST</span></td></tr>'
    '</table>',
    ar("كل طلب فيه طريقة طلب HTTP بتوضح نوع العملية المطلوبة. GET بيستخدم عادةً لطلب مورد أو بيانات من الخادم، زي عرض صفحة أو نتايج بحث. POST بيستخدم عادةً لإرسال بيانات يعالجها الخادم، زي تسجيل الدخول أو إرسال نموذج.")))

A(s("",
    eyebrow("3 &#183; The response: a status code"),
    h2("Three numbers to know"),
    sub("Every response carries a <b>status code</b>: a number that reports the result.", "max-width:58ch;margin-top:.4rem"),
    '<table class="rise">'
    '<tr><th>Status code</th><th>Meaning</th></tr>'
    '<tr><td><b>200</b></td><td>Success &#8212; the request was processed successfully</td></tr>'
    '<tr><td><b>404</b></td><td>Page not found &#8212; the requested address does not exist</td></tr>'
    '<tr><td><b>500</b></td><td>Server error &#8212; a problem occurred on the server side</td></tr>'
    '</table>',
    sub("The Arabic book adds: a 500 alone does not say <b>what</b> went wrong &#8212; only that it was on the server.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("الاستجابة فيها رقم بيوضح نتيجة المعالجة اسمه رمز حالة HTTP. 200: نجاح. 404: المورد المطلوب مش موجود بالعنوان ده. 500: خطأ داخلي في الخادم منعه يكمّل الطلب؛ والرمز لوحده مش بيحدد السبب بالتفصيل.")))

A(s("",
    eyebrow("3 &#183; One request, one matching response"),
    h2("Watch a page arrive, then a login", "max-width:26ch"),
    flow([
        {"t": "c", "msg": "GET  /search?q=cats", "en": "① You search 'cats'. The browser (client) sends a request with the GET method: it wants to retrieve data.",
         "ar": "① بتدوّر على cats. المتصفح (العميل) بيبعت طلب بأسلوب GET: عايز يجيب بيانات."},
        {"t": "s", "msg": "processing…", "en": "② The server receives the request and processes it: it finds the results.",
         "ar": "② الخادم بيستقبل الطلب ويعالجه: بيدوّر على النتايج."},
        {"t": "c", "msg": "200 OK  +  the results page", "en": "③ The server returns a response with status code 200 (success) and the page. The browser shows it.",
         "ar": "③ الخادم بيرجّع استجابة برمز حالة 200 (نجاح) ومعاها الصفحة، والمتصفح بيعرضها."},
        {"t": "c", "msg": "POST  /login  (HTTPS 🔒)", "en": "④ Now you log in. Sending data means POST, and over HTTPS the password travels encrypted.",
         "ar": "④ دلوقتي بتسجل دخول. إرسال بيانات يعني POST، ومع HTTPS الباسورد بيمشي متشفر."},
        {"t": "s", "msg": "checking the password…", "en": "⑤ The server receives the login data and checks it.",
         "ar": "⑤ الخادم بيستقبل بيانات الدخول ويتحقق منها."},
        {"t": "c", "msg": "200 OK  +  your account", "en": "⑥ Success: status code 200, and your account page comes back.",
         "ar": "⑥ نجاح: رمز حالة 200، وصفحة حسابك بترجع."},
    ], [("c", "&#128241;", "Client", "your browser"), ("s", "&#128452;", "Server", "far away")]),
    ar("طلب HTTP واحد، واستجابة مطابقة واحدة. دوس Next step وتابع.")))

A(s("dark",
    eyebrow("Pause &amp; think"),
    h2("If a browser receives status code 404, what should it tell the user &#8212; and whose side had the problem?",
       "max-width:28ch"),
    '<ul class="rise check" style="margin-top:1rem">'
    '<li class="reveal rv">Tell the user&#8230; <span class="ans">&#8212; &#8220;page not found&#8221;: the address asked for does not exist.</span></li>'
    '<li class="reveal rv">Whose side? <span class="ans">&#8212; the server is working; the <b>requested address</b> is wrong or the page is gone. A server breakdown would be <b>500</b>.</span></li>'
    '</ul>',
    ar("وقّف وفكّر: لو المتصفح استقبل 404، يقول للمستخدم إيه — وأنهي جانب كان فيه المشكلة؟")))

A(s("",
    eyebrow("3 &#183; Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">The client requests data or processing from the server, and the server returns the response. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv tf-t">HTTPS is a communication protocol that adds encryption to HTTP. <span class="ans">&#8212; <b>true</b>: TLS.</span></li>'
    '<li class="reveal rv">The GET method is for sending data to the server. <span class="ans">&#8212; <b>false</b>: GET retrieves; POST sends.</span></li>'
    '<li class="reveal rv tf-t">Status code 404 indicates that the page is not found. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: العميل بيطلب والخادم بيرد — صح. HTTPS بيضيف تشفير لـ HTTP — صح. GET لإرسال البيانات — غلط، ده POST. 404 الصفحة مش موجودة — صح.")))

# ---------------- part 4: API and JSON ----------------

A(s("",
    eyebrow("Part 4 &#183; API (Application Programming Interface)"),
    h2("Programs asking programs"),
    '<div class="rise statement def"><em>API</em> &#8212; a system for exchanging data between different pieces of software.</div>',
    sub("In web applications, the frontend often sends requests to the backend <b>through an API</b> and receives data back. That data is often written in <b>JSON</b> (JavaScript Object Notation): easy for people to read, and for computers to process.",
        "max-width:58ch;margin-top:.8rem"),
    '<div class="rise json">{\n  <span class="key">"city"</span>: <span class="val">"Cairo"</span>,\n  <span class="key">"temperature"</span>: <span class="num">31</span>\n}</div>',
    '<ul class="rise check">'
    '<li class="reveal rv">Name one <b>key</b> and its <b>value</b>. <span class="ans">&#8212; key <b>"city"</b>, value <b>"Cairo"</b> (or key "temperature", value 31).</span></li>'
    '</ul>',
    ar("واجهة برمجة التطبيقات (API): مجموعة قواعد واضحة بتسمح لبرنامج يطلب بيانات أو وظائف من برنامج تاني. وممكن ترجّع بيانات بصيغة JSON، وهي صيغة نصية لتمثيل البيانات المهيكلة. اقرا البيانات دي وحدد مفتاح (key) وقيمته (value).")))

A(s("",
    eyebrow("4 &#183; Exam-style question"),
    h2("Match each description with a term"),
    '<table class="rise">'
    '<tr><th>Description</th><th>Term</th></tr>'
    '<tr><td>a &#183; A communication protocol for exchanging data between web browsers and servers</td><td class="reveal"><span>A &#183; HTTP</span></td></tr>'
    '<tr><td>b &#183; A system for exchanging data between different pieces of software</td><td class="reveal"><span>B &#183; API</span></td></tr>'
    '<tr><td>c &#183; A communication protocol that adds encryption to HTTP</td><td class="reveal"><span>C &#183; HTTPS</span></td></tr>'
    '</table>',
    sub("Choices: <b>A</b> HTTP &#183; <b>B</b> API &#183; <b>C</b> HTTPS.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("اربط كل وصف بالمصطلح: بروتوكول تبادل البيانات بين المتصفح والخادم = HTTP. تبادل البيانات بين برمجيات مختلفة = API. HTTP مع تشفير = HTTPS.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Status code 500 means the request was processed successfully. <span class="ans">&#8212; <b>false</b>: 500 is a server error; success is 200.</span></li>'
    '<li class="reveal rv">An API is a technology for adjusting the appearance of web pages. <span class="ans">&#8212; <b>false</b>: it exchanges data between software.</span></li>'
    '<li class="reveal rv">JSON is used to encrypt the connection. <span class="ans">&#8212; <b>false</b>: JSON is a data format; HTTPS encrypts.</span></li>'
    '<li class="reveal rv tf-t">To send login data, POST is the right method. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    ar("خلّي بالك: 500 مش نجاح — ده خطأ في الخادم. الـ API مش لشكل الصفحة. JSON صيغة بيانات مش تشفير. وبيانات الدخول بتتبعت بـ POST.")))

A(s("",
    eyebrow("Exam-style question &#183; 6 marks"),
    h2("A browser asks for a web page", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Explain, step by step&#8230;</h3><ul>'
    '<li>what happens when a browser requests a web page and the server responds</li>'
    '<li>refer to: <b>client</b>, <b>request</b>, <b>HTTP method</b>, <b>response</b>, <b>status code</b></li>'
    '</ul></div>'
    '<div class="pane b"><h3>A plan for your answer</h3><ul>'
    '<li>the client sends a request &#8212; GET, to retrieve</li>'
    '<li>the server receives and processes it</li>'
    '<li>the response comes back with a status code: 200, 404 or 500</li>'
    '</ul></div>'
    '</div>',
    ar("سؤال على نمط الامتحان: اشرح خطوة بخطوة إيه اللي بيحصل لما المتصفح يطلب صفحة ويب والخادم يستجيب. أشِر إلى: العميل، الطلب، طريقة طلب HTTP، الاستجابة، رمز حالة HTTP.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("A school wants a timetable app", "max-width:26ch"),
    sub("Students log in, view their timetable, and download a PDF. You plan how the client and server communicate.",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Choose the method.</b> Loading a student&#8217;s grade history, submitting the login form, requesting today&#8217;s schedule from another school system: GET or POST? Is an API involved in the last?</li>'
    '<li><b>Choose the protocol.</b> Should the login use HTTP or HTTPS? Why?</li>'
    '<li><b>Decide.</b> Recommend the design, with two reasons. In pairs, agree which action must use POST.</li>'
    '</ul>',
    sub("Stuck? GET retrieves and shows; POST sends data such as a login; HTTPS encrypts so passwords are not intercepted.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: مدرسة عايزة تطبيق ويب الطلاب يسجلوا فيه دخول ويشوفوا جدولهم وينزّلوا PDF. اختار GET ولا POST لكل إجراء، واختار HTTP ولا HTTPS للدخول، وقرّر بسببين.")))

A(s("",
    eyebrow("In a new context"),
    h2("A weather API", "max-width:26ch"),
    sub("A weather service offers an API that returns today&#8217;s forecast when a client sends a request.", "max-width:56ch;margin-top:.7rem"),
    '<table class="rise">'
    '<tr><th>Question</th><th>Answer</th></tr>'
    '<tr><td>Which HTTP method retrieves the forecast?</td><td class="reveal"><span>GET</span></td></tr>'
    '<tr><td>Why should the service use HTTPS?</td><td class="reveal"><span>So the data is encrypted and not changed on the way</span></td></tr>'
    '<tr><td>One advantage of receiving the data as JSON?</td><td class="reveal"><span>Easy for people to read and for programs to process</span></td></tr>'
    '</table>',
    ar("طبّق اللي اتعلمته: خدمة طقس عندها API بترجّع توقعات النهارده. أنهي طريقة طلب هتستخدم؟ وليه HTTPS؟ وميزة واحدة لـ JSON.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 3-2"),
    h2("Ask, answer, by the rules", "max-width:24ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> that <b>404</b> &#8212; Internet broken, server broken, or something else?</p>'
    '<div class="rise statement">Client <em>requests</em>, server <em>responds</em> &#8212; over HTTP/HTTPS, with a method (<em>GET/POST</em>), a <em>status code</em>, and often an <em>API</em> returning <em>JSON</em>.</div>',
    ar("افتكر: العميل بيطلب، والخادم بيستجيب — عبر HTTP/HTTPS، بأسلوب (GET/POST)، ورمز حالة، وغالبًا واجهة برمجة تطبيقات بترجّع بيانات JSON.")))

# ---------------- part 5: Qureo chapter 32, Flowchart ----------------

A(s("dark",
    '<div class="rise part">5</div>',
    h2("On the platform: Flowchart"),
    sub("Qureo chapter 32: plan a program as a drawing first &#8212; then write the code. With if and calculations.", "max-width:56ch"),
    ar("الجزء الخامس على المنصة: الفصل 32 — المخطط الانسيابي: نرسم البرنامج الأول، وبعدين نكتب الكود.")))

A(s("",
    eyebrow("5 &#183; The symbols"),
    h2("Four shapes, joined by arrows"),
    fig(FLOWSYM),
    sub("A <b>flowchart</b> draws a program&#8217;s steps in order. Arrows show which step comes next.", "max-width:60ch;margin-top:.3rem"),
    ar("المخطط الانسيابي بيرسم خطوات البرنامج بالترتيب: البيضاوي للبداية والنهاية، والمستطيل لخطوة معالجة، والمعين لسؤال إجابته نعم أو لا (يعني if)، ومتوازي الأضلاع للإدخال والإخراج (زي console.log). والأسهم بتوضح الخطوة اللي بعدها.")))

A(s("",
    eyebrow("5 &#183; if + operations"),
    h2("Follow the arrows"),
    chart(PRICE, ["price", "total"], [
        {"el": "start", "en": "Start here.", "ar": "نبدأ من هنا."},
        {"el": "p0", "set": {"price": "40"}, "en": "A process: price = 40.", "ar": "خطوة معالجة: price = 40."},
        {"el": "p1", "set": {"total": "120"}, "en": "A process with an operation: total = 40 * 3 = 120.", "ar": "خطوة فيها عملية حسابية: total = 40 * 3 = 120."},
        {"el": "d", "en": "A decision: is 120 > 100? Yes.", "ar": "سؤال: هل 120 > 100؟ أيوه."},
        {"el": "yes", "out": "Too expensive", "en": "Follow the Yes arrow: show \"Too expensive\".", "ar": "نمشي على سهم Yes: نعرض \"Too expensive\"."},
        {"el": "end", "en": "End. The No branch was never used.", "ar": "النهاية. فرع No متستخدمش خالص."},
    ]),
    ar("دوس Next step وامشي مع الأسهم: المستطيل بيحسب، والمعين بيسأل، وبنمشي في فرع واحد بس.")))

A(s("",
    eyebrow("5 &#183; From the drawing to the code"),
    h2("Every shape becomes a line"),
    '<div class="rise twocol"><div class="fcfig">' + PRICE.strip() + '</div><div>'
    '<div class="code" style="font-size:clamp(12px,1.45vw,19px)">' + K("let") + " price = " + Nn("40") + ";\n"
    + K("let") + " total = price * " + Nn("3") + ";\n\n" + K("if") + " (total > " + Nn("100") + ") {\n  "
    + LOG + "(" + S_('"Too expensive"') + ");\n} " + K("else") + " {\n  " + LOG + "(" + S_('"Buy it"') + ");\n}</div>"
    '<table><tr><th>Shape</th><th>In the code</th></tr>'
    '<tr><td>Rectangle (process)</td><td class="reveal"><span>let &#8230; = &#8230;; a calculation</span></td></tr>'
    '<tr><td>Diamond (decision)</td><td class="reveal"><span>if ( &#8230; )</span></td></tr>'
    '<tr><td>Yes / No arrows</td><td class="reveal"><span>the if { } and the else { }</span></td></tr>'
    '<tr><td>Parallelogram (output)</td><td class="reveal"><span>console.log( &#8230; )</span></td></tr>'
    '</table></div></div>',
    ar("كل شكل بيتحول لسطر: المستطيل = let أو عملية حسابية، المعين = if، سهم Yes = جوّه if، سهم No = else، ومتوازي الأضلاع = console.log.")))

A(s("",
    eyebrow("5 &#183; Your turn"),
    h2("Write the code for this flowchart", "max-width:24ch"),
    '<div class="rise twocol"><div class="fcfig">' + AB.strip() + '</div><div>'
    '<ul class="check">'
    '<li class="reveal rv">What does it show? <span class="ans">&#8212; <b>8</b>: 8 &gt; 5 is true, so the Yes branch shows a.</span></li>'
    '<li class="reveal rv">The code: <span class="ans"><span class="mono" style="white-space:pre;display:block;font-size:.92em">let a = 8;\nlet b = 5;\nif (a &gt; b) {\n  console.log(a);\n} else {\n  console.log(b);\n}</span></span></li>'
    '<li class="reveal rv">What would it show if b were 11? <span class="ans">&#8212; <b>11</b>: 8 &gt; 11 is false, so the No branch.</span></li>'
    '</ul></div></div>',
    ar("اكتب الكود للمخطط ده. فكّر الأول، وبعدين دوس على كل سطر. ده نفس فكرة مقارنة القيم في المحاضرة 9.")))

A(s("",
    eyebrow("5 &#183; Watch out"),
    h2("Rules of a good flowchart", "max-width:24ch"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">A diamond has only one way out. <span class="ans">&#8212; <b>false</b>: two, labelled <b>Yes</b> and <b>No</b>.</span></li>'
    '<li class="reveal rv tf-t">A flowchart begins at Start and finishes at End. <span class="ans">&#8212; <b>true</b>: ovals.</span></li>'
    '<li class="reveal rv">A calculation such as total = price * 3 goes in a diamond. <span class="ans">&#8212; <b>false</b>: a calculation is a process, a rectangle.</span></li>'
    '<li class="reveal rv tf-t">The arrows show the order the steps run in. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    ar("خلّي بالك: المعين ليه مخرجين Yes و No. بنبدأ بـ Start ونخلص بـ End. الحساب في مستطيل مش معين. والأسهم بتوضح الترتيب.")))

# ---------------- part 6: Qureo chapter 33, comprehension check ----------------

A(s("dark",
    '<div class="rise part">6</div>',
    h2("Comprehension check: chapters 31 and 32"),
    sub("Qureo chapter 33 reviews functions and flowcharts. Today, together: a function inside a flowchart.", "max-width:56ch"),
    ar("الجزء السادس: الفصل 33 — مراجعة الفصلين 31 و 32: الدوال والمخطط الانسيابي، مع بعض.")))

A(s("",
    eyebrow("6 &#183; A function in a flowchart"),
    h2("add3, then decide"),
    '<div class="rise code" style="font-size:clamp(12px,1.4vw,18px)">' + K("function") + " " + F("add3") + "(a, b, c) {\n  " + K("return") + " a + b + c;\n}</div>",
    chart(REVIEW, ["total"], [
        {"el": "start", "en": "Start.", "ar": "البداية."},
        {"el": "p0", "set": {"total": "12"}, "en": "A process that calls a function: add3(2, 4, 6) returns 12, so total = 12.", "ar": "خطوة بتنادي دالة: add3(2, 4, 6) بترجّع 12، يعني total = 12."},
        {"el": "d", "en": "A decision: is 12 > 10? Yes.", "ar": "سؤال: هل 12 > 10؟ أيوه."},
        {"el": "yes", "out": "Big total", "en": "Yes branch: show \"Big total\".", "ar": "فرع Yes: نعرض \"Big total\"."},
        {"el": "end", "en": "End.", "ar": "النهاية."},
    ]),
    ar("الدالة بترجّع قيمة، والمخطط بيقرر بيها. دوس Next step.")))

A(s("",
    eyebrow("6 &#183; Review &#183; your turn"),
    h2("Functions and flowcharts"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">add3(1, 1, 1) returns&#8230; <span class="ans">&#8212; <b>3</b>.</span></li>'
    '<li class="reveal rv">In the flowchart above, with add3(1, 2, 3), what is shown? <span class="ans">&#8212; <b>Small total</b>: 6 &gt; 10 is false.</span></li>'
    '<li class="reveal rv">Which shape would hold <span class="mono">if (total &gt; 10)</span>? <span class="ans">&#8212; the <b>diamond</b>.</span></li>'
    '<li class="reveal rv">A function without <span class="mono">return</span> gives back&#8230; <span class="ans">&#8212; <b>undefined</b>.</span></li>'
    '</ul>',
    ar("مراجعة: فكّر في كل سطر الأول، وبعدين دوس عليه.")))

A(s("dark",
    eyebrow("Remember these"),
    h2("What we learned"),
    '<ul class="rise check">'
    '<li>The <b>client</b> requests, the <b>server</b> responds.</li>'
    '<li><b>HTTP</b> carries the messages; <b>HTTPS</b> adds TLS encryption.</li>'
    '<li><b>GET</b> retrieves, <b>POST</b> sends. Status codes: <b>200</b> success, <b>404</b> not found, <b>500</b> server error.</li>'
    '<li>An <b>API</b> lets programs exchange data, often as <b>JSON</b>.</li>'
    '<li>A <b>flowchart</b>: oval start/end, rectangle process, diamond decision (if), parallelogram output.</li>'
    '</ul>',
    ar("العميل بيطلب والخادم بيرد • HTTP بينقل و HTTPS بيشفّر • GET بيجيب و POST بيبعت • 200 و 404 و 500 • API و JSON • والمخطط الانسيابي: بيضاوي، مستطيل، معين، متوازي أضلاع.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 10"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 10 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers lesson 3-2 and Qureo chapters 32 and 33. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس 3-2 والفصلين 32 و 33 على المنصة. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))
