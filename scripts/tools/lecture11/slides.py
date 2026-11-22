SLIDES = []
A = SLIDES.append

# 1 title
A(s("dark",
    '<div class="rise eyebrow" id="lectureBadge">Programming &amp; Artificial Intelligence</div>',
    h2("What is a web page made of?", "font-size:clamp(34px,6vw,86px);max-width:18ch"),
    sub("Every page you open is three technologies working together. Today: what each one does &#8212; and on the platform, you build pages yourself: HTML, then CSS, then a small project.",
        "max-width:58ch;margin-top:1rem"),
    ar("كل صفحة بتفتحها فيها تلات تقنيات شغالين مع بعض. النهارده: كل واحدة بتعمل إيه — وعلى المنصة هتبني صفحات بنفسك: HTML، وبعدين CSS، وبعدين مشروع صغير.")))

# 2 recap -- lesson 3-2
A(s("",
    eyebrow("Before we start &#183; Lesson 3-2"),
    h2("Last time: how they talk", "max-width:24ch"),
    '<table class="rise">'
    '<tr><th>Word</th><th>Meaning</th></tr>'
    '<tr><td><b>Client / server</b></td><td>the client requests, the server responds</td></tr>'
    '<tr><td><b>HTTP / HTTPS</b></td><td>the rules for the messages; HTTPS adds TLS encryption</td></tr>'
    '<tr><td><b>GET / POST</b></td><td>retrieve data / send data</td></tr>'
    '<tr><td><b>200 / 404 / 500</b></td><td>success / not found / server error</td></tr>'
    '</table>',
    sub("The page the server sends back is what the <b>frontend</b> shows. Today: what that page is made of.", "max-width:60ch;margin-top:.9rem"),
    ar("المرة اللي فاتت: العميل بيطلب والخادم بيرد. الصفحة اللي الخادم بيرجّعها هي اللي الواجهة الأمامية بتعرضها. النهارده: الصفحة دي معمولة من إيه.")))

# 3 hook -- the book's opening paragraph
A(s("",
    eyebrow("Open any web page"),
    h2("Three technologies at work", "max-width:22ch"),
    sub("<b>HTML</b> builds the structure &#8212; headings, paragraphs and links, like the frame of a building. <b>CSS</b> adds the appearance &#8212; colours, layout and fonts, like a building&#8217;s interior. <b>JavaScript</b> adds behavior &#8212; search boxes that respond, buttons that count, screens that update.",
        "max-width:58ch;margin-top:1rem"),
    '<div class="rise" style="margin-top:1rem;padding:clamp(12px,1.5vw,22px);background:var(--gold-pale);border-radius:12px;max-width:62ch">'
    '<p style="font-size:clamp(14px,1.6vw,21px)"><b>Hands up:</b> you want a page&#8217;s title to turn pink. Which of the three would you change? Remember your answer.</p></div>',
    ar("عند فتح أي صفحة ويب، بتشوف تلات تقنيات شغالين مع بعض: HTML بيبني الهيكل — العناوين والفقرات والروابط — زي هيكل المبنى. و CSS بيضيف المظهر — الألوان والتخطيط والخطوط — زي التصميم الداخلي. و JavaScript بيضيف السلوك التفاعلي — مربعات بحث بتستجيب، وأزرار بتعد، وشاشات بتتحدّث.")))

# 4 guiding question
A(s("dark",
    eyebrow("Today&#8217;s question"),
    h2("How do HTML, CSS, and JavaScript work together to build a web page, and what makes a modern frontend meaningful, adaptable, and efficient to build?",
       "max-width:30ch"),
    ar("السؤال الرئيسي: إزاي HTML و CSS و JavaScript بيشتغلوا مع بعض عشان يبنوا صفحة ويب، وإيه اللي بيخلي الواجهة الأمامية الحديثة ليها معنى، وقابلة للتكيف، وفعّالة في البناء؟")))

# 5 the map
A(s("",
    eyebrow("Today&#8217;s map &#183; a long one"),
    h2("Three parts from the book, three on the platform", "max-width:26ch"),
    '<div class="rise kit">'
    '<div class="card"><div class="ico">&#127959;</div><div class="role">Part 1</div><h3>HTML, CSS, JS</h3><p>Who does what</p></div>'
    '<div class="card"><div class="ico">&#127991;</div><div class="role">Part 2</div><h3>Semantic HTML</h3><p>Tags with meaning</p></div>'
    '<div class="card"><div class="ico">&#128241;</div><div class="role">Part 3</div><h3>Responsive &amp; frameworks</h3><p>Every screen; ready-made parts</p></div>'
    '<div class="card"><div class="ico">&#128221;</div><div class="role">Qureo 34</div><h3>HTML (2)</h3><p>Ranges, inputs, buttons</p></div>'
    '<div class="card"><div class="ico">&#127912;</div><div class="role">Qureo 35</div><h3>CSS (2)</h3><p>Decorate a button, add borders</p></div>'
    '<div class="card"><div class="ico">&#128295;</div><div class="role">Qureo 36</div><h3>Review</h3><p>Build a sign-up card</p></div>'
    '</div>',
    ar("خريطة المحاضرة: 1 أدوار HTML و CSS و JavaScript. 2 HTML الدلالية. 3 التصميم المتجاوب وأطر العمل. وعلى المنصة: الفصل 34 HTML (2)، والفصل 35 CSS (2)، والفصل 36 مراجعة.")))

# 6 explore
A(s("",
    eyebrow("Explore &#183; in pairs"),
    h2("Before you read on", "max-width:20ch"),
    sub("Think of a page you use often &#8212; YouTube, your school&#8217;s site, a shop. With your partner, point to:",
        "max-width:56ch;margin-top:1rem"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>one thing that is <b>structure</b> &#8212; a heading, a list, a link;</li>'
    '<li>one thing that is <b>style</b> &#8212; a colour, a font, a layout;</li>'
    '<li>one thing that <b>reacts to you</b> when you click or type.</li>'
    '</ul>',
    sub("Keep your three. Part 1 says which technology does each.", "margin-top:.8rem;color:var(--soft)"),
    ar("في صفحة بتستخدمها كتير، إيه الأجزاء اللي بتمثل البنية (HTML)، وإيه اللي بتمثل الشكل (CSS)، وإيه اللي بيتفاعل معاك (JavaScript)؟")))

# ---------------- part 1: the roles of HTML, CSS and JavaScript ----------------

A(s("",
    eyebrow("Part 1 &#183; The roles of HTML, CSS, and JavaScript"),
    h2("A page is built like a building"),
    fig(LAYERS),
    sub("These three technologies each have independent roles, and a web page is created using them in combination.",
        "max-width:60ch;margin-top:.3rem"),
    ar("التقنيات دي بتأدي أدوار مختلفة: HTML بيبني الهيكل، و CSS بيضيف التنسيق، و JS بيضيف السلوك التفاعلي.")))

A(s("",
    eyebrow("1 &#183; Who does what"),
    h2("Structure, appearance, behavior"),
    '<table class="rise">'
    '<tr><th>Technology</th><th>Role</th><th>Analogy</th></tr>'
    '<tr><td><b>HTML</b></td><td>Defines the structure (skeleton): headings, paragraphs, images, links</td><td>The frame of a building</td></tr>'
    '<tr><td><b>CSS</b></td><td>Specifies the appearance: colours, layout, size, fonts</td><td>The interior and exterior</td></tr>'
    '<tr><td><b>JavaScript</b></td><td>Adds behavior and interactivity: responds when buttons are pressed, updates part of the screen</td><td>The electrical and plumbing systems</td></tr>'
    '</table>',
    sub("The Arabic book adds: a page does not have to use all three. It can be HTML alone, or HTML with CSS and JavaScript, depending on what it needs to do.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("HTML بيحدد بنية الصفحة، و CSS بيحدد مظهرها، و JavaScript بيضيف السلوك والتفاعلية. والصفحة ممكن تستخدم HTML لوحده، أو HTML مع CSS و JavaScript حسب الوظايف اللي محتاجاها.")))

A(s("",
    eyebrow("1 &#183; Watch it happen"),
    h2("Switch on the layers, one at a time"),
    layers(),
    ar("دوس 1 وبعدين 2 وبعدين 3: نفس الصفحة بـ HTML بس، وبعدين مع CSS، وبعدين مع JavaScript. جرّب تدوس على الزرار في كل مرحلة.")))

A(s("",
    eyebrow("1 &#183; Your turn"),
    h2("Which technology does each task?"),
    '<table class="rise">'
    '<tr><th>Task</th><th>Technology</th></tr>'
    '<tr><td>a &#183; Describing the structure of headings and paragraphs</td><td class="reveal"><span>A &#183; HTML</span></td></tr>'
    '<tr><td>b &#183; Changing the colour and size of text</td><td class="reveal"><span>B &#183; CSS</span></td></tr>'
    '<tr><td>c &#183; Updating part of the screen when a button is pressed</td><td class="reveal"><span>C &#183; JavaScript</span></td></tr>'
    '<tr><td>d &#183; Placing images and links</td><td class="reveal"><span>A &#183; HTML</span></td></tr>'
    '<tr><td>e &#183; Setting the background colour of the whole page</td><td class="reveal"><span>B &#183; CSS</span></td></tr>'
    '<tr><td>f &#183; Validating what is entered into a form</td><td class="reveal"><span>C &#183; JavaScript</span></td></tr>'
    '</table>',
    ar("لكل مهمة، أنهي تقنية؟ البنية ← HTML، الشكل ← CSS، التفاعل والتحديث ← JavaScript. جاوب الأول وبعدين دوس.")))

A(s("",
    eyebrow("1 &#183; Your turn &#183; worked example"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv tf-t">HTML is a technology that defines the structure (skeleton) of a web page. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv">CSS is a technology that adds behavior to a web page. <span class="ans">&#8212; <b>false</b>: CSS is appearance; behavior is JavaScript.</span></li>'
    '<li class="reveal rv tf-t">Responsive design adjusts the layout automatically to different screen sizes. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '<li class="reveal rv tf-t">Using a framework means you do not write all the code from scratch. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    sub("Tap each one to check.", "margin-top:.7rem;color:var(--soft)"),
    ar("المثال المحلول: HTML بيحدد البنية — صح. CSS بيضيف السلوك — غلط، ده JavaScript. التصميم المتجاوب بيظبط التخطيط حسب الشاشة — صح. إطار العمل بيوفّر الكتابة من الصفر — صح.")))

A(s("",
    eyebrow("1 &#183; Exam-style question"),
    h2("Match each role with a technology"),
    '<table class="rise">'
    '<tr><th>Role</th><th>Technology</th></tr>'
    '<tr><td>a &#183; Defines the structure of a web page</td><td class="reveal"><span>A &#183; HTML</span></td></tr>'
    '<tr><td>b &#183; Specifies the appearance of a web page</td><td class="reveal"><span>B &#183; CSS</span></td></tr>'
    '<tr><td>c &#183; Adds behavior and interactivity to a web page</td><td class="reveal"><span>C &#183; JavaScript</span></td></tr>'
    '</table>',
    sub("Choices: <b>A</b> HTML &#183; <b>B</b> CSS &#183; <b>C</b> JavaScript.", "max-width:58ch;margin-top:.8rem;color:var(--soft)"),
    ar("اربط كل دور بالتقنية: البنية = HTML، المظهر = CSS، السلوك والتفاعلية = JavaScript.")))

# ---------------- part 2: semantic HTML ----------------

A(s("",
    eyebrow("Part 2 &#183; Semantic HTML"),
    h2("Tags that say what a part is"),
    '<div class="rise statement def"><em>Semantic HTML</em> &#8212; describing each part of a page with element names (tags) that show their meaning.</div>',
    fig(SEMANTIC),
    ar("HTML الدلالي: استخدام عناصر بتوضح وظيفة أجزاء الصفحة، زي <span class='mono' dir='ltr'>&lt;header&gt;</span> في أعلى الصفحة، و <span class='mono' dir='ltr'>&lt;nav&gt;</span> للتنقل، و <span class='mono' dir='ltr'>&lt;main&gt;</span> للمحتوى الرئيسي، و <span class='mono' dir='ltr'>&lt;footer&gt;</span> في أسفل الصفحة.")))

A(s("",
    eyebrow("2 &#183; Why use it?"),
    h2("Two benefits"),
    '<table class="rise">'
    '<tr><th>Benefit</th><th>What it means</th></tr>'
    '<tr><td><b>Accessibility</b></td><td>Screen-reader software can understand the page&#8217;s structure, so information reaches users with visual impairments more easily.</td></tr>'
    '<tr><td><b>SEO</b> (search engine optimization)</td><td>Search engines can understand the content more easily, so it is more likely to be shown properly in results.</td></tr>'
    '</table>',
    sub("The Arabic book is careful: semantic HTML <b>helps</b> search engines, but it does not <b>guarantee</b> a higher ranking &#8212; and accessibility needs other good practices too.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Pause &amp; think: why does a screen reader understand a page better with &lt;header&gt;, &lt;nav&gt; and &lt;main&gt; than with plain boxes? <span class="ans">&#8212; the tag <b>names the part</b>, so it can say &#8220;navigation&#8221; or &#8220;main content&#8221; and let the user jump there.</span></li>'
    '</ul>',
    ar("فوايد HTML الدلالي: إمكانية الوصول — بيساعد قارئ الشاشة يفهم بنية الصفحة ويتنقل فيها، مع الحاجة لممارسات وصول تانية. وفهم محركات البحث للمحتوى — ممكن يساعدها، لكنه مش بيضمن ترتيب أعلى.")))

A(s("",
    eyebrow("2 &#183; The same page, two ways"),
    h2("Plain boxes or meaningful tags?"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Plain boxes</h3>'
    '<div class="code" style="font-size:clamp(11px,1.3vw,16px)">' + hl('<div>Science Club</div>\n<div>Home | Events</div>\n<div>Robot day ...</div>\n<div>© 2026</div>') + '</div>'
    '<p>Works &#8212; but nothing says which part is which.</p></div>'
    '<div class="pane b"><h3>Semantic HTML</h3>'
    '<div class="code" style="font-size:clamp(11px,1.3vw,16px)">' + hl('<header>Science Club</header>\n<nav>Home | Events</nav>\n<main>Robot day ...</main>\n<footer>© 2026</footer>') + '</div>'
    '<p>Same look &#8212; and every part is named.</p></div>'
    '</div>',
    ar("الاتنين ممكن يبانوا نفس الشكل، بس في التاني كل جزء ليه اسم بيوضح وظيفته.")))

A(s("",
    eyebrow("2 &#183; Your turn"),
    h2("Which element is used for&#8230;?"),
    '<table class="rise">'
    '<tr><th>Element</th><th>Used for</th></tr>'
    '<tr><td><b class="mono">&lt;header&gt;</b></td><td class="reveal"><span>the top of the page</span></td></tr>'
    '<tr><td><b class="mono">&lt;nav&gt;</b></td><td class="reveal"><span>navigating between parts of the site</span></td></tr>'
    '<tr><td><b class="mono">&lt;main&gt;</b></td><td class="reveal"><span>the main content</span></td></tr>'
    '<tr><td><b class="mono">&lt;footer&gt;</b></td><td class="reveal"><span>the bottom of the page</span></td></tr>'
    '</table>',
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Which is NOT a semantic element: &lt;header&gt;, &lt;E-mail&gt;, &lt;main&gt;, &lt;footer&gt;? <span class="ans">&#8212; <b>&lt;E-mail&gt;</b>: there is no such element.</span></li>'
    '</ul>',
    ar("العنصر <span class='mono' dir='ltr'>&lt;header&gt;</span> لرأس الصفحة، و <span class='mono' dir='ltr'>&lt;nav&gt;</span> للتنقل، و <span class='mono' dir='ltr'>&lt;main&gt;</span> للمحتوى الرئيسي، و <span class='mono' dir='ltr'>&lt;footer&gt;</span> للتذييل. أسئلة زي دي موجودة في كتاب التقييمات.")))

# ---------------- part 3: responsive design and frameworks ----------------

A(s("",
    eyebrow("Part 3 &#183; Responsive design"),
    h2("One page, every screen"),
    '<div class="rise statement def"><em>Responsive design</em> &#8212; the layout adjusts automatically to different screen sizes: PCs, smartphones and tablets.</div>',
    resp(),
    ar("التصميم المتجاوب: مفهوم تصميمي بيتظبط فيه التخطيط تلقائيًا حسب أحجام الشاشات المختلفة. دوس Phone و Tablet و PC وشوف نفس الصفحة بتتغير.")))

A(s("",
    eyebrow("3 &#183; Mobile first"),
    h2("Why it matters now", "max-width:24ch"),
    sub("Many people use the web on their phones, so developers think about small screens from the very start of the design. This is called <b>mobile-first</b>.",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li class="reveal rv">Why is responsive design needed? <span class="ans">&#8212; because websites are accessed from many devices: PCs, smartphones and tablets.</span></li>'
    '<li class="reveal rv">Does it make the server faster? <span class="ans">&#8212; <b>no</b>: it is about the layout on the screen.</span></li>'
    '<li class="reveal rv">&#8220;Mobile-first&#8221; means designing first for&#8230; <span class="ans">&#8212; <b>small screens such as phones</b>.</span></li>'
    '</ul>',
    ar("ناس كتير بتستخدم الويب من الموبايل، عشان كده المطورين بيراعوا الشاشات الصغيرة من بداية التصميم. وده اسمه نهج الأولوية للجوال.")))

A(s("",
    eyebrow("3 &#183; Frameworks"),
    h2("Frameworks: ready-made parts", "max-width:24ch"),
    '<div class="rise statement def"><em>Framework</em> &#8212; a structure that provides common functions and components in advance, to make web application development more efficient.</div>',
    '<table class="rise" style="margin-top:.8rem">'
    '<tr><th>Name</th><th>What to know</th></tr>'
    '<tr><td><b>React</b></td><td>From Meta (formerly Facebook). Updates only part of the screen; suits large web apps. The Arabic book: a JavaScript library for building interfaces from reusable components.</td></tr>'
    '<tr><td><b>Vue</b></td><td>A simple structure; build an app step by step, starting from small features.</td></tr>'
    '<tr><td><b>Next.js</b></td><td>Built on React; adds ways to show pages faster (routing, rendering on the server and the client).</td></tr>'
    '</table>',
    ar("إطار العمل: بنية بتوفر وظايف ومكونات شائعة مسبقًا، عشان تطوير تطبيقات الويب يبقى أكفأ؛ فمش لازم تكتب الكود كله من الصفر. React مكتبة JavaScript لبناء الواجهات من مكونات بتتعاد، و Vue بنيته بسيطة، و Next.js مبني على React.")))

A(s("",
    eyebrow("Exam warning"),
    h2("True or false?"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">Using semantic HTML necessarily makes a page display faster. <span class="ans">&#8212; <b>false</b>: its benefits are accessibility and SEO.</span></li>'
    '<li class="reveal rv">A framework is a language for defining the structure of a page. <span class="ans">&#8212; <b>false</b>: that is HTML.</span></li>'
    '<li class="reveal rv">Responsive design means the page works only on computers. <span class="ans">&#8212; <b>false</b>: it adapts to every screen.</span></li>'
    '<li class="reveal rv tf-t">Next.js is built on React. <span class="ans">&#8212; <b>true</b>.</span></li>'
    '</ul>',
    ar("خلّي بالك: HTML الدلالي مش بيسرّع الصفحة بالضرورة. إطار العمل مش لغة لبنية الصفحة. التصميم المتجاوب مش للكمبيوتر بس. و Next.js مبني على React — صح.")))

A(s("",
    eyebrow("Exam-style question &#183; 6 marks"),
    h2("A library page", "max-width:24ch"),
    '<div class="rise vs">'
    '<div class="pane a"><h3>Explain&#8230;</h3><ul>'
    '<li>how HTML, CSS and JavaScript each contribute to a library page that <b>lists books</b>, is <b>styled</b>, and <b>filters the results</b> as the user types</li>'
    '<li>refer to: structure, appearance, behavior</li>'
    '</ul></div>'
    '<div class="pane b"><h3>A plan for your answer</h3><ul>'
    '<li>HTML: the list of books, the search box</li>'
    '<li>CSS: colours, fonts, the layout of the list</li>'
    '<li>JavaScript: hides the books that do not match, as you type</li>'
    '</ul></div>'
    '</div>',
    ar("سؤال على نمط الامتحان: اشرح إزاي HTML و CSS و JavaScript بيساهموا في صفحة مكتبة بتعرض قائمة كتب، ومتنسّقة، وبتصفّي النتايج وانت بتكتب. راجع: البنية، المظهر، السلوك.")))

A(s("",
    eyebrow("Think as an engineer"),
    h2("A student club wants a page", "max-width:26ch"),
    sub("It lists the club&#8217;s events, uses the club&#8217;s colours, and has a button showing how many people have signed up.",
        "max-width:58ch;margin-top:.6rem"),
    '<ul class="rise check" style="margin-top:.8rem">'
    '<li><b>Observe first.</b> On a page you use, note two things that change when you click or type. Then: the list of events, the club&#8217;s colours and layout, the live sign-up counter &#8212; which technology does each, and why?</li>'
    '<li><b>Make it reach everyone.</b> One change for phones (responsive design), one semantic-HTML choice for a screen reader.</li>'
    '<li><b>Decide.</b> Separate HTML, CSS and JavaScript? Two reasons. In pairs, agree on what the counter needs.</li>'
    '</ul>',
    sub("Stuck? HTML holds the content; CSS styles it; JavaScript makes it react and update.",
        "max-width:60ch;margin-top:.8rem;color:var(--soft)"),
    ar("فكّر كمهندس: نادي طلابي عايز صفحة بتعرض الفعاليات، بألوان النادي، وفيها زرار بيعرض عدد المسجلين. حدد التقنية لكل ميزة، وغيّر حاجة للموبايل وحاجة لقارئ الشاشة، وقرّر بسببين.")))

A(s("",
    eyebrow("In a new context"),
    h2("A news site", "max-width:26ch"),
    sub("It must look good on phones and be found easily by search engines.", "max-width:56ch;margin-top:.7rem"),
    '<table class="rise">'
    '<tr><th>Choice</th><th>What it improves</th></tr>'
    '<tr><td>A responsive-design choice, e.g. one column on a phone</td><td class="reveal"><span>easy to read on any screen</span></td></tr>'
    '<tr><td>A semantic-HTML choice, e.g. &lt;header&gt;, &lt;nav&gt;, &lt;main&gt;</td><td class="reveal"><span>search engines and screen readers understand it</span></td></tr>'
    '</table>',
    ar("طبّق اللي اتعلمته: موقع أخبار لازم يبان كويس على الموبايل ويتلاقي بسهولة في محركات البحث. اذكر اختيار من التصميم المتجاوب واختيار من HTML الدلالي، وكل واحد بيحسّن إيه.")))

A(s("",
    eyebrow("Key takeaway &middot; lesson 3-3"),
    h2("Structure, style, behavior", "max-width:24ch"),
    '<p class="rise sub" style="max-width:60ch;margin-bottom:.6rem"><b>Hands up again:</b> the pink title &#8212; which technology? (CSS: it is appearance.)</p>'
    '<div class="rise statement">HTML <em>structures</em>, CSS <em>styles</em>, JavaScript <em>behaves</em> &#8212; and semantic HTML, responsive design and frameworks make a modern frontend <em>meaningful, adaptable and efficient</em>.</div>',
    ar("افتكر: HTML بيبني، و CSS بينسّق، و JavaScript بيتفاعل — و HTML الدلالي والتصميم المتجاوب وأطر العمل بيخلّوا الواجهة الأمامية الحديثة ليها معنى، وبتتكيف، وفعّالة في البناء.")))

# unit wrap -- this lesson closes Unit 3
A(s("",
    eyebrow("Unit 3 &#183; complete"),
    h2("Web applications, in three lessons", "max-width:28ch"),
    '<div class="rise timeline">'
    '<div class="tl"><h3>3-1 &#183; The overall structure of web applications</h3><p>Frontend, backend, database &#8212; three tiers cooperating</p></div>'
    '<div class="tl"><h3>3-2 &#183; Web application communication methods</h3><p>Client and server, HTTP/HTTPS, GET/POST, status codes, API and JSON</p></div>'
    '<div class="tl"><h3>3-3 &#183; Fundamentals of frontend technology</h3><p>HTML, CSS, JavaScript; semantic HTML, responsive design, frameworks</p></div>'
    '</div>',
    ar("خلصنا الوحدة التالتة: 3-1 البنية العامة لتطبيقات الويب، 3-2 طرق اتصال تطبيقات الويب، 3-3 أساسيات تقنية الواجهة الأمامية.")))

# ---------------- part 4: Qureo 34, HTML (2) ----------------

A(s("dark",
    '<div class="rise part">4</div>',
    h2("On the platform: HTML (2)"),
    sub("Qureo chapter 34: an HTML review, then marking ranges with div and span, then text boxes and buttons. You will type it yourself.", "max-width:56ch"),
    ar("الجزء الرابع على المنصة: الفصل 34 — HTML (2): مراجعة، وبعدين تحديد نطاقات بـ div و span، وبعدين خانات الإدخال والأزرار. وهتكتب بنفسك.")))

A(s("",
    eyebrow("4 &#183; HTML review"),
    h2("An element: a tag, the content, a closing tag", "max-width:28ch"),
    codebox('<h1>Science Club</h1>\n<p>We build robots every Thursday.</p>\n<a href="events.html">See the events</a>'),
    '<table class="rise">'
    '<tr><th>Tag</th><th>Makes</th></tr>'
    '<tr><td><b class="mono">&lt;h1&gt;</b></td><td class="reveal"><span>a big heading</span></td></tr>'
    '<tr><td><b class="mono">&lt;p&gt;</b></td><td class="reveal"><span>a paragraph</span></td></tr>'
    '<tr><td><b class="mono">&lt;a href="..."&gt;</b></td><td class="reveal"><span>a link to another page</span></td></tr>'
    '</table>',
    ar("العنصر = وسم فتح + المحتوى + وسم قفل، زي <span class='mono' dir='ltr'>&lt;p&gt;…&lt;/p&gt;</span>. والوسم بيقول للمتصفح الجزء ده إيه: عنوان، ولا فقرة، ولا رابط.")))

A(s("",
    eyebrow("4 &#183; Try it"),
    h2("Write HTML, see the page"),
    live('<h1>Science Club</h1>\n<p>We build robots every Thursday.</p>\n<p>Next event: Robot day.</p>', 6),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>Change the heading to your own club&#8217;s name.</li>'
    '<li>Add a third paragraph with the day and the time.</li>'
    '<li>Change <span class="codeline">&lt;h1&gt;</span> to <span class="codeline">&lt;h2&gt;</span> &#8212; what happens?</li>'
    '</ul>',
    ar("اكتب في المربع الغامق، والنتيجة بتتحدّث لوحدها. جرّب المهام التلاتة اللي تحت.")))

A(s("",
    eyebrow("4 &#183; Specifying ranges"),
    h2("div for a box, span for a few words"),
    '<div class="rise twocol"><div>'
    + '<div class="code" style="font-size:clamp(11px,1.3vw,17px)">' + hl('<div class="card">\n  <h3>Robot day</h3>\n  <p>Thursday, 2 pm</p>\n</div>\n\n<p>Bring your <span class="hot">own laptop</span>.</p>') + '</div>'
    + '</div><div>'
    '<div class="preview"><div style="border:2px solid var(--teal);border-radius:10px;padding:.6rem .8rem;margin-bottom:.8rem">'
    '<h3 style="margin:0 0 .2rem">Robot day</h3><p style="margin:0">Thursday, 2 pm</p></div>'
    '<p style="margin:0">Bring your <span style="background:var(--gold-pale);color:#9C3B2E;font-weight:700">own laptop</span>.</p></div>'
    '<table style="margin-top:.8rem"><tr><th>Tag</th><th>Marks</th></tr>'
    '<tr><td><b class="mono">&lt;div&gt;</b></td><td>a block: a box that holds several elements</td></tr>'
    '<tr><td><b class="mono">&lt;span&gt;</b></td><td>a range inside a line of text</td></tr></table>'
    '</div></div>',
    ar("<span class='mono' dir='ltr'>&lt;div&gt;</span> بيحدد نطاق كبير — صندوق جوّاه كذا عنصر. و <span class='mono' dir='ltr'>&lt;span&gt;</span> بيحدد نطاق صغير جوّه سطر. ومع class نقدر ننسّق النطاق ده بـ CSS.")))

A(s("",
    eyebrow("4 &#183; Input fields and buttons"),
    h2("Let the user type and press"),
    codebox('<input type="text" placeholder="Your name">\n<button>Sign up</button>', "font-size:clamp(12px,1.45vw,19px)"),
    '<div class="rise preview" style="max-width:520px"><input type="text" placeholder="Your name" style="font:inherit;padding:.35em .6em;margin-right:.4rem"> <button type="button" style="font:inherit;padding:.35em .9em">Sign up</button></div>',
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">What does <span class="codeline">placeholder</span> do? <span class="ans">&#8212; shows a grey hint in the box until the user types.</span></li>'
    '<li class="reveal rv">Does &lt;input&gt; need a closing tag? <span class="ans">&#8212; <b>no</b>: it stands alone. &lt;button&gt; does: &lt;button&gt;Sign up&lt;/button&gt;.</span></li>'
    '</ul>',
    ar("<span class='mono' dir='ltr'>&lt;input&gt;</span> بيعمل خانة يكتب فيها المستخدم، و placeholder تلميح رمادي. و <span class='mono' dir='ltr'>&lt;button&gt;</span> بيعمل زرار. ودوس جرّب تكتب في الخانة اللي فوق.")))

A(s("",
    eyebrow("4 &#183; Try it"),
    h2("Build a sign-up row"),
    live('<h2>Join the club</h2>\n<input type="text" placeholder="Your name">\n<button>Sign up</button>', 5),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>Add a second input with the placeholder <span class="codeline">Your class</span>.</li>'
    '<li>Change the button&#8217;s text to <span class="codeline">Join now</span>.</li>'
    '<li>Put the heading and the two inputs in one <span class="codeline">&lt;div&gt;</span>.</li>'
    '</ul>',
    ar("زوّد خانة تانية، وغيّر كلام الزرار، وحط كله جوّه div واحد.")))

A(s("",
    eyebrow("4 &#183; Your turn"),
    h2("Which tag?"),
    '<table class="rise">'
    '<tr><th>I want&#8230;</th><th>Tag</th></tr>'
    '<tr><td>a box where the user types a name</td><td class="reveal"><span>&lt;input&gt;</span></td></tr>'
    '<tr><td>a box that groups a heading and two paragraphs</td><td class="reveal"><span>&lt;div&gt;</span></td></tr>'
    '<tr><td>to colour two words in the middle of a sentence</td><td class="reveal"><span>&lt;span&gt;</span></td></tr>'
    '<tr><td>something the user can press</td><td class="reveal"><span>&lt;button&gt;</span></td></tr>'
    '<tr><td>a link to another page</td><td class="reveal"><span>&lt;a href="..."&gt;</span></td></tr>'
    '</table>',
    ar("لكل حاجة، أنهي وسم؟ فكّر الأول وبعدين دوس.")))

# ---------------- part 5: Qureo 35, CSS (2) ----------------

A(s("dark",
    '<div class="rise part">5</div>',
    h2("On the platform: CSS (2)"),
    sub("Qureo chapter 35: a CSS review, then decorating a button, then adding borders.", "max-width:56ch"),
    ar("الجزء الخامس على المنصة: الفصل 35 — CSS (2): مراجعة، وبعدين تزيين الزرار، وبعدين إضافة إطارات.")))

A(s("",
    eyebrow("5 &#183; CSS review"),
    h2("Which part, what to change, how"),
    codebox('button {\n  color: white;\n  background-color: green;\n}'),
    '<table class="rise">'
    '<tr><th>Part</th><th>In the example</th><th>It says</th></tr>'
    '<tr><td><b>selector</b></td><td class="mono">button</td><td><b>which</b> part to change</td></tr>'
    '<tr><td><b>property</b></td><td class="mono">background-color</td><td><b>what</b> to change</td></tr>'
    '<tr><td><b>value</b></td><td class="mono">green</td><td><b>how</b> to change it</td></tr>'
    '</table>',
    sub("A class selector starts with a dot: <span class=\"codeline\">.big { &#8230; }</span> styles every element with <span class=\"codeline\">class=\"big\"</span>.", "max-width:60ch;margin-top:.7rem"),
    ar("CSS بيحدد أنهي جزء (المحدِّد selector)، وإيه اللي يتغير (الخاصية property)، وإزاي (القيمة value). ومحدِّد الـ class بيبدأ بنقطة.")))

A(s("",
    eyebrow("5 &#183; Decorating a button (1)"),
    h2("Colours and size"),
    '<div class="rise twocol"><div>'
    '<div class="code" style="font-size:clamp(11px,1.3vw,17px)">' + hl('button {\n  background-color: #2D7A4B;\n  color: white;\n  font-size: 20px;\n}') + '</div></div><div>'
    '<table><tr><th>Before</th><th>After</th></tr><tr>'
    '<td><button type="button" style="font:14px Arial">Sign up</button></td>'
    '<td><button type="button" style="background-color:#2D7A4B;color:#fff;font-size:20px;border:1px solid #2D7A4B">Sign up</button></td></tr></table>'
    '<ul class="check" style="margin-top:.6rem">'
    '<li class="reveal rv"><span class="codeline">color</span> or <span class="codeline">background-color</span> &#8212; which one colours the text? <span class="ans">&#8212; <b>color</b>. background-color fills behind it.</span></li>'
    '</ul></div></div>',
    ar("background-color بيلوّن خلفية الزرار، و color بيلوّن الكلام، و font-size بيكبّر الخط.")))

A(s("",
    eyebrow("5 &#183; Decorating a button (2)"),
    h2("Space inside, round corners"),
    '<div class="rise twocol"><div>'
    '<div class="code" style="font-size:clamp(11px,1.3vw,17px)">' + hl('button {\n  background-color: #2D7A4B;\n  color: white;\n  padding: 12px 28px;\n  border-radius: 30px;\n}') + '</div></div><div>'
    '<table><tr><th>Property</th><th>Result</th></tr>'
    '<tr><td><b class="mono">padding</b></td><td>space <b>inside</b> the button, around the text</td></tr>'
    '<tr><td><b class="mono">border-radius</b></td><td>rounds the corners</td></tr></table>'
    '<div class="preview" style="margin-top:.8rem;text-align:center">'
    '<button type="button" style="background-color:#2D7A4B;color:#fff;padding:12px 28px;border-radius:30px;border:0;font:600 18px Inter,sans-serif">Sign up</button></div>'
    '</div></div>',
    ar("padding بيعمل مسافة جوّه الزرار حوالين الكلام، و border-radius بيدوّر الأركان.")))

A(s("",
    eyebrow("5 &#183; Adding borders"),
    h2("border: width, style, colour"),
    codebox('.card {\n  border: 3px solid #7A3B69;\n  border-radius: 12px;\n  padding: 16px;\n}', "font-size:clamp(12px,1.45vw,19px)"),
    '<div class="rise" style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:.4rem">'
    '<div class="preview" style="border:3px solid #7A3B69;border-radius:12px">solid</div>'
    '<div class="preview" style="border:3px dashed #7A3B69;border-radius:12px">dashed</div>'
    '<div class="preview" style="border:3px dotted #7A3B69;border-radius:12px">dotted</div>'
    '</div>',
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">In <span class="codeline">border: 2px dashed red</span>, what are the three parts? <span class="ans">&#8212; the width <b>2px</b>, the style <b>dashed</b>, the colour <b>red</b>.</span></li>'
    '</ul>',
    ar("border بياخد تلات حاجات: السُمك، والنوع (solid أو dashed أو dotted)، واللون.")))

A(s("",
    eyebrow("5 &#183; Try it"),
    h2("Decorate the button yourself"),
    live('<button>Sign up</button>\n\n<style>\n  button {\n    background-color: green;\n    color: white;\n    font-size: 20px;\n  }\n</style>', 9),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>Add <span class="codeline">padding: 12px 28px;</span></li>'
    '<li>Add <span class="codeline">border-radius: 30px;</span></li>'
    '<li>Add a border: <span class="codeline">border: 3px solid black;</span> &#8212; then try <span class="codeline">dashed</span>.</li>'
    '</ul>',
    ar("زوّد كل سطر جوّه أقواس button وشوف الزرار بيتغير إزاي.")))

A(s("",
    eyebrow("5 &#183; Your turn"),
    h2("Predict, then check"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv"><span class="codeline">color: red;</span> on a button changes&#8230; <span class="ans">&#8212; the colour of its <b>text</b>.</span></li>'
    '<li class="reveal rv"><span class="codeline">padding: 30px;</span> makes the button&#8230; <span class="ans">&#8212; <b>bigger</b>: more space inside.</span></li>'
    '<li class="reveal rv"><span class="codeline">border-radius: 0;</span> gives&#8230; <span class="ans">&#8212; <b>sharp</b> corners.</span></li>'
    '<li class="reveal rv">To style only buttons with <span class="codeline">class="big"</span>, the selector is&#8230; <span class="ans">&#8212; <b>.big</b> (with a dot).</span></li>'
    '</ul>',
    ar("توقّع الأول، وبعدين دوس وشوف.")))

# ---------------- part 6: Qureo 36, comprehension check ----------------

A(s("dark",
    '<div class="rise part">6</div>',
    h2("Comprehension check: chapters 34 and 35"),
    sub("Qureo chapter 36 reviews HTML (2) and CSS (2). Put them together: build a sign-up card.", "max-width:56ch"),
    ar("الجزء السادس: الفصل 36 — مراجعة الفصلين 34 و 35. هنجمعهم ونبني كارت تسجيل.")))

A(s("",
    eyebrow("6 &#183; Mini project"),
    h2("A sign-up card"),
    live('<div class="card">\n  <h2>Science Club</h2>\n  <p>Join us on <span class="hot">Thursday</span>!</p>\n  <input type="text" placeholder="Your name">\n  <button>Sign up</button>\n</div>\n\n<style>\n  .card {\n    border: 3px solid #7A3B69;\n    border-radius: 12px;\n    padding: 16px;\n  }\n</style>', 12),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li>Style the button: a background colour, white text, padding, round corners.</li>'
    '<li>Make <span class="codeline">.hot</span> red and bold: <span class="codeline">color: red; font-weight: bold;</span></li>'
    '<li>Give the card a background colour of your own.</li>'
    '</ul>',
    ar("مشروع صغير: كارت تسجيل فيه div و span و input و button، ونسّقه بـ CSS. نفّذ المهام التلاتة.")))

A(s("",
    eyebrow("6 &#183; Review &#183; your turn"),
    h2("HTML and CSS, quick-fire"),
    '<ul class="rise check" style="margin-top:.6rem">'
    '<li class="reveal rv">The tag for a text box&#8230; <span class="ans">&#8212; <b>&lt;input&gt;</b>.</span></li>'
    '<li class="reveal rv">The tag that marks a range inside a sentence&#8230; <span class="ans">&#8212; <b>&lt;span&gt;</b>.</span></li>'
    '<li class="reveal rv">In <span class="codeline">p { color: blue; }</span>, the property is&#8230; <span class="ans">&#8212; <b>color</b> (p is the selector, blue the value).</span></li>'
    '<li class="reveal rv">The property that adds space inside a button&#8230; <span class="ans">&#8212; <b>padding</b>.</span></li>'
    '<li class="reveal rv">HTML, CSS or JavaScript: making the button count sign-ups&#8230; <span class="ans">&#8212; <b>JavaScript</b>: that is behavior.</span></li>'
    '</ul>',
    ar("مراجعة سريعة: فكّر في كل سطر الأول، وبعدين دوس عليه.")))

A(s("dark",
    eyebrow("Remember these"),
    h2("What we learned"),
    '<ul class="rise check">'
    '<li><b>HTML</b> structures, <b>CSS</b> styles, <b>JavaScript</b> behaves &#8212; a page uses them in combination.</li>'
    '<li><b>Semantic HTML</b> (&lt;header&gt;, &lt;nav&gt;, &lt;main&gt;, &lt;footer&gt;) helps accessibility and SEO.</li>'
    '<li><b>Responsive design</b> fits every screen; <b>mobile-first</b> starts with phones. <b>Frameworks</b> give ready-made parts.</li>'
    '<li>HTML (2): <b>div</b> and <b>span</b> mark ranges; <b>input</b> and <b>button</b> let the user type and press.</li>'
    '<li>CSS (2): <b>selector { property: value; }</b> &#8212; background-color, color, padding, border-radius, border.</li>'
    '</ul>',
    ar("HTML بيبني، CSS بينسّق، JavaScript بيتفاعل • HTML الدلالي للوصول ومحركات البحث • التصميم المتجاوب وأطر العمل • div و span و input و button • والـ CSS: محدِّد وخاصية وقيمة.")))

# QR -- must stay last
A(s("dark",
    eyebrow("Before you go"),
    h2("Exam &#8212; Lecture 11"),
    '<div class="rise qrwrap qrgate" id="qrgate" role="button" tabindex="0" '
    'aria-label="Reveal the exam code">'
    '<div class="qrhide"><b>Exam code hidden</b>'
    '<span>The code appears when your teacher reveals it &#8212; press <kbd>E</kbd></span>'
    '<span class="ar">الكود بيظهر لما المدرّس يعرضه &#8212; اضغط E</span></div>'
    '<img id="qr" alt="QR code linking to the Lecture 11 quiz" width="250" height="250">'
    '<div class="txt"><p class="sub">It covers lesson 3-3 and Qureo chapters 34 to 36. '
    'At the end it shows you, section by section, which parts to read again.</p>'
    '<p class="sub mono" style="margin-top:.7rem;font-size:clamp(12px,1.3vw,17px)">'
    '<a id="quizLink" href="../quiz/"></a></p></div>'
    '</div>',
    ar("امتحان على الدرس 3-3 والفصول من 34 لـ 36 على المنصة. في الآخر هيوضحلك انت ضعيف في أنهي جزء بالظبط.")))
