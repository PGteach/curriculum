# -*- coding: utf-8 -*-
"""Write Lecture 7's quiz questions into lecture7/quiz/index.html.

    python scripts/build_lecture7_quiz.py && python scripts/protect_answers.py 7

The second command is required: this writes plaintext a: indices, and
protect_answers turns them into fingerprints before publishing.

Lecture 7's paper: 20 questions, all on lesson 2-3, Incident Response and
Risk Management (English textbook pp. 48-54; Arabic textbook pp. 44-49).
Curriculum only: the book's own Worked Example, Try and Exercise items, and
the ministry's assessment book for the lesson (stage 6's second name, the
incident defined by availability, high impact with low likelihood as medium).

Every question has four options, every wrong option taken from the same
lesson. d: 1 easy, 2 medium, 3 hard -- the page runs easy to hard.
"""
import io, re

SECTIONS = [
    "Security incidents",
    "The six stages of incident response",
    "Containment and eradication",
    "Risk assessment",
]

# (section, difficulty, question, options, answer index, why, src, glosses)
Q = [
    # ================= band 1 =================
    (0, 1, "What is a security incident?",
     ["A situation in which actual damage occurs due to an information security problem",
      "The possibility of a problem occurring in the future",
      "A procedure prepared in advance for emergencies",
      "A software update that adds new features"], 0,
     "Real damage has happened. The second option is risk, which is about the future.",
     "p.49 — Point 1(1); p.52 Try 1 (1)", []),
    (1, 1, "Which is the first stage of incident response?",
     ["Preparation", "Detection", "Containment", "Recovery"], 0,
     "Procedures and structures are set up in advance, before any incident.",
     "p.49 — Point 2(1); Ministry assessments, period 1", []),
    (1, 1, "Which is the final stage of incident response?",
     ["Prevention of recurrence (lessons learned and improvement)", "Recovery", "Eradication", "Detection"], 0,
     "The last stage analyzes the cause so the same incident does not happen again.",
     "p.51 — Worked Example (1) D", []),
    (3, 1, "How is the size of a risk calculated in the lesson's model?",
     ["Impact × likelihood", "Impact + likelihood", "Impact − likelihood", "Impact ÷ likelihood"], 0,
     "Risk size = impact × likelihood.",
     "p.50 — Point 3(2); Ministry assessments, period 1 home tasks", []),
    (3, 1, "In risk assessment, what is impact?",
     ["How much damage occurs if the risk materializes",
      "How probable it is that the risk materializes",
      "How fast the team responds to an incident",
      "How many times the incident has happened"], 0,
     "Impact is the size of the damage. How probable it is, is likelihood.",
     "p.50 — Point 3(2)①; Ministry assessments, period 2", []),
    (2, 1, "Disconnecting a malware-infected computer from the network is which stage?",
     ["Containment", "Eradication", "Recovery", "Preparation"], 0,
     "It stops the damage spreading — containment.",
     "p.51 — Worked Example (2) b", []),

    # ================= band 2 =================
    (0, 2, "Which is NOT an appropriate example of a security incident?",
     ["A software update was performed to add new features",
      "Data was encrypted by a ransomware infection",
      "Customer information was leaked through unauthorized access",
      "A web service became unavailable due to an attack on the server"], 0,
     "An update damages nothing. The other three are real damage.",
     "p.52 — Try 2(1)", []),
    (0, 2, "Data within a system is altered without authorization. Which type of incident is this?",
     ["Data tampering", "Information leak", "Service outage", "Preparation"], 0,
     "Altered without authorization is tampering.",
     "p.49 — Point 1(2); Ministry assessments, form B", []),
    (0, 2, "Which incident affects the availability of a service?",
     ["A service outage caused by attacks on the server",
      "Personal information leaked to the outside",
      "Data altered without authorization",
      "Response procedures set up in advance"], 0,
     "Availability means the service can be used; an outage takes that away.",
     "Ministry assessments, period 1 — MCQ 1", [["availability", "التوافر — الخدمة متاحة للاستخدام"]]),
    (2, 2, "Removing the malware infection is which stage?",
     ["Eradication", "Containment", "Detection", "Recovery"], 0,
     "Removing the cause is eradication.",
     "p.51 — Worked Example (2) c", []),
    (1, 2, "Which stage returns systems and services to their normal state, possibly from a clean backup?",
     ["Recovery", "Containment", "Detection", "Preparation"], 0,
     "Recovery — and only after the cause has been removed.",
     "p.49 — Point 2(1)⑤; Ministry assessments, form B", []),
    (3, 2, "Which describes risk assessment most appropriately?",
     ["Risks with both high impact and high likelihood should be addressed first",
      "It is enough to address only risks with large impact",
      "It is enough to address only risks with high likelihood",
      "All risks must be addressed simultaneously"], 0,
     "Both factors count, and no team can fix everything at once.",
     "p.52 — Try 2(2)", []),
    (1, 2, "Which order of incident response is correct?",
     ["Preparation → Detection → Containment → Eradication → Recovery → Prevention of recurrence",
      "Detection → Eradication → Containment → Recovery",
      "Detection → Recovery → Containment → Prevention of recurrence",
      "Containment → Detection → Eradication → Preparation"], 0,
     "Prepare, detect, contain, eradicate, recover, prevent.",
     "p.54 — Exercise 3(2)", []),
    (3, 2, "A risk has high impact but low likelihood. How is it usually classed in the risk matrix?",
     ["Medium", "Very high", "Very low", "None at all"], 0,
     "3 × 1 = 3: in the middle of the scale.",
     "Ministry assessments, form C — MCQ 3", []),

    # ================= band 3 =================
    (2, 3, "Why must containment come before eradication?",
     ["So the damage does not keep spreading while the cause is being removed",
      "Because eradication cannot start until the system is restored",
      "Because containment removes the malware",
      "Because the order of the stages does not matter"], 0,
     "Containment stops the spread first; then the cause is removed safely.",
     "p.50 — Pause & Think", []),
    (2, 3, "A team restores the system from a backup before removing the malware. What is the most likely result?",
     ["The same incident may occur again",
      "The incident is fully solved",
      "The risk size becomes zero",
      "Containment is no longer needed"], 0,
     "The cause is still there, so the incident can return.",
     "p.50 — Point 2(2); p.51 exam-style question", []),
    (3, 3, "Risk a: impact 3, likelihood 3. Risk b: impact 1, likelihood 3. Risk c: impact 3, likelihood 2. Risk d: impact 1, likelihood 1. Which order is highest priority first?",
     ["a, c, b, d", "a, b, c, d", "c, a, b, d", "b, a, d, c"], 0,
     "9, 6, 3, 1.",
     "p.54 — Exercise 3(1)", []),
    (1, 3, "During recovery, traces of the threat are found. What should the team do?",
     ["Go back to containment or eradication",
      "Finish recovery and ignore the traces",
      "Jump to prevention of recurrence",
      "Start again from preparation"], 0,
     "In practice stages can overlap or repeat; the Arabic book gives exactly this example.",
     "Arabic book p.46 — Point 2(2); Ministry assessments, period 2 home tasks", []),
    (1, 3, "The last stage is called prevention of recurrence in the English book. What is it called in the Arabic book and the ministry's papers?",
     ["Lessons learned and improvement", "Detection", "Recovery", "Risk assessment"], 0,
     "Same stage, two names: analyze what happened, document the lessons, improve the controls.",
     "Arabic book p.46; Ministry assessments, period 2", []),
    (0, 3, "Under the Arabic book's definition, which is a security incident?",
     ["An event that affects the confidentiality, integrity or availability of information, or violates a security policy",
      "Any planned change to a computer system",
      "A risk that has not happened yet",
      "Any slow Internet connection"], 0,
     "Confidentiality, integrity, availability — or a broken security policy.",
     "Arabic book p.45 — Point 1(1); Ministry assessments, form A", []),
]


def js_str(t):
    return '"' + t.replace("\\", "\\\\").replace('"', '\\"') + '"'


if __name__ == "__main__":
    from collections import Counter
    assert len(Q) == 20, len(Q)
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

    p = "lecture7/quiz/index.html"
    page = io.open(p, encoding="utf-8").read()
    page = re.sub(r"const SECTIONS = \[.*?\n\];", lambda m: "const SECTIONS = " + secs,
                  page, count=1, flags=re.DOTALL)
    page = re.sub(r"const QUESTIONS = \[.*?\n\];", lambda m: "const QUESTIONS = " + qs,
                  page, count=1, flags=re.DOTALL)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    print("written: %d questions" % len(Q))
