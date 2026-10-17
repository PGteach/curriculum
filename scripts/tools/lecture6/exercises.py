# -*- coding: utf-8 -*-
import io, json
E = []
def X(**k): E.append(k)
def m(q, en, ar): return {"q": q, "a": en, "ar": ar}
MODEL = {}

# ---------------- class work ----------------
X(n=1, type="truefalse", prompt="Write ✓ if the statement is true, ✗ if it is false.",
  promptAr="حط ✓ لو الجملة صح، و ✗ لو غلط.",
  statements=["A firewall allows or denies communication based on rules set in advance.",
              "Using a VPN can reduce the risk of eavesdropping even on public Wi-Fi.",
              "A DMZ is a system that exposes all servers to the outside.",
              "Defense in depth is the concept of layering multiple security measures."],
  src="p.44 — Worked Example (1) A-D")
X(n=2, type="match", prompt="Match each description to the most appropriate term.",
  promptAr="وصّل كل وصف بأنسب مصطلح.",
  left=["A technology that creates an encrypted virtual private line over the Internet for safe connection from a remote location",
        "An area where servers exposed to the outside are placed separately from the internal network",
        "A system that allows or denies communication based on rules set in advance"],
  right=["Firewall", "VPN", "DMZ"], src="p.44 — Worked Example (2)")
X(n=3, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "What is the term for the system installed at the entry/exit point of a network that allows or denies communication based on rules?", "lines": 1},
             {"q": "What is the three-letter abbreviation for the technology that creates an encrypted virtual private line over the Internet?", "lines": 1},
             {"q": "What is the three-letter abbreviation for the area where servers exposed to the outside are placed separately from the internal network?", "lines": 1},
             {"q": "What is the term for the concept of layering multiple security measures?", "lines": 1}],
  src="p.45 — Try 1")
X(n=4, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Choose the one that is NOT an appropriate use of a VPN. A: Connecting safely from home to an organization's network B: Connecting offices in different locations safely C: Automatically deleting files infected with viruses D: Encrypting communication content on public Wi-Fi", "lines": 1},
             {"q": "Write the layer of defense in depth each measure belongs to — A: Network entry, B: Communication path, C: Server placement, D: Endpoints. (a) Blocking unauthorized communication with a firewall (b) Encrypting communication with a VPN (c) Installing antivirus software (d) Separating public-facing servers from the internal network using a DMZ", "lines": 1}],
  src="p.45 — Try 2")

# ---------------- homework ----------------
X(n=5, type="fill", prompt="Fill in ( a ) to ( d ).", promptAr="املا الفراغات من ( أ ) لـ ( د ).",
  passage="To protect an organization's network, it is important to combine multiple security measures. First, a ( a ) is installed at the entry/exit point of the network to block unauthorized communication based on rules. Web servers and other servers exposed to the outside are placed in a ( b ), separated from the internal network. To connect safely from outside, such as with remote work, communication is encrypted using a ( c ). The concept of layering multiple measures in this way is called ( d ).",
  src="p.47 — Exercise 2")
X(n=6, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "Choose the most appropriate reason for providing a DMZ. A: To improve communication speed. B: To expose all servers to the outside. C: To prevent damage to the internal network even if a public-facing server is attacked. D: To automatically detect and remove viruses.", "lines": 1},
             {"q": "Choose the one that most appropriately describes zero trust. A: Access from within the organization's network is safe, so verification is unnecessary. B: A firewall alone is sufficient to protect the network. C: No communication is trusted and is always verified. D: Only access from outside needs to be monitored.", "lines": 1}],
  src="p.47 — Exercise 3")
X(n=7, type="extended", prompt="Explain why layering several security measures (defense in depth) protects an organization better than relying on a firewall alone. Refer to what happens if one measure is breached.",
  promptAr="اشرح ليه تكديس إجراءات أمنية في طبقات (الدفاع في العمق) بيحمي المؤسسة أحسن من الاعتماد على جدار الحماية لوحده. استعن بـ: إيه اللي بيحصل لو إجراء واحد اتخرق.",
  marks=6, lines=8, src="p.45 — Exam-style question [6]")
X(n=8, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "What is meant by a VPN (virtual private network)? Give two of its main uses.", "lines": 3},
             {"q": "Why is placing a public web server in a DMZ safer than placing it directly inside the organization's internal network?", "lines": 3}],
  src="Ministry assessments, period 1 — home tasks; p.43 Pause & Think")
X(n=9, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Explain what is meant by a DMZ in network design, and how it protects the internal infrastructure.", "lines": 3},
             {"q": "Compare briefly traditional security and zero trust in how they treat users inside the network.", "lines": 3}],
  src="Ministry assessments, period 2 — performance tasks")
X(n=10, type="table", prompt="Give an example of the security measure for each layer of defense in depth.",
  promptAr="اذكر مثال للإجراء الأمني في كل طبقة من طبقات الدفاع في العمق.",
  head=["Layer", "Example of a measure"],
  rows=[["1 · Network entry", "____"], ["2 · Communication path", "____"], ["3 · Server placement", "____"], ["4 · Endpoints", "____"]],
  src="p.43 — Point 4(2); Ministry assessments, period 2 — home tasks")
X(n=11, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "What is the term for the traditional boundary that assumes inside the organization's network is completely safe and outside is not — a boundary blurred by cloud services and remote work? A: The DMZ B: The perimeter C: Edge computing D: Quantum superposition", "lines": 1},
             {"q": "Which layer of defense in depth is directly linked to installing antivirus software and updating the operating system? A: Network entry B: Communication path C: Server placement D: Endpoints", "lines": 1},
             {"q": "Which of these is the first layer (network entry) in defense in depth? A: Encrypting communication with a VPN B: Blocking unauthorized communication with a firewall C: Separating public-facing servers with a DMZ D: Installing antivirus software on endpoints", "lines": 1}],
  src="Ministry assessments, period 2 home tasks; form C")
X(n=12, type="extended", prompt="Explain the technical role of a firewall in monitoring network traffic, and give an example using the protection of databases.",
  promptAr="وضّح الدور التقني لجدار الحماية في مراقبة حركة مرور الشبكة، ومثّل على ده بحماية قواعد البيانات.",
  marks=4, lines=6, src="Ministry assessments, form A — essay 2")
X(n=13, type="extended", prompt="Explain the concept of a VPN, and show how it protects data sent over public Wi-Fi from eavesdropping.",
  promptAr="اذكر مفهوم الشبكة الافتراضية الخاصة (VPN)، وبيّن إزاي بتحمي البيانات اللي بتتنقل على Wi-Fi عام من التنصت.",
  marks=4, lines=6, src="Ministry assessments, form A — essay 3")
X(n=14, type="extended", prompt="Explain how zero trust verifies every access, based on identity, permissions and context.",
  promptAr="وضّح إزاي نهج انعدام الثقة بيتحقق من كل عملية وصول بناءً على الهوية والصلاحيات والسياق.",
  marks=4, lines=6, src="Ministry assessments, form B — essay 3; Arabic book p.40")
X(n=15, type="extended", prompt="Discuss why the traditional perimeter has become less effective in modern workplaces that rely on cloud computing and remote work.",
  promptAr="ناقش سبب تراجع فاعلية المحيط الأمني التقليدي في بيئات العمل الحديثة اللي بتعتمد على الحوسبة السحابية والشغل عن بُعد.",
  marks=4, lines=6, src="Ministry assessments, form B — essay 4; p.43 Point 5(2)")
X(n=16, type="extended", prompt="A hospital moves its patient records to a cloud service and lets doctors access them from home. Using zero trust and defense in depth, suggest two measures it should apply and say where each one helps, then identify one risk that could still remain.",
  promptAr="مستشفى بينقل سجلات المرضى لخدمة سحابية وبيسمح للدكاترة يفتحوها من البيت. باستخدام نهج انعدام الثقة والدفاع في العمق، اقترح إجراءين وبيّن كل واحد بيساعد فين، وحدد خطر واحد ممكن يفضل موجود.",
  marks=4, lines=6, src="p.46 — In a New Context")
X(n=17, type="extended", prompt="Think as an engineer. A company has a public website, staff who work from home, and confidential customer data. List its three assets with the main threat to each, say which defense-in-depth layer matters most for this company and why, and recommend a design with two reasons why layering is safer than a single firewall.",
  promptAr="فكّر كمهندس: شركة عندها موقع عام، وموظفين من البيت، وبيانات عملاء سرية. اذكر الأصول التلاتة والتهديد الرئيسي لكل واحد، وأنهي طبقة أهم للشركة دي وليه، وأوصِ بتصميم بسببين.",
  marks=4, lines=8, src="p.45-46 — Think as an Engineer")
X(n=18, type="extended", prompt="Explain how the firewall, the VPN, the DMZ and endpoint controls fit together to form one defense-in-depth strategy.",
  promptAr="اشرح إزاي جدار الحماية والـ VPN والمنطقة المعزولة وضوابط الأجهزة الطرفية بيتكاملوا مع بعض في استراتيجية دفاع في العمق واحدة.",
  marks=6, lines=8, src="Ministry assessments, form C — essay 2")
X(n=19, type="extended", prompt="Challenge: suggest one measure a small company could add beyond a firewall, and one threat it would still not remove.",
  promptAr="التحدي: اقترح إجراء واحد ممكن شركة صغيرة تضيفه جنب جدار الحماية، وتهديد واحد هيفضل مش متشال.",
  marks=2, lines=4, src="p.47 — Reflect & Challenge")
X(n=20, type="extended", prompt="Reflect: which layer of defense do you think is easiest for an attacker to get past, and why?",
  promptAr="تأمل: أنهي طبقة دفاعية في رأيك الأسهل على المهاجم إنه يعدّيها، وليه؟",
  marks=2, lines=4, src="p.47 — Reflect & Challenge")

A = {
 "1": ["✓ — a firewall controls communication by rules", "✓ — a VPN encrypts communication, reducing eavesdropping on public Wi-Fi",
       "✗ — a DMZ keeps public-facing servers apart from the internal network; it does not expose all servers", "✓ — correct definition of defense in depth"],
 "2": ["Encrypted virtual private line → B (VPN)", "Area for public-facing servers → C (DMZ)", "Allows or denies by rules → A (Firewall)"],
 "3": ["1. Firewall", "2. VPN", "3. DMZ", "4. Defense in depth"],
 "4": ["(1) C — deleting infected files is antivirus software, not a VPN", "(2) a A, b B, c D, d C"],
 "5": {"a": "firewall", "b": "DMZ", "c": "VPN", "d": "defense in depth"},
 "6": ["(1) C", "(2) C — no communication is trusted, and it is always verified"],
 "7": {"marks": 6,
       "model": "A firewall alone is a single barrier: if it is breached, nothing else stands between the attacker and everything inside the network. Defense in depth layers several measures, each at a different point: a firewall at the network entry, a VPN on the communication path, a DMZ for server placement, and antivirus and updates on the endpoints. If one measure is breached, the next can still protect the system — for example, an attacker who gets into a public web server in the DMZ still cannot reach the internal database. So a single failure is far less likely to expose the whole network.",
       "points": ["A firewall alone is one barrier (1)", "If that one barrier is breached, everything inside is exposed (1)",
                  "Defense in depth layers several measures (1)", "Names at least two layers or measures, e.g. VPN, DMZ, endpoints (1)",
                  "If one is breached, the next still protects the system (1)", "Conclusion: one breach is much less likely to expose the whole network (1)"]},
 "8": ["1. A VPN creates an encrypted virtual private line (a tunnel) over the Internet for safe connection from a remote location. Uses: remote work (connecting from home or while away) and connecting branches (offices in different places).",
       "2. In a DMZ, the public server is separated from the internal network, so if it is attacked the attacker cannot go on to the internal network and its confidential data. Inside the internal network, a hacked public server would give a way straight in."],
 "9": ["1. A DMZ is an area where servers exposed to the external network (web, mail) are placed separately from the internal network. If one of those servers is attacked, the damage does not reach the internal network.",
       "2. Traditional security trusts users inside the perimeter and checks only at the boundary. Zero trust trusts no one automatically — even inside the network, identity and permissions are verified every time."],
 "10": ["1 · Network entry — block unauthorized communication with a firewall", "2 · Communication path — encrypt communication with a VPN",
        "3 · Server placement — separate public-facing servers with a DMZ", "4 · Endpoints — install antivirus software and keep the OS updated"],
 "11": ["(1) B — the perimeter", "(2) D — endpoints", "(3) B — the firewall at the network entry"],
 "12": {"marks": 4,
        "model": "A firewall monitors the traffic at the entry/exit point of a network (it can also sit between parts of a network or on a host) and allows or denies each communication according to rules set in advance. For example, it can allow outside users to reach the public web server but deny any direct access from outside to the database server, so the database is never exposed to the Internet.",
        "points": ["Sits at the network's entry/exit point (or between parts / on a host) (1)", "Allows or denies communication (1)", "According to rules set in advance (1)", "Database example: allow the web server, deny direct external access to the database (1)"]},
 "13": {"marks": 4,
        "model": "A VPN is an encrypted virtual private line, or tunnel, created over a public network such as the Internet, so that a remote user can connect safely to an organization's network. On public Wi-Fi other people can try to read the traffic, but with a VPN the content is encrypted inside the tunnel, so an eavesdropper sees only scrambled data. The risk of eavesdropping is therefore reduced.",
        "points": ["Encrypted virtual private line / tunnel over the Internet (1)", "Lets a remote user connect safely (1)", "The content is encrypted (1)", "So an eavesdropper on public Wi-Fi cannot read it (1)"]},
 "14": {"marks": 4,
        "model": "Zero trust does not trust any user or device automatically just because it is inside the network or belongs to the organization. Every time a resource is requested, it checks identity (who is asking), permissions (whether they are allowed this resource) and context (whether the request fits — the device, the place, the time), according to the organization's policy. Only then is access given, and the check is repeated for each access.",
        "points": ["No automatic trust from being inside the network (1)", "Identity is checked (1)", "Permissions are checked (1)", "Context is checked, every time access is requested (1)"]},
 "15": {"marks": 4,
        "model": "Traditional security protected a perimeter, on the idea that inside the organization's network is safe and outside is dangerous. With cloud services, data and systems sit outside the office network; with remote work, staff connect from home and from public places. The line between inside and outside has therefore blurred, so a design that protects only the perimeter leaves gaps — which is why zero trust verifies every access instead.",
        "points": ["The perimeter idea: inside safe, outside dangerous (1)", "Cloud services put data and systems outside the network (1)", "Remote work puts users outside the network (1)", "So the boundary blurs and perimeter-only protection is not enough (1)"]},
 "16": {"marks": 4, "open": True,
        "points": ["A zero-trust measure, with where it helps (e.g. verify each doctor's identity and permissions every time they open records) (1)",
                   "A defense-in-depth measure, with where it helps (e.g. a VPN for doctors at home; updated devices) (1)", "Each placed correctly (1)",
                   "One risk that could remain, with a reason (e.g. a doctor's own device is infected; a stolen password) (1)"]},
 "17": {"marks": 4, "open": True,
        "points": ["Three assets with a threat each (website attacked; remote staff eavesdropped; database leaked) (1)",
                   "A top layer chosen for this company, with a reason (1)", "A layered design recommended (1)", "Two reasons why layering is safer than one firewall (1)"]},
 "18": {"marks": 6,
        "model": "Each measure guards a different point. The firewall, at the network entry, allows or denies communication by rules. The VPN protects the communication path by encrypting remote connections. The DMZ governs server placement, keeping public-facing servers apart so an attack on them cannot reach the internal network. Endpoint controls — antivirus and an updated OS — protect each device. Because they are at different points, an attacker who gets past one still faces the next, which is what defense in depth means.",
        "points": ["Firewall — network entry, allows/denies by rules (1)", "VPN — communication path, encrypts remote connections (1)", "DMZ — server placement, keeps public servers apart (1)",
                   "Endpoints — antivirus and OS updates on each device (1)", "Each guards a different point (1)", "So breaching one still leaves the next — defense in depth (1)"]},
 "19": {"marks": 2, "open": True, "points": ["One fitting measure beyond the firewall (VPN, DMZ, antivirus/updates, MFA) (1)", "One threat it would still not remove, with a reason (1)"]},
 "20": {"marks": 2, "open": True, "points": ["One layer named (1)", "A reason why it is easiest to get past (1)"]},
}

MODEL = {
 "1": [m("A. Firewall by rules", "✓ True — a firewall controls communication based on rules set in advance.", "صح."),
       m("B. VPN on public Wi-Fi", "✓ True — a VPN encrypts the communication, so eavesdropping is reduced even on public Wi-Fi.", "صح: البيانات متشفرة جوه النفق."),
       m("C. A DMZ exposes all servers", "✗ False — a DMZ keeps the public-facing servers separate from the internal network; it does not expose all servers.", "غلط: الـ DMZ بتعزل الخوادم العامة، مش بتعرّض الكل."),
       m("D. Defense in depth", "✓ True — that is its definition.", "صح.")],
 "2": [m("Encrypted virtual private line", "B — VPN.", "الخط المشفر = VPN."), m("Area for servers exposed to the outside", "C — DMZ.", "المنطقة المعزولة."),
       m("Allows or denies by rules", "A — Firewall.", "جدار الحماية.")],
 "3": [m("1.", "Firewall.", ""), m("2.", "VPN.", ""), m("3.", "DMZ.", ""), m("4.", "Defense in depth.", "تكديس الإجراءات = الدفاع في العمق.")],
 "4": [m("(1) NOT a use of a VPN", "C — automatically deleting infected files is the job of antivirus software on the endpoints, not a VPN.", "الـ VPN بتشفر الاتصال، مش بتمسح فيروسات."),
       m("(2) Which layer?", "a A (network entry) · b B (communication path) · c D (endpoints) · d C (server placement).", "جدار ← مدخل، VPN ← مسار، مكافحة فيروسات ← أجهزة طرفية، DMZ ← وضع الخوادم.")],
 "5": [m("( a )", "firewall", "عند مدخل الشبكة."), m("( b )", "DMZ", "للخوادم العامة."), m("( c )", "VPN", "للاتصال الآمن من برّه."), m("( d )", "defense in depth", "تكديس الإجراءات.")],
 "6": [m("(1) Why a DMZ?", "C — to prevent damage to the internal network even if a public-facing server is attacked.", "الهدف حماية الشبكة الداخلية، مش السرعة."),
       m("(2) Zero trust", "C — no communication is trusted, and every one is always verified.", "مفيش ثقة تلقائية، حتى من جوه.")],
 "7": [m(None, A["7"]["model"], "حاجز واحد لو اتخرق كل حاجة بتتكشف، لكن الطبقات: لو واحدة وقعت، اللي بعدها لسه بتحمي.")],
 "8": [m("1. What a VPN is, and two uses", A["8"][0][3:], "خط مشفر عبر الإنترنت — للشغل من البيت ولربط الفروع."),
       m("2. Why a DMZ is safer", A["8"][1][3:], "لو الخادم العام اتخرق، المهاجم ميقدرش يكمل للشبكة الداخلية.")],
 "9": [m("1. What a DMZ is and how it protects", A["9"][0][3:], "عزل الخوادم العامة بيحمي اللي جوه."),
       m("2. Traditional compared with zero trust", A["9"][1][3:], "التقليدي بيثق في اللي جوه، وانعدام الثقة بيتحقق من الكل كل مرة.")],
 "10": [m("1 · Network entry", "Block unauthorized communication with a firewall.", ""), m("2 · Communication path", "Encrypt communication with a VPN.", ""),
        m("3 · Server placement", "Separate public-facing servers from the internal network with a DMZ.", ""),
        m("4 · Endpoints", "Install antivirus software and keep the operating system updated.", "طبقة لكل مكان: المدخل، المسار، الخوادم، الأجهزة.")],
 "11": [m("1.", "B — the perimeter.", "المحيط الأمني."), m("2.", "D — endpoints.", "الأجهزة الطرفية."), m("3.", "B — blocking unauthorized communication with a firewall.", "أول طبقة = مدخل الشبكة.")],
 "12": [m(None, A["12"]["model"], "جدار الحماية بيقرر: يسمح ولا يمنع، حسب قواعد — ويمنع أي حد من برّه يوصل لقاعدة البيانات مباشرة.")],
 "13": [m(None, A["13"]["model"], "النفق المشفر بيخلي اللي بيتصنت يشوف بيانات متلخبطة بس.")],
 "14": [m(None, A["14"]["model"], "الهوية، والصلاحيات، والسياق — كل مرة.")],
 "15": [m(None, A["15"]["model"], "السحابة والشغل من البيت مسحوا الحد بين الداخل والخارج.")],
 "16": [m(None, "One possible answer. Measure 1 (zero trust): every time a doctor opens a record, their identity and permissions are verified — so being logged in once is not enough. Measure 2 (defense in depth): doctors connect from home through a VPN, so the records cannot be read on the way, and their devices have antivirus and updates. One risk that could remain: a doctor's password could be stolen, or their home computer infected — no design is absolute.",
          "مثال لإجابة: إجراء لكل مفهوم، ومكانه، وخطر لسه موجود.")],
 "17": [m(None, "One possible answer. Assets and threats: the public website could be attacked; remote staff could be eavesdropped on; the customer database could be leaked. Most important layer: server placement — putting the website in a DMZ, because it is the most exposed asset and an attack on it must not reach the database. Design: a firewall, a VPN for remote staff, a DMZ for the website, and antivirus and updates on every device, with zero trust checking each access. Two reasons: if one layer is breached the next still protects the system; and each layer covers a different threat that a firewall alone does not.",
          "مثال لإجابة: الأصول والتهديدات، والطبقة الأهم بسبب، وتصميم بسببين.")],
 "18": [m(None, A["18"]["model"], "كل إجراء بيحمي نقطة مختلفة — ولو واحد اتعدّى، اللي بعده لسه موجود.")],
 "19": [m(None, "One possible answer. Extra measure: a VPN for staff who work from home, so their communication is encrypted. A threat it would still not remove: a member of staff tricked into giving away their password — the VPN protects the connection, not the password.",
          "أي إجراء مناسب، مع تهديد فعلًا هيفضل موجود.")],
 "20": [m(None, "One possible answer. The endpoints, because they depend on every user: one person who skips an update or opens an infected file can let an attacker in, however strong the other layers are.",
          "أي طبقة، مع سبب مقنع.")],
}
DATA = {"SHEET": {"lecture": 6, "title": "What if one wall falls?", "parts": [{"exercises": E}]}, "ANSWERS": A, "MODEL": MODEL}
assert [x["n"] for x in E] == list(range(1, 21)) and set(A) == set(MODEL) == {str(x["n"]) for x in E}
io.open("lecture6/_teacher/exercises.json", "w", encoding="utf-8", newline="\n").write(json.dumps(DATA, ensure_ascii=False, indent=1) + "\n")
print("exercises:", len(E))
