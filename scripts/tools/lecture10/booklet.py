# ------------------------------------------------------------------ booklet
def booklet(head, tail):
    """The booklet follows the deck slide by slide, in the same order, so what
    a student revises from is what they were taught from. The slide numbers
    in the comments are the deck's; keep them in step when either changes.
    The players (the request flow and the flowcharts) print as their finished
    trace tables. The title and the exam QR have no page."""
    CS, SYM, PRICE, AB, REVIEW = (slide_svg(n) for n in ("CLIENTSERVER", "FLOWSYM", "PRICE", "AB", "REVIEW"))

    def code(t):
        return '<div class="code">' + esc(t) + '</div>'

    def chart(svg):
        return '<div class="fcx">' + svg + '</div>'

    p = []
    # slides 2-6: recap, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Before we start &middot; lesson 3-1</h2>'
        '<table><tr><th>Tier</th><th>Its job</th></tr>'
        '<tr><td class="k">Frontend</td><td>shows and collects</td></tr>'
        '<tr><td class="k">Backend</td><td>decides and processes</td></tr>'
        '<tr><td class="k">Database</td><td>stores and retrieves</td></tr></table>'
        '<p class="ar">في الدرس 3-1 اتعلمت إن الواجهة الأمامية والخلفية بيتعاونوا؛ في الدرس ده هتتعلم إزاي الطلبات والاستجابات بتتنقل بين العميل والخادم.</p>'
        '<h2>Your device asks, a server answers</h2>'
        '<p>When you click a link or press &#8220;search&#8221;, your device does not hold the whole website &mdash; it asks a '
        'distant computer for it. Your browser is the <b>client</b> that makes the <b>request</b>; a <b>server</b> somewhere '
        'answers with a <b>response</b>. This exchange, governed by shared rules called <b>protocols</b>, is how every web '
        'application communicates.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> How do the client and server communicate to make a web '
        'application work, and what rules and messages do they use?</p>'
        '<p class="ar">إزاي العميل والخادم بيتواصلوا عشان يشغّلوا تطبيق الويب، وإيه القواعد والرسائل اللي بيستخدموها؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> You open YouTube and search <i>cats</i>. What does your '
        'phone send? What comes back? Should your password travel as it is, or locked?</p>'
        '<p class="ar">اكتبوا إجاباتكم قبل ما تكمّلوا.</p></div>'))
    # slides 7-10: client and server, client or server, HTTP and HTTPS
    p.append(page(
        '<h2>Part 1 &middot; Client and server</h2>'
        + dg(CS)
        + '<table><tr><th style="width:18%">Term</th><th>Meaning</th></tr>'
        '<tr><td class="k">Client</td><td>The side that requests data or processing from the server. Web browsers and smartphone apps.</td></tr>'
        '<tr><td class="k">Server</td><td>The side that receives requests from clients, processes them, and returns responses.</td></tr></table>'
        '<p class="ar">العميل: برنامج أو جهاز بيبعت طلب لخدمة تانية. الخادم: بيستقبل الطلبات ويعالجها ويرجّع الاستجابات.</p>'
        '<h2>Part 2 &middot; HTTP and HTTPS</h2>'
        + term('HTTP (HyperText Transfer Protocol)', 'A communication protocol for exchanging data between clients (browsers and apps) and servers.',
               'بروتوكول بيستخدم لتبادل الرسائل بين عميل وخادم على الويب.')
        + term('HTTPS (HTTP Secure)', 'HTTP with TLS encryption added. The content is encrypted, so the risk of it being read by '
               'third parties is reduced. Addresses that begin with https:// use it.',
               'استخدام HTTP عبر اتصال TLS آمن: بيحمي سرية الاتصال وسلامته وبيتحقق من الخادم.')
        + '<div class="summary hw"><p><b>Pause and think.</b> Why should a login page use HTTPS rather than plain HTTP?</p>'
        '<p class="ar">ليه صفحة الدخول لازم تستخدم HTTPS؟</p></div>'))
    # slides 11-14: methods, status codes, the request flow, 404
    p.append(page(
        '<h2>Part 3 &middot; The request carries an HTTP method</h2>'
        '<table><tr><th style="width:14%">Method</th><th style="width:30%">Role</th><th>Examples</th></tr>'
        '<tr><td class="k">GET</td><td>Retrieve data from the server</td><td>Displaying a web page, retrieving search results</td></tr>'
        '<tr><td class="k">POST</td><td>Send data to the server</td><td>Sending login information, submitting a form</td></tr></table>'
        '<h2>The response carries a status code</h2>'
        '<table><tr><th style="width:18%">Status code</th><th>Meaning</th></tr>'
        '<tr><td class="k">200</td><td>Success &mdash; the request was processed successfully</td></tr>'
        '<tr><td class="k">404</td><td>Page not found &mdash; the requested address does not exist</td></tr>'
        '<tr><td class="k">500</td><td>Server error &mdash; a problem occurred on the server side (on its own it does not say the detailed cause)</td></tr></table>'
        '<h2>One request, one matching response</h2>'
        '<table><tr><th style="width:8%">Step</th><th style="width:16%">Where</th><th>What happens</th></tr>'
        '<tr><td>&#9312;</td><td class="k">Client</td><td>You search <i>cats</i>: the browser sends a <b>GET</b> request</td></tr>'
        '<tr><td>&#9313;</td><td class="k">Server</td><td>Receives the request and processes it</td></tr>'
        '<tr><td>&#9314;</td><td class="k">Client</td><td>The response arrives: status code <b>200</b> and the results page</td></tr>'
        '<tr><td>&#9315;</td><td class="k">Client</td><td>You log in: a <b>POST</b> request, over <b>HTTPS</b>, so the password is encrypted</td></tr>'
        '<tr><td>&#9316;</td><td class="k">Server</td><td>Receives the login data and checks it</td></tr>'
        '<tr><td>&#9317;</td><td class="k">Client</td><td>Status code <b>200</b>, and your account page comes back</td></tr></table>'
        '<div class="summary hw"><p><b>Pause and think.</b> If a browser receives status code 404, what should it tell the user '
        '&mdash; and whose side had the problem?</p></div>'))
    # slides 15-19: true or false, API and JSON, match, exam warning, exam-style
    p.append(page(
        '<table><tr><th>True or false?</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>The client requests data or processing; the server returns the response.</td><td>True</td></tr>'
        '<tr><td>HTTPS is a communication protocol that adds encryption to HTTP.</td><td>True</td></tr>'
        '<tr><td>The GET method is for sending data to the server.</td><td><b>False</b> &mdash; POST sends</td></tr>'
        '<tr><td>Status code 404 indicates that the page is not found.</td><td>True</td></tr></table>'
        '<h2>Part 4 &middot; API and JSON</h2>'
        + term('API (Application Programming Interface)', 'A system for exchanging data between different pieces of software. '
               'In web applications, the frontend often sends requests to the backend through an API and receives data.',
               'مجموعة قواعد واضحة بتسمح لبرنامج يطلب بيانات أو وظائف من برنامج تاني.')
        + term('JSON (JavaScript Object Notation)', 'A data format that is easy for humans to read and for computers to process. '
               'It is made of keys and their values.', 'صيغة نصية شائعة لتمثيل وتبادل البيانات المهيكلة.')
        + code('{\n  "city": "Cairo",\n  "temperature": 31\n}')
        + '<p>Key <b>&quot;city&quot;</b> has the value <b>&quot;Cairo&quot;</b>; key <b>&quot;temperature&quot;</b> has the value <b>31</b>.</p>'
        '<table><tr><th>Looks right, but is false</th><th style="width:38%">Why</th></tr>'
        '<tr><td>Status code 500 means the request was processed successfully.</td><td>500 is a server error; success is 200.</td></tr>'
        '<tr><td>An API adjusts the appearance of web pages.</td><td>It exchanges data between software.</td></tr>'
        '<tr><td>JSON encrypts the connection.</td><td>JSON is a data format; HTTPS encrypts.</td></tr></table>'))
    # slides 20-23: exam-style, engineer, new context, takeaway
    p.append(page(
        '<div class="summary"><p><b>Exam-style question &middot; 6 marks.</b> Explain what happens, step by step, when a '
        'browser requests a web page and the server responds. Refer to: client, request, HTTP method, response, status code.</p>'
        '<p class="ar">اشرح خطوة بخطوة لما المتصفح يطلب صفحة ويب والخادم يستجيب.</p></div>'
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A school wants a web app where students log in, view their timetable and download a PDF. '
        '<b>Choose the method</b> (GET or POST) for loading grade history, submitting the login form, and requesting today&#8217;s '
        'schedule from another school system &mdash; is an API involved in the last? <b>Choose the protocol</b> for the login. '
        '<b>Decide</b>, with two reasons.</p>'
        '<p class="ar">تلميح: GET بيجيب ويعرض؛ POST بيبعت بيانات زي الدخول؛ HTTPS بيشفّر عشان الباسورد ميتسرقش.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A weather service offers an API that returns today&#8217;s forecast. Which HTTP method would '
        'the client use? Why should the service use HTTPS? One advantage of receiving the data as JSON?</p></div>'
        '<h2>Key takeaway &middot; lesson 3-2</h2><div class="summary">'
        '<p>Client requests, server responds &mdash; over HTTP/HTTPS, with a method (GET/POST), a status code, and often an API '
        'returning JSON.</p>'
        '<p class="ar">العميل بيطلب، والخادم بيستجيب — عبر HTTP/HTTPS، بأسلوب (GET/POST)، ورمز حالة، وغالبًا API بترجّع JSON.</p></div>'))
    # slides 24-27: Qureo 32 -- symbols, follow the arrows, to the code
    p.append(page(
        '<h2>Part 5 &middot; On the platform: Flowchart (Qureo chapter 32)</h2>'
        '<p>A <b>flowchart</b> draws a program&#8217;s steps in order. Arrows show which step comes next.</p>'
        + dg(SYM)
        + '<div class="fcrow">' + chart(PRICE)
        + '<div><table><tr><th>Step</th><th>Shape</th><th>What happens</th></tr>'
        '<tr><td>1</td><td>Rectangle</td><td>price = 40</td></tr>'
        '<tr><td>2</td><td>Rectangle</td><td>total = 40 &times; 3 = 120</td></tr>'
        '<tr><td>3</td><td>Diamond</td><td>120 &gt; 100? <b>Yes</b></td></tr>'
        '<tr><td>4</td><td>Parallelogram</td><td>shows &quot;Too expensive&quot;</td></tr></table>'
        + code('let price = 40;\nlet total = price * 3;\nif (total > 100) {\n  console.log("Too expensive");\n} else {\n  console.log("Buy it");\n}')
        + '</div></div>'
        '<p class="ar">كل شكل بيتحول لسطر: المستطيل = let أو حساب، المعين = if، سهم Yes = جوّه if، سهم No = else، متوازي الأضلاع = console.log.</p>'))
    # slides 28-32: your turn, rules, Qureo 33 review, what we learned
    p.append(page(
        '<h2>Your turn &middot; write the code</h2>'
        '<div class="fcrow">' + chart(AB)
        + '<div>' + code('let a = 8;\nlet b = 5;\nif (a > b) {\n  console.log(a);\n} else {\n  console.log(b);\n}')
        + '<p>It shows <b>8</b>. If b were 11, it would show <b>11</b>.</p>'
        '<table><tr><th>Rules of a good flowchart</th></tr>'
        '<tr><td>One Start and one End, both ovals</td></tr>'
        '<tr><td>A diamond has two exits: Yes and No</td></tr>'
        '<tr><td>A calculation goes in a rectangle, not a diamond</td></tr>'
        '<tr><td>The arrows show the order the steps run in</td></tr></table></div></div>'
        '<h2>Part 6 &middot; Review of chapters 31-32 (Qureo chapter 33)</h2>'
        '<div class="fcrow">' + chart(REVIEW)
        + '<div>' + code('function add3(a, b, c) {\n  return a + b + c;\n}')
        + '<p>add3(2, 4, 6) returns <b>12</b>, so total = 12. 12 &gt; 10 is true: it shows <b>&quot;Big total&quot;</b>. '
        'With add3(1, 2, 3) the total is 6, so it shows &quot;Small total&quot;.</p></div></div>'
        '<p class="ar">الدالة بترجّع قيمة، والمخطط بيقرر بيها.</p>'))
    p.append(page('<h2>Class work</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
                  + exercise(1, 1) + exercise(2, 2)))
    p.append(page('<h2>Class work</h2><p class="ar">كمّل مع زميلك.</p>'
                  + exercise(3, 3) + exercise(4, 4)))
    return head + ''.join(p) + lastpage('booklet') + tail