# ------------------------------------------------------------------ booklet
def booklet(head, tail):
    """The booklet follows the deck slide by slide, in the same order, so what
    a student revises from is what they were taught from. The slide numbers
    in the comments are the deck's; keep them in step when either changes.
    The two players (the request flow and the code tracer) print as their
    finished trace tables. The title and the exam QR have no page."""
    TIERS = slide_svg("TIERS")

    def code(t):
        return '<div class="code">' + esc(t) + '</div>'

    p = []
    # slides 2-6: unit 3, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Unit 3 &middot; Web applications</h2>'
        '<table><tr><th>Lesson</th><th>Topic</th></tr>'
        '<tr><td class="k">3-1 &middot; today</td><td>The overall structure of web applications</td></tr>'
        '<tr><td class="k">3-2</td><td>Web application communication methods</td></tr>'
        '<tr><td class="k">3-3</td><td>Fundamentals of frontend technology</td></tr></table>'
        '<h2>Every time you go online</h2>'
        '<p>Every time you search on YouTube, buy on Amazon, or open Gmail, you are using a <b>web application</b> &mdash; '
        'a program you use through your browser, with nothing to install. Behind the simple screen, three tiers work '
        'together: the page you interact with, the hidden server that processes the request, and the database that holds '
        'all the data. Understanding these three tiers explains how almost every online service is built.</p>'
        '<p class="ar">لما بتدوّر في موقع فيديو، أو بتتسوق أونلاين، أو بتستخدم إيميل على الويب، إنت بتستخدم تطبيق ويب، '
        'وورا اللي بتشوفه فيه أجزاء مختلفة شغالة مع بعض.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> How is a web application structured, and how do its three '
        'tiers work together to respond to what a user does?</p>'
        '<p class="ar">إزاي بيتبني تطبيق الويب، وإزاي طبقاته التلاتة بتشتغل مع بعض عشان تستجيب للمستخدم؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> You type <i>red shoes</i> in a shopping site and press '
        'Enter. Who read your words? Who found the shoes? Where were the shoes kept? Write three guesses.</p>'
        '<p class="ar">اكتبوا تلات تخمينات قبل ما تكمّلوا.</p></div>'))
    # slides 7-9: what is a web application, which one is, the three tiers
    p.append(page(
        '<h2>Part 1 &middot; What is a web application?</h2>'
        + term('Web application', 'An application used through a web browser. It can be used as long as you have a browser, '
               'without installing dedicated software. e.g. YouTube, Amazon, Gmail, Google Maps.',
               'تطبيق الويب: تطبيق بيتستخدم عادةً من خلال متصفح الويب، وبعض تطبيقات الويب ممكن كمان تتثبت على الجهاز.')
        + '<table><tr><th>Is it a web application?</th><th style="width:34%">Answer</th></tr>'
        '<tr><td>A video player on the device</td><td>No &mdash; installed on the device</td></tr>'
        '<tr><td>A maps website on the Internet</td><td><b>Yes</b> &mdash; used through a browser</td></tr>'
        '<tr><td>A calculator app on the desktop</td><td>No &mdash; installed on the computer</td></tr>'
        '<tr><td>A photo-editing program</td><td>No &mdash; installed software</td></tr></table>'
        '<h2>Part 2 &middot; The three tiers of a web application</h2>'
        '<p>A web application is broadly composed of three tiers: the <b>frontend</b>, the <b>backend</b> and the '
        '<b>database</b>. This is the <b>three-tier architecture</b>.</p>'
        + dg(TIERS)))
    # slides 10-13: what each tier does, the restaurant, true or false, match
    p.append(page(
        '<table><tr><th style="width:16%">Tier</th><th>Role</th><th style="width:30%">Examples</th></tr>'
        '<tr><td class="k">Frontend</td><td>The screen component that users see directly. It runs on the browser and accepts user input.</td><td>Search screen, product listing pages, input forms</td></tr>'
        '<tr><td class="k">Backend</td><td>The server-side processing that users do not see. It processes data and makes decisions.</td><td>Searching for matching products, login authentication</td></tr>'
        '<tr><td class="k">Database</td><td>A system that organizes, stores and manages data. It retrieves data when needed and records new data.</td><td>Product information, user information, order history</td></tr></table>'
        '<p class="ar">الواجهة الأمامية: الجزء اللي بنشوفه ونتعامل معاه في المتصفح. الواجهة الخلفية: بتشتغل على الخادم وبتعالج الطلبات. '
        'قاعدة البيانات: بتحفظ البيانات وتوفرها وقت الحاجة.</p>'
        '<h2>A way to remember: a restaurant</h2>'
        '<table><tr><th>In a restaurant</th><th>In a web application</th></tr>'
        '<tr><td>The <b>waiter</b>: takes your order, brings your plate</td><td><b>Frontend</b> &mdash; shows and collects</td></tr>'
        '<tr><td>The <b>kitchen</b> you never see: decides and cooks</td><td><b>Backend</b> &mdash; decides and processes</td></tr>'
        '<tr><td>The <b>storeroom</b>: keeps the food, hands it over</td><td><b>Database</b> &mdash; stores and retrieves</td></tr></table>'
        '<p class="ar">المطعم مثال مننا مش من الكتاب؛ الجمل اللي على اليمين هي جمل الكتاب — احفظها.</p>'
        '<table><tr><th>True or false?</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>The frontend is the screen component that users see directly.</td><td>True</td></tr>'
        '<tr><td>The backend is the part that runs on the browser.</td><td><b>False</b> &mdash; on the server</td></tr>'
        '<tr><td>A database organizes, stores and manages data.</td><td>True</td></tr>'
        '<tr><td>A web application operates with the frontend alone.</td><td><b>False</b> &mdash; all three tiers</td></tr></table>'))
    # slides 14-17: the flow, pause & think, familiar services, which tier
    p.append(page(
        '<h2>Part 3 &middot; How the three tiers cooperate</h2>'
        '<p>Searching for a product on an online shopping site. A request flows down the tiers, and the reply returns:</p>'
        '<table><tr><th style="width:8%">Step</th><th style="width:18%">Tier</th><th>What happens</th></tr>'
        '<tr><td>&#9312;</td><td class="k">Frontend</td><td>Receives the search keywords entered by the user</td></tr>'
        '<tr><td>&#9313;</td><td class="k">Frontend</td><td>Sends the search keywords to the backend</td></tr>'
        '<tr><td>&#9314;</td><td class="k">Backend</td><td>Searches the database for products that match the criteria</td></tr>'
        '<tr><td>&#9315;</td><td class="k">Database</td><td>Returns the data of the matching products to the backend</td></tr>'
        '<tr><td>&#9316;</td><td class="k">Backend</td><td>Organizes the search results and returns them to the frontend</td></tr>'
        '<tr><td>&#9317;</td><td class="k">Frontend</td><td>Displays the search results on the user&#8217;s screen</td></tr></table>'
        '<div class="summary hw"><p><b>Pause and think.</b> When you type in a search box and see results, which tier '
        'collected your input, and which tier found the answer?</p>'
        '<p class="ar">أنهي طبقة جمعت المدخلات، وأنهي طبقة لقت الإجابة؟</p></div>'
        '<h2>Familiar web applications</h2>'
        '<table><tr><th>Service</th><th>Frontend</th><th>Backend</th><th>Database</th></tr>'
        '<tr><td class="k">Video sharing</td><td>Playback and search screens</td><td>Recommended videos; view counts</td><td>Videos, users, viewing history</td></tr>'
        '<tr><td class="k">SNS</td><td>Timeline and post screens</td><td>Who sees a post; push notifications</td><td>Posts, follow relationships, messages</td></tr>'
        '<tr><td class="k">E-commerce</td><td>Product listings, cart screens</td><td>Stock checking; payments</td><td>Products, order history, customers</td></tr></table>'
        '<p class="ar">كل خدمة: واجهة أمامية بتعرض وتجمع، وواجهة خلفية بتقرر وتعالج، وقاعدة بيانات بتخزن وتسترجع.</p>'))
    # slides 18-23: exam warning, exam-style, engineer, new context, takeaway
    p.append(page(
        '<table><tr><th>Looks right, but is false</th><th style="width:40%">Why</th></tr>'
        '<tr><td>The frontend has the role of storing and managing data.</td><td>That is the database.</td></tr>'
        '<tr><td>The backend is the part users interact with directly on the browser.</td><td>That is the frontend.</td></tr>'
        '<tr><td>The database has the role of displaying screens to users.</td><td>The frontend displays.</td></tr>'
        '<tr><td>The frontend sends the request straight to the database.</td><td>The <b>backend</b> asks the database.</td></tr></table>'
        '<div class="summary"><p><b>Exam-style question &middot; 6 marks.</b> Explain how the three tiers cooperate when a '
        'user posts a photo on a social media app. Refer to the role of the frontend, backend, and database.</p>'
        '<p class="ar">اشرح دور كل طبقة لما المستخدم ينشر صورة.</p></div>'
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A clinic wants a web app where patients book appointments, check free time slots and see '
        'past visits. <b>Assign</b> each job to a tier. <b>Diagnose</b>: the booking page opens but no free slots appear. '
        '<b>Decide</b>: three tiers or not, with two reasons.</p>'
        '<p class="ar">تلميح: الأمامية تعرض وتجمع؛ الخلفية تقرر وتعالج؛ قاعدة البيانات تخزن وتسترجع.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A weather app lets users type a city and see the forecast. Which tier takes the city name, '
        'looks up the forecast, and stores past forecasts? Name one job the frontend cannot do on its own.</p></div>'
        '<h2>Key takeaway &middot; lesson 3-1</h2><div class="summary">'
        '<p>The frontend shows and collects, the backend decides and processes, the database stores and retrieves &mdash; '
        'three tiers cooperating make a web application work. (The Arabic book: a simplified teaching model; real '
        'applications can differ.)</p>'
        '<p class="ar">الواجهة الأمامية بتعرض وتجمع، والخلفية بتقرر وتعالج، وقاعدة البيانات بتخزن وتسترجع.</p></div>'))
    # slides 24-27: Qureo chapter 31 -- a function, add, add3
    p.append(page(
        '<h2>Part 4 &middot; On the platform: Functions (4)</h2>'
        '<p>Qureo chapter 31: a function that adds two values, adds three, and compares three. A function is a small '
        'machine: it receives values, processes them, and gives a value back.</p>'
        + code('function name(argumentName) {\n  // processing\n  return result;\n}')
        + '<table><tr><th style="width:26%">Word</th><th>Meaning</th></tr>'
        '<tr><td class="k">argument</td><td>the value you pass <b>into</b> the function</td></tr>'
        '<tr><td class="k">return value</td><td>the value the function gives <b>back</b> with <span class="mono">return</span></td></tr></table>'
        '<p class="ar">الدالة زي ماكينة العصير: الوسيط هو اللي بتحطه، والقيمة المرجعة هي اللي بتطلع بـ return.</p>'
        '<h2>A function to add two values</h2>'
        + code('function add(a, b) {\n  return a + b;\n}\n\nconsole.log(add(3, 5));')
        + '<table><tr><th>Step</th><th>What happens</th><th style="width:22%">Values</th></tr>'
        '<tr><td>1</td><td>The call add(3, 5) runs the function</td><td></td></tr>'
        '<tr><td>2</td><td>The arguments go in</td><td>a = 3, b = 5</td></tr>'
        '<tr><td>3</td><td>a + b is computed; return sends it back</td><td>return 8</td></tr>'
        '<tr><td>4</td><td>console.log prints the return value</td><td>prints 8</td></tr></table>'))
    # slides 27-28: add three, compare three
    p.append(page(
        '<h2>A function that adds three values</h2>'
        + code('function add3(a, b, c) {\n  return a + b + c;\n}\n\nconsole.log(add3(2, 4, 6));      // 12\nconsole.log(add3(10, 20, 30));   // 60')
        + '<p class="ar">نفس الفكرة بتلات وسائط مفصولين بفواصل.</p>'
        '<h2>A function that compares three values</h2>'
        + code('function biggest(a, b, c) {\n  let big = a;\n  if (b > big) {\n    big = b;\n  }\n  if (c > big) {\n    big = c;\n  }\n  return big;\n}\n\nconsole.log(biggest(4, 9, 7));')
        + '<table><tr><th>Step</th><th>Question</th><th style="width:30%">big</th></tr>'
        '<tr><td>1</td><td>let big = a;</td><td>4</td></tr>'
        '<tr><td>2</td><td>b &gt; big? 9 &gt; 4 is true</td><td>9</td></tr>'
        '<tr><td>3</td><td>c &gt; big? 7 &gt; 9 is false</td><td>stays 9</td></tr>'
        '<tr><td>4</td><td>return big</td><td>prints 9</td></tr></table>'
        '<p class="ar">بنبدأ ونقول إن الأولاني هو الأكبر، وبعدين نقارن بـ if — زي المحاضرة 8.</p>'))
    # slides 29-31: Math.max, no return, what we learned
    p.append(page(
        '<h2>A shortcut: Math.max and Math.min</h2>'
        + code('console.log(Math.max(4, 9, 7));   // 9\nconsole.log(Math.min(4, 9, 7));   // 4')
        + '<div class="summary hw"><p><b>Watch out: no return.</b> If you write <span class="mono">a + b;</span> without '
        '<span class="mono">return</span>, the function gives nothing back and console.log prints <b>undefined</b> &mdash; '
        'a juice machine with no cup.</p>'
        '<p class="ar">من غير return بيطبع undefined.</p></div>'
        '<h2>What we learned</h2><div class="summary">'
        '<p>A web application is used through a browser. Frontend shows and collects; backend decides and processes; '
        'database stores and retrieves. A request flows down the tiers and the reply comes back.</p>'
        '<p>A function takes arguments, processes them, and gives back a return value.</p></div>'))
    p.append(page('<h2>Class work</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
                  + exercise(1, 1) + exercise(2, 2)))
    p.append(page('<h2>Class work</h2><p class="ar">كمّل مع زميلك.</p>'
                  + exercise(3, 3) + exercise(4, 4)))
    return head + ''.join(p) + lastpage('booklet') + tail