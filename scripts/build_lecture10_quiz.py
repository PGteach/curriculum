# -*- coding: utf-8 -*-
"""Write Lecture 10's quiz questions into lecture10/quiz/index.html.

    python scripts/build_lecture10_quiz.py && python scripts/protect_answers.py 10

The second command is required: this writes plaintext a: indices, and
protect_answers turns them into fingerprints before publishing.

Lecture 10's paper: lesson 3-2, Web Application Communication Methods
(English textbook pp. 62-67; the Arabic textbook's lesson 3-2), with the
ministry's assessment book for the lesson, and Qureo chapters 32 (Flowchart)
and 33 (the comprehension check on 31-32). Curriculum only.

Every question has four options, every wrong option taken from the same
lesson. d: 1 easy, 2 medium, 3 hard -- the page runs easy to hard. A code
question carries its code in `c`, shown as a code box under the question
(added to the page by add_code_box below, as on lectures 8 and 9).
"""
import io, re

SECTIONS = [
    "Client and server",
    "HTTP and HTTPS",
    "HTTP methods and status codes",
    "API and JSON",
    "Flowcharts",
    "Review: functions and flowcharts",
]

JSON = '{\n  "city": "Cairo",\n  "temperature": 31\n}'
REVIEW = ("function add3(a, b, c) {\n  return a + b + c;\n}\nlet total = add3(1, 2, 3);\n"
          'if (total > 10) {\n  console.log("Big total");\n} else {\n  console.log("Small total");\n}')
CHART = ('let price = 40;\nlet total = price * 3;\nif (total > 100) {\n  console.log("Too expensive");\n'
         '} else {\n  console.log("Buy it");\n}')
SYM = ["A diamond (decision)", "An oval (start / end)", "A rectangle (process)", "A parallelogram (input / output)"]

# (section, difficulty, question, code, options, answer index, why, src, glosses)
Q = [
    # ================= band 1 =================
    (0, 1, "What is the client?", "",
     ["The side that requests data or processing from the server",
      "The side that receives requests, processes them, and returns responses",
      "A protocol that adds encryption to HTTP",
      "A number that reports the result of a request"], 0,
     "The client asks. The side that answers is the server.",
     "p.63 — Point 1(1); p.65 Try 1 (1)", []),
    (0, 1, "What is the server?", "",
     ["The side that receives requests from clients, processes them, and returns responses",
      "The side that requests data or processing from the server",
      "A data format that is easy to read",
      "An HTTP method for retrieving data"], 0,
     "The server answers the client's requests.",
     "p.63 — Point 1(2); p.65 Try 1 (2)", []),
    (1, 1, "What does HTTPS add to HTTP?", "",
     ["TLS encryption", "A faster connection", "A data format for exchanging data", "A status code"], 0,
     "HTTPS is HTTP with TLS encryption, so the content is hard to read on the way.",
     "p.63 — Point 2(2); p.65 Try 1 (3)", [["encryption", "تشفير"]]),
    (2, 1, "Which HTTP method retrieves data from the server?", "",
     ["GET", "POST", "API", "JSON"], 0,
     "GET retrieves; POST sends.",
     "p.65 — Try 1 (4); Ministry assessments, form A — MCQ 2", [["retrieves", "بيجيب"]]),
    (2, 1, "What does status code 200 mean?", "",
     ["Success: the request was processed", "Page not found", "Server error", "The request was not sent"], 0,
     "200 is success.",
     "p.64 — Point 3(2); Ministry assessments, period 1 — home tasks MCQ", []),
    (4, 1, "Which flowchart symbol is a decision (a Yes / No question)?", "",
     SYM, 0,
     "A diamond asks a question and has two exits, Yes and No.",
     "Qureo chapter 32 — Flowchart", []),

    # ================= band 2 =================
    (0, 2, "In web applications, the client is:", "",
     ["The program or device that sends requests", "The server that processes requests",
      "The database", "The communication protocol"], 0,
     "A browser or a phone app: it sends the request.",
     "Ministry assessments, period 1 — MCQ 1", []),
    (2, 2, "Which is preferred when sending login data?", "",
     ["POST", "GET", "200", "404"], 0,
     "Sending data to the server is POST. 200 and 404 are status codes, not methods.",
     "Ministry assessments, period 1 — MCQ 2; p.64 Point 3(1)", []),
    (2, 2, "What does status code 404 indicate?", "",
     ["The requested resource is not found", "An internal server error", "Success", "The connection is secure"], 0,
     "404: the page asked for is not there.",
     "Ministry assessments, period 1 and form A — MCQ", [["resource", "مورد — الصفحة أو البيانات المطلوبة"]]),
    (2, 2, "Which combination of status code and meaning is NOT appropriate?", "",
     ["500 — The request was processed successfully", "200 — The request was processed successfully",
      "404 — Page not found", "500 — A problem occurred on the server side"], 0,
     "500 is a server error. Success is 200.",
     "p.65 — Try 2(1)", []),
    (1, 2, "What is the basic difference between HTTP and HTTPS?", "",
     ["HTTPS uses TLS encryption", "HTTP is always faster", "HTTPS does not support POST", "HTTP uses JSON"], 0,
     "HTTPS encrypts the communication with TLS.",
     "Ministry assessments, period 2 — MCQ 1", []),
    (3, 2, "Which most appropriately describes an API?", "",
     ["A system for exchanging data between different pieces of software",
      "A technology for adjusting the appearance of web pages",
      "A technology for encrypting data and sending it safely",
      "An HTTP method for retrieving data from the server"], 0,
     "An API lets programs exchange data. Appearance is CSS; encryption is HTTPS; retrieving is GET.",
     "p.66 — Try 2(2)", []),
    (3, 2, "What is the JSON format used for?", "",
     ["Exchanging structured data", "Designing the user interface", "Encrypting the connection", "Setting the status code"], 0,
     "JSON is a data format: easy for people to read and for programs to process.",
     "Ministry assessments, period 2 — MCQ 2", []),
    (2, 2, "Displaying search results from the server usually uses:", "",
     ["GET", "POST", "500", "HTTPS"], 0,
     "Showing results is retrieving data: GET.",
     "Ministry assessments, period 2 — home tasks MCQ 2; p.67 Exercise 3(1) c", []),
    (4, 2, "In a flowchart, which symbol holds a calculation such as total = price * 3?", "",
     [SYM[2], SYM[0], SYM[1], SYM[3]], 0,
     "A calculation is a process: a rectangle.",
     "Qureo chapter 32 — if + Operations", []),
    (4, 2, "In a flowchart, which symbol shows a result, like console.log does?", "",
     [SYM[3], SYM[0], SYM[1], SYM[2]], 0,
     "Showing a result is output: a parallelogram.",
     "Qureo chapter 32 — Flowchart (1)", []),
    (4, 2, "This is the code of a flowchart. What is shown?", CHART,
     ["Too expensive", "Buy it", "120", "40"], 0,
     "total = 40 * 3 = 120, and 120 > 100 is true, so the Yes branch.",
     "Qureo chapter 32 — if + Operations", []),
    (5, 2, "A function from chapter 31: what does this print?",
     "function add3(a, b, c) {\n  return a + b + c;\n}\nconsole.log(add3(5, 5, 5));",
     ["15", "555", "5", "undefined"], 0,
     "5 + 5 + 5 = 15.",
     "Qureo chapter 33 — review of chapter 31", []),

    # ================= band 3 =================
    (1, 3, "Which most appropriately describes HTTPS?", "",
     ["A communication protocol that adds SSL/TLS encryption to HTTP",
      "A method for retrieving data from the server",
      "A system for exchanging data between different pieces of software",
      "A status code indicating that a problem has occurred on the server side"], 0,
     "HTTPS = HTTP + SSL/TLS encryption.",
     "p.67 — Exercise 3(2)", []),
    (3, 3, "In this JSON data, which one is a key?", JSON,
     ['"city"', '"Cairo"', "31", "{"], 0,
     '"city" is a key; "Cairo" is its value.',
     "Arabic book, lesson 3-2 — Read the data (JSON)", []),
    (2, 3, "A browser receives status code 404. Which is true?", "",
     ["The address asked for does not exist; the server itself is working",
      "The server has broken down", "The connection was not encrypted", "The request succeeded"], 0,
     "404 is page not found. A server breakdown would be 500.",
     "p.65 — Pause & Think", []),
    (4, 3, "In code, a diamond with Yes and No branches becomes:", "",
     ["An if ... else statement", "A console.log", "A function", "A let"], 0,
     "The question goes in if ( ); the Yes branch in the if, the No branch in the else.",
     "Qureo chapter 32 — Flowchart (2)", []),
    (4, 3, "A flowchart: a = 8, b = 5; is a > b? Yes: show a. No: show b. What is shown if b is changed to 11?", "",
     ["11", "8", "5", "Nothing is shown"], 0,
     "8 > 11 is false, so the No branch shows b, which is 11.",
     "Qureo chapter 32 — Flowchart (2)", []),
    (5, 3, "A function inside a decision: what does this print?", REVIEW,
     ["Small total", "Big total", "6", "undefined"], 0,
     "add3(1, 2, 3) returns 6, and 6 > 10 is false, so the else branch.",
     "Qureo chapter 33 — review of chapters 31-32", []),
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

    p = "lecture10/quiz/index.html"
    page = io.open(p, encoding="utf-8").read()
    page = add_code_box(page)
    page = re.sub(r"const SECTIONS = \[.*?\n\];", lambda m: "const SECTIONS = " + secs,
                  page, count=1, flags=re.DOTALL)
    page = re.sub(r"const QUESTIONS = \[.*?\n\];", lambda m: "const QUESTIONS = " + qs,
                  page, count=1, flags=re.DOTALL)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    print("written: %d questions" % len(Q))
