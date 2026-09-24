# -*- coding: utf-8 -*-
"""Write Lecture 3's quiz questions into lecture3/quiz/index.html.

    python scripts/build_lecture3_quiz.py && python scripts/protect_answers.py 3

The second command is required: this writes plaintext a: indices, and
protect_answers turns them into fingerprints before publishing.

Lecture 3's paper: 36 questions, cumulative, weighted to lectures 2 and 3.

The distractors are the point of this rewrite. The previous set offered
things like "cashless payment" as a wrong answer to a deep-learning
question, so a student could score well by eliminating the absurd rather
than by knowing the lesson. Every wrong option here is something from the
same material that a student who half-knows could genuinely pick, and most
questions carry four options rather than three, which takes a pure guess
from 33% to 25%.

d: 1 easy, 2 medium, 3 hard. Answers go in as plaintext `a:` and are
fingerprinted afterwards by scripts/protect_answers.py.
"""
import io, re

SECTIONS = [
    "Lecture 1 foundations",
    "Lecture 2 technology",
    "AI and machine learning",
    "Deep learning and generative AI",
    "AI in daily life and industry",
]

# (section, difficulty, question, options, answer index, why, src)
Q = [
    # ================= band 1 =================
    (0, 1, "Which sequence describes how a computer handles a task?",
     ["Input, processing, output", "Input, output, processing",
      "Processing, input, output", "Output, processing, input"], 0,
     "It takes input, processes it, then produces output. Every option here is a real permutation, so the order has to be known.",
     "Lecture 1"),
    (1, 1, "Roughly how often does Moore's Law say the transistor count doubles?",
     ["About every two years", "About every year",
      "About every five years", "About every ten years"], 0,
     "About every two years. The other intervals are the ones most often misremembered.",
     "p.7 — Moore's Law"),
    (2, 1, "Machine learning learns its patterns from what?",
     ["Data", "Rules a programmer writes", "The operating system",
      "The speed of the processor"], 0,
     "It learns patterns from data. Rules written by a programmer is the OTHER approach — that is traditional programming.",
     "p.14 — Machine Learning"),
    (3, 1, "A neural network is modelled on what?",
     ["The nerve cells of the human brain", "The transistors on a chip",
      "The way data is stored in the cloud", "The layers of the Internet"], 0,
     "It is modelled on the neurons of the human brain. The other three are all real things from these lectures, but none of them is the model.",
     "p.14 — Neural network"),
    (3, 1, "Generative AI is built on top of which technology?",
     ["Deep learning", "Machine translation", "A recommendation system",
      "Face recognition"], 0,
     "Generative AI uses deep learning. The other three are AI applications, not the technology underneath it.",
     "p.14 — Generative AI"),
    (1, 1, "What is SNS?",
     ["A service that lets users connect, post and share information",
      "A service for paying without cash",
      "A service that translates between languages",
      "A service for studying over the Internet"], 0,
     "SNS is social networking. The other three are cashless payment, machine translation and online learning — all real, all different.",
     "p.7 — social changes"),

    # ================= band 2 =================
    (0, 2, "You wrote for an hour, the battery died, and the work was gone. Where had it been?",
     ["In RAM", "In storage", "In the CPU", "In the input device"], 0,
     "Unsaved work sits in RAM, which is wiped when the power goes. Saving is what copies it to storage.",
     "Lecture 1"),
    (2, 2, "Which puts the four in the right order, broadest first?",
     ["AI, machine learning, deep learning, generative AI",
      "AI, deep learning, machine learning, generative AI",
      "Machine learning, AI, deep learning, generative AI",
      "AI, machine learning, generative AI, deep learning"], 0,
     "They are nested in that order. The other three each swap one pair, which is exactly the mistake the exam looks for.",
     "p.13-14 — hierarchy"),
    (2, 2, "A spam filter and a shop's recommendations do different jobs. What do they share?",
     ["Both learn patterns from data",
      "Both generate new text",
      "Both use a neural network with large-scale data",
      "Both need the user to write a rule first"], 0,
     "Both are machine learning. The neural-network option describes deep learning specifically, which is narrower than what they share.",
     "p.14 — Machine Learning"),
    (2, 2, "Why is today's AI called narrow?",
     ["Each system is expert at one task only",
      "It can only work in one language",
      "It only runs on small devices",
      "It can only handle small amounts of data"], 0,
     "Narrow means expert at one task. A translation app cannot recognise a face, however much data it is given.",
     "p.13 — narrow AI"),
    (3, 2, "What does deep learning need a great deal of?",
     ["Large-scale data", "Hand-written rules for each case",
      "A faster Internet connection", "Storage on the user's own device"], 0,
     "It needs large-scale data. Hand-written rules is the approach it replaces, not something it needs more of.",
     "p.14 — Deep Learning"),
    (4, 2, "In manufacturing, what is predictive maintenance?",
     ["Predicting that a machine will fail before it does",
      "Repairing a machine as soon as it breaks",
      "Inspecting product quality automatically",
      "Planning which machine to buy next"], 0,
     "It predicts a failure in advance. Automatic quality inspection is the book's OTHER manufacturing example, which is why it is here.",
     "p.21 — manufacturing"),
    (4, 2, "Which of these is AI good at?",
     ["Finding and classifying patterns in complex data",
      "Deciding who is responsible when something goes wrong",
      "Judging whether an outcome is fair",
      "Deciding who may see someone's personal data"], 0,
     "Finding patterns is the strength. The other three are the book's cautions: responsibility, ethics and privacy.",
     "p.21 — what AI is good at"),
    (4, 2, "Which industry and use are correctly paired?",
     ["Logistics — optimising delivery routes",
      "Agriculture — predictive maintenance",
      "Healthcare — detecting pests and diseases",
      "Manufacturing — drug-discovery support"], 0,
     "Only the first pair is right. The other three take a real use from the book and attach it to the wrong industry, so the whole table has to be known.",
     "p.21 — AI in industry"),
    (2, 3, "A team has thousands of labelled photographs and wants a system that improves as more arrive. What fits?",
     ["A machine-learning model trained on the photographs",
      "A program with a rule written for each kind of photograph",
      "A larger database to store the photographs",
      "A faster processor to open the photographs"], 0,
     "Learning from examples and improving with more of them is machine learning. Hand-written rules cannot improve on their own.",
     "p.14 — Machine Learning"),
    (4, 2, "What is the clearest privacy concern in a recommendation system?",
     ["It keeps a record of what you watched and bought",
      "It needs a fast Internet connection",
      "It sometimes recommends the wrong thing",
      "It shows different items to different people"], 0,
     "It works by holding your past behaviour, which is personal data. Being wrong sometimes is a quality problem, not a privacy one.",
     "p.21 — cautions when using AI"),


    # ================= band 3 =================
    (3, 3, "Deep learning is a completely different technology from machine learning.",
     ["False — it is an advanced kind of machine learning",
      "False — machine learning is a kind of deep learning",
      "True — they developed separately",
      "True — deep learning replaced machine learning"], 0,
     "Deep learning sits INSIDE machine learning. The second option reverses the nesting, which is the commonest wrong answer.",
     "p.15 — Worked Example (1) B"),
    (3, 3, "VR is a technology that speeds up a computer's processing.",
     ["False — VR immerses you in a generated space; quantum computing is about speed",
      "False — VR overlays information on the real world",
      "True — VR needs and provides a faster processor",
      "True — VR speeds up graphics only"], 0,
     "VR has nothing to do with speed. The second option is wrong for a different reason: overlaying on the real world is AR, not VR.",
     "p.9 — Lecture 2 exam trap"),
    (3, 3, "An AI misjudges a horse and cart on a road at night. What is the most likely reason?",
     ["It had rarely seen that situation in its training data",
      "The camera resolution was too low",
      "It was not connected to the cloud at the time",
      "The vehicle was moving too slowly"], 0,
     "A model learns what it was shown, so the rare case is the one it fails — and it stays confident. A low-resolution camera would affect every situation, not just the rare one.",
     "p.14 — large-scale data"),
    (3, 3, "A chatbot gives a fluent, confident answer that is factually wrong. Why does this happen?",
     ["It is built to produce text that reads well, not text that is checked",
      "It did not have enough training data on any subject",
      "It was asked a question that was too short",
      "It confused one language with another"], 0,
     "Fluency and correctness are different things, and it has no way of knowing it is wrong. That is a hallucination.",
     "p.16 — using generative AI carefully"),
    (3, 3, "An app names a crop disease from a photo, then writes a treatment plan. Which is which?",
     ["Naming the disease classifies; writing the plan generates",
      "Naming the disease generates; writing the plan classifies",
      "Both parts classify", "Both parts generate"], 0,
     "Choosing from known diseases is classifying. Producing a plan that did not exist before is generating.",
     "p.14 — classify and generate"),
    (1, 3, "Why did cloud computing matter for AI?",
     ["It made large-scale data and processing available without owning them",
      "It made the Internet faster for everyone",
      "It let programs run without an operating system",
      "It replaced the need for machine learning"], 0,
     "Renting storage and processing is what large-scale data analysis and AI need. That is why the 2010s stage opened the door to this lesson.",
     "p.6 — cloud computing"),
    (3, 3, "A self-driving car must decide in a fraction of a second. Why is edge computing used?",
     ["The round trip to the cloud is too slow to brake in time",
      "The cloud cannot store enough images",
      "Edge computing is cheaper than cloud computing",
      "The car has no Internet connection at all"], 0,
     "A delay of even 0.1 seconds can cause an accident, so the decision is made on the vehicle. Cars do have connections — the problem is the delay.",
     "p.8 — autonomous driving"),
    (0, 3, "Which statement about a touchscreen is correct?",
     ["It is both an input and an output device",
      "It is an input device only", "It is an output device only",
      "It is neither; it is a storage device"], 0,
     "It takes your finger in and shows the picture out, so it is both. A very common exam question.",
     "Lecture 1"),
    (1, 3, "Why is Moore's Law called an observation rather than a law of physics?",
     ["Moore noticed it kept happening; nothing forces it to continue",
      "It was proved, then later disproved",
      "It applies only to memory chips",
      "It was a target the industry agreed to meet"], 0,
     "It is empirical, and it is said to be nearing a physical limit. The last option is a tempting misreading — it was never an agreement.",
     "p.7 — Moore's Law"),
    (1, 3, "Transistors cannot simply keep shrinking. What goes wrong?",
     ["Electrons slip through a barrier that has become too thin",
      "The chip draws too little current to work",
      "The chip becomes physically too heavy",
      "The manufacturing machines cannot be made smaller"], 0,
     "That is quantum tunneling, along with leakage current. The responses are parallel processing and quantum computers.",
     "p.7 — why shrinking is hard"),
    (4, 3, "A hospital uses AI to read X-rays. Why should a doctor still confirm the diagnosis?",
     ["A wrong result can harm a patient, and it is unclear how the AI decided",
      "The AI cannot read image files reliably",
      "A doctor can read the image faster than the AI",
      "The AI would need to be retrained for each patient"], 0,
     "Final decision-making and responsibility need a human, and the black-box problem means the reasoning is not visible.",
     "p.21 — Think It Through"),
    (2, 2, "Which is the clearest sign a system is machine learning rather than ordinary programming?",
     ["Its answers improve as it is given more examples",
      "It runs without an Internet connection",
      "It was written by more than one programmer",
      "It produces an answer very quickly"], 0,
     "Improving from examples is the defining behaviour. Speed and offline working say nothing about how the rules were arrived at.",
     "p.14 — Machine Learning"),

    # ---- minimal pairs: each two questions differ by one word, and that word
    # ---- changes the answer. Recognising the shape of the question is not
    # ---- enough; the distinction has to be understood.

    # pair 1 — sorting is classifying, writing is generating
    (3, 3, "A photo app sorts your pictures into “people” and “places”. What is it doing?",
     ["Classifying — choosing from labels that already exist",
      "Generating — producing something new",
      "Both, at the same time",
      "Neither; that is ordinary programming"], 0,
     "Sorting into existing labels is classifying. Compare this with the app that WRITES a caption — same app, different job.",
     "p.14 — classify and generate"),
    (3, 3, "The same photo app writes a caption describing your picture. What is it doing now?",
     ["Generating — producing text that did not exist before",
      "Classifying — choosing from captions that already exist",
      "Both, at the same time",
      "Neither; that is ordinary programming"], 0,
     "Writing a caption produces something new, so it is generating. One word changed in the question and the answer changed with it.",
     "p.14 — classify and generate"),

    # pair 2 — who is in the photo, against what is wrong in it
    (4, 3, "An AI looks at a photograph and identifies WHO is in it. Which technology is that?",
     ["Face recognition", "Image-diagnosis AI", "A recommendation system",
      "Machine translation"], 0,
     "Identifying a person is face recognition. The next question changes only what is being identified.",
     "p.20 — face recognition"),
    (4, 3, "An AI looks at a photograph and identifies a DISEASE in it. Which technology is that?",
     ["Image-diagnosis AI", "Face recognition", "Predictive maintenance",
      "A recommendation system"], 0,
     "Identifying a disease in a scan is image-diagnosis AI, used in healthcare. Same action, same kind of input, different answer.",
     "p.21 — healthcare"),

    # pair 3 — who is at home changes which of the five changes it is
    (1, 3, "Staff join a work meeting from home over the Internet. Which of the five changes is that?",
     ["Remote work", "Online learning", "E-commerce", "SNS"], 0,
     "Work performed from home over the Internet is remote work. Change who is at home and the answer changes.",
     "p.7 — social changes"),
    (1, 3, "Students join a class from home over the Internet. Which of the five changes is that?",
     ["Online learning", "Remote work", "E-commerce", "SNS"], 0,
     "Classes delivered over the Internet are online learning. The sentence is almost identical to the last one — only the people changed.",
     "p.7 — social changes"),

    # pair 4 — adding to the room, against replacing it
    (1, 3, "An app shows repair steps on top of the engine you are looking at, through your camera. Which is it?",
     ["AR — it adds to the real world",
      "VR — it replaces the real world",
      "Quantum computing", "Autonomous driving"], 0,
     "The real engine is still there and information is laid over it, so this is AR.",
     "p.8 — AR and VR"),
    (1, 3, "An app puts you inside a workshop that does not exist, and the room around you disappears. Which is it?",
     ["VR — it replaces the real world",
      "AR — it adds to the real world",
      "Quantum computing", "Autonomous driving"], 0,
     "The real room is gone and a generated one has taken its place, so this is VR. Same app idea, opposite answer.",
     "p.8 — AR and VR"),
]


def js_str(t):
    return '"' + t.replace("\\", "\\\\").replace('"', '\\"') + '"'


if __name__ == "__main__":
    from collections import Counter
    assert len(Q) == 36, len(Q)
    for s, d, q, o, a, why, src in Q:
        assert 0 <= s < len(SECTIONS), q
        assert d in (1, 2, 3), q
        assert 0 <= a < len(o), q
        assert len(o) == len(set(o)), "repeated option: " + q
        assert len(o) >= 3, q
        assert why.strip() and src.strip(), q
    print("sections:", dict(sorted(Counter(x[0] for x in Q).items())))
    print("difficulty:", dict(sorted(Counter(x[1] for x in Q).items())))
    print("options per question:", dict(sorted(Counter(len(x[3]) for x in Q).items())))

    secs = "[\n" + ",\n".join("  " + js_str(x) for x in SECTIONS) + "\n];"
    rows = ["  {s:%d,d:%d,q:%s,o:[%s],a:%d,why:%s,src:%s}"
            % (s, d, js_str(q), ",".join(js_str(x) for x in o), a, js_str(why), js_str(src))
            for s, d, q, o, a, why, src in Q]
    qs = "[\n" + ",\n".join(rows) + "\n];"

    p = "lecture3/quiz/index.html"
    page = io.open(p, encoding="utf-8").read()
    page = re.sub(r"const SECTIONS = \[.*?\n\];", lambda m: "const SECTIONS = " + secs,
                  page, count=1, flags=re.DOTALL)
    page = re.sub(r"const QUESTIONS = \[.*?\n\];", lambda m: "const QUESTIONS = " + qs,
                  page, count=1, flags=re.DOTALL)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    print("written: %d questions" % len(Q))
