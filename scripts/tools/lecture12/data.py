# -*- coding: utf-8 -*-
"""Chapter 1 (Unit 1) revision: what each lesson must leave behind.

One record per lesson, read by the deck (slides.py), the booklet
(booklet.py) and the flashcards. The "remember" line is the book's own Key
takeaway; the terms are the book's Key Terms and Point definitions; the
traps are statements the book, the quizzes or the ministry's assessment
book mark false (or true); the exam question is the lesson's own
exam-style question, with the marking points written when that lecture
was made (lectures 2-4).
"""

LESSONS = [
    {
        "id": "1-1", "lecture": 2,
        "title": "Development of Information Technology and Social Transformation",
        "remember": "Information technology developed in stages — computers, the Internet, smartphones, and cloud computing. At each stage it introduced a new technology or service and also changed how society communicates, works, learns, and pays.",
        "remember_ar": "تكنولوجيا المعلومات اتطورت على مراحل: الكمبيوتر، والإنترنت، والموبايل الذكي، والحوسبة السحابية — وكل مرحلة غيّرت طريقة تواصلنا وشغلنا وتعليمنا ودفعنا.",
        "svg": "TIMELINE",
        "terms": [
            ("Moore's Law", "the number of transistors on an integrated circuit doubles approximately every two years", "عدد الترانزستورات في الشريحة بيتضاعف تقريبًا كل سنتين"),
            ("SNS", "services that let users connect, post and share information; very effective at spreading information fast", "خدمات التواصل الاجتماعي: نتواصل وننشر ونشارك"),
            ("E-commerce (EC)", "buying and selling goods and services through the Internet", "التجارة الإلكترونية: البيع والشراء عبر الإنترنت"),
            ("Remote work", "working from home or another remote place using the Internet", "العمل عن بُعد من البيت عبر الإنترنت"),
            ("Online learning", "classes and study materials delivered over the Internet", "التعلّم عبر الإنترنت"),
            ("Cashless payment", "paying with electronic money, QR codes, etc., without cash", "الدفع من غير كاش: فلوس إلكترونية أو QR"),
            ("Cloud computing", "IT delivered as a service over the Internet (2010s onward)", "الحوسبة السحابية: التكنولوجيا كخدمة عبر الإنترنت"),
            ("Edge computing", "processing data on the device itself, instantly, instead of sending it to the cloud", "معالجة البيانات على الجهاز نفسه فورًا"),
            ("Autonomous driving", "uses AI to drive a vehicle without human operation", "القيادة الذاتية: الذكاء الاصطناعي بيسوق من غير إنسان"),
            ("AR", "overlays digital information on real-world images", "الواقع المعزز: معلومات رقمية فوق الصورة الحقيقية"),
            ("VR", "lets users immerse themselves in a virtual space made by a computer", "الواقع الافتراضي: تعيش جوّه عالم افتراضي"),
            ("Quantum computing", "uses quantum mechanics to speed up computations that are hard for traditional computers", "الحوسبة الكمية: بتسرّع حسابات صعبة على الكمبيوتر العادي"),
        ],
        "traps": [
            ("E-commerce means buying goods in physical stores with cash.", False, "It is buying and selling through the Internet."),
            ("VR overlays digital information on real-world images.", False, "That is AR. VR replaces the real world with a virtual one."),
            ("Moore's Law has been said to be approaching a physical limit in recent years.", True, "Transistors are now so small that problems like leakage current appear."),
            ("The correct order is: computer → smartphones → Internet → cloud.", False, "Computer → Internet → smartphones → cloud."),
        ],
        "exam": {"from": (2, "12"), "q": "Analyse how the spread of cloud computing (from the 2010s onward) has changed the way information technology is used. Refer to: large-scale data analysis, AI, and \"IT as a service\".", "marks": 6, "src": "p.10 — Exam-style question [6]"},
    },
    {
        "id": "1-2", "lecture": 3,
        "title": "How AI Works",
        "remember": "AI is the broad field; machine learning sits inside it, deep learning inside machine learning, and today's generative AI is built on deep learning — from the broadest idea to the most specialized.",
        "remember_ar": "الذكاء الاصطناعي هو المجال الواسع؛ جوّاه التعلم الآلي، وجوّه التعلم الآلي التعلم العميق، والذكاء الاصطناعي التوليدي مبني على التعلم العميق.",
        "svg": "NESTED",
        "terms": [
            ("AI (Artificial Intelligence)", "the broad field: technologies that perform intelligent human behaviour on a computer, e.g. speech recognition", "الذكاء الاصطناعي: الكمبيوتر بيعمل سلوك ذكي زي الإنسان"),
            ("Machine learning", "learns patterns from data to make predictions and judgments, e.g. a spam filter", "التعلم الآلي: بيتعلم أنماط من البيانات"),
            ("Deep learning", "uses neural networks on large-scale data to learn complex patterns, e.g. image analysis", "التعلم العميق: شبكات عصبية وبيانات كتير"),
            ("Neural network", "a system modeled on the nerve cells (neurons) of the human brain, used to learn from data", "الشبكة العصبية: متصممة زي خلايا المخ"),
            ("Generative AI", "uses deep learning to generate new data such as text, images and audio, e.g. ChatGPT", "الذكاء الاصطناعي التوليدي: بيولّد بيانات جديدة"),
        ],
        "traps": [
            ("Deep learning is a completely different technology from machine learning.", False, "Deep learning is a type of machine learning."),
            ("AI and machine learning have the same meaning.", False, "AI is the broad concept; machine learning is one technology inside it."),
            ("Generative AI uses deep learning to generate new data.", True, "That is its definition."),
            ("Machine learning follows only fixed rules written by people.", False, "It learns patterns from data."),
        ],
        "exam": {"from": (3, "11"), "q": "Analyse the relationship between AI, machine learning, deep learning and generative AI, with an example of each.", "marks": 6, "src": "p.16 — Exam-style question [6]"},
    },
    {
        "id": "1-3", "lecture": 3,
        "title": "AI in Daily Life and Industry",
        "remember": "AI is good at finding and classifying patterns in data — recommendations, voice, translation, face recognition, and many industry tasks — but human judgment is still needed where ethics, privacy, and responsibility are involved.",
        "remember_ar": "الذكاء الاصطناعي شاطر في إيجاد الأنماط وتصنيفها، بس لسه محتاجين حكم الإنسان لما يكون فيه أخلاق أو خصوصية أو مسؤولية.",
        "svg": "RECSYS",
        "terms": [
            ("Recommendation system", "predicts preferences from past behaviour data and shows recommendations", "نظام التوصيات: بيتوقع اللي هيعجبك من سلوكك"),
            ("Voice assistant", "lets you operate a phone by speaking to it", "المساعد الصوتي: بتكلم الموبايل فينفّذ"),
            ("Machine translation", "converts foreign-language text into your own language", "الترجمة الآلية"),
            ("Face recognition", "identifies a person from their face, e.g. to unlock a phone", "التعرف على الوجه"),
            ("Image-diagnosis AI", "detects diseases from X-ray and CT images (healthcare)", "تشخيص الأمراض من صور الأشعة"),
            ("Predictive maintenance", "predicts when a machine will fail (manufacturing)", "الصيانة التنبؤية: تتوقع إمتى الماكينة هتعطل"),
            ("Black-box problem", "when it is unclear how an AI reached its judgment", "مشكلة الصندوق الأسود: مش عارفين وصل للنتيجة إزاي"),
            ("Hallucination", "generative AI producing information that sounds plausible but is wrong", "الهلوسة: إجابة شكلها مقنع بس غلط"),
        ],
        "traps": [
            ("AI is good at high-speed processing of large amounts of data.", True, "One of its strengths, with recognising images and audio."),
            ("AI can be left to make ethical judgments on its own.", False, "Ethical judgments need human judgment: they may carry discrimination or prejudice."),
            ("The black-box problem means it is clear how an AI reached its judgment.", False, "It means it is unclear."),
            ("Predicting harvest timing and detecting pests is an AI use in agriculture.", True, "From the book's table of industries."),
        ],
        "exam": {"from": (3, "23"), "q": "Analyse why AI is well suited to some tasks but requires caution in others.", "marks": 6, "src": "p.22 — Exam-style question [6]"},
    },
    {
        "id": "1-4", "lecture": 4,
        "title": "Ethical Issues with AI",
        "remember": "If training data is biased, an AI can reproduce that bias; using AI responsibly means checking for bias, being able to explain decisions, and knowing who is accountable — guided by fairness, transparency, privacy protection, and accountability.",
        "remember_ar": "لو بيانات التدريب متحيزة، الذكاء الاصطناعي هيكرر التحيز. الاستخدام المسؤول: نفحص التحيز، ونقدر نفسّر القرار، ونعرف مين المسؤول — بالعدالة والشفافية وحماية الخصوصية والمساءلة.",
        "svg": "BIAS",
        "terms": [
            ("Algorithmic bias", "bias in AI judgments caused by bias in the training data", "التحيز الخوارزمي: سببه تحيز في بيانات التدريب"),
            ("Privacy", "the appropriate handling and protection of personal data", "الخصوصية: التعامل الصح مع البيانات الشخصية"),
            ("Explainable AI (XAI)", "technology that lets humans understand why an AI made a particular judgment", "الذكاء الاصطناعي القابل للتفسير"),
            ("Responsibility", "the roles and duties of each party — who answers when an AI judgment is wrong", "المسؤولية: دور كل طرف"),
            ("Fairness", "not unjustly discriminating against any particular person or group", "العدالة: من غير تمييز ظالم"),
            ("Transparency", "showing the AI's decision-making process clearly", "الشفافية: نوضح إزاي بيقرر"),
            ("Privacy protection", "handling personal information appropriately", "حماية الخصوصية"),
            ("Accountability", "being answerable for the AI's decisions", "المساءلة: حد يتحاسب على القرار"),
        ],
        "traps": [
            ("Algorithmic bias is caused by the AI's processing speed.", False, "It comes from bias in the training data."),
            ("If an AI's process is opaque, there is no problem as long as the result is correct.", False, "An opaque result cannot be checked."),
            ("Who is responsible when an AI is wrong has already been clearly decided.", False, "No clear standard exists yet among developers, users and operators."),
            ("Bias in training data can cause discriminatory bias in AI judgments.", True, "That is exactly algorithmic bias."),
        ],
        "exam": {"from": (4, "14"), "q": "Analyze how algorithmic bias can arise in an AI system, and how it can be reduced, using the principles of AI ethics.", "marks": 6, "src": "p.30 — Exam-style question [6]"},
    },
]

QUICK = [
    ("Which came first: the Internet or the smartphone?", "The Internet (1990s); smartphones came in the 2000s."),
    ("Why does a self-driving car use edge computing?", "A delay of even 0.1 seconds can cause an accident, so it decides on the car itself."),
    ("Is deep learning a kind of machine learning?", "Yes: it sits inside machine learning."),
    ("A spam filter that learns from examples is&#8230;", "machine learning."),
    ("A video site suggests your next clip. Which AI?", "A recommendation system."),
    ("Why must a human keep the final decision on a diagnosis?", "Someone has to be responsible; AI can be a black box and can be wrong."),
    ("A hiring AI rates one group lower. Which principle is broken?", "Fairness."),
    ("Showing users in plain language how the AI decides is&#8230;", "transparency."),
]

EXAM_TIPS = [
    ("Know the definition word for word", "MCQ options often swap two definitions from the same lesson.", "احفظ التعريف بالنص — الاختيارات بتبدّل تعريفين من نفس الدرس."),
    ("One mark, one point", "A [6]-mark answer needs about six separate points. Use each term the question asks for, and explain it.", "سؤال الـ 6 درجات محتاج حوالي 6 نقط منفصلة."),
    ("Give an example", "\"e.g.\" turns a definition into an answer: a spam filter, a hiring AI, Netflix.", "المثال بيحوّل التعريف لإجابة."),
    ("Watch the order", "Stages of IT; the nested layers of AI: say them in order.", "خلّي بالك من الترتيب."),
]


# the exam questions' marking points, copied from each lecture's answer key
# (lectureN/_teacher/exercises.json) by the generator, so this file stands alone
POINTS = {
 "1-1": [
  "Cloud computing spread from the 2010s onward.",
  "It made large-scale data analysis possible, because storage and processing power can be rented rather than owned.",
  "That data and power in turn support AI.",
  "IT became something delivered as a service over the Internet, rather than hardware each organisation buys and maintains.",
  "Effect: smaller organisations and individuals can now use computing power that previously needed a large investment."
 ],
 "1-2": [
  "AI is the broad field: technologies that perform intelligent human behaviour on a computer. Example: speech recognition.",
  "Machine learning sits inside AI: it learns patterns from data to make predictions and judgments. Example: a spam filter.",
  "Deep learning sits inside machine learning: it uses neural networks and large-scale data. Example: image analysis for autonomous driving.",
  "Generative AI is built on deep learning and generates new data. Example: ChatGPT.",
  "The four are nested categories, each more specialised than the one before, not four separate technologies."
 ],
 "1-3": [
  "AI is good at finding and classifying patterns in complex data such as images and text.",
  "It is good at recognition and generation of images, audio and text.",
  "It is good at probabilistic reasoning and prediction from data.",
  "Caution: ethical judgments may carry discrimination or prejudice.",
  "Caution: anything involving personal data raises privacy questions.",
  "Caution: final decision-making — someone has to be responsible for the result."
 ],
 "1-4": [
  "Cause: the AI learns from training data",
  "Biased or insufficient data is reproduced in its judgments, with an example",
  "A second source: past discrimination in data, or proxy variable / variable choice",
  "Reduction through fairness: check data, test results across groups",
  "Reduction through transparency: show the decision process / XAI",
  "Links the measures back to the cause, so the answer is an analysis, not a list"
 ]
}
