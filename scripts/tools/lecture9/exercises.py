# -*- coding: utf-8 -*-
import io, json
E = []
def X(**k): E.append(k)
def m(q, en, ar): return {"q": q, "a": en, "ar": ar}

ADD = "function add(a, b) {\n  return a + b;\n}\nconsole.log(add(3, 5));\nconsole.log(add(10, 4));"
BIG = ("function biggest(a, b, c) {\n  let big = a;\n  if (b > big) {\n    big = b;\n  }\n"
       "  if (c > big) {\n    big = c;\n  }\n  return big;\n}\nconsole.log(biggest(3, 8, 6));")
ABC = "A: Frontend, B: Backend, C: Database"

# ---------------- class work ----------------
X(n=1, type="truefalse", prompt="Write ✓ if the statement is true, ✗ if it is false.",
  promptAr="حط ✓ لو الجملة صح، و ✗ لو غلط.",
  statements=["The frontend is the screen component that users see directly.",
              "The backend is the part that runs on the browser.",
              "A database is a system that organizes, stores, and manages data.",
              "A web application operates with the frontend alone."],
  src="p.57-58 — Worked Example (1) A-D")
X(n=2, type="match", prompt="Match each description with the most appropriate term.",
  promptAr="اربط كل وصف بالمصطلح الأنسب.",
  left=["The part responsible for server-side processing that users do not see",
        "The screen component that users interact with directly",
        "A system that organizes, stores, and manages data"],
  right=["Frontend", "Backend", "Database"],
  src="p.58 — Worked Example (2)")
X(n=3, type="category", prompt="Write the tier each part of an e-commerce site belongs to — " + ABC + ".",
  promptAr="اكتب كل جزء من موقع التجارة الإلكترونية تابع لأنهي طبقة.",
  items=["Product listing page", "Stock checking processing", "Storage of customer information",
         "Cart screen", "Payment processing", "Storage of order history"],
  src="p.59 — Try 2(2)")
X(n=4, type="short", prompt="Read the code, then answer.", promptAr="اقرا الكود وبعدين جاوب.",
  code=ADD,
  questions=[{"q": "What does the first console.log print?", "lines": 1},
             {"q": "What does the second console.log print?", "lines": 1},
             {"q": "In add(3, 5), what are the arguments, and what is the return value?", "lines": 2}],
  src="Qureo chapter 31 — Function to add two values")

# ---------------- homework ----------------
X(n=5, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "What is the term for an application used through a web browser?", "lines": 1},
             {"q": "What is the term for the screen component that users see directly?", "lines": 1},
             {"q": "What is the term for the part responsible for server-side processing that users do not see?", "lines": 1},
             {"q": "What is the term for a system that organizes, stores, and manages data?", "lines": 1}],
  src="p.58 — Try 1")
X(n=6, type="fill", prompt="Fill in ( a ) to ( c ).", promptAr="املا الفراغات من ( أ ) لـ ( ج ).",
  passage="A web application is broadly composed of three tiers. The screen component that users see directly is called the ( a ). The part responsible for server-side processing that users do not see is called the ( b ). A system that organizes, stores, and manages data is called the ( c ). In response to user actions, these three tiers cooperate to perform processing.",
  src="p.60 — Exercise 2")
X(n=7, type="category", prompt="Write the tier each part of a social network (SNS) belongs to — " + ABC + ".",
  promptAr="اكتب كل جزء من شبكة التواصل الاجتماعي تابع لأنهي طبقة.",
  items=["Timeline screen", "Processing that determines the audience for a post", "Storage of post data",
         "Post screen", "Notification processing", "Storage of follow relationships"],
  src="p.60 — Exercise 3(1)")
X(n=8, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "When searching for a product on an online shopping site, which is responsible for searching through data for products that match the search keywords? A: Frontend B: Backend C: Database", "lines": 1},
             {"q": "Choose the one that most appropriately describes the three-tier architecture of a web application. A: The frontend has the role of storing and managing data. B: The backend is the part that users interact with directly on the browser. C: In response to user actions, the frontend, backend, and database cooperate to perform processing. D: The database has the role of displaying screens to users.", "lines": 1},
             {"q": "When you search for a product in an online store, which tier sends the request to the database? A: The frontend B: The backend C: The database itself D: The browser", "lines": 1}],
  src="p.58 Try 2(1); p.61 Exercise 3(2); Ministry assessments, form A")
X(n=9, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "A web application is usually built from: A: Three tiers B: Two tiers C: One tier D: Several tiers", "lines": 1},
             {"q": "The tier responsible for displaying screens and collecting the user's data and actions is: A: The backend B: The database C: The frontend D: The processing server", "lines": 1},
             {"q": "On a video-sharing site, counting views and choosing recommended videos is done by: A: The frontend B: The backend C: The database D: The communication network", "lines": 1},
             {"q": "Storing posts, follow relationships and messages on a social network is the job of: A: The processing server B: The database C: The frontend D: The backend", "lines": 1}],
  src="Ministry assessments, periods 1 and 2 — MCQ")
X(n=10, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Define a web application, and give two examples from your daily life.", "lines": 3},
             {"q": "List the main tiers that a web application is made of.", "lines": 2}],
  src="Ministry assessments, period 1 — performance tasks; form B — essay 1")
X(n=11, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Compare the role of the frontend and the role of the backend in a social network app.", "lines": 3},
             {"q": "What is the role of the database in a social network?", "lines": 2}],
  src="Ministry assessments, period 1 — home tasks; form C — essay 2")
X(n=12, type="extended", prompt="Explain how the three tiers of a web application cooperate when a user posts a photo on a social media app. Refer to the role of the frontend, backend, and database.",
  promptAr="اشرح إزاي الطبقات التلاتة لتطبيق الويب بتتعاون لما المستخدم ينشر صورة على تطبيق تواصل اجتماعي. أشِر إلى دور الواجهة الأمامية والواجهة الخلفية وقاعدة البيانات.",
  marks=6, lines=8, src="p.58 — Exam-style question [6]")
X(n=13, type="extended", prompt="Trace the steps of a request when a user searches for a product in an online store, through the three tiers, and give the role of each tier.",
  promptAr="تتبّع خطوات طلب المستخدم لما يدوّر على منتج في متجر إلكتروني عبر الطبقات التلاتة، ووضّح دور كل طبقة.",
  marks=4, lines=7, src="Ministry assessments, form A — essay 3; p.57 Point 3")
X(n=14, type="extended", prompt="Discuss the importance of the database tier in e-commerce sites.",
  promptAr="ناقش أهمية طبقة قاعدة البيانات في مواقع التجارة الإلكترونية.",
  marks=4, lines=6, src="Ministry assessments, period 2 — performance tasks")
X(n=15, type="extended", prompt="How does the backend deal with the data coming from the frontend and the data stored in the database in an e-commerce site?",
  promptAr="إزاي الواجهة الخلفية بتتعامل مع البيانات اللي جاية من الواجهة الأمامية والبيانات المتخزنة في قاعدة البيانات في موقع تجارة إلكترونية؟",
  marks=4, lines=6, src="Ministry assessments, period 1 — home tasks")
X(n=16, type="extended", prompt="Think as an engineer. A clinic wants a web app where patients book appointments, check which time slots are free, and see their past visits. Say which tier should handle the booking form, checking free slots, and storing past visits, and why. The booking page opens but no free slots appear: which tier is clearly working, and which has probably failed? Recommend whether the clinic should separate its app into three tiers, with two reasons.",
  promptAr="فكّر كمهندس: عيادة عايزة تطبيق ويب للحجز. وزّع المهام التلاتة على الطبقات وليه، وشخّص العطل لما صفحة الحجز تفتح ومفيش مواعيد، وقرّر نفصل الطبقات ولا لأ بسببين.",
  marks=4, lines=8, src="p.59 — Think as an Engineer")
X(n=17, type="extended", prompt="A weather app lets users type a city and see the forecast. Name which tier does each job — taking the city name, looking up the forecast data, and storing past forecasts — and identify one job the frontend cannot do on its own.",
  promptAr="تطبيق طقس بيخليك تكتب اسم مدينة وتشوف التوقعات. سمّي أنهي طبقة بتعمل كل مهمة، وحدد مهمة واحدة الواجهة الأمامية متقدرش تعملها لوحدها.",
  marks=4, lines=6, src="p.59 — In a New Context")
X(n=18, type="short", prompt="Read the code, then answer.", promptAr="اقرا الكود وبعدين جاوب.",
  code=BIG,
  questions=[{"q": "What is the value of big right after let big = a; runs?", "lines": 1},
             {"q": "Is b > big true or false the first time? Then what is big?", "lines": 1},
             {"q": "Is c > big true or false? What does the program print?", "lines": 1}],
  src="Qureo chapter 31 — Function that compares three values")
X(n=19, type="short", prompt="Write the code.", promptAr="اكتب الكود.",
  questions=[{"q": "Write a function add3(a, b, c) that returns the sum of three values. Then print add3(2, 4, 6).", "lines": 5},
             {"q": "Write a function smallest(a, b, c) that returns the smallest of three values, using if. Then print smallest(7, 2, 5).", "lines": 9}],
  src="Qureo chapter 31 — Functions that add and compare three values")
X(n=20, type="short", prompt="Reflect and challenge.", promptAr="فكّر وتحدّى نفسك.",
  questions=[{"q": "Reflect: which tier do you think fails most noticeably to a user when something goes wrong, and why?", "lines": 3},
             {"q": "Challenge: name one online service you use and describe what its frontend, backend, and database each do.", "lines": 4}],
  src="p.60 — Reflect & Challenge")

SMALL = ("function smallest(a, b, c) {\n  let small = a;\n  if (b < small) {\n    small = b;\n  }\n"
         "  if (c < small) {\n    small = c;\n  }\n  return small;\n}\nconsole.log(smallest(7, 2, 5));")
A = {
 "1": ["✓ — the frontend is the screen users see directly", "✗ — the backend runs on the server, not on the browser",
       "✓ — correct definition of a database", "✗ — a web application operates with three tiers"],
 "2": ["a — B Backend", "b — A Frontend", "c — C Database"],
 "3": ["a A — frontend", "b B — backend", "c C — database", "d A — frontend", "e B — backend", "f C — database"],
 "4": ["1. 8", "2. 14", "3. The arguments are 3 and 5 (a = 3, b = 5); the return value is 8."],
 "5": ["1. A web application", "2. The frontend", "3. The backend", "4. A database"],
 "6": {"a": "frontend", "b": "backend", "c": "database"},
 "7": ["a A — frontend", "b B — backend", "c C — database", "d A — frontend", "e B — backend", "f C — database"],
 "8": ["(1) B — Backend", "(2) C", "(3) B — the backend"],
 "9": ["(1) A — three tiers", "(2) C — the frontend", "(3) B — the backend", "(4) B — the database"],
 "10": ["1. An application used through a web browser, without installing dedicated software (some can also be installed). e.g. YouTube, Amazon, Gmail, Google Maps.",
        "2. The frontend, the backend and the database (the three-tier architecture)."],
 "11": ["1. The frontend shows the timeline and the post screen and sends what the user types; the backend processes it: it decides the audience for a post and controls the notifications.",
        "2. It stores the posts, the follow relationships and the messages, and retrieves them when needed."],
 "12": {"marks": 6,
        "model": "The user picks a photo and writes a caption on the post screen: the frontend collects this input and sends it to the backend. The backend processes the request: it checks it, decides who the audience for the post is, and sends the photo and the post to the database. The database stores the post data and the photo, linked to the user and to their follow relationships. The backend then returns a result to the frontend, which shows the new post on the user's timeline. Each tier has one role, and only together do they publish the photo.",
        "points": ["Frontend collects the photo and caption on the post screen (1)", "Frontend sends them to the backend (1)",
                   "Backend processes the request / decides the audience (1)", "Backend sends the data to the database (1)",
                   "Database stores the post data (1)", "Result returns to the frontend, which displays the post (1)"]},
 "13": {"marks": 4,
        "model": "① The frontend receives the keywords the user typed. ② It sends them to the backend. ③ The backend searches the database for products that match. ④ The database returns the matching products to the backend. ⑤ The backend organizes the results and returns them to the frontend. ⑥ The frontend displays them on the user's screen. So the frontend shows and collects, the backend decides and processes, and the database stores and retrieves.",
        "points": ["Frontend receives the keywords and sends them to the backend (1)", "Backend searches the database (1)",
                   "Database returns the matching products to the backend (1)", "Backend organizes the results; frontend displays them (1)"]},
 "14": {"marks": 4,
        "model": "Without the database the site would have nothing to show or sell: it stores and manages the product information, the customers' information and the order history, and retrieves them when the backend needs them, for example to show products, check stock or record a new order. It also keeps that data organized and safe over time, so that a customer's orders and details are still there the next time.",
        "points": ["Stores product information (1)", "Stores customer information and order history (1)",
                   "Retrieves data when the backend needs it (1)", "Records new data, e.g. a new order (1)"]},
 "15": {"marks": 4,
        "model": "The backend receives the data the user entered on the frontend, such as a search or an order. It applies the site's rules to it: for example, it checks the stock or runs the payment. It asks the database for the stored data it needs, such as the products or the customer's details, and records new data, such as the new order. Then it organizes the result and returns it to the frontend to display.",
        "points": ["Receives the data from the frontend (1)", "Processes it / applies the rules, e.g. stock, payment (1)",
                   "Retrieves from and records to the database (1)", "Returns the result to the frontend (1)"]},
 "16": {"marks": 4, "open": True,
        "points": ["Booking form: frontend; free slots: backend; past visits: database — with reasons (1)",
                   "Fault: the frontend is working (the page opens) (1)",
                   "The backend (or the database it reads) has probably failed (1)",
                   "Recommends three tiers with two reasons, e.g. a fault is easier to find; each tier can be changed alone (1)"]},
 "17": {"marks": 4,
        "points": ["Taking the city name: frontend (1)", "Looking up the forecast: backend (1)",
                   "Storing past forecasts: database (1)", "One job the frontend cannot do alone, e.g. look up or store the forecast data (1)"]},
 "18": ["1. 3", "2. True (8 > 3), so big becomes 8.", "3. False (6 > 8 is false). It prints 8."],
 "19": ["1. function add3(a, b, c) { return a + b + c; }  console.log(add3(2, 4, 6));  → 12",
        "2. " + SMALL.replace("\n", " ") + "  → 2"],
 "20": {"marks": 4, "open": True,
        "points": ["Reflect: names a tier, with a reason (e.g. the frontend: the user sees it fail at once) (2)",
                   "Challenge: one service, with what each of its three tiers does (2)"]},
}

MODEL = {
 "1": [m("A. The frontend", "✓ True — it is the screen users see directly.", "صح."),
       m("B. The backend", "✗ False — the backend runs on the server, not on the browser.", "غلط: على الخادم."),
       m("C. The database", "✓ True — it organizes, stores and manages data.", "صح."),
       m("D. The frontend alone", "✗ False — a web application needs all three tiers.", "غلط: لازم التلات طبقات.")],
 "2": [m("a. Server-side processing", "B — Backend.", "المعالجة من جانب الخادم = الواجهة الخلفية."),
       m("b. The screen users interact with", "A — Frontend.", "الشاشة = الواجهة الأمامية."),
       m("c. Organizes, stores and manages data", "C — Database.", "التخزين = قاعدة البيانات.")],
 "3": [m("a. Product listing page", "A — Frontend.", "شاشة."), m("b. Stock checking", "B — Backend.", "معالجة."),
       m("c. Customer information", "C — Database.", "تخزين."), m("d. Cart screen", "A — Frontend.", "شاشة."),
       m("e. Payment processing", "B — Backend.", "معالجة."), m("f. Order history", "C — Database.", "تخزين.")],
 "4": [m("1.", "8 — a = 3 and b = 5, and return sends back 3 + 5.", "‏3 + 5 = 8."),
       m("2.", "14 — 10 + 4.", ""),
       m("3.", "The arguments are 3 and 5; the return value is 8.", "الوسائط هي اللي بندخّلها، والقيمة المرجعة هي اللي return بترجّعها.")],
 "5": [m("1.", "A web application.", "تطبيق الويب."), m("2.", "The frontend.", "الواجهة الأمامية."),
       m("3.", "The backend.", "الواجهة الخلفية."), m("4.", "A database.", "قاعدة البيانات.")],
 "6": [m("( a )", "frontend", "الواجهة الأمامية."), m("( b )", "backend", "الواجهة الخلفية."), m("( c )", "database", "قاعدة البيانات.")],
 "7": [m("a. Timeline screen", "A — Frontend.", "شاشة."), m("b. Deciding the audience", "B — Backend.", "قرار ومعالجة."),
       m("c. Storage of post data", "C — Database.", "تخزين."), m("d. Post screen", "A — Frontend.", "شاشة."),
       m("e. Notification processing", "B — Backend.", "معالجة."), m("f. Follow relationships", "C — Database.", "تخزين.")],
 "8": [m("(1)", "B — the backend searches the data; the database only holds it.", "الواجهة الخلفية هي اللي بتدوّر."),
       m("(2)", "C — the three tiers cooperate. The other options give one tier another tier's job.", "التلات طبقات بيتعاونوا."),
       m("(3)", "B — the backend sends the request to the database.", "الواجهة الخلفية هي اللي بتكلم قاعدة البيانات.")],
 "9": [m("(1)", "A — three tiers.", ""), m("(2)", "C — the frontend: it shows and collects.", "تعرض وتجمع."),
       m("(3)", "B — the backend: counting and choosing are processing.", "تقرر وتعالج."),
       m("(4)", "B — the database: storing.", "تخزن وتسترجع.")],
 "10": [m("1. A web application", A["10"][0][3:], "تطبيق بيتستخدم من خلال المتصفح."),
        m("2. The main tiers", A["10"][1][3:], "الواجهة الأمامية والواجهة الخلفية وقاعدة البيانات.")],
 "11": [m("1. Frontend and backend", A["11"][0][3:], "الأمامية بتعرض وتجمع، والخلفية بتقرر وتعالج."),
        m("2. The database", A["11"][1][3:], "بتخزن المنشورات والمتابعات والرسائل.")],
 "12": [m(None, A["12"]["model"], "الأمامية تجمع الصورة وتبعتها، الخلفية تعالج وتقرر الجمهور، قاعدة البيانات تخزن، والنتيجة ترجع تتعرض.")],
 "13": [m(None, A["13"]["model"], "الطلب بينزل من الأمامية للخلفية لقاعدة البيانات، والرد بيطلع تاني.")],
 "14": [m(None, A["14"]["model"], "من غير قاعدة البيانات مفيش منتجات ولا عملاء ولا طلبات.")],
 "15": [m(None, A["15"]["model"], "الخلفية بتستقبل من الأمامية، وتسأل قاعدة البيانات، وترجّع النتيجة.")],
 "16": [m(None, "One possible answer. The booking form is the frontend, because it is the screen that collects the patient's choice. Checking free slots is the backend, because it processes and decides. Storing past visits is the database, because it stores and retrieves. If the page opens but no slots appear, the frontend is clearly working; the backend has probably failed, or the database it reads from. Yes, separate the three tiers: a fault is easier to find, and each tier can be changed without breaking the others.",
          "مثال لإجابة: الفورم = أمامية، المواعيد = خلفية، الزيارات = قاعدة بيانات؛ والعطل غالبًا في الخلفية.")],
 "17": [m(None, "Taking the city name is the frontend. Looking up the forecast data is the backend. Storing past forecasts is the database. One job the frontend cannot do on its own: look up the forecast — it has to ask the backend, which gets the data from the database.",
          "الأمامية تاخد اسم المدينة، الخلفية تدوّر على التوقعات، قاعدة البيانات تخزن القديم.")],
 "18": [m("1.", "3 — big starts as a.", ""), m("2.", "True: 8 > 3, so big becomes 8.", "‏8 > 3 صح."),
        m("3.", "False: 6 > 8 is false, so big stays 8. It prints 8.", "‏6 > 8 غلط، فبيطبع 8.")],
 "19": [m("1.", "function add3(a, b, c) { return a + b + c; } then console.log(add3(2, 4, 6)); prints 12.", "تلات وسائط، و return بترجّع مجموعهم."),
        m("2.", SMALL.replace("\n", " ") + " — prints 2.", "نفس فكرة biggest بس بعلامة <.")],
 "20": [m("Reflect", "One possible answer. The frontend: if it fails, the user sees a broken or blank page at once, while a backend or database fault may only show up as missing results.",
          "أي طبقة بسبب مقنع."),
        m("Challenge", "One possible answer. YouTube: the frontend shows the player and the search box; the backend chooses recommended videos and counts views; the database stores the videos, users and viewing history.",
          "أي خدمة، مع دور كل طبقة.")],
}
DATA = {"SHEET": {"lecture": 9, "title": "What happens when you click?", "parts": [{"exercises": E}]}, "ANSWERS": A, "MODEL": MODEL}
assert [x["n"] for x in E] == list(range(1, 21)) and set(A) == set(MODEL) == {str(x["n"]) for x in E}
io.open("lecture9/_teacher/exercises.json", "w", encoding="utf-8", newline="\n").write(json.dumps(DATA, ensure_ascii=False, indent=1) + "\n")
print("exercises:", len(E))
