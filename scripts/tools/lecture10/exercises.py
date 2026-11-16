# -*- coding: utf-8 -*-
import io, json, os, re
E = []
def X(**k): E.append(k)
def m(q, en, ar): return {"q": q, "a": en, "ar": ar}

# the flowcharts are the deck's own, read out of content.py so they cannot drift
_C = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "content.py"), encoding="utf-8").read()
def svg(name): return re.search(r"^%s = '''(.*?)'''" % name, _C, re.S | re.M).group(1).strip()

JSON = '{\n  "city": "Cairo",\n  "temperature": 31\n}'
GP = "A: GET, B: POST"

# ---------------- class work ----------------
X(n=1, type="truefalse", prompt="Write ✓ if the statement is true, ✗ if it is false.",
  promptAr="حط ✓ لو الجملة صح، و ✗ لو غلط.",
  statements=["The client is the side that requests data or processing from the server, and the server is the side that returns the response.",
              "HTTPS is a communication protocol that adds encryption to HTTP.",
              "The GET method is for sending data to the server.",
              "Status code 404 indicates that the page is not found."],
  src="p.64-65 — Worked Example (1) A-D")
X(n=2, type="match", prompt="Match each description with the most appropriate term.",
  promptAr="اربط كل وصف بالمصطلح الأنسب.",
  left=["A communication protocol for exchanging data between web browsers and servers",
        "A system for exchanging data between different pieces of software",
        "A communication protocol that adds encryption to HTTP"],
  right=["HTTP", "API", "HTTPS"],
  src="p.64-65 — Worked Example (2)")
X(n=3, type="category", prompt="Write the HTTP method each operation uses — " + GP + ".",
  promptAr="اكتب طريقة طلب HTTP اللي بتستخدمها كل عملية.",
  items=["Displaying a web page", "Entering an ID and password into a login form and submitting them",
         "Displaying search results", "Submitting the contents of a contact form"],
  src="p.67 — Exercise 3(1)")
X(n=4, type="match", prompt="Match each job in a flowchart with its symbol.",
  promptAr="اربط كل وظيفة في المخطط الانسيابي بالشكل بتاعها.",
  left=["Where the program begins and ends", "A step, such as a calculation",
        "A question with two exits, Yes and No", "Showing a result, like console.log"],
  right=["Rectangle", "Oval", "Parallelogram", "Diamond"],
  src="Qureo chapter 32 — Flowchart")

# ---------------- homework ----------------
X(n=5, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "What is the term for the side that requests data or processing from the server (e.g., a web browser)?", "lines": 1},
             {"q": "What is the term for the side that receives requests from clients, processes them, and returns responses?", "lines": 1},
             {"q": "What is the term for the communication protocol that adds encryption to HTTP?", "lines": 1},
             {"q": "What is the term for the HTTP method for retrieving data from the server?", "lines": 1},
             {"q": "What is the term for the system for exchanging data between different pieces of software?", "lines": 1}],
  src="p.65 — Try 1")
X(n=6, type="fill", prompt="Fill in ( a ) to ( d ).", promptAr="املا الفراغات من ( أ ) لـ ( د ).",
  passage="A web application operates by communication between a ( a ), which requests data or processing from the server, and a ( b ), which receives the request, processes it, and returns a response. This communication uses a protocol called ( c ). The protocol that adds SSL/TLS encryption to ( c ) is called ( d ).",
  src="p.67 — Exercise 2")
X(n=7, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "Choose the combination of status code and meaning that is NOT appropriate. A: 200 — The request was processed successfully B: 404 — Page not found C: 500 — The request was processed successfully D: 500 — A problem occurred on the server side", "lines": 1},
             {"q": "Choose the one that most appropriately describes an API. A: A technology for adjusting the appearance of web pages B: A system for exchanging data between different pieces of software C: A technology for encrypting data and sending it safely D: An HTTP method for retrieving data from the server", "lines": 1},
             {"q": "Choose the one that most appropriately describes HTTPS. A: A method for retrieving data from the server B: A system for exchanging data between different pieces of software C: A communication protocol that adds SSL/TLS encryption to HTTP D: A status code indicating that a problem has occurred on the server side", "lines": 1}],
  src="p.65 Try 2(1); p.66 Try 2(2); p.67 Exercise 3(2)")
X(n=8, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "The client in web applications is: A: The server that processes requests B: The program or device that sends requests C: The database D: The communication protocol", "lines": 1},
             {"q": "When sending login data, it is preferred to use: A: GET B: POST C: 200 D: 404", "lines": 1},
             {"q": "Status code 200 means: A: An internal server error B: The request succeeded C: The resource is not found D: A request that is not allowed", "lines": 1},
             {"q": "Status code 404 indicates: A: The request succeeded B: An internal server error C: The resource is not found D: The connection is secure", "lines": 1}],
  src="Ministry assessments, period 1 — MCQ; form A")
X(n=9, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "The basic difference between HTTP and HTTPS is: A: HTTPS uses TLS encryption B: HTTP is always faster C: HTTPS does not support POST D: HTTP uses JSON", "lines": 1},
             {"q": "The JSON format is used for: A: Designing the user interface B: Exchanging structured data C: Encrypting the connection D: Setting the status code", "lines": 1},
             {"q": "An API is: A: A database B: A set of rules for communication between programs C: A security protocol D: A data format", "lines": 1},
             {"q": "Displaying search results from the server usually uses: A: POST B: GET C: 500 D: HTTPS", "lines": 1}],
  src="Ministry assessments, period 2 — MCQ")
X(n=10, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Explain the client and server model.", "lines": 3},
             {"q": "Why is the HTTPS protocol more secure than HTTP? Give an example.", "lines": 3}],
  src="Ministry assessments, period 1 — performance tasks and home tasks; form A — essay 1")
X(n=11, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Explain the meaning of status code 200 in HTTP.", "lines": 1},
             {"q": "What does status code 404 mean, and when does it appear?", "lines": 2},
             {"q": "What is the role of status code 500 in the communication between the client and the server?", "lines": 2},
             {"q": "What is an API, and how does it help in developing web applications?", "lines": 3}],
  src="Ministry assessments, period 2 — performance tasks and home tasks")
X(n=12, type="extended", prompt="Explain what happens, step by step, when a browser requests a web page and the server responds. Refer to: client, request, HTTP method, response, status code.",
  promptAr="اشرح خطوة بخطوة إيه اللي بيحصل لما المتصفح يطلب صفحة ويب والخادم يستجيب. أشِر إلى: العميل، الطلب، طريقة طلب HTTP، الاستجابة، رمز حالة HTTP.",
  marks=6, lines=8, src="p.65 — Exam-style question [6]")
X(n=13, type="extended", prompt="Distinguish between using the GET method and the POST method, and give a suitable situation for each.",
  promptAr="ميّز بين استخدام طريقة GET وطريقة POST، وحدد موقف مناسب لكل واحدة.",
  marks=4, lines=6, src="Ministry assessments, form C — essay 2; period 1 — home tasks")
X(n=14, type="extended", prompt="Explain the importance of the HTTPS protocol in protecting data while it travels over the network.",
  promptAr="اشرح أهمية بروتوكول HTTPS في حماية البيانات أثناء النقل عبر الشبكة.",
  marks=4, lines=6, src="Ministry assessments, form C — essay 3")
X(n=15, type="short", prompt="Read the data (JSON), then answer.", promptAr="اقرا البيانات (JSON) وبعدين جاوب.",
  code=JSON,
  questions=[{"q": "Name one key and the value that goes with it.", "lines": 1},
             {"q": "Explain how the JSON format is used to exchange data, and why it suits web applications.", "lines": 4}],
  src="Arabic book, lesson 3-2 — Read the data (JSON); Ministry assessments, form C")
X(n=16, type="extended", prompt="Think as an engineer. A school wants a web app where students log in, view their timetable, and download a PDF. For loading a student's grade history, submitting the login form, and requesting today's schedule from another school system, say whether GET or POST fits, and for the last whether an API is involved. Decide whether the login should use HTTP or HTTPS, and why. Recommend the design, with two reasons.",
  promptAr="فكّر كمهندس: مدرسة عايزة تطبيق ويب للدخول والجدول وتنزيل PDF. اختار GET ولا POST لكل إجراء وهل فيه API، واختار HTTP ولا HTTPS للدخول وليه، وأوصِ بالتصميم بسببين.",
  marks=4, lines=8, src="p.66 — Think as an Engineer")
X(n=17, type="extended", prompt="A weather service offers an API that returns today's forecast when a client sends a request. Name the HTTP method the client would use to retrieve the forecast, say why the service should use HTTPS, and give one advantage of receiving the data as JSON.",
  promptAr="خدمة طقس عندها API بترجّع توقعات النهارده. اذكر طريقة الطلب، وليه HTTPS، وميزة واحدة لـ JSON.",
  marks=4, lines=6, src="p.66 — In a New Context")
X(n=18, type="short", prompt="Follow the flowchart, then answer.", promptAr="امشي مع المخطط الانسيابي وبعدين جاوب.",
  svg=svg("PRICE"),
  questions=[{"q": "What is the value of total?", "lines": 1},
             {"q": "Is total > 100 Yes or No? What is shown?", "lines": 1},
             {"q": "Which symbol holds the calculation total = price * 3, and which holds the question?", "lines": 1}],
  src="Qureo chapter 32 — if + Operations")
X(n=19, type="short", prompt="From flowchart to code, and back.", promptAr="من المخطط للكود، والعكس.",
  svg=svg("AB"),
  questions=[{"q": "Write the code for this flowchart.", "lines": 6},
             {"q": "What is shown? And what is shown if b is changed to 11?", "lines": 1},
             {"q": "Draw a flowchart for this code: let age = 15; if (age >= 12) { console.log(\"Ticket OK\"); } else { console.log(\"Too young\"); }", "lines": 8}],
  src="Qureo chapters 32-33 — Flowchart (2); review")
X(n=20, type="short", prompt="Reflect and challenge.", promptAr="فكّر وتحدّى نفسك.",
  questions=[{"q": "Reflect: when a page fails to load, which status code would help you most to understand why, and what would it tell you?", "lines": 3},
             {"q": "Challenge: name one app you use and describe one request it sends and the response it expects.", "lines": 4}],
  src="p.67 — Reflect & Challenge")

A = {
 "1": ["✓ — correct roles of client and server", "✓ — HTTPS adds SSL/TLS encryption to HTTP",
       "✗ — GET retrieves data; POST sends it", "✓ — 404 means the page is not found"],
 "2": ["a — HTTP", "b — API", "c — HTTPS"],
 "3": ["a A — GET", "b B — POST", "c A — GET", "d B — POST"],
 "4": ["Begins and ends — Oval", "A step / calculation — Rectangle", "A Yes / No question — Diamond", "Showing a result — Parallelogram"],
 "5": ["1. The client", "2. The server", "3. HTTPS", "4. GET", "5. An API"],
 "6": {"a": "client", "b": "server", "c": "HTTP", "d": "HTTPS"},
 "7": ["(1) C — 500 is a server error, not success", "(2) B", "(3) C"],
 "8": ["(1) B", "(2) B — POST", "(3) B", "(4) C"],
 "9": ["(1) A", "(2) B", "(3) B", "(4) B — GET"],
 "10": ["1. A client (a browser or app) sends a request to a server; the server receives it, processes it, and returns a response. Many clients can send requests to one server.",
        "2. HTTPS adds TLS encryption to HTTP, so someone listening on the network cannot easily read or change the content, and the server is authenticated. e.g. a password typed on a login page travels encrypted."],
 "11": ["1. 200: success — the request was processed successfully.",
        "2. 404: the requested page or resource is not found; it appears when the address asked for does not exist, e.g. a mistyped URL or a deleted page.",
        "3. 500 tells the client that a problem occurred on the server side, so the request could not be completed; on its own it does not say the detailed cause.",
        "4. A set of rules that lets one program request data or functions from another. The frontend can get data from the backend, or one app can use another service's data, without knowing how it works inside."],
 "12": {"marks": 6,
        "model": "The browser is the client. When the user opens the page, the client sends a request to the server. The request carries an HTTP method that says what is wanted: GET, to retrieve the page. The server receives the request and processes it, for example finding the page. It then returns a response to the client. The response carries a status code that reports the result: 200 if it succeeded, 404 if the page was not found, or 500 if a problem occurred on the server. With 200, the browser shows the page.",
        "points": ["The browser is the client and sends a request (1)", "The request carries an HTTP method, e.g. GET to retrieve (1)",
                   "The server receives and processes the request (1)", "The server returns a response (1)",
                   "The response carries a status code (1)", "200 success / 404 not found / 500 server error, and the browser shows the page (1)"]},
 "13": {"marks": 4,
        "model": "GET is used to retrieve data or a resource from the server, for example displaying a web page or search results. POST is used to send data to the server for it to process, for example submitting a login form, a contact form, or registering a new user. So reading data is GET, and sending data is POST.",
        "points": ["GET retrieves data from the server (1)", "A suitable GET situation, e.g. a page or search results (1)",
                   "POST sends data to the server (1)", "A suitable POST situation, e.g. a login or a form (1)"]},
 "14": {"marks": 4,
        "model": "HTTPS uses HTTP over a TLS connection, so the data is encrypted while it travels. Someone listening on the network, for example on public Wi-Fi, cannot easily read it, so passwords and personal data stay confidential. TLS also stops the data being changed on the way, and checks that the client is talking to the real server. That is why login and payment pages must use HTTPS.",
        "points": ["The data is encrypted with TLS while it travels (1)", "Eavesdroppers cannot easily read it — confidentiality (1)",
                   "It cannot easily be changed on the way / the server is authenticated (1)", "An example, e.g. login or payment pages (1)"]},
 "15": ["1. e.g. key \"city\", value \"Cairo\" (or key \"temperature\", value 31).",
        "2. An API often returns its data in JSON: keys with values, which programs can read and process easily and people can also read. Many languages and tools support it, so the frontend and the backend, or different apps, can exchange structured data in the same format."],
 "16": {"marks": 4, "open": True,
        "points": ["Grade history: GET; login: POST (1)", "Today's schedule from another school: GET, through an API (1)",
                   "Login over HTTPS, so the password is encrypted and not intercepted (1)",
                   "A recommended design with two reasons, e.g. security and the right method for each action (1)"]},
 "17": {"marks": 4,
        "points": ["GET, to retrieve the forecast (1)", "HTTPS: the data is encrypted and cannot easily be read or changed (1)",
                   "JSON: easy for programs to process (1)", "and easy for people to read / widely supported (1)"]},
 "18": ["1. total = 40 * 3 = 120", "2. Yes (120 > 100), so \"Too expensive\" is shown.",
        "3. The calculation is in a rectangle (process); the question is in a diamond (decision)."],
 "19": ["1. let a = 8; let b = 5; if (a > b) { console.log(a); } else { console.log(b); }",
        "2. 8 is shown (8 > 5). If b is 11, 11 is shown (8 > 11 is false).",
        "3. Start (oval) → age = 15 (rectangle) → age >= 12 ? (diamond) → Yes: \"Ticket OK\" / No: \"Too young\" (parallelograms) → End (oval)."],
 "20": {"marks": 4, "open": True,
        "points": ["Reflect: names a status code, e.g. 404 or 500, and what it tells (2)",
                   "Challenge: one app, one request and the expected response (2)"]},
}

MODEL = {
 "1": [m("A. Client and server", "✓ True — the client requests, the server returns the response.", "صح."),
       m("B. HTTPS", "✓ True — it adds SSL/TLS encryption to HTTP.", "صح."),
       m("C. GET", "✗ False — GET retrieves data; POST is for sending it.", "غلط: GET بيجيب، و POST بيبعت."),
       m("D. 404", "✓ True — the page is not found.", "صح.")],
 "2": [m("a. Protocol between browsers and servers", "HTTP.", ""), m("b. Data exchange between software", "API.", ""),
       m("c. HTTP with encryption", "HTTPS.", "")],
 "3": [m("a. Displaying a web page", "A — GET.", "عرض = GET."), m("b. Submitting a login form", "B — POST.", "إرسال = POST."),
       m("c. Displaying search results", "A — GET.", ""), m("d. Submitting a contact form", "B — POST.", "")],
 "4": [m("Begins and ends", "Oval.", "البيضاوي."), m("A step or calculation", "Rectangle.", "المستطيل."),
       m("A Yes / No question", "Diamond.", "المعين = if."), m("Showing a result", "Parallelogram.", "متوازي الأضلاع = console.log.")],
 "5": [m("1.", "The client.", "العميل."), m("2.", "The server.", "الخادم."), m("3.", "HTTPS.", ""), m("4.", "GET.", ""),
       m("5.", "An API.", "واجهة برمجة التطبيقات.")],
 "6": [m("( a )", "client", "العميل."), m("( b )", "server", "الخادم."), m("( c )", "HTTP", ""), m("( d )", "HTTPS", "")],
 "7": [m("(1)", "C — 500 is a server error, so 'processed successfully' is wrong.", "‏500 خطأ في الخادم مش نجاح."),
       m("(2)", "B — a system for exchanging data between different pieces of software.", ""),
       m("(3)", "C — HTTP with SSL/TLS encryption added.", "")],
 "8": [m("(1)", "B — the program or device that sends requests.", "اللي بيطلب."), m("(2)", "B — POST, because it sends data.", ""),
       m("(3)", "B — the request succeeded.", ""), m("(4)", "C — the resource is not found.", "")],
 "9": [m("(1)", "A — HTTPS uses TLS encryption.", ""), m("(2)", "B — exchanging structured data.", ""),
       m("(3)", "B — rules for communication between programs.", ""), m("(4)", "B — GET: showing results is retrieving.", "")],
 "10": [m("1. The client and server model", A["10"][0][3:], "العميل بيطلب والخادم بيعالج ويرد."),
        m("2. Why HTTPS is more secure", A["10"][1][3:], "‏HTTPS بيشفّر، فمحدش يقدر يقرا الباسورد.")],
 "11": [m("1. 200", A["11"][0][3:], "نجاح."), m("2. 404", A["11"][1][3:], "الصفحة مش موجودة."),
        m("3. 500", A["11"][2][3:], "مشكلة في الخادم."), m("4. API", A["11"][3][3:], "قواعد بتخلي برنامج يطلب من برنامج.")],
 "12": [m(None, A["12"]["model"], "العميل يطلب بـ GET، الخادم يعالج ويرد، والاستجابة فيها رمز حالة.")],
 "13": [m(None, A["13"]["model"], "‏GET بيجيب، و POST بيبعت.")],
 "14": [m(None, A["14"]["model"], "‏HTTPS بيشفّر البيانات وهي ماشية، ويمنع تعديلها، ويتحقق من الخادم.")],
 "15": [m("1. A key and its value", A["15"][0][3:], "المفتاح \"city\" وقيمته \"Cairo\"."),
        m("2. JSON in web applications", A["15"][1][3:], "صيغة نصية مهيكلة سهلة على الناس والبرامج.")],
 "16": [m(None, "One possible answer. Loading the grade history is GET, because it retrieves data. Submitting the login form is POST, because it sends the ID and password. Requesting today's schedule from another school's system is GET, through an API, because one program asks another for data. The login must use HTTPS, so the password is encrypted and cannot be intercepted. Design: HTTPS for everything, GET to retrieve and POST to send — it keeps passwords safe, and each action uses the method meant for it.",
          "مثال لإجابة: GET للدرجات، POST للدخول، GET عبر API للجدول، و HTTPS للدخول.")],
 "17": [m(None, "The client uses GET, because it retrieves the forecast. The service should use HTTPS so the data is encrypted and cannot easily be read or changed on the way. JSON is easy for the app to process, and easy for people to read.",
          "‏GET، و HTTPS للأمان، و JSON سهلة.")],
 "18": [m("1.", "total = 40 * 3 = 120.", ""), m("2.", "Yes: 120 > 100, so \"Too expensive\" is shown.", "‏120 أكبر من 100."),
        m("3.", "The calculation is in a rectangle; the question is in a diamond.", "الحساب في مستطيل، والسؤال في معين.")],
 "19": [m("1.", A["19"][0][3:], "المعين = if، والفرعين = if و else."),
        m("2.", A["19"][1][3:], ""),
        m("3.", A["19"][2][3:], "بيضاوي ← مستطيل ← معين ← متوازي أضلاع لكل فرع ← بيضاوي.")],
 "20": [m("Reflect", "One possible answer. 404, because it says the page is not found, so the address is wrong or the page was removed — or 500, which says the problem is on the server.",
          "أي رمز بسبب مقنع."),
        m("Challenge", "One possible answer. A weather app sends a GET request for today's forecast in my city and expects a response with status code 200 and the forecast as JSON.",
          "أي تطبيق، مع طلب واحد والاستجابة المتوقعة.")],
}
DATA = {"SHEET": {"lecture": 10, "title": "How do they talk?", "parts": [{"exercises": E}]}, "ANSWERS": A, "MODEL": MODEL}
assert [x["n"] for x in E] == list(range(1, 21)) and set(A) == set(MODEL) == {str(x["n"]) for x in E}
io.open("lecture10/_teacher/exercises.json", "w", encoding="utf-8", newline="\n").write(json.dumps(DATA, ensure_ascii=False, indent=1) + "\n")
print("exercises:", len(E))
