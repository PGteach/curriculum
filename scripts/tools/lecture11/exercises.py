# -*- coding: utf-8 -*-
import io, json
E = []
def X(**k): E.append(k)
def m(q, en, ar): return {"q": q, "a": en, "ar": ar}

T3 = "A: HTML, B: CSS, C: JavaScript"
CARD = ('<div class="card">\n  <h2>Science Club</h2>\n  <p>Join us on <span class="hot">Thursday</span>!</p>\n'
        '  <input type="text" placeholder="Your name">\n  <button>Sign up</button>\n</div>')
BTN = ("button {\n  background-color: green;\n  color: white;\n  padding: 12px 28px;\n"
       "  border-radius: 30px;\n  border: 3px solid black;\n}")
CARDCSS = (CARD + "\n\n<style>\n  .card {\n    border: 3px solid purple;\n    border-radius: 12px;\n    padding: 16px;\n  }\n"
           "  .hot {\n    color: red;\n  }\n</style>")

# ---------------- class work ----------------
X(n=1, type="truefalse", prompt="Write ✓ if the statement is true, ✗ if it is false.",
  promptAr="حط ✓ لو الجملة صح، و ✗ لو غلط.",
  statements=["HTML is a technology that defines the structure (skeleton) of a web page.",
              "CSS is a technology that adds behavior to a web page.",
              "Responsive design is a concept in which the layout is automatically adjusted according to different screen sizes.",
              "Using a framework eliminates the need to write all code from scratch and allows efficient development."],
  src="p.71 — Worked Example (1) A-D")
X(n=2, type="match", prompt="Match each role with the most appropriate technology.",
  promptAr="اربط كل دور بالتقنية الأنسب.",
  left=["Defines the structure of a web page", "Specifies the appearance of a web page",
        "Adds behavior and interactivity to a web page"],
  right=["HTML", "CSS", "JavaScript"],
  src="p.71 — Worked Example (2)")
X(n=3, type="category", prompt="Write the technology used for each task — " + T3 + ".",
  promptAr="اكتب التقنية المستخدمة في كل مهمة.",
  items=["Describing the structure of headings and paragraphs", "Changing the color and size of text",
         "Updating part of the screen when a button is pressed", "Placing images and links",
         "Setting the background color of the entire page", "Validating the contents entered into a form"],
  src="p.74 — Exercise 3(1)")
X(n=4, type="match", prompt="Match each part of a page with its semantic HTML element.",
  promptAr="اربط كل جزء من الصفحة بعنصر HTML الدلالي بتاعه.",
  left=["The top of the page", "Navigation between the parts of the site", "The main content", "The bottom of the page"],
  right=["<footer>", "<main>", "<header>", "<nav>"],
  src="p.70 — Point 2(1); Ministry assessments, periods 1-2 and forms A-C")
X(n=5, type="short", prompt="Read the HTML, then answer.", promptAr="اقرا الـ HTML وبعدين جاوب.",
  code=CARD,
  questions=[{"q": "Which tag groups the whole card into one box?", "lines": 1},
             {"q": "Which tag marks the word Thursday so it can be styled?", "lines": 1},
             {"q": "What does the user see in the text box before typing?", "lines": 1},
             {"q": "Which tag in the code has no closing tag?", "lines": 1}],
  src="Qureo chapter 34 — Specifying Ranges; Input fields & button display")
X(n=6, type="short", prompt="Read the CSS, then answer.", promptAr="اقرا الـ CSS وبعدين جاوب.",
  code=BTN,
  questions=[{"q": "Which line colours the text of the button?", "lines": 1},
             {"q": "Which property adds space inside the button, and which rounds its corners?", "lines": 1},
             {"q": "In border: 3px solid black; name the width, the style and the colour.", "lines": 1},
             {"q": "Name the selector, one property and its value.", "lines": 1}],
  src="Qureo chapter 35 — CSS Review; Button Decoration; Adding Borders")

# ---------------- homework ----------------
X(n=7, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "What is the four-letter abbreviation for the technology that defines the structure (skeleton) of a web page?", "lines": 1},
             {"q": "What is the three-letter abbreviation for the technology that specifies the appearance of a web page (colors, layout, size, etc.)?", "lines": 1},
             {"q": "What is the term for the technology that adds behavior and interactivity to a web page?", "lines": 1},
             {"q": "What is the term for the design concept in which the layout is automatically adjusted according to different screen sizes?", "lines": 1}],
  src="p.72 — Try 1")
X(n=8, type="fill", prompt="Fill in ( a ) to ( d ).", promptAr="املا الفراغات من ( أ ) لـ ( د ).",
  passage="Web pages are mainly composed of three technologies: ( a ), which defines the structure of the page; ( b ), which specifies the appearance; and ( c ), which adds behavior and interactivity. The concept of adjusting the layout according to different screen sizes such as PCs, smartphones, and tablets is called ( d ).",
  src="p.74 — Exercise 2")
X(n=9, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "Choose the one that is NOT an appropriate benefit of using semantic HTML. A: Screen reader software can correctly understand the structure of the page. B: Search engines can more easily understand the content of a web page. C: The display speed of a web page necessarily becomes faster. D: Information becomes easier to convey to users with visual impairments.", "lines": 1},
             {"q": "Choose the one that most appropriately describes a framework. A: A language for defining the structure of a web page B: A structure for making web application development more efficient C: A technology for encrypting data and sending it safely D: A design concept for supporting different screen sizes", "lines": 1},
             {"q": "Choose the most appropriate reason responsive design is needed. A: To improve the display speed of websites B: Because websites are accessed from various devices such as PCs, smartphones, and tablets C: To raise rankings in search engines D: To add behavior to web pages", "lines": 1}],
  src="p.72 Try 2(1)-(2); p.74 Exercise 3(2)")
X(n=10, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "HTML is responsible for: A: The visual appearance B: The basic structure of the page C: The interactive behavior D: Improving performance", "lines": 1},
             {"q": "JavaScript adds: A: Headings and paragraphs B: Colors and fonts C: Interactive behavior D: Semantic elements", "lines": 1},
             {"q": "CSS is used for: A: Building the structure B: Adding interaction C: Formatting the appearance D: Managing databases", "lines": 1},
             {"q": "The Next.js framework is built on: A: Vue B: React C: CSS D: HTML", "lines": 1}],
  src="Ministry assessments, periods 1-2 — MCQ")
X(n=11, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "All of these are semantic HTML elements EXCEPT: A: <header> B: <E-mail> C: <main> D: <footer>", "lines": 1},
             {"q": "The <footer> element is used for: A: Showing the main content B: Showing the footer at the bottom of the page C: Showing the main title D: Navigating between the parts of the site", "lines": 1},
             {"q": "Which JavaScript framework lets you build applications step by step, from small features? A: React B: Vue C: Next.js D: HTML", "lines": 1}],
  src="Ministry assessments, period 1 and form C — MCQ")
X(n=12, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Explain the role of each of HTML, CSS and JavaScript in building a web page.", "lines": 4},
             {"q": "Why is semantic HTML important when building web pages?", "lines": 3}],
  src="Ministry assessments, period 1 — performance tasks")
X(n=13, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Give an example of a semantic HTML element and write its function.", "lines": 2},
             {"q": "How does responsive design help improve the user experience?", "lines": 3},
             {"q": "What is the benefit of using a framework in frontend development?", "lines": 2}],
  src="Ministry assessments, period 2 — performance tasks; period 1 — home tasks")
X(n=14, type="extended", prompt="Explain how HTML, CSS, and JavaScript each contribute to a library page that lists books, is styled, and filters the results as the user types. Refer to: structure, appearance, behavior.",
  promptAr="اشرح إزاي HTML و CSS و JavaScript بيساهموا في صفحة مكتبة بتعرض قائمة كتب، ومتنسّقة، وبتصفّي النتايج وانت بتكتب. راجع: البنية، المظهر، السلوك.",
  marks=6, lines=8, src="p.71 — Exam-style question [6]")
X(n=15, type="extended", prompt="How does JavaScript add interactivity to a web page? Give a practical example.",
  promptAr="إزاي JavaScript بيضيف التفاعلية لصفحة الويب؟ اذكر مثال عملي.",
  marks=4, lines=6, src="Ministry assessments, form C — essay 1")
X(n=16, type="extended", prompt="Explain the concept of \"mobile-first\" in responsive design, and why it is used.",
  promptAr="اشرح مفهوم «الأولوية للجوال» في التصميم المتجاوب، وليه بيستخدم.",
  marks=4, lines=5, src="Ministry assessments, form B — essay 3; period 2 — home tasks")
X(n=17, type="extended", prompt="Name two common libraries or frameworks for web development, and explain the characteristics of each.",
  promptAr="اذكر اتنين من المكتبات وأطر العمل الشائعة لتطوير الويب، ووضّح خصائص كل واحد.",
  marks=4, lines=5, src="Ministry assessments, form B — essay 4; p.70 Point 4(3)")
X(n=18, type="extended", prompt="Think as an engineer. A student club wants a simple web page that lists its events, is styled in the club's colors, and has a button showing how many people have signed up. Say which technology does each of the three features, and why. Name one responsive-design change for phones and one semantic-HTML choice for a screen reader. Recommend whether the club should separate HTML, CSS and JavaScript, with two reasons.",
  promptAr="فكّر كمهندس: نادي طلابي عايز صفحة بسيطة. حدد التقنية لكل ميزة وليه، واقترح تغيير للموبايل واختيار دلالي لقارئ الشاشة، وقرّر نفصل التلاتة ولا لأ بسببين.",
  marks=4, lines=8, src="p.72-73 — Think as an Engineer")
X(n=19, type="extended", prompt="A news site must look good on phones and be found easily by search engines. Name one responsive-design choice and one semantic-HTML choice it should make, and say what each one improves.",
  promptAr="موقع أخبار لازم يبان كويس على الموبايل ويتلاقي بسهولة في محركات البحث. اذكر اختيار من التصميم المتجاوب واختيار من HTML الدلالي، وكل واحد بيحسّن إيه.",
  marks=4, lines=5, src="p.73 — In a New Context")
X(n=20, type="short", prompt="Write the HTML.", promptAr="اكتب الـ HTML.",
  questions=[{"q": "Write HTML for: a <div> that holds a heading \"Robot day\" and a paragraph \"Thursday, 2 pm\", where the word Thursday is marked with a <span>.", "lines": 5},
             {"q": "Under it, write a text box with the hint \"Your name\" and a button that says \"Join\".", "lines": 3}],
  src="Qureo chapter 34 — Specifying Ranges; Input fields & button display")
X(n=21, type="short", prompt="Write the CSS.", promptAr="اكتب الـ CSS.",
  questions=[{"q": "Write CSS for every button: a blue background, white text, 10px of space inside, round corners (20px), and a 2px solid black border.", "lines": 8}],
  src="Qureo chapter 35 — Button Decoration; Adding Borders")
X(n=22, type="short", prompt="Read the code, then describe the result.", promptAr="اقرا الكود وبعدين اوصف النتيجة.",
  code=CARDCSS,
  questions=[{"q": "What does the card's border look like?", "lines": 1},
             {"q": "Which word is red, and why only that word?", "lines": 2},
             {"q": "Does pressing the button do anything? Why or why not?", "lines": 2}],
  src="Qureo chapter 36 — review of chapters 34-35")
X(n=23, type="short", prompt="Reflect and challenge.", promptAr="فكّر وتحدّى نفسك.",
  questions=[{"q": "Reflect: of structure, style, and behavior, which do you notice most when a web page is badly made, and why?", "lines": 3},
             {"q": "Challenge: name one website you use and describe one thing HTML, CSS, and JavaScript each do on it.", "lines": 4}],
  src="p.73 — Reflect & Challenge")
X(n=24, type="short", prompt="Challenge: build a small page.", promptAr="تحدي: ابني صفحة صغيرة.",
  questions=[{"q": "Write a page for your class with a <header>, a <main> holding one card (a <div> with a heading, an input and a button), and a <footer>. Then write CSS that gives the card a border and the button a colour of your choice.", "lines": 12}],
  src="Qureo chapter 36; p.70 Point 2 — semantic HTML")

A = {
 "1": ["✓ — HTML defines the structure", "✗ — CSS is appearance; behavior is JavaScript",
       "✓ — correct definition of responsive design", "✓ — the benefit of frameworks"],
 "2": ["a — HTML", "b — CSS", "c — JavaScript"],
 "3": ["a A — HTML", "b B — CSS", "c C — JavaScript", "d A — HTML", "e B — CSS", "f C — JavaScript"],
 "4": ["Top of the page — <header>", "Navigation — <nav>", "Main content — <main>", "Bottom of the page — <footer>"],
 "5": ["1. <div>", "2. <span>", "3. The grey hint \"Your name\" (the placeholder)", "4. <input>"],
 "6": ["1. color: white;", "2. padding adds space inside; border-radius rounds the corners",
       "3. width 3px, style solid, colour black", "4. Selector: button; e.g. property background-color, value green"],
 "7": ["1. HTML", "2. CSS", "3. JavaScript", "4. Responsive design"],
 "8": {"a": "HTML", "b": "CSS", "c": "JavaScript", "d": "responsive design"},
 "9": ["(1) C — semantic HTML does not necessarily make a page faster", "(2) B", "(3) B"],
 "10": ["(1) B", "(2) C", "(3) C", "(4) B — React"],
 "11": ["(1) B — <E-mail> is not an element", "(2) B", "(3) B — Vue"],
 "12": ["1. HTML defines the structure (headings, paragraphs, images, links); CSS specifies the appearance (colours, layout, size, fonts); JavaScript adds behavior and interactivity (responding to buttons, updating part of the screen). A page uses them in combination.",
        "2. Its tags name each part of the page (<header>, <nav>, <main>, <footer>), so screen readers understand the structure (accessibility) and search engines understand the content more easily (SEO)."],
 "13": ["1. e.g. <nav>: holds the navigation links between the parts of the site (or <header> top, <main> main content, <footer> bottom).",
        "2. The layout adjusts to the screen, so the page is easy to read and use on a phone, a tablet or a PC, without zooming or scrolling sideways.",
        "3. It provides common functions and components in advance, so developers do not write everything from scratch and build more efficiently."],
 "14": {"marks": 6,
        "model": "HTML gives the page its structure: the page heading, the search box and the list of books, each book with its title and author. CSS gives it its appearance: the colours, the fonts and the layout of the list, so it is easy to read. JavaScript gives it its behavior: as the user types in the search box, it checks each book and hides the ones that do not match, updating the list without reloading the page. Each technology has its own role, and together they make the page.",
        "points": ["HTML: the structure (1)", "e.g. the list of books and the search box (1)", "CSS: the appearance (1)",
                   "e.g. colours, fonts, layout of the list (1)", "JavaScript: the behavior (1)", "e.g. filtering the list as the user types (1)"]},
 "15": {"marks": 4,
        "model": "JavaScript makes the page react to what the user does. It can respond when a button is pressed, check what is typed into a form, or update part of the screen without loading a new page. Example: on a sign-up page, pressing the button adds one to a counter shown on the page; or a search box hides the results that do not match as you type.",
        "points": ["Responds to the user's actions, e.g. clicks and typing (1)", "Can update part of the screen without reloading (1)",
                   "Can check form input (1)", "A practical example (1)"]},
 "16": {"marks": 4,
        "model": "Mobile-first means designing for small screens such as phones from the very start, then adapting the layout for bigger screens. It is used because many people use the web on their phones, so the page must work well there first: easy to read, with no sideways scrolling, and with the most important content first.",
        "points": ["Design for small screens (phones) first (1)", "Then adapt to bigger screens (1)",
                   "Because many people use the web on phones (1)", "So the page is easy to read and use on them (1)"]},
 "17": {"marks": 4,
        "points": ["React: from Meta; updates only part of the screen; builds interfaces from reusable components (2)",
                   "Vue: a simple structure; build step by step from small features — or Next.js: built on React, adds routing and faster page display (2)"]},
 "18": {"marks": 4, "open": True,
        "points": ["Events list: HTML; colours and layout: CSS; live counter: JavaScript — with reasons (1)",
                   "One responsive change, e.g. one column on a phone (1)",
                   "One semantic choice, e.g. <nav> for the menu, <main> for the events (1)",
                   "Recommends separating them, with two reasons, e.g. easier to change and to find faults (1)"]},
 "19": {"marks": 4,
        "points": ["A responsive choice, e.g. the layout becomes one column on phones (1)", "It improves reading on phones (1)",
                   "A semantic choice, e.g. <header>, <main>, <article> (1)", "It helps search engines understand the page (and screen readers) (1)"]},
 "20": ["1. <div>\n  <h2>Robot day</h2>\n  <p><span>Thursday</span>, 2 pm</p>\n</div>",
        "2. <input type=\"text\" placeholder=\"Your name\">\n<button>Join</button>"],
 "21": ["button {\n  background-color: blue;\n  color: white;\n  padding: 10px;\n  border-radius: 20px;\n  border: 2px solid black;\n}"],
 "22": ["1. A solid purple line, 3px wide, with round corners (12px), and space inside (16px)",
        "2. Thursday — it is the only text inside <span class=\"hot\">, and .hot sets color: red",
        "3. No — there is no JavaScript, so the button has no behavior"],
 "23": {"marks": 4, "open": True,
        "points": ["Reflect: names structure, style or behavior, with a reason (2)",
                   "Challenge: one website, one thing each of HTML, CSS and JavaScript does on it (2)"]},
 "24": {"marks": 4, "open": True,
        "points": ["<header>, <main> and <footer> used correctly (1)", "A <div> card with a heading, an <input> and a <button> (1)",
                   "CSS: a border on the card (1)", "CSS: a colour on the button (1)"]},
}

MODEL = {
 "1": [m("A. HTML", "✓ True — HTML defines the structure.", "صح."),
       m("B. CSS", "✗ False — CSS specifies the appearance; adding behavior is JavaScript.", "غلط: السلوك ده JavaScript."),
       m("C. Responsive design", "✓ True.", "صح."), m("D. Frameworks", "✓ True.", "صح.")],
 "2": [m("a. Structure", "HTML.", "البنية."), m("b. Appearance", "CSS.", "المظهر."), m("c. Behavior", "JavaScript.", "السلوك.")],
 "3": [m("a. Headings and paragraphs", "A — HTML.", ""), m("b. Colour and size of text", "B — CSS.", ""),
       m("c. Updating part of the screen", "C — JavaScript.", ""), m("d. Images and links", "A — HTML.", ""),
       m("e. Background colour", "B — CSS.", ""), m("f. Validating a form", "C — JavaScript.", "")],
 "4": [m("Top of the page", "<header>", ""), m("Navigation", "<nav>", ""), m("Main content", "<main>", ""),
       m("Bottom of the page", "<footer>", "")],
 "5": [m("1.", "<div> — it groups the card into one box.", "‏div بيعمل صندوق."), m("2.", "<span> — it marks a range inside the sentence.", "‏span بيحدد كلام جوّه سطر."),
       m("3.", "The grey hint \"Your name\".", "التلميح الرمادي."), m("4.", "<input> — it stands alone.", "‏input ملوش وسم قفل.")],
 "6": [m("1.", "color: white;", "‏color للكلام."), m("2.", "padding adds the space inside; border-radius rounds the corners.", ""),
       m("3.", "Width 3px, style solid, colour black.", ""), m("4.", "Selector button; property background-color, value green (or any other pair).", "")],
 "7": [m("1.", "HTML.", ""), m("2.", "CSS.", ""), m("3.", "JavaScript.", ""), m("4.", "Responsive design.", "التصميم المتجاوب.")],
 "8": [m("( a )", "HTML", ""), m("( b )", "CSS", ""), m("( c )", "JavaScript", ""), m("( d )", "responsive design", "التصميم المتجاوب.")],
 "9": [m("(1)", "C — semantic HTML does not necessarily make a page faster.", "فوايده الوصول ومحركات البحث، مش السرعة."),
       m("(2)", "B — a structure for making development more efficient.", ""), m("(3)", "B — many different devices.", "")],
 "10": [m("(1)", "B — the basic structure.", ""), m("(2)", "C — interactive behavior.", ""),
        m("(3)", "C — formatting the appearance.", ""), m("(4)", "B — React.", "")],
 "11": [m("(1)", "B — <E-mail> is not an HTML element.", ""), m("(2)", "B — the footer at the bottom.", ""),
        m("(3)", "B — Vue.", "")],
 "12": [m("1. The three roles", A["12"][0][3:], "‏HTML بيبني، CSS بينسّق، JavaScript بيتفاعل."),
        m("2. Why semantic HTML", A["12"][1][3:], "بيساعد قارئ الشاشة ومحركات البحث.")],
 "13": [m("1. A semantic element", A["13"][0][3:], ""), m("2. Responsive design", A["13"][1][3:], "الصفحة بتتظبط على أي شاشة."),
        m("3. Frameworks", A["13"][2][3:], "أجزاء جاهزة.")],
 "14": [m(None, A["14"]["model"], "‏HTML القائمة، و CSS الشكل، و JavaScript التصفية وانت بتكتب.")],
 "15": [m(None, A["15"]["model"], "‏JavaScript بيخلي الصفحة تستجيب.")],
 "16": [m(None, A["16"]["model"], "نصمّم للموبايل الأول.")],
 "17": [m(None, "React, from Meta, updates only part of the screen and builds interfaces from reusable components; it suits large web apps. Vue has a simple structure and lets you build an app step by step, starting from small features. (Or Next.js: built on React, it adds routing and ways to show pages faster.)",
          "‏React و Vue (أو Next.js) بخصائص كل واحد.")],
 "18": [m(None, "One possible answer. The list of events is HTML, because it is content and structure. The club's colours and layout are CSS, because that is appearance. The live sign-up counter is JavaScript, because it must react to the button and update. For phones: show the events in one column. For a screen reader: put the menu in <nav> and the events in <main>. Yes, separate them: each file has one job, so it is easier to change the colours without touching the content, and easier to find a fault.",
          "مثال لإجابة: HTML للقائمة، CSS للألوان، JavaScript للعدّاد.")],
 "19": [m(None, "Responsive design: show the articles in one column on a phone, so they are easy to read without zooming. Semantic HTML: use <header>, <nav> and <main> (and <article> for each story), so search engines — and screen readers — understand which part is the news itself.",
          "عمود واحد على الموبايل، وعناصر دلالية لمحركات البحث.")],
 "20": [m("1.", "<div>\n  <h2>Robot day</h2>\n  <p><span>Thursday</span>, 2 pm</p>\n</div>", "‏div للصندوق و span للكلمة."),
        m("2.", "<input type=\"text\" placeholder=\"Your name\">\n<button>Join</button>", "")],
 "21": [m(None, A["21"][0], "كل سطر خاصية وقيمة جوّه أقواس button.")],
 "22": [m("1.", A["22"][0][3:], ""), m("2.", A["22"][1][3:], "‏.hot بتلوّن اللي جوّه span بس."),
        m("3.", A["22"][2][3:], "مفيش JavaScript، فمفيش سلوك.")],
 "23": [m("Reflect", "One possible answer. Style: a badly styled page is hard to read straight away, even if its structure and behavior are fine.", "أي اختيار بسبب مقنع."),
        m("Challenge", "One possible answer. YouTube: HTML gives the video list and the search box; CSS the dark layout and fonts; JavaScript plays the video and suggests searches as I type.", "أي موقع.")],
 "24": [m(None, "One possible answer.\n<header><h1>Class 2B</h1></header>\n<main>\n  <div class=\"card\">\n    <h2>Trip to the museum</h2>\n    <input type=\"text\" placeholder=\"Your name\">\n    <button>Sign up</button>\n  </div>\n</main>\n<footer>School 2026</footer>\n\n<style>\n  .card { border: 2px solid teal; padding: 12px; }\n  button { background-color: teal; color: white; }\n</style>",
          "أي صفحة فيها العناصر المطلوبة.")],
}
DATA = {"SHEET": {"lecture": 11, "title": "What is a web page made of?", "parts": [{"exercises": E}]}, "ANSWERS": A, "MODEL": MODEL}
assert [x["n"] for x in E] == list(range(1, 25)) and set(A) == set(MODEL) == {str(x["n"]) for x in E}
io.open("lecture11/_teacher/exercises.json", "w", encoding="utf-8", newline="\n").write(json.dumps(DATA, ensure_ascii=False, indent=1) + "\n")
print("exercises:", len(E))
