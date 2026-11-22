# -*- coding: utf-8 -*-
"""Write Lecture 11's quiz questions into lecture11/quiz/index.html.

    python scripts/build_lecture11_quiz.py && python scripts/protect_answers.py 11

The second command is required: this writes plaintext a: indices, and
protect_answers turns them into fingerprints before publishing.

Lecture 11's paper: lesson 3-3, Fundamentals of Frontend Technology (English
textbook pp. 68-74; the Arabic textbook's lesson 3-3), with the ministry's
assessment book for the lesson, and Qureo chapters 34 HTML (2), 35 CSS (2)
and 36 (the comprehension check on 34-35). Curriculum only. A longer paper
than usual, for a longer lecture.

Every question has four options, every wrong option taken from the same
lesson. d: 1 easy, 2 medium, 3 hard -- the page runs easy to hard. A code
question carries its code in `c`, shown as a code box under the question
(added to the page by add_code_box below, as on lectures 8 to 10).
"""
import io, re

SECTIONS = [
    "HTML, CSS and JavaScript",
    "Semantic HTML",
    "Responsive design and frameworks",
    "HTML (2): ranges, inputs and buttons",
    "CSS (2): decorating a button, borders",
    "Review: HTML and CSS together",
]

T3 = ["HTML", "CSS", "JavaScript"]

# (section, difficulty, question, code, options, answer index, why, src, glosses)
Q = [
    # ================= band 1 =================
    (0, 1, "Which technology defines the structure (skeleton) of a web page?", "",
     ["HTML", "CSS", "JavaScript", "JSON"], 0,
     "HTML is the structure: headings, paragraphs, images, links.",
     "p.69 — Point 1(1); p.72 Try 1 (1)", [["structure", "البنية"]]),
    (0, 1, "Which technology specifies the appearance of a web page: colours, layout, size, fonts?", "",
     ["CSS", "HTML", "JavaScript", "SQL"], 0,
     "CSS is the appearance.",
     "p.72 — Try 1 (2); Ministry assessments, form A — MCQ 1", [["appearance", "المظهر"]]),
    (0, 1, "Which technology adds behavior and interactivity to a web page?", "",
     ["JavaScript", "HTML", "CSS", "SQL"], 0,
     "JavaScript makes the page respond.",
     "p.72 — Try 1 (3); Ministry assessments, form C — MCQ 1", []),
    (1, 1, "In semantic HTML, the <header> element is used for:", "",
     ["The top of the page", "The main content", "Navigation", "The bottom of the page"], 0,
     "<header> is the top; <main> the body; <nav> navigation; <footer> the bottom.",
     "p.70 — Point 2(1); Ministry assessments, period 2 — MCQ 1", []),
    (2, 1, "What is responsive design?", "",
     ["The layout adjusts automatically to different screen sizes", "Using JavaScript only",
      "Improving databases", "Hiding the less important content"], 0,
     "One page that fits PCs, phones and tablets.",
     "p.70 — Point 3(1); Ministry assessments, period 2 — MCQ 2", []),
    (3, 1, "Which tag makes a box where the user can type?", "",
     ["<input>", "<button>", "<span>", "<h1>"], 0,
     "<input> is a text box; <button> is something to press.",
     "Qureo chapter 34 — Input fields & button display", []),
    (4, 1, "In p { color: blue; }, which part is the property?", "",
     ["color", "p", "blue", "the curly brackets { }"], 0,
     "p is the selector (which part), color the property (what), blue the value (how).",
     "Qureo chapter 35 — CSS Review", []),
    (4, 1, "Which property changes the colour of a button's text?", "",
     ["color", "background-color", "padding", "border"], 0,
     "color is the text; background-color fills behind it.",
     "Qureo chapter 35 — Button Decoration (1)", []),

    # ================= band 2 =================
    (0, 2, "In the book's analogy, HTML is like:", "",
     ["The frame of a building", "The interior and exterior of a building",
      "The electrical and plumbing systems", "Ready-made parts from a framework"], 0,
     "HTML is the frame; CSS the interior and exterior; JavaScript the electricity and plumbing.",
     "p.69 — Point 1(1), the analogy", []),
    (0, 2, "Updating part of the screen when a button is pressed uses which technology?", "",
     ["JavaScript", "HTML", "CSS", "Semantic HTML"], 0,
     "Reacting and updating is behavior: JavaScript.",
     "p.74 — Exercise 3(1) c", []),
    (0, 2, "Setting the background colour of the whole page uses which technology?", "",
     ["CSS", "HTML", "JavaScript", "A framework"], 0,
     "A colour is appearance: CSS.",
     "p.74 — Exercise 3(1) e", []),
    (1, 2, "Which is NOT an appropriate benefit of using semantic HTML?", "",
     ["The display speed of the page necessarily becomes faster",
      "Screen-reader software can understand the structure of the page",
      "Search engines can understand the content more easily",
      "Information becomes easier to convey to users with visual impairments"], 0,
     "Its benefits are accessibility and SEO, not speed.",
     "p.72 — Try 2(1)", []),
    (1, 2, "Which HTML element marks the main content of a page?", "",
     ["<main>", "<header>", "<footer>", "<nav>"], 0,
     "<main> holds the body of the page.",
     "Ministry assessments, form A — MCQ 2", []),
    (1, 2, "The <nav> element is used for:", "",
     ["Navigating between the parts of the site", "Showing the main content",
      "Showing the main title", "Showing the footer"], 0,
     "nav = navigation.",
     "Ministry assessments, form B — MCQ 2", []),
    (2, 2, "Which most appropriately describes a framework?", "",
     ["A structure for making web application development more efficient",
      "A language for defining the structure of a web page",
      "A technology for encrypting data and sending it safely",
      "A design concept for supporting different screen sizes"], 0,
     "Ready-made functions and parts, so you do not start from scratch.",
     "p.72 — Try 2(2)", []),
    (2, 2, "Why is responsive design needed?", "",
     ["Websites are accessed from many devices: PCs, smartphones and tablets",
      "To improve the display speed of websites", "To raise rankings in search engines",
      "To add behavior to web pages"], 0,
     "Different screens, one page.",
     "p.74 — Exercise 3(2)", []),
    (2, 2, "In responsive design, \"mobile-first\" means:", "",
     ["Designing first for small screens such as phones", "Designing first for computers",
      "Using JavaScript to add interactivity", "Making the server faster"], 0,
     "Start from the phone, then the bigger screens.",
     "p.70 — Point 3(3); Ministry assessments, form C — MCQ 3", []),
    (2, 2, "Which of these is a JavaScript library for building user interfaces?", "",
     ["React", "HTML", "CSS", "SQL"], 0,
     "React builds interfaces from reusable components.",
     "Ministry assessments, form A — MCQ 4; Arabic book 3-3", []),
    (3, 2, "Which tag groups a heading and two paragraphs into one box?", "",
     ["<div>", "<span>", "<input>", "<a>"], 0,
     "<div> marks a block range: a box holding several elements.",
     "Qureo chapter 34 — Specifying Ranges", []),
    (3, 2, "Which tag marks a few words inside a sentence, so they can be styled?", "",
     ["<span>", "<div>", "<button>", "<h1>"], 0,
     "<span> marks a range inside a line of text.",
     "Qureo chapter 34 — Specifying Ranges", []),
    (4, 2, "Which property adds space inside a button, around its text?", "",
     ["padding", "border", "color", "font-size"], 0,
     "padding is the space inside.",
     "Qureo chapter 35 — Button Decoration (2)", []),
    (4, 2, "In border: 2px dashed red; what is dashed?", "",
     ["The style of the line", "The width of the line", "The colour of the line", "The shape of the corners"], 0,
     "2px is the width, dashed the style, red the colour.",
     "Qureo chapter 35 — Adding Borders", []),
    (5, 2, "What does this button look like?", "<button>Join</button>\n\n<style>\n  button {\n    background-color: green;\n    color: white;\n  }\n</style>",
     ["Green, with white text", "White, with green text", "A green border, white inside", "No change at all"], 0,
     "background-color fills the button; color is its text.",
     "Qureo chapter 36 — review of chapters 34-35", []),

    # ================= band 3 =================
    (0, 3, "Which statement about HTML, CSS and JavaScript is correct?", "",
     ["Each has its own role, and a page combines them as it needs",
      "CSS adds the behavior of a page",
      "JavaScript defines the structure of a page",
      "Every page must always use all three"], 0,
     "Independent roles, used in combination. The Arabic book adds that a page can even be HTML alone.",
     "p.69 — Point 1(2); Arabic book 3-3, Point 1(2)", []),
    (1, 3, "What does semantic HTML do for search engines?", "",
     ["It helps them understand the page, but does not guarantee a higher ranking",
      "It guarantees the first place in the results", "It makes the page load faster",
      "It replaces the need for CSS"], 0,
     "The Arabic book is careful: it may help, but it guarantees nothing.",
     "Arabic book 3-3, Point 2(2); Ministry assessments, form C — essay 2", []),
    (2, 3, "Which is built on React and provides routing and ways of showing pages?", "",
     ["Next.js", "Vue", "HTML", "CSS"], 0,
     "Next.js is a framework built on React.",
     "p.70 — Point 4(3); Ministry assessments, form B — MCQ 4", []),
    (3, 3, "With no CSS at all, how does the span change the look of this sentence?", "<p>Bring your <span>own laptop</span>.</p>",
     ["It does not change it: it only marks a range", "The two words become bold",
      "The two words move to a new line", "The two words get a box around them"], 0,
     "A span only marks the words. CSS is what then styles them.",
     "Qureo chapter 34 — Specifying Ranges", []),
    (3, 3, "What does the user see before typing anything?", '<input type="text" placeholder="Your name">',
     ["A box with the grey hint \"Your name\"", "The word placeholder", "A button that says Your name", "Nothing at all"], 0,
     "placeholder is a hint shown until the user types.",
     "Qureo chapter 34 — Input fields & button display", []),
    (4, 3, "Which button gets the bigger text?", '<button class="big">A</button>\n<button>B</button>\n\n<style>\n  .big {\n    font-size: 30px;\n  }\n</style>',
     ["Only A", "Only B", "Both A and B", "Neither"], 0,
     "The selector .big styles only elements with class=\"big\".",
     "Qureo chapter 35 — CSS Review (class)", []),
    (4, 3, "Which CSS gives a button round corners and a 2px green border?", "",
     ["border: 2px solid green; border-radius: 20px;", "border-radius: 2px green;",
      "border: 20px; color: green;", "padding: 2px; background-color: green;"], 0,
     "border sets the width, style and colour; border-radius rounds the corners.",
     "Qureo chapter 35 — Button Decoration (2); Adding Borders", []),
    (5, 3, "A sign-up button must count how many people pressed it. What does it need?", "",
     ["JavaScript", "Only HTML", "Only CSS", "Semantic HTML"], 0,
     "Counting is behavior. HTML makes the button and CSS styles it, but only JavaScript makes it count.",
     "Qureo chapter 36; p.72 Think as an Engineer", []),
]


def js_str(t):
    return '"' + t.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


CODE_CSS = ('  .qcode{background:#16233F;color:#E6EDF3;font-family:"JetBrains Mono",ui-monospace,monospace;'
            'font-size:15px;line-height:1.6;border-radius:10px;padding:12px 14px;margin:-6px 0 18px;'
            'white-space:pre;overflow-x:auto;text-align:left;direction:ltr;font-variant-ligatures:none}\n'
            '  .review-card .qcode{font-size:13px;margin:4px 0 8px}')


def add_code_box(page):
    """Show q.c, when a question has one, as a code box under the question
    and in the review of wrong answers. textContent, never innerHTML."""
    if 'id="qcode"' in page:
        return page
    for a, b in [
        ('<div class="q" id="question"></div>',
         '<div class="q" id="question"></div>\n    <pre class="qcode" id="qcode" hidden></pre>'),
        ('  $("question").textContent = q.q;\n',
         '  $("question").textContent = q.q;\n  $("qcode").textContent = q.c || "";\n  $("qcode").hidden = !q.c;\n'),
        ("      question: q.q,\n", '      question: q.q,\n      code: q.c || "",\n'),
        ('      card.appendChild(el("h4", "", item.question));\n',
         '      card.appendChild(el("h4", "", item.question));\n'
         '      if(item.code) card.appendChild(el("pre", "qcode", item.code));\n'),
        ("  .q{font-size:19px;font-weight:600;line-height:1.4;margin-bottom:18px}",
         "  .q{font-size:19px;font-weight:600;line-height:1.4;margin-bottom:18px}\n" + CODE_CSS),
    ]:
        assert page.count(a) == 1, a
        page = page.replace(a, b, 1)
    return page


if __name__ == "__main__":
    from collections import Counter
    for s, d, q, c, o, a, why, src, v in Q:
        assert 0 <= s < len(SECTIONS), q
        assert d in (1, 2, 3), q
        assert 0 <= a < len(o), q
        assert len(o) == 4, "four options: " + q
        assert len(o) == len(set(o)), "repeated option: " + q
        assert why.strip() and src.strip(), q
        hay = (q + " " + " ".join(o)).lower()
        for en, ar in v:
            assert en.lower() in hay, "gloss not on screen: %r in %r" % (en, q)
    assert len({x[2] for x in Q}) == len(Q), "duplicate question text (the page tells questions apart by it)"
    print("sections:", dict(sorted(Counter(x[0] for x in Q).items())))
    print("difficulty:", dict(sorted(Counter(x[1] for x in Q).items())))

    secs = "[\n" + ",\n".join("  " + js_str(x) for x in SECTIONS) + "\n];"
    rows = []
    for s, d, q, c, o, a, why, src, v in Q:
        gl = (",v:[%s]" % ",".join("[%s,%s]" % (js_str(en), js_str(ar)) for en, ar in v)) if v else ""
        code = (",c:%s" % js_str(c)) if c else ""
        rows.append("  {s:%d,d:%d,q:%s%s,o:[%s],a:%d,why:%s,src:%s%s}"
                    % (s, d, js_str(q), code, ",".join(js_str(x) for x in o), a,
                       js_str(why), js_str(src), gl))
    qs = "[\n" + ",\n".join(rows) + "\n];"

    p = "lecture11/quiz/index.html"
    page = io.open(p, encoding="utf-8").read()
    page = add_code_box(page)
    page = re.sub(r"const SECTIONS = \[.*?\n\];", lambda m: "const SECTIONS = " + secs,
                  page, count=1, flags=re.DOTALL)
    page = re.sub(r"const QUESTIONS = \[.*?\n\];", lambda m: "const QUESTIONS = " + qs,
                  page, count=1, flags=re.DOTALL)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    print("written: %d questions" % len(Q))
