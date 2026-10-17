# -*- coding: utf-8 -*-
import io, json
E = []
def X(**k): E.append(k)
def m(q, en, ar): return {"q": q, "a": en, "ar": ar}

# ---------------- class work ----------------
X(n=1, type="truefalse", prompt="Write ✓ if the statement is true, ✗ if it is false.",
  promptAr="حط ✓ لو الجملة صح، و ✗ لو غلط.",
  statements=["A security incident is a situation in which actual damage occurs due to an information security problem.",
              "In incident response, it is important first to prevent the spread of damage before removing the cause.",
              "The size of a risk can be determined by impact alone.",
              "The final stage of incident response is prevention of recurrence."],
  src="p.50-51 — Worked Example (1) A-D")
X(n=2, type="category", prompt="Write the stage each action belongs to — A: Preparation, B: Containment, C: Eradication, D: Prevention of recurrence.",
  promptAr="اكتب كل إجراء تابع لأنهي مرحلة.",
  items=["Establishing response procedures in advance, in preparation for incidents.",
         "Disconnecting a malware-infected computer from the network.",
         "Removing the malware infection.",
         "Analyzing the cause and taking measures so that the same incident does not occur again."],
  src="p.51 — Worked Example (2)")
X(n=3, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "What is the term for a situation in which actual damage occurs due to an information security problem?", "lines": 1},
             {"q": "Name the six stages of incident response in order.", "lines": 2},
             {"q": "What are the two factors used to determine the size of a risk?", "lines": 1}],
  src="p.52 — Try 1")
X(n=4, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "Choose the one that is NOT an appropriate example of a security incident. A: Data was encrypted by a ransomware infection. B: Customer information was leaked to the outside through unauthorized access. C: A software update was performed to add new features. D: A web service became unavailable due to an attack on the server.", "lines": 1},
             {"q": "Choose the one that most appropriately describes risk assessment. A: It is enough to address only risks with large impact. B: It is enough to address only risks with high likelihood. C: Risks with both high impact and high likelihood should be addressed first. D: All risks must be addressed simultaneously.", "lines": 1}],
  src="p.52 — Try 2")

# ---------------- homework ----------------
X(n=5, type="fill", prompt="Fill in ( a ) to ( e ).", promptAr="املا الفراغات من ( أ ) لـ ( هـ ).",
  passage="A situation in which actual damage occurs due to an information security problem is called ( a ). When ( a ) occurs, ( b ), which prevents the spread of damage, is performed first, followed by ( c ), which removes the cause of the incident. After that, ( d ), which returns the system to its normal state, is performed, and finally ( e ), in which the cause is analyzed to prevent recurrence, is performed.",
  src="p.53-54 — Exercise 2")
X(n=6, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Reorder the risks from highest priority to lowest, using impact × likelihood. a: Impact large (3), Likelihood high (3) b: Impact small (1), Likelihood high (3) c: Impact large (3), Likelihood medium (2) d: Impact small (1), Likelihood low (1)", "lines": 2},
             {"q": "Choose the one that describes the order of incident response. A: Detection → Eradication → Containment → Recovery B: Preparation → Detection → Containment → Eradication → Recovery → Prevention of recurrence C: Detection → Recovery → Containment → Prevention of recurrence D: Containment → Detection → Eradication → Preparation", "lines": 1}],
  src="p.54 — Exercise 3")
X(n=7, type="extended", prompt="Explain why the six stages of incident response must be carried out in order, using recovery and eradication as an example. Refer to what happens if the cause is not removed.",
  promptAr="اشرح ليه المراحل الست للاستجابة للحوادث لازم تتنفذ بالترتيب، مستخدمًا الاستعادة والاستئصال كمثال. استعن بـ: إيه اللي بيحصل لو السبب متشالش.",
  marks=6, lines=8, src="p.51 — Exam-style question [6]")
X(n=8, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "What is meant by a security incident, and what are its typical examples?", "lines": 3},
             {"q": "Name the six stages of incident response, and give the main purpose of the preparation and detection stages.", "lines": 3}],
  src="Ministry assessments, period 1 — performance tasks")
X(n=9, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Explain the purpose of the containment and eradication stages.", "lines": 3},
             {"q": "How is the size of a risk estimated in the lesson's simple model? Give the formula and its two factors.", "lines": 2}],
  src="Ministry assessments, period 1 — home tasks")
X(n=10, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Explain what is meant by the recovery stage and the lessons-learned-and-improvement stage.", "lines": 3},
             {"q": "Why must containment be carried out before eradication? What could happen if the order were reversed?", "lines": 3}],
  src="Ministry assessments, period 2 — performance tasks")
X(n=11, type="short", prompt="Answer the following questions.", promptAr="جاوب على الأسئلة دي.",
  questions=[{"q": "Explain how risks are handled with the risk evaluation matrix, and which category has the highest priority.", "lines": 3},
             {"q": "Give an example of the overlap or repetition that can happen between the stages of incident response in practice.", "lines": 2}],
  src="Ministry assessments, period 2 — home tasks; Arabic book p.46")
X(n=12, type="short", prompt="Choose the correct option.", promptAr="اختار الإجابة الصح.",
  questions=[{"q": "Which is a typical example of a security incident that affects the availability of a service? A: Personal information leaked to the outside B: Data altered without authorization C: A service outage caused by attacks on the server D: Establishing response procedures in advance", "lines": 1},
             {"q": "What is the term for isolating the affected part, or limiting its effect, to stop the problem spreading? A: Preparation B: Detection C: Containment D: Recovery", "lines": 1},
             {"q": "In the risk evaluation matrix, how are risks with high impact and low likelihood usually classed? A: Very high B: Medium C: Very low D: None", "lines": 1}],
  src="Ministry assessments, period 1 and form C")
X(n=13, type="table", prompt="Describe the three types of security incident given in the lesson.",
  promptAr="اوصف أنواع الحوادث الأمنية التلاتة اللي في الدرس.",
  head=["Type", "Description"],
  rows=[["Information leak", "____"], ["Data tampering", "____"], ["Service outage", "____"]],
  src="p.49 — Point 1(2); Ministry assessments, form B — essay 4")
X(n=14, type="extended", prompt="Why must containment come before eradication in the six-stage response?",
  promptAr="ليه الاحتواء لازم ييجي قبل الاستئصال في الاستجابة ذات المراحل الست؟",
  marks=3, lines=5, src="p.50 — Pause & Think")
X(n=15, type="extended", prompt="Discuss the importance of the lessons-learned-and-improvement stage, and how it helps prevent security incidents from happening again.",
  promptAr="اتكلم عن أهمية مرحلة الدروس المستفادة والتحسين، وإزاي بتساعد تمنع تكرار الحوادث الأمنية.",
  marks=4, lines=6, src="Ministry assessments, form B — essay 3")
X(n=16, type="extended", prompt="Explain how the recovery stage and the lessons-learned-and-improvement stage are carried out when dealing with a ransomware attack.",
  promptAr="اشرح إزاي مرحلتي الاستعادة والدروس المستفادة والتحسين بيتنفذوا لما نتعامل مع هجوم ببرمجية فدية.",
  marks=4, lines=6, src="Ministry assessments, form C — essay 1")
X(n=17, type="extended", prompt="An online shop has just detected that customer data has been leaked. Using the six-stage response and risk assessment, name the next two stages it should carry out and why, and identify one risk it should prioritize afterward.",
  promptAr="متجر إلكتروني لسه مكتشف إن بيانات العملاء اتسربت. باستخدام المراحل الست وتقييم المخاطر، حدد المرحلتين الجايين وليه، وحدد خطر واحد لازم ياخد الأولوية بعد كده.",
  marks=4, lines=6, src="p.53 — In a New Context")
X(n=18, type="extended", prompt="Think as an engineer. A school's student-records system is hit by ransomware: files are encrypted and staff cannot log in, and the incident has just been detected. List the stages still to carry out and what each means here; compare two risks, (i) another ransomware attack and (ii) a brief power cut, by impact and likelihood; and recommend the first three actions, with one reason why order matters.",
  promptAr="فكّر كمهندس: نظام سجلات الطلاب اتهاجم ببرمجية فدية، والحادث لسه اتكشف. اذكر المراحل اللي لسه هتتنفذ ومعنى كل واحدة هنا، وقارن مخاطرتين بالتأثير والاحتمالية، وأوصِ بأول تلات إجراءات بسبب واحد لأهمية الترتيب.",
  marks=4, lines=8, src="p.52 — Think as an Engineer")
X(n=19, type="extended", prompt="Reflect: which stage of incident response do you think is hardest to do well under pressure, and why?",
  promptAr="تأمل: أنهي مرحلة في الاستجابة للحوادث في رأيك الأصعب تتنفذ كويس تحت الضغط، وليه؟",
  marks=2, lines=4, src="p.53 — Reflect & Challenge")
X(n=20, type="extended", prompt="Challenge: suggest one thing an organization could prepare in advance (stage 1) that would make the other stages faster.",
  promptAr="التحدي: اقترح حاجة واحدة ممكن مؤسسة تجهزها مسبقًا (المرحلة 1) تخلي باقي المراحل أسرع.",
  marks=2, lines=4, src="p.53 — Reflect & Challenge")

SIX = "Preparation, detection, containment, eradication, recovery, prevention of recurrence (lessons learned and improvement)."
A = {
 "1": ["✓ — correct definition of a security incident", "✓ — containment comes before eradication",
       "✗ — the size of a risk is determined by both impact and likelihood", "✓ — the final stage is prevention of recurrence"],
 "2": ["a A — preparation", "b B — containment", "c C — eradication", "d D — prevention of recurrence"],
 "3": ["1. A security incident", "2. " + SIX, "3. Impact and likelihood"],
 "4": ["(1) C — a software update to add features damages nothing", "(2) C"],
 "5": {"a": "a security incident", "b": "containment", "c": "eradication", "d": "recovery", "e": "prevention of recurrence (lessons learned and improvement)"},
 "6": ["(1) a (9) → c (6) → b (3) → d (1)", "(2) B"],
 "7": {"marks": 6,
       "model": "Each stage depends on the one before it. Containment comes first, to stop the damage spreading; eradication then removes the cause, such as the malware; only then does recovery return the systems to normal. If recovery is done before eradication, the systems are restored while the cause is still there — the malware or the weakness it used — so the same incident can happen again, and the work has to be repeated. Following the order keeps the damage small and stops the incident returning. In practice some stages can overlap: recovery may reveal traces of the threat, and the team goes back to containment or eradication.",
       "points": ["Containment first stops the damage spreading (1)", "Eradication removes the cause, e.g. the malware (1)", "Recovery returns systems to normal only after that (1)",
                  "If recovery comes before eradication, the cause is still there (1)", "So the same incident can happen again (1)", "Conclusion: order keeps damage small / may need to step back (1)"]},
 "8": ["1. A situation in which actual damage occurs due to an information security problem (the Arabic book: an event that affects the confidentiality, integrity or availability of information, or violates a security policy). Examples: an information leak, data tampering, a service outage.",
       "2. " + SIX + " Preparation sets up procedures and structures in advance, so the team is ready; detection discovers and confirms that an incident has happened."],
 "9": ["1. Containment limits the scope of the impact so the damage does not spread further (e.g. disconnecting an infected computer). Eradication removes the cause of the incident (e.g. removing the malware).",
       "2. Risk size = impact × likelihood. Impact: how much damage if the risk happens. Likelihood: how probable it is that it happens."],
 "10": ["1. Recovery returns systems and services to a safe, normal state, which may include restoring from a clean backup. Lessons learned and improvement analyzes what happened, documents the lessons and improves the controls, so the incident is less likely to happen again.",
        "2. Containment stops the damage spreading while the cause is still active. If eradication came first, the damage could keep spreading during it, to more machines or data — and the response would have to chase it."],
 "11": ["1. Each risk is given an impact score and a likelihood score, and its size is impact × likelihood. Risks with both high impact and high likelihood are the highest priority and are addressed first; the others are ranked by their scores.",
        "2. e.g. During recovery, traces of the threat are found, so the team goes back to containment or eradication before finishing recovery."],
 "12": ["(1) C — a service outage", "(2) C — containment", "(3) B — medium"],
 "13": ["Information leak — personal or confidential information is leaked to the outside", "Data tampering — data within a system is altered without authorization",
        "Service outage — a service becomes unavailable due to attacks on the server, etc."],
 "14": {"marks": 3,
        "model": "Containment limits the spread of the damage. While the cause is being removed, it could keep spreading — for example, malware moving to other computers on the network. So the infected part is isolated first, and then the cause is removed safely.",
        "points": ["Containment stops the damage spreading (1)", "During eradication the threat could otherwise keep spreading (1)", "So isolate first, then remove the cause (1)"]},
 "15": {"marks": 4,
        "model": "Lessons learned and improvement is the last stage. The team analyzes what happened and how the attacker got in, documents the lessons, and improves the controls — for example patching the weakness, adding a protection, or changing a procedure. Without it, the same weakness stays and the same incident can return. With it, the incident becomes less likely to happen again, and its effect smaller if it does.",
        "points": ["Analyze what happened / the cause (1)", "Document the lessons (1)", "Improve the controls (1)", "So the same incident is less likely to happen again (1)"]},
 "16": {"marks": 4,
        "model": "Recovery: once the ransomware has been removed, the encrypted systems are restored to a safe, normal state from a clean backup, and checked before they are used again. Lessons learned and improvement: the team finds how the ransomware got in, documents it, and improves the controls — for example updating the software it exploited, training staff, and keeping regular backups — so it does not happen again.",
        "points": ["Recovery comes after the ransomware is removed (1)", "Restore from a clean backup to a normal, safe state (1)", "Lessons learned: find how it got in and document it (1)", "Improve the controls so it does not happen again (1)"]},
 "17": {"marks": 4, "open": True,
        "points": ["Next stage: containment, with a reason (stop more data leaking) (1)", "Then eradication, with a reason (remove the cause of the leak) (1)",
                   "One risk to prioritize afterward (1)", "Justified by impact × likelihood (1)"]},
 "18": {"marks": 4, "open": True,
        "points": ["Stages still to do from detection: containment, eradication, recovery, prevention of recurrence (1)", "What each means for this incident (1)",
                   "Risk comparison: ransomware higher impact (and likelihood) than a brief power cut, so first (1)", "First three actions in order, with a reason why order matters (1)"]},
 "19": {"marks": 2, "open": True, "points": ["One stage named (1)", "A reason why it is hard under pressure (1)"]},
 "20": {"marks": 2, "open": True, "points": ["One thing prepared in advance (1)", "How it makes another stage faster (1)"]},
}

MODEL = {
 "1": [m("A. Definition of a security incident", "✓ True.", "صح."),
       m("B. Prevent the spread before removing the cause", "✓ True — containment comes before eradication.", "صح: الاحتواء قبل الاستئصال."),
       m("C. Risk size by impact alone", "✗ False — the size of a risk is determined by both impact and likelihood.", "غلط: التأثير × الاحتمالية."),
       m("D. The final stage", "✓ True — prevention of recurrence (lessons learned and improvement) is the last stage.", "صح.")],
 "2": [m("a. Procedures in advance", "A — Preparation.", "التحضير."), m("b. Disconnecting the infected computer", "B — Containment.", "الاحتواء: نمنع الانتشار."),
       m("c. Removing the malware", "C — Eradication.", "الاستئصال: نشيل السبب."), m("d. Analyzing the cause", "D — Prevention of recurrence.", "الدروس المستفادة والتحسين.")],
 "3": [m("1.", "A security incident.", ""), m("2.", SIX, "تحضير ← اكتشاف ← احتواء ← استئصال ← استعادة ← الدروس المستفادة والتحسين."),
       m("3.", "Impact and likelihood.", "التأثير والاحتمالية.")],
 "4": [m("(1) NOT an incident", "C — a software update to add new features damages nothing, so it is not a security incident.", "مفيش ضرر، فمش حادث."),
       m("(2) Risk assessment", "C — risks with both high impact and high likelihood are addressed first.", "الاتنين عاليين = الأول.")],
 "5": [m("( a )", "a security incident", ""), m("( b )", "containment", "الاحتواء الأول."), m("( c )", "eradication", "بعدين الاستئصال."),
       m("( d )", "recovery", "بعدين الاستعادة."), m("( e )", "prevention of recurrence (lessons learned and improvement)", "وفي الآخر الدروس المستفادة.")],
 "6": [m("(1) Order of the risks", "a (3 × 3 = 9) → c (3 × 2 = 6) → b (1 × 3 = 3) → d (1 × 1 = 1).", "اضرب، ورتّب من الأكبر."),
       m("(2) Order of incident response", "B — preparation → detection → containment → eradication → recovery → prevention of recurrence.", "الاحتواء قبل الاستئصال.")],
 "7": [m(None, A["7"]["model"], "لو رجّعنا النظام قبل ما نشيل السبب، البرمجية لسه موجودة والحادث ممكن يتكرر.")],
 "8": [m("1. Security incident and examples", A["8"][0][3:], "حادث فيه ضرر فعلي — تسرب، تلاعب، انقطاع خدمة."),
       m("2. The six stages; preparation and detection", A["8"][1][3:], "التحضير عشان نبقى جاهزين، والاكتشاف عشان نتأكد إن فيه حادث.")],
 "9": [m("1. Containment and eradication", A["9"][0][3:], "الاحتواء يوقف الانتشار، والاستئصال يشيل السبب."),
       m("2. How risk size is estimated", A["9"][1][3:], "درجة الخطر = التأثير × الاحتمالية.")],
 "10": [m("1. Recovery; lessons learned and improvement", A["10"][0][3:], "الاستعادة ترجّع النظام، والدروس المستفادة تمنع التكرار."),
        m("2. Why containment before eradication", A["10"][1][3:], "لو عكسنا، الضرر هيفضل ينتشر.")],
 "11": [m("1. The risk evaluation matrix", A["11"][0][3:], "التأثير العالي والاحتمالية العالية أعلى أولوية."),
        m("2. Overlap in practice", A["11"][1][3:], "الاستعادة ممكن تكشف بقايا، فنرجع للاحتواء.")],
 "12": [m("1.", "C — a service outage caused by attacks on the server.", "التوافر = الخدمة متاحة."), m("2.", "C — containment.", ""),
        m("3.", "B — medium (3 × 1 = 3).", "تأثير عالي واحتمالية منخفضة = متوسطة.")],
 "13": [m("Information leak", "Personal or confidential information is leaked to the outside.", ""),
        m("Data tampering", "Data within a system is altered without authorization.", ""),
        m("Service outage", "A service becomes unavailable because of attacks on the server, etc.", "تسرب، وتلاعب، وانقطاع خدمة.")],
 "14": [m(None, A["14"]["model"], "اعزل الأول، وبعدين شيل السبب بأمان.")],
 "15": [m(None, A["15"]["model"], "من غير المرحلة دي، نفس الثغرة بتفضل والحادث يتكرر.")],
 "16": [m(None, A["16"]["model"], "استعادة من نسخة احتياطية سليمة، وبعدين نعرف دخلت إزاي ونحسّن الحماية.")],
 "17": [m(None, "One possible answer. Next stage: containment — cut off the route the data is leaking through, so no more customer data leaves. Then eradication — remove the cause, for example close the weakness the attacker used or remove the malware. Afterward, one risk to prioritize: customers' leaked passwords being used to log in to their accounts — high impact and, now that the data is out, high likelihood — so it comes first.",
          "مثال لإجابة: الاحتواء ثم الاستئصال بالأسباب، وخطر واحد بالتأثير × الاحتمالية.")],
 "18": [m(None, "One possible answer. Still to do: containment (disconnect the infected computers so the ransomware cannot spread), eradication (remove the ransomware and close the weakness it used), recovery (restore the records from a clean backup), and prevention of recurrence (find how it got in, document it, improve the controls). Risks: another ransomware attack has large impact and, until the weakness is fixed, high likelihood; a brief power cut has smaller impact. So ransomware comes first. First three actions: isolate the infected computers, remove the ransomware, then restore from the backup — because restoring before the cause is removed would let the ransomware encrypt the files again.",
          "مثال لإجابة: المراحل الباقية، ومقارنة المخاطر، وأول تلات إجراءات بالسبب.")],
 "19": [m(None, "One possible answer. Containment, because it has to be decided fast while the damage is still spreading, and disconnecting systems also stops people working — under pressure it is tempting to skip it and go straight to recovery.",
          "أي مرحلة، بسبب مقنع.")],
 "20": [m(None, "One possible answer. A written response plan that says who does what and how to isolate each system, with regular, tested backups — then containment and recovery can start at once instead of being worked out during the incident.",
          "أي حاجة مسبقة، مع إزاي بتسرّع مرحلة تانية.")],
}
DATA = {"SHEET": {"lecture": 7, "title": "When something goes wrong", "parts": [{"exercises": E}]}, "ANSWERS": A, "MODEL": MODEL}
assert [x["n"] for x in E] == list(range(1, 21)) and set(A) == set(MODEL) == {str(x["n"]) for x in E}
io.open("lecture7/_teacher/exercises.json", "w", encoding="utf-8", newline="\n").write(json.dumps(DATA, ensure_ascii=False, indent=1) + "\n")
print("exercises:", len(E))
