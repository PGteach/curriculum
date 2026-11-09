# -*- coding: utf-8 -*-
"""Write Lecture 9's quiz questions into lecture9/quiz/index.html.

    python scripts/build_lecture9_quiz.py && python scripts/protect_answers.py 9

The second command is required: this writes plaintext a: indices, and
protect_answers turns them into fingerprints before publishing.

Lecture 9's paper: lesson 3-1, The Overall Structure of Web Applications
(English textbook pp. 56-61), with the ministry's assessment book for the
lesson, and Qureo chapter 31, Functions (4). Curriculum only.

Every question has four options, every wrong option taken from the same
lesson. d: 1 easy, 2 medium, 3 hard -- the page runs easy to hard. A code
question carries its code in `c`, shown as a code box under the question
(added to the page by add_code_box below, as on lecture 8).
"""
import io, re

SECTIONS = [
    "What is a web application?",
    "The three tiers",
    "How the tiers cooperate",
    "Familiar web applications",
    "Functions that add values",
    "Functions that compare values",
]

ADD = "function add(a, b) {\n  return a + b;\n}\nconsole.log(add(2, 3));"
ADD3 = "function add3(a, b, c) {\n  return a + b + c;\n}\nconsole.log(add3(1, 2, 3));"
NORET = "function add(a, b) {\n  a + b;\n}\nconsole.log(add(3, 5));"
BIG = ("function biggest(a, b, c) {\n  let big = a;\n  if (b > big) {\n    big = b;\n  }\n"
       "  if (c > big) {\n    big = c;\n  }\n  return big;\n}\n")

# (section, difficulty, question, code, options, answer index, why, src, glosses)
Q = [
    # ================= band 1 =================
    (0, 1, "What is a web application?", "",
     ["An application used through a web browser, without installing dedicated software",
      "The server-side processing that users do not see",
      "A system that organizes, stores and manages data",
      "The screen component that users see directly"], 0,
     "You use it through a browser. The other three are the backend, the database and the frontend.",
     "p.56 — Point 1(1); p.58 Try 1 (1)", [["dedicated", "مخصّص — برنامج معيّن لازم يتثبت"]]),
    (1, 1, "What is the frontend?", "",
     ["The screen component that users see directly",
      "The server-side processing that users do not see",
      "A system that organizes, stores and manages data",
      "An application used through a web browser"], 0,
     "The frontend is the screen you see and use.",
     "p.56 — Point 2(1); p.58 Try 1 (2)", []),
    (1, 1, "What is the backend?", "",
     ["The server-side processing that users do not see",
      "The screen component that users see directly",
      "A system that organizes, stores and manages data",
      "An application used through a web browser"], 0,
     "The backend is hidden, on the server: it processes and decides.",
     "p.56 — Point 2(1); p.58 Try 1 (3)", []),
    (1, 1, "What is the database?", "",
     ["A system that organizes, stores and manages data",
      "The screen component that users see directly",
      "The server-side processing that users do not see",
      "An application used through a web browser"], 0,
     "The database stores the data and retrieves it when needed.",
     "p.56 — Point 2(1); p.58 Try 1 (4)", []),
    (1, 1, "A web application is usually built from how many tiers?", "",
     ["Three tiers", "One tier", "Two tiers", "Many tiers, with no fixed number"], 0,
     "Frontend, backend and database: three tiers.",
     "Ministry assessments, period 1 — MCQ 1", [["tiers", "طبقات"]]),
    (4, 1, "A function that adds two values: what does this print?", ADD,
     ["5", "23", "6", "undefined"], 0,
     "a = 2 and b = 3, so return sends back 2 + 3 = 5.",
     "Qureo chapter 31 — Function to add two values", []),

    # ================= band 2 =================
    (1, 2, "Which tier displays the screens and collects the user's data and actions?", "",
     ["The frontend", "The backend", "The database", "The processing server"], 0,
     "Showing and collecting is the frontend's job.",
     "Ministry assessments, period 1 — MCQ 2", []),
    (2, 2, "When you search for a product on a shopping site, which tier searches through the data for products that match?", "",
     ["The backend", "The frontend", "The database", "The browser"], 0,
     "The backend searches the database; the database only holds the data.",
     "p.58 — Try 2(1)", []),
    (2, 2, "When you search for a product in an online store, which tier sends the request to the database?", "",
     ["The backend", "The frontend", "The database itself", "The browser"], 0,
     "The frontend sends to the backend, and the backend asks the database.",
     "Ministry assessments, form A — MCQ 2; p.57 Point 3 ③", []),
    (2, 2, "In the search example, what is the very last step?", "",
     ["The frontend displays the search results on the user's screen",
      "The backend searches the database for matching products",
      "The database returns the matching products to the backend",
      "The frontend receives the search keywords"], 0,
     "Step ⑥: the frontend displays the results.",
     "p.57 — Point 3 ⑥", []),
    (3, 2, "On a video-sharing site, counting views and choosing recommended videos is done by which tier?", "",
     ["The backend", "The frontend", "The database", "The communication network"], 0,
     "Counting and choosing are processing and decisions: the backend.",
     "Ministry assessments, period 2 — MCQ 1; p.57 Point 4", []),
    (3, 2, "On a social network, storing posts, follow relationships and messages is done by which tier?", "",
     ["The database", "The frontend", "The backend", "The processing server"], 0,
     "Storing is the database's job.",
     "Ministry assessments, period 2 — MCQ 2; p.57 Point 4", []),
    (3, 2, "Which is an example of data stored in an e-commerce site's database?", "",
     ["The order history", "The search screen", "Checking the login", "The user interface"], 0,
     "Order history is stored data. The search screen is the frontend; checking the login is the backend.",
     "Ministry assessments, form A — MCQ 3", []),
    (0, 2, "Which of these is an example of a web application?", "",
     ["A maps website on the Internet", "A video player on the device",
      "A calculator app on the desktop", "A photo-editing program"], 0,
     "The maps website is used through a browser; the others are installed on the device.",
     "Ministry assessments, form B — MCQ 1", []),
    (4, 2, "A function that adds three values: what does this print?", ADD3,
     ["6", "123", "3", "undefined"], 0,
     "1 + 2 + 3 = 6. The three arguments are numbers, so they are added.",
     "Qureo chapter 31 — Function that adds three values", []),
    (5, 2, "A function that compares three values: what does this print?", BIG + "console.log(biggest(4, 9, 7));",
     ["9", "4", "7", "20"], 0,
     "big starts at 4, becomes 9, and 7 > 9 is false. return sends back 9.",
     "Qureo chapter 31 — Function that compares three values", []),
    (5, 2, "Math.max with three values: what does this print?", "console.log(Math.max(3, 8, 5));",
     ["8", "3", "5", "16"], 0,
     "Math.max gives back the biggest value.",
     "Qureo chapter 12 — Math.max; chapter 31", []),

    # ================= band 3 =================
    (2, 3, "Which statement most appropriately describes the three-tier architecture of a web application?", "",
     ["In response to user actions, the frontend, backend and database cooperate to perform processing",
      "The frontend has the role of storing and managing data",
      "The backend is the part that users interact with directly on the browser",
      "The database has the role of displaying screens to users"], 0,
     "The three tiers cooperate. Each of the other options gives one tier another tier's job.",
     "p.61 — Exercise 3(2)", []),
    (0, 3, "What is the main idea of the overall structure of web applications?", "",
     ["An application is built from three tiers that cooperate",
      "Each tier works alone, without cooperating",
      "The application works through the browser only",
      "The application relies only on the database"], 0,
     "Three tiers, cooperating.",
     "Ministry assessments, forms B and C — MCQ", []),
    (3, 3, "What is the main role of the database tier in a web application?", "",
     ["Storing data and retrieving it", "Receiving the user's actions",
      "Processing calculations", "Displaying screens and interfaces"], 0,
     "The database stores and retrieves. Receiving and displaying is the frontend; processing is the backend.",
     "Ministry assessments, period 1 — performance tasks MCQ 2", []),
    (4, 3, "This function has a mistake. What does it print?", NORET,
     ["undefined", "8", "0", "3"], 0,
     "There is no return, so the function gives nothing back: undefined.",
     "Qureo chapter 31 — return value", []),
    (4, 3, "Which function correctly adds three values?", "",
     ["function add3(a, b, c) { return a + b + c; }",
      "function add3(a, b, c) { a + b + c; }",
      "function add3(a, b) { return a + b + c; }",
      "function add3(a + b + c) { return; }"], 0,
     "Three arguments, and return sends back their sum.",
     "Qureo chapter 31 — Function that adds three values", []),
    (5, 3, "Two values are the same. What does this print?", BIG + "console.log(biggest(5, 5, 2));",
     ["5", "2", "12", "10"], 0,
     "big starts at 5. 5 > 5 is false and 2 > 5 is false, so big stays 5.",
     "Qureo chapter 31 — Function that compares three values", []),
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

    p = "lecture9/quiz/index.html"
    page = io.open(p, encoding="utf-8").read()
    page = add_code_box(page)
    page = re.sub(r"const SECTIONS = \[.*?\n\];", lambda m: "const SECTIONS = " + secs,
                  page, count=1, flags=re.DOTALL)
    page = re.sub(r"const QUESTIONS = \[.*?\n\];", lambda m: "const QUESTIONS = " + qs,
                  page, count=1, flags=re.DOTALL)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    print("written: %d questions" % len(Q))
