# -*- coding: utf-8 -*-
"""Chapter 2 (Unit 2) revision: what each lesson must leave behind.

One record per lesson, read by the deck (slides.py), the booklet
(booklet.py) and the flashcards. The "remember" line is the book's own Key
takeaway; the terms are the book's Key Terms and Point definitions; the
traps are statements the book, the quizzes or the ministry's assessment
book mark false (or true); the exam question is the lesson's own
exam-style question, with the marking points written when that lecture
was made (lectures 5-7).
"""

LESSONS = [
    {
        "id": "2-1", "lecture": 5,
        "title": "Cryptographic Technologies and Authentication",
        "remember": "HTTPS uses public-key cryptography to share a key safely and common-key cryptography to move data quickly. Services stay safe by layering encryption, certificates, signatures, and multi-factor authentication.",
        "remember_ar": "HTTPS بيستخدم تشفير المفتاح العام عشان يشارك المفتاح بأمان، وتشفير المفتاح المشترك عشان ينقل البيانات بسرعة. والخدمات بتفضل آمنة بالتشفير والشهادات والتوقيعات والمصادقة متعددة العوامل مع بعض.",
        "svg": "KEYS",
        "terms": [
            ("Common-key cryptography", "the same key locks and unlocks; fast, so it exchanges the data", "تشفير المفتاح المشترك: مفتاح واحد للقفل والفتح، وسريع"),
            ("Public-key cryptography", "a public key locks, only the private key unlocks; slow, so it shares the key safely", "تشفير المفتاح العام: العام بيقفل والخاص بس بيفتح"),
            ("HTTPS", "HTTP with SSL/TLS encryption; uses both kinds of cryptography", "HTTPS: HTTP مع تشفير TLS"),
            ("Encryption", "keeps communication content from being read by third parties", "التشفير: محدش يقرا المحتوى"),
            ("Digital signature", "detects tampering and impersonation, and gives non-repudiation", "التوقيع الرقمي: يكشف التلاعب وانتحال الشخصية"),
            ("Non-repudiation", "the sender cannot deny afterward having sent the data", "عدم الإنكار: المرسِل ميقدرش ينكر"),
            ("Digital certificate", "verifies that the communication partner (the site) is genuine", "الشهادة الرقمية: الموقع حقيقي"),
            ("Multi-factor authentication", "combining two or more of the three factors: knowledge, possession, biometric", "المصادقة متعددة العوامل: عاملين أو أكتر من التلاتة"),
        ],
        "traps": [
            ("HTTPS exchanges all of its data using public-key cryptography.", False, "Public-key only shares the key; common-key moves the data."),
            ("Setting two passwords is multi-factor authentication.", False, "Both are knowledge: one factor twice."),
            ("A digital certificate verifies that the communication partner is genuine.", True, "That is its job."),
            ("A digital signature keeps the content from being read by third parties.", False, "That is encryption; a signature detects tampering."),
        ],
        "exam": {"from": (5, "12"), "q": "Explain why HTTPS uses public-key cryptography to share the key and common-key cryptography to exchange the data.", "marks": 6, "src": "p.37 — Exam-style question [6]"},
    },
    {
        "id": "2-2", "lecture": 6,
        "title": "Network Security Design",
        "remember": "Layer your defenses — firewall, VPN, DMZ, endpoints — and verify every access (zero trust). One breach is then far less likely to expose the whole network.",
        "remember_ar": "اعمل حمايتك طبقات — جدار حماية، VPN، منطقة معزولة، والأجهزة الطرفية — واتحقق من كل وصول (انعدام الثقة). كده اختراق واحد صعب يكشف الشبكة كلها.",
        "svg": "LAYERS",
        "terms": [
            ("Firewall", "allows or denies communication at a network's entry/exit point, based on rules set in advance", "جدار الحماية: يسمح أو يمنع حسب قواعد"),
            ("VPN", "an encrypted virtual private line over the Internet; for remote work and connecting offices", "الشبكة الافتراضية الخاصة: خط خاص متشفر"),
            ("DMZ", "a zone for public-facing servers, separated from the internal network", "المنطقة المعزولة: سيرفرات الجمهور بعيد عن الشبكة الداخلية"),
            ("Defense in depth", "layering several measures, so if one is breached the next still protects", "الدفاع في العمق: حماية في طبقات"),
            ("Zero trust", "trust no communication; verify every access, inside or outside", "انعدام الثقة: اتحقق من كل وصول"),
            ("Perimeter", "the old \"inside is safe, outside is dangerous\" boundary that cloud and remote work have blurred", "المحيط: الحد القديم اللي السحابة والشغل عن بُعد غيّروه"),
        ],
        "traps": [
            ("A VPN automatically deletes files infected with viruses.", False, "That is antivirus software on the endpoints."),
            ("A DMZ is mainly there to make communication faster.", False, "It stops an attack on a public server reaching the internal network."),
            ("Under zero trust, access from inside the network needs no checking.", False, "Every access is verified, inside or outside."),
            ("In defense in depth, if one measure is breached the next can still protect the system.", True, "That is the whole point."),
        ],
        "exam": {"from": (6, "7"), "q": "Explain why layering several security measures (defense in depth) protects an organization better than relying on a firewall alone. Refer to what happens if one measure is breached.", "marks": 6, "src": "p.45 — Exam-style question [6]"},
    },
    {
        "id": "2-3", "lecture": 7,
        "title": "Incident Response and Risk Management",
        "remember": "Follow the six stages in order (prepare → detect → contain → eradicate → recover → prevent), and prioritize risks by impact × likelihood.",
        "remember_ar": "امشي على المراحل الست بالترتيب (تحضير ← اكتشاف ← احتواء ← استئصال ← استعادة ← منع التكرار)، ورتّب المخاطر بالتأثير × الاحتمالية.",
        "svg": "STAGES",
        "terms": [
            ("Security incident", "a situation in which actual damage occurs due to an information security problem", "الحادث الأمني: ضرر حقيقي بسبب مشكلة أمن معلومات"),
            ("Containment", "limits the spread of damage, e.g. disconnecting an infected computer", "الاحتواء: نوقف انتشار الضرر"),
            ("Eradication", "removes the cause, e.g. the malware", "الاستئصال: نشيل السبب"),
            ("Recovery", "returns systems and services to normal, e.g. from a clean backup", "الاستعادة: نرجّع الأنظمة لطبيعتها"),
            ("Prevention of recurrence", "stage 6, also called lessons learned and improvement: analyze the cause so it does not happen again", "منع التكرار = الدروس المستفادة والتحسين"),
            ("Risk", "the possibility of a problem occurring in the future, and its impact", "الخطر: احتمال حدوث مشكلة وحجم أثرها"),
            ("Impact", "how much damage occurs if the risk happens", "التأثير: حجم الضرر"),
            ("Likelihood", "how probable it is that the risk happens", "الاحتمالية: مدى احتمال حدوثه"),
        ],
        "traps": [
            ("Detection → Eradication → Containment → Recovery is the right order.", False, "Containment comes before eradication."),
            ("The size of a risk can be judged by impact alone.", False, "Risk = impact × likelihood."),
            ("All risks must be addressed at the same time.", False, "Set priorities: the biggest first."),
            ("A software update that adds features is a security incident.", False, "Nothing was damaged."),
        ],
        "exam": {"from": (7, "7"), "q": "Explain why the six stages of incident response must be carried out in order, using recovery and eradication as an example. Refer to what happens if the cause is not removed.", "marks": 6, "src": "p.51 — Exam-style question [6]"},
    },
]

QUICK = [
    ("Which cryptography shares the key in HTTPS?", "Public-key cryptography."),
    ("A password and a fingerprint: how many factors?", "Two: knowledge and biometric."),
    ("Which technology proves a shopping site is genuine?", "A digital certificate."),
    ("Where does a public web server belong?", "In the DMZ."),
    ("Which layer is antivirus software and an updated OS?", "Endpoints."),
    ("Ransomware is spreading. What comes first: contain or eradicate?", "Contain: stop it spreading first."),
    ("Impact 3, likelihood 2: the risk size?", "6."),
    ("Stage 6 has a second name. What is it?", "Lessons learned and improvement."),
]

EXAM_TIPS = [
    ("Know the definition word for word", "MCQ options often swap two terms from the same lesson: a VPN for a DMZ, a signature for a certificate.", "احفظ التعريف بالنص — الاختيارات بتبدّل مصطلحين."),
    ("One mark, one point", "A [6]-mark answer needs about six separate points. Use each term the question asks for, and explain it.", "سؤال الـ 6 درجات محتاج حوالي 6 نقط منفصلة."),
    ("Match the threat to the tool", "Read the threat first — eavesdropping, tampering, fake site, stolen password — then name the technology.", "اقرا التهديد الأول وبعدين اختار التقنية."),
    ("Watch the order", "The six stages, and the three stages of HTTPS: say them in order.", "خلّي بالك من الترتيب."),
]


# the exam questions' marking points, copied from each lecture's answer key
# (lectureN/_teacher/exercises.json) by the generator, so this file stands alone
POINTS = {
 "2-1": [
  "Both sides need the same common key, and sharing it openly is not safe",
  "Public-key cryptography shares the key safely — public key locks, private key unlocks",
  "Public-key cryptography is slow for large amounts of data",
  "Common-key cryptography exchanges large amounts of data quickly",
  "So public-key is used only to share the key, common-key for the data",
  "Result: security and speed together"
 ],
 "2-2": [
  "A firewall alone is one barrier",
  "If that one barrier is breached, everything inside is exposed",
  "Defense in depth layers several measures",
  "Names at least two layers or measures, e.g. VPN, DMZ, endpoints",
  "If one is breached, the next still protects the system",
  "Conclusion: one breach is much less likely to expose the whole network"
 ],
 "2-3": [
  "Containment first stops the damage spreading",
  "Eradication removes the cause, e.g. the malware",
  "Recovery returns systems to normal only after that",
  "If recovery comes before eradication, the cause is still there",
  "So the same incident can happen again",
  "Conclusion: order keeps damage small / may need to step back"
 ]
}
