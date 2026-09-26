# -*- coding: utf-8 -*-
"""Write Lecture 4's quiz questions into lecture4/quiz/index.html.

    python scripts/build_lecture4_quiz.py && python scripts/protect_answers.py 4

The second command is required: this writes plaintext a: indices, and
protect_answers turns them into fingerprints before publishing.

Lecture 4's paper: 24 questions. Eighteen on lesson 1-4, Ethical Issues with
AI (textbook pp. 26-32), and six reviewing lessons 1-1 to 1-3 -- curriculum
only, nothing from the programming foundations of lecture 1, because the
printed unit exam is what this rehearses.

Every question has four options, and every wrong option is something from
the same lesson a student who half-knows could genuinely pick: the other
three principles, the other ethical issue, the other cause. Several are the
book's own Try and Worked Example items, and two are from the ministry's
assessment book (the responsibility/accountability distinction, and
training data as the source of bias).

d: 1 easy, 2 medium, 3 hard -- bandedOrder() on the page runs easy to hard,
shuffling inside each band. v: word glosses, heavy words only, by the thumb
test in README: cover the word, and if the sentence still carries it, it is
not glossed. Syllabus terms (fairness, XAI, accountability ...) are never
glossed; they are what is being learned.
"""
import io, re

SECTIONS = [
    "Unit 1 review",
    "Algorithmic bias",
    "Privacy",
    "Explainable AI and responsibility",
    "The four principles of AI ethics",
]

# (section, difficulty, question, options, answer index, why, src, glosses)
Q = [
    # ================= band 1 =================
    (1, 1, "What is algorithmic bias?",
     ["Bias in AI judgments caused by bias in the training data",
      "Technology that lets humans understand why an AI made a judgment",
      "The question of who answers when an AI judgment is wrong",
      "The appropriate handling and protection of personal data"], 0,
     "Algorithmic bias comes from biased training data. The other three are XAI, responsibility and privacy — all from this lesson, which is why they are here.",
     "p.27 — Algorithmic bias", []),
    (1, 1, "Which of these is the book's example of algorithmic bias?",
     ["A face-recognition AI more likely to misidentify particular ethnic groups",
      "A spam filter that sorts email into separate folders",
      "An AI that is slow to process a very large image",
      "A translation app that needs an Internet connection"], 0,
     "The book's two examples are a hiring AI that unfairly evaluates a particular gender, and a face-recognition AI that misidentifies particular ethnic groups.",
     "p.27 — Algorithmic bias e.g.", []),
    (2, 1, "Which is a privacy issue associated with AI?",
     ["Individuals are identified and tracked through face-recognition technology",
      "AI creates creative works such as images",
      "AI computation speed improves every year",
      "AI translates text into another language"], 0,
     "Surveillance through face recognition is one of the two privacy issues in the lesson; mass collection of online behaviour data is the other.",
     "p.30 — Try 2(2)", []),
    (3, 1, "What does explainable AI (XAI) make possible?",
     ["Humans understanding why an AI made a particular judgment",
      "An AI making its decisions faster",
      "An AI generating new text and images",
      "An AI working without any training data"], 0,
     "XAI is about understanding the reasoning. Generating new data is generative AI, from lesson 1-2.",
     "p.28 — Explainable AI (XAI)", []),
    (3, 1, "When it is unclear how an AI reached its judgment, this is called:",
     ["The black-box problem", "Algorithmic bias", "A hallucination",
      "A proxy variable"], 0,
     "An opaque decision process is the black box. A hallucination is fluent content that differs from the facts — a different caution.",
     "p.28 — black box; p.21 key terms", []),
    (4, 1, "Which principle of AI ethics requires not unjustly discriminating against any particular person or group?",
     ["Fairness", "Transparency", "Privacy protection", "Accountability"], 0,
     "That is fairness. Learn all four definitions exactly — the exam matches them.",
     "p.28 — basic principles; p.30 Try 1(3)",
     [["unjustly", "بشكل ظالم"], ["discriminating", "يميّز ضد"]]),
    (0, 1, "Which lists the stages of IT development in the correct chronological order?",
     ["Birth of the computer → Commercialization of the Internet → Rise of smartphones → Spread of cloud computing",
      "Birth of the computer → Rise of smartphones → Commercialization of the Internet → Spread of cloud computing",
      "Commercialization of the Internet → Birth of the computer → Spread of cloud computing → Rise of smartphones",
      "Rise of smartphones → Commercialization of the Internet → Birth of the computer → Spread of cloud computing"], 0,
     "1940s-60s computer, 1990s Internet, 2000s smartphones, 2010s cloud.",
     "Lesson 1-1, p.8 — Worked Example (1)",
     [["chronological order", "الترتيب الزمني — الأقدم الأول"],
      ["Commercialization", "التحوّل لخدمة تجارية بتتباع"]]),
    (0, 1, "Which puts these in the right order, broadest first?",
     ["AI > Machine learning > Deep learning > Generative AI",
      "AI > Deep learning > Machine learning > Generative AI",
      "Machine learning > AI > Generative AI > Deep learning",
      "Generative AI > Deep learning > Machine learning > AI"], 0,
     "They are nested: each is inside the one before it.",
     "Lesson 1-2, p.16 — Try 2(1)", []),

    # ================= band 2 =================
    (1, 2, "Which of these is NOT an appropriate cause of algorithmic bias?",
     ["The processing speed of the computer is slow",
      "Training data is biased",
      "Past discriminatory tendencies are reflected in the data",
      "There is insufficient data on certain attributes"], 0,
     "Bias comes from the data or the way the system is built — never from how fast it runs.",
     "p.30 — Try 2(1)",
     [["discriminatory tendencies", "ميول للتمييز"], ["insufficient", "مش كفاية"],
      ["attributes", "سمات / صفات"]]),
    (1, 2, "A face-recognition AI was trained mostly on photos of one group. What will it most likely do?",
     ["Be accurate for that group and misidentify others more often",
      "Be equally accurate for every group",
      "Refuse to recognise anyone outside that group",
      "Become slower for every group"], 0,
     "It learns the pattern in the data it was given. Too little data on a group is one of the book's main causes of bias.",
     "p.27 — main causes of bias", []),
    (2, 2, "A shopping site collects and analyses large amounts of what you click, search and buy. Which issue does this raise?",
     ["Privacy — mass collection of personal data",
      "Algorithmic bias — biased training data",
      "The black-box problem — an opaque decision process",
      "Hallucination — content that differs from the facts"], 0,
     "Collecting and analysing large amounts of online behaviour data is the lesson's second privacy issue.",
     "p.28 — Privacy issues (2)", []),
    (3, 2, "\"Even if an AI's decision-making process is opaque, there is no problem as long as the result is correct.\" Is this true?",
     ["False — when the process is opaque, it is difficult to verify whether the result is correct",
      "True — only the result of an AI matters",
      "False — an opaque AI is always wrong",
      "True — explainable AI is only needed for slow systems"], 0,
     "The point is verification: you cannot check a result you cannot see the reasons for. It is not that opaque AI is always wrong.",
     "p.29 — Worked Example (1) B",
     [["opaque", "مقفول / مش واضح"]]),
    (3, 2, "Has it been clearly decided who is responsible when an AI makes an incorrect judgment?",
     ["No — views differ depending on whether one is the developer, the user or the operator",
      "Yes — it is always the developer who built it",
      "Yes — it is always the user who acted on it",
      "Yes — the AI itself is held responsible"], 0,
     "No clear standard has been established yet. Each option that says 'always' is the trap.",
     "p.29 — Worked Example (1) D", []),
    (4, 2, "A company explains to users, in an easy-to-understand way, how its AI reaches decisions. Which principle is this?",
     ["Transparency", "Fairness", "Privacy protection", "Accountability"], 0,
     "Showing the decision-making process clearly is transparency.",
     "p.32 — Exercise 3(1) b", []),
    (4, 2, "A company promises never to use the personal data it collects for any purpose other than the original one. Which principle is this?",
     ["Privacy protection", "Transparency", "Fairness", "Accountability"], 0,
     "Handling personal information appropriately is privacy protection.",
     "p.32 — Exercise 3(1) c", []),
    (0, 2, "Which is NOT an appropriate description of an emerging technology?",
     ["VR is a technology that dramatically improves the processing speed of a computer",
      "Autonomous driving uses AI to drive a vehicle without human operation",
      "AR is a technology that overlays digital information on real-world images",
      "Quantum computing is expected to speed up computations that are difficult for traditional computers"], 0,
     "Speed describes quantum computing. VR immerses the user in a virtual space.",
     "Lesson 1-1, p.9 — Try 2(2)",
     [["appropriate", "مناسب / صحيح"], ["emerging technology", "تكنولوجيا ناشئة — جديدة وبتنتشر"],
      ["dramatically", "بشكل كبير جدًا"], ["overlays", "بيحُطّ فوق — يضيف طبقة"]]),
    (0, 2, "Which is NOT an example of generative AI?",
     ["A spam filter", "ChatGPT", "Image generation AI", "Audio generation AI"], 0,
     "A spam filter classifies email; it does not generate anything new.",
     "Lesson 1-2, p.16 — Try 2(2)", []),
    (0, 2, "In manufacturing, what is the system that predicts product failures in advance?",
     ["Predictive maintenance", "Automation of quality inspection",
      "Image-diagnosis AI", "Optimisation of delivery routes"], 0,
     "Predictive maintenance. Quality inspection is the book's other manufacturing example; the last two belong to healthcare and logistics.",
     "Lesson 1-3, p.22 — Try 1(4)", []),

    # ================= band 3 =================
    (1, 3, "A hiring AI is never given applicants' gender, yet it still rates one gender lower. What best explains this?",
     ["Another variable it uses stands in for gender — a proxy variable",
      "The black-box problem makes it rate some applicants lower",
      "It had too little processing power for some applicants",
      "It was not trained on any data at all"], 0,
     "A proxy variable indirectly stands in for a protected attribute, so removing gender from the data is not enough. The black box hides the reason; it is not the cause.",
     "p.27 — main causes of bias (proxy variable)", []),
    (1, 3, "A hiring AI was trained on ten years of a company's past hiring decisions, and now favours one gender. Where did the bias most likely come from?",
     ["Past discriminatory tendencies reflected in the training data",
      "The AI generating new data, as generative AI does",
      "The black-box problem in the AI's design",
      "A privacy issue in the way the data was stored"], 0,
     "If past decisions were unfair, the data carries that unfairness, and the AI learns it. That is one of the book's two data causes.",
     "p.27 — main causes of bias",
     [["discriminatory tendencies", "ميول للتمييز"]]),
    (2, 3, "Face-recognition cameras at a station make entry safer and faster, but they can track every passenger. Which principle is most directly at stake?",
     ["Privacy protection", "Transparency", "Fairness", "Accountability"], 0,
     "Tracking individuals in a public space is the surveillance issue, which is privacy. Safety and convenience are the benefits it has to be balanced against.",
     "p.28 — Think It Through",
     [["at stake", "في خطر / على المحك"]]),
    (3, 3, "Which statement correctly separates responsibility from accountability?",
     ["Responsibility is each party's roles and duties; accountability is being answerable for decisions according to those roles",
      "Responsibility is showing the decision process clearly; accountability is protecting personal data",
      "Accountability is explaining why an AI decided; responsibility is avoiding bias in the data",
      "They mean exactly the same thing"], 0,
     "Responsibility sets out who does what; accountability is who can be held to account. Options two and three borrow the definitions of the other principles.",
     "p.28 responsibility & accountability; ministry assessment, lesson 4",
     [["answerable", "يتحاسب / مسؤول قدام حد"]]),
    (4, 3, "No one can explain why an AI rejected a job application, and no one will answer for the decision. Which TWO principles are missing?",
     ["Transparency and accountability", "Fairness and privacy protection",
      "Privacy protection and transparency", "Fairness and accountability"], 0,
     "'No one can explain' is transparency; 'no one will answer' is accountability. Each clause of the question points to one principle.",
     "p.29 — Pause & Think", []),
    (0, 3, "Which of these should NOT be left entirely to AI?",
     ["Ethical judgments",
      "Finding and classifying patterns in images and text",
      "Probabilistic reasoning and prediction based on data",
      "Recognising images and audio"], 0,
     "Ethical judgments can lead to discrimination or prejudice. The other three are exactly what the book lists AI as good at.",
     "Lesson 1-3, p.22 — Worked Example (2) C", []),
]


def js_str(t):
    return '"' + t.replace("\\", "\\\\").replace('"', '\\"') + '"'


if __name__ == "__main__":
    from collections import Counter
    assert len(Q) == 24, len(Q)
    for s, d, q, o, a, why, src, v in Q:
        assert 0 <= s < len(SECTIONS), q
        assert d in (1, 2, 3), q
        assert 0 <= a < len(o), q
        assert len(o) == 4, "four options: " + q
        assert len(o) == len(set(o)), "repeated option: " + q
        assert why.strip() and src.strip(), q
        hay = (q + " " + " ".join(o)).lower()
        for en, ar in v:
            assert en.lower() in hay, "gloss not on screen: %r in %r" % (en, q)
    assert len({x[2] for x in Q}) == len(Q), "duplicate question text"
    print("sections:", dict(sorted(Counter(x[0] for x in Q).items())))
    print("difficulty:", dict(sorted(Counter(x[1] for x in Q).items())))

    secs = "[\n" + ",\n".join("  " + js_str(x) for x in SECTIONS) + "\n];"
    rows = []
    for s, d, q, o, a, why, src, v in Q:
        gl = (",v:[%s]" % ",".join("[%s,%s]" % (js_str(en), js_str(ar)) for en, ar in v)) if v else ""
        rows.append("  {s:%d,d:%d,q:%s,o:[%s],a:%d,why:%s,src:%s%s}"
                    % (s, d, js_str(q), ",".join(js_str(x) for x in o), a,
                       js_str(why), js_str(src), gl))
    qs = "[\n" + ",\n".join(rows) + "\n];"

    p = "lecture4/quiz/index.html"
    page = io.open(p, encoding="utf-8").read()
    page = re.sub(r"const SECTIONS = \[.*?\n\];", lambda m: "const SECTIONS = " + secs,
                  page, count=1, flags=re.DOTALL)
    page = re.sub(r"const QUESTIONS = \[.*?\n\];", lambda m: "const QUESTIONS = " + qs,
                  page, count=1, flags=re.DOTALL)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    print("written: %d questions" % len(Q))
