# ------------------------------------------------------------------ booklet
def booklet(head, tail):
    """The booklet follows the deck slide by slide, in the same order, so what
    a student revises from is what they were taught from. The slide numbers
    in the comments are the deck's; keep them in step when either changes.
    The live demos print as tables and as the code students typed. The
    title and the exam QR have no page."""
    LAYERS, SEMANTIC = slide_svg("LAYERS"), slide_svg("SEMANTIC")

    def code(t):
        return '<div class="code">' + esc(t) + '</div>'

    p = []
    # slides 2-6: recap, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Before we start &middot; lesson 3-2</h2>'
        '<table><tr><th style="width:26%">Word</th><th>Meaning</th></tr>'
        '<tr><td class="k">Client / server</td><td>the client requests, the server responds</td></tr>'
        '<tr><td class="k">HTTP / HTTPS</td><td>the rules for the messages; HTTPS adds TLS encryption</td></tr>'
        '<tr><td class="k">GET / POST</td><td>retrieve data / send data</td></tr>'
        '<tr><td class="k">200 / 404 / 500</td><td>success / not found / server error</td></tr></table>'
        '<h2>Three technologies at work</h2>'
        '<p>Open any web page and you are seeing three technologies at work together. HTML builds the structure &mdash; the '
        'headings, paragraphs and links, like the frame of a building. CSS adds the appearance &mdash; colours, layout and '
        'fonts, like a building&#8217;s interior. JavaScript adds behavior &mdash; search boxes that respond, buttons that '
        'count, screens that update.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> How do HTML, CSS, and JavaScript work together to build a web '
        'page, and what makes a modern frontend meaningful, adaptable, and efficient to build?</p>'
        '<p class="ar">إزاي HTML و CSS و JavaScript بيشتغلوا مع بعض عشان يبنوا صفحة ويب، وإيه اللي بيخلي الواجهة الأمامية الحديثة ليها معنى وقابلة للتكيف وفعّالة؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> On a page you use often, point to one thing that is '
        'structure, one that is style, and one that reacts to you.</p>'
        '<p class="ar">اكتبوا التلاتة قبل ما تكمّلوا.</p></div>'))
    # slides 7-10: the three roles, watch the layers
    p.append(page(
        '<h2>Part 1 &middot; The roles of HTML, CSS, and JavaScript</h2>'
        + dg(LAYERS)
        + '<table><tr><th style="width:16%">Technology</th><th>Role</th><th style="width:28%">Analogy</th></tr>'
        '<tr><td class="k">HTML</td><td>Defines the structure (skeleton): headings, paragraphs, images, links</td><td>The frame of a building</td></tr>'
        '<tr><td class="k">CSS</td><td>Specifies the appearance: colours, layout, size, fonts</td><td>The interior and exterior</td></tr>'
        '<tr><td class="k">JavaScript</td><td>Adds behavior and interactivity: responds to buttons, updates part of the screen</td><td>The electrical and plumbing systems</td></tr></table>'
        '<p class="ar">والصفحة مش لازم تستخدم التلاتة: ممكن HTML لوحده، أو HTML مع CSS و JavaScript حسب اللي محتاجاه.</p>'
        '<h2>Switch on the layers</h2>'
        '<table><tr><th style="width:22%">Stage</th><th>What you see</th></tr>'
        '<tr><td class="k">HTML only</td><td>The content and its structure: a heading, a paragraph, a button. No colours; the button does nothing.</td></tr>'
        '<tr><td class="k">+ CSS</td><td>The same content with colours, spacing and a styled button. The button still does nothing.</td></tr>'
        '<tr><td class="k">+ JavaScript</td><td>Now the button responds: press it and the count goes up.</td></tr></table>'))
    # slides 10-13: your turn, true or false, match, semantic HTML defined
    p.append(page(
        '<table><tr><th>Task</th><th style="width:22%">Technology</th></tr>'
        '<tr><td>Describing the structure of headings and paragraphs</td><td>HTML</td></tr>'
        '<tr><td>Changing the colour and size of text</td><td>CSS</td></tr>'
        '<tr><td>Updating part of the screen when a button is pressed</td><td>JavaScript</td></tr>'
        '<tr><td>Placing images and links</td><td>HTML</td></tr>'
        '<tr><td>Setting the background colour of the whole page</td><td>CSS</td></tr>'
        '<tr><td>Validating what is entered into a form</td><td>JavaScript</td></tr></table>'
        '<table><tr><th>True or false?</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>HTML defines the structure (skeleton) of a web page.</td><td>True</td></tr>'
        '<tr><td>CSS adds behavior to a web page.</td><td><b>False</b> &mdash; behavior is JavaScript</td></tr>'
        '<tr><td>Responsive design adjusts the layout to different screen sizes.</td><td>True</td></tr>'
        '<tr><td>A framework means you do not write all the code from scratch.</td><td>True</td></tr></table>'
        '<h2>Part 2 &middot; Semantic HTML</h2>'
        + term('Semantic HTML', 'Describing each part of a web page with element names (tags) that show their meaning: '
               '<header> at the top, <nav> for navigation, <main> for the body, <footer> at the bottom.',
               'HTML الدلالي: استخدام عناصر بتوضح وظيفة أجزاء الصفحة.')))
    # slides 13-15: the skeleton, benefits, two ways
    p.append(page(
        dg(SEMANTIC)
        + '<table><tr><th style="width:24%">Benefit</th><th>What it means</th></tr>'
        '<tr><td class="k">Accessibility</td><td>Screen readers understand the page&#8217;s structure, so information reaches users with visual impairments more easily.</td></tr>'
        '<tr><td class="k">SEO</td><td>Search engines understand the content more easily, so it is more likely to be shown properly in results.</td></tr></table>'
        '<p class="ar">الكتاب العربي: HTML الدلالي بيساعد محركات البحث لكنه مش بيضمن ترتيب أعلى، والوصول محتاج ممارسات تانية كمان.</p>'
        '<div class="fcrow"><div><b>Plain boxes</b>'
        + code('<div>Science Club</div>\n<div>Home | Events</div>\n<div>Robot day ...</div>\n<div>© 2026</div>')
        + '</div><div><b>Semantic HTML</b>'
        + code('<header>Science Club</header>\n<nav>Home | Events</nav>\n<main>Robot day ...</main>\n<footer>© 2026</footer>')
        + '</div></div>'))
    # slides 16-18: which element, responsive design, mobile first
    p.append(page(
        '<table><tr><th style="width:24%">Element</th><th>Used for</th></tr>'
        '<tr><td class="k">&lt;header&gt;</td><td>the top of the page</td></tr>'
        '<tr><td class="k">&lt;nav&gt;</td><td>navigating between the parts of the site</td></tr>'
        '<tr><td class="k">&lt;main&gt;</td><td>the main content</td></tr>'
        '<tr><td class="k">&lt;footer&gt;</td><td>the bottom of the page</td></tr></table>'
        '<p>&lt;E-mail&gt; is <b>not</b> an element &mdash; the assessment book asks for the odd one out.</p>'
        '<h2>Part 3 &middot; Responsive design</h2>'
        + term('Responsive design', 'A design concept in which the layout is automatically adjusted to different screen sizes '
               'such as PCs, smartphones and tablets. One page, easy to view on any device.',
               'التصميم المتجاوب: التخطيط بيتظبط تلقائيًا حسب حجم الشاشة.')
        + '<table><tr><th style="width:20%">Screen</th><th>The same three boxes</th></tr>'
        '<tr><td class="k">Phone</td><td>one column: the boxes stack</td></tr>'
        '<tr><td class="k">Tablet</td><td>two side by side, the third below</td></tr>'
        '<tr><td class="k">PC</td><td>all three in one row</td></tr></table>'
        '<p><b>Mobile-first:</b> many people use the web on their phones, so developers think about small screens from the '
        'very start of the design.</p>'))
    # slides 19-20: frameworks, exam warning
    p.append(page(
        '<h2>Frameworks</h2>'
        + term('Framework', 'A structure that provides common functions and components in advance, to make web application '
               'development more efficient &mdash; you do not write everything from scratch.',
               'إطار العمل: وظايف ومكونات جاهزة عشان التطوير يبقى أكفأ.')
        + '<table><tr><th style="width:16%">Name</th><th>What to know</th></tr>'
        '<tr><td class="k">React</td><td>From Meta. Updates only part of the screen; a JavaScript library for interfaces built from reusable components.</td></tr>'
        '<tr><td class="k">Vue</td><td>A simple structure; build step by step from small features.</td></tr>'
        '<tr><td class="k">Next.js</td><td>Built on React; adds routing and faster ways to show pages.</td></tr></table>'
        '<table><tr><th>Looks right, but is false</th><th style="width:36%">Why</th></tr>'
        '<tr><td>Semantic HTML necessarily makes a page display faster.</td><td>Its benefits are accessibility and SEO.</td></tr>'
        '<tr><td>A framework is a language for defining the structure of a page.</td><td>That is HTML.</td></tr>'
        '<tr><td>Responsive design means the page works only on computers.</td><td>It adapts to every screen.</td></tr></table>'))
    # slides 20-25: exam warning, exam-style, engineer, new context, takeaway, unit 3
    p.append(page(
        '<div class="summary"><p><b>Exam-style question &middot; 6 marks.</b> Explain how HTML, CSS, and JavaScript each '
        'contribute to a library page that lists books, is styled, and filters the results as the user types. Refer to: '
        'structure, appearance, behavior.</p></div>'
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A student club wants a page that lists its events, uses the club&#8217;s colours, and has '
        'a button showing how many have signed up. Which technology does each? One change for phones, one semantic choice '
        'for a screen reader. Separate the three or not &mdash; two reasons.</p>'
        '<p class="ar">تلميح: HTML بيحمل المحتوى، CSS بينسّقه، JavaScript بيخليه يتفاعل ويتحدّث.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A news site must look good on phones and be found easily by search engines. One '
        'responsive-design choice and one semantic-HTML choice, and what each improves.</p></div>'
        '<h2>Key takeaway &middot; lesson 3-3</h2><div class="summary">'
        '<p>HTML structures, CSS styles, JavaScript behaves &mdash; and semantic HTML, responsive design and frameworks make a '
        'modern frontend meaningful, adaptable and efficient.</p></div>'
        '<table><tr><th style="width:12%">Unit 3</th><th>What to know</th></tr>'
        '<tr><td class="k">3-1</td><td>Frontend, backend, database &mdash; three tiers cooperating</td></tr>'
        '<tr><td class="k">3-2</td><td>Client and server, HTTP/HTTPS, GET/POST, status codes, API and JSON</td></tr>'
        '<tr><td class="k">3-3</td><td>HTML, CSS, JavaScript; semantic HTML, responsive design, frameworks</td></tr></table>'))
    # slides 26-32: Qureo 34, HTML (2)
    p.append(page(
        '<h2>Part 4 &middot; On the platform: HTML (2) (Qureo chapter 34)</h2>'
        '<p>An <b>element</b> is an opening tag, the content, and a closing tag.</p>'
        + code('<h1>Science Club</h1>\n<p>We build robots every Thursday.</p>\n<a href="events.html">See the events</a>')
        + '<table><tr><th style="width:24%">Tag</th><th>Makes</th></tr>'
        '<tr><td class="k">&lt;h1&gt;</td><td>a big heading</td></tr>'
        '<tr><td class="k">&lt;p&gt;</td><td>a paragraph</td></tr>'
        '<tr><td class="k">&lt;a href="..."&gt;</td><td>a link to another page</td></tr></table>'
        '<h2>Specifying ranges: div and span</h2>'
        + code('<div class="card">\n  <h3>Robot day</h3>\n  <p>Thursday, 2 pm</p>\n</div>\n\n<p>Bring your <span class="hot">own laptop</span>.</p>')
        + '<table><tr><th style="width:24%">Tag</th><th>Marks</th></tr>'
        '<tr><td class="k">&lt;div&gt;</td><td>a block: a box that holds several elements</td></tr>'
        '<tr><td class="k">&lt;span&gt;</td><td>a range inside a line of text</td></tr></table>'
        '<h2>Input fields and buttons</h2>'
        + code('<input type="text" placeholder="Your name">\n<button>Sign up</button>')
        + '<p><b>placeholder</b> shows a grey hint until the user types. &lt;input&gt; has no closing tag; &lt;button&gt; does.</p>'))
    # slides 33-39: Qureo 35, CSS (2)
    p.append(page(
        '<h2>Part 5 &middot; On the platform: CSS (2) (Qureo chapter 35)</h2>'
        + code('button {\n  color: white;\n  background-color: green;\n}')
        + '<table><tr><th style="width:20%">Part</th><th style="width:30%">In the example</th><th>It says</th></tr>'
        '<tr><td class="k">selector</td><td>button</td><td><b>which</b> part to change</td></tr>'
        '<tr><td class="k">property</td><td>background-color</td><td><b>what</b> to change</td></tr>'
        '<tr><td class="k">value</td><td>green</td><td><b>how</b> to change it</td></tr></table>'
        '<p>A class selector starts with a dot: <b>.big { ... }</b> styles every element with class="big".</p>'
        '<h2>Decorating a button, adding borders</h2>'
        + code('button {\n  background-color: #2D7A4B;\n  color: white;\n  font-size: 20px;\n  padding: 12px 28px;\n  border-radius: 30px;\n  border: 3px solid black;\n}')
        + '<table><tr><th style="width:28%">Property</th><th>Changes</th></tr>'
        '<tr><td class="k">background-color</td><td>the colour behind the text</td></tr>'
        '<tr><td class="k">color</td><td>the colour of the text</td></tr>'
        '<tr><td class="k">font-size</td><td>the size of the text</td></tr>'
        '<tr><td class="k">padding</td><td>the space inside, around the text</td></tr>'
        '<tr><td class="k">border-radius</td><td>how round the corners are</td></tr>'
        '<tr><td class="k">border</td><td>the line around it: width, style (solid, dashed, dotted), colour</td></tr></table>'))
    # slides 40-43: Qureo 36, review, what we learned
    p.append(page(
        '<h2>Part 6 &middot; Review of chapters 34-35 (Qureo chapter 36)</h2>'
        '<p>A sign-up card that puts them together:</p>'
        + code('<div class="card">\n  <h2>Science Club</h2>\n  <p>Join us on <span class="hot">Thursday</span>!</p>\n'
               '  <input type="text" placeholder="Your name">\n  <button>Sign up</button>\n</div>\n\n<style>\n'
               '  .card {\n    border: 3px solid #7A3B69;\n    border-radius: 12px;\n    padding: 16px;\n  }\n</style>')
        + '<table><tr><th>Quick-fire</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>The tag for a text box</td><td>&lt;input&gt;</td></tr>'
        '<tr><td>The tag that marks a range inside a sentence</td><td>&lt;span&gt;</td></tr>'
        '<tr><td>In p { color: blue; }, the property</td><td>color</td></tr>'
        '<tr><td>The property that adds space inside a button</td><td>padding</td></tr>'
        '<tr><td>Making the button count sign-ups</td><td>JavaScript</td></tr></table>'
        '<h2>What we learned</h2><div class="summary">'
        '<p>HTML structures, CSS styles, JavaScript behaves. Semantic HTML helps accessibility and SEO. Responsive design fits '
        'every screen; frameworks give ready-made parts.</p>'
        '<p>div and span mark ranges; input and button let the user type and press. CSS: selector { property: value; }.</p></div>'))
    p.append(page('<h2>Class work</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
                  + exercise(1, 1) + exercise(2, 2)))
    p.append(page('<h2>Class work</h2><p class="ar">كمّل مع زميلك.</p>'
                  + exercise(3, 3) + exercise(4, 4)))
    p.append(page('<h2>Class work &middot; on the platform</h2><p class="ar">اقرا الكود وجاوب.</p>'
                  + exercise(5, 5)))
    p.append(page('<h2>Class work &middot; on the platform</h2><p class="ar">كمّل.</p>'
                  + exercise(6, 6)))
    return head + ''.join(p) + lastpage('booklet') + tail