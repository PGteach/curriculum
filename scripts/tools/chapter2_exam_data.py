# -*- coding: utf-8 -*-
"""Write lecture7/_teacher/chapter2-exam.json: the Chapter 2 exam.

    python scripts/tools/chapter2_exam_data.py && python scripts/build_chapter2_exam.py

Every item is from the textbook's own questions or the ministry's assessment
book for the first term, and says which in `src`. Ministry items are
translated into the textbook's English. Nothing is invented. Options are
written correct-first; `pos` is the letter it is printed at.
"""
import io, json

LEVELS = [
    {"name": "Level 1 · Remember", "nameAr": "المستوى الأول — التذكر"},
    {"name": "Level 2 · Understand", "nameAr": "المستوى التاني — الفهم"},
    {"name": "Level 3 · Apply and analyse", "nameAr": "المستوى التالت — التطبيق والتحليل"},
]

def q(level, lesson, text, opts, src):
    return {"level": level, "lesson": lesson, "q": text, "o": opts, "src": src}

MCQ = [
    # ================= level 0 · recall =================
    q(0, "2-1", "A protocol in which HTTP is carried over a secured TLS connection, giving confidentiality and integrity of data in transit, is known as:",
      ["HTTPS", "FTP", "SMTP", "DNS"],
      "Ministry assessments, lesson 2-1, weekly model A, MCQ 1; Book p.34"),
    q(0, "2-1", "Using two independent factors from two different categories to prove identity is known as:",
      ["Two-factor authentication (2FA)", "Symmetric encryption", "A digital signature", "A digital certificate"],
      "Ministry assessments, lesson 2-1, weekly model A, MCQ 2"),
    q(0, "2-1", "Which accurately lists the categories of factors used in multi-factor authentication (MFA)?",
      ["Knowledge, possession and biometric", "Speed, efficiency and cost",
       "Public key, private key and password", "Wireless, local network and cloud"],
      "Ministry assessments, lesson 2-1, weekly model A, MCQ 4; Book p.35"),
    q(0, "2-2", "What is the term for a system that monitors network traffic and allows or blocks it according to defined security rules?",
      ["A firewall", "A virtual private network (VPN)", "A DMZ", "Zero trust"],
      "Ministry assessments, lesson 2-2, period 1, MCQ 2; Book p.42"),
    q(0, "2-2", "What is the area called in which public-facing servers are isolated from the internal network to reduce the impact of attacks?",
      ["The DMZ (demilitarized zone)", "The perimeter", "The communication path", "The endpoints"],
      "Ministry assessments, lesson 2-2, weekly model A, MCQ 2; Book p.42"),
    q(0, "2-3", "Which is a typical example of a security incident that affects the availability of a service?",
      ["A service outage caused by attacks on the server", "Personal or confidential information leaked to the outside",
       "Data altered within a system without authorization", "Response procedures and structures set up in advance"],
      "Ministry assessments, lesson 2-3, period 1, MCQ 1; Book p.49"),
    q(0, "2-3", "Which first stage of incident response aims to set up response procedures and structures in advance, in preparation for incidents?",
      ["Preparation", "Detection", "Containment", "Recovery"],
      "Ministry assessments, lesson 2-3, period 1, MCQ 2; Book p.49"),
    q(0, "2-3", "How is the risk score calculated in the simplified risk matrix?",
      ["Impact × likelihood", "Impact + likelihood", "Impact − likelihood", "Impact ÷ likelihood"],
      "Ministry assessments, lesson 2-3, period 1 home tasks, MCQ 2; Book p.50"),

    # ================= level 1 · understand =================
    q(1, "2-1", "Which technology is mainly used to encrypt session data quickly and efficiently after the handshake and the agreement on security are complete?",
      ["Symmetric (common-key) encryption", "Public-key encryption", "A digital signature", "A digital certificate"],
      "Ministry assessments, lesson 2-1, period 1, MCQ 1; Book p.35"),
    q(1, "2-1", "What are the steps called that set up a secure connection and verify the server's identity and domain name over HTTPS?",
      ["The TLS handshake", "A digital signature", "Two-factor authentication", "Symmetric encryption"],
      "Ministry assessments, lesson 2-1, period 1, MCQ 2; Book p.34"),
    q(1, "2-1", "Which technology detects tampering and impersonation, and provides evidence that supports non-repudiation?",
      ["A digital signature", "Symmetric encryption", "The TLS handshake", "Two-factor authentication"],
      "Ministry assessments, lesson 2-1, period 2, MCQ 2; Book p.36"),
    q(1, "2-2", "Which is the precise definition of defense in depth in network security?",
      ["Several layers of controls, so the others reduce the risk if one fails",
       "Relying completely on one strong firewall at the edge of the network",
       "Trusting every device inside the organization's site automatically",
       "Encrypting traffic only when public Wi-Fi is used"],
      "Ministry assessments, lesson 2-2, period 1, MCQ 1; Book p.43"),
    q(1, "2-2", "Which layer of defense in depth is directly linked to installing antivirus software and keeping the operating system updated?",
      ["Endpoints", "Network entry", "Communication path", "Server placement"],
      "Ministry assessments, lesson 2-2, period 2 home tasks, MCQ 2; Book p.43"),
    q(1, "2-2", "Which is the most appropriate reason for providing a DMZ?",
      ["To prevent damage to the internal network even if a public-facing server is attacked",
       "To improve communication speed", "To expose all servers to the outside",
       "To automatically detect and remove viruses"],
      "Book p.47 — Exercise 3(1)"),
    q(1, "2-3", "What is the term for isolating the affected part, or limiting its effect, to stop the problem spreading?",
      ["Containment", "Preparation", "Detection", "Recovery"],
      "Ministry assessments, lesson 2-3, period 1 home tasks, MCQ 1; Book p.49"),
    q(1, "2-3", "What is meant by impact in risk assessment?",
      ["The amount of damage if the risk occurs", "How likely the event is to happen",
       "How fast the team responds to the incident", "How many times the incident has happened"],
      "Ministry assessments, lesson 2-3, period 2 home tasks, MCQ 2; Book p.50"),
    q(1, "2-3", "Which stage returns systems and services to a safe, normal state, and may include restoring from a clean backup?",
      ["Recovery", "Preparation", "Containment", "Lessons learned and improvement"],
      "Ministry assessments, lesson 2-3, period 2, MCQ 1; Book p.49"),

    # ================= level 2 · apply and reason =================
    q(2, "2-1", "Which is a WRONG example of two-factor authentication, because both factors are from the same category (knowledge)?",
      ["Password + a second secret password", "Password + a one-time password sent to the phone",
       "Password + fingerprint", "Password + a code from an authenticator app"],
      "Ministry assessments, lesson 2-1, period 3 home tasks, MCQ 2; Book p.37 Worked Example (1) D"),
    q(2, "2-1", "Which is NOT an appropriate description of combinations of security technologies?",
      ["Digital signatures are a technology that improves communication speed",
       "Encryption prevents communication content from being read by third parties",
       "Digital certificates verify that the communication partner is authentic",
       "Combining several security technologies addresses various threats"],
      "Book p.38 — Try 2(2)"),
    q(2, "2-2", "What is the basic assumption of zero trust in protecting an organization's resources?",
      ["Nothing is trusted just for being inside; identity and context are checked",
       "Every device or user inside the organization's network is fully trusted automatically",
       "Relying completely on the outer perimeter, without checking internal applications",
       "Encrypting email only, without attention to access permissions"],
      "Ministry assessments, lesson 2-2, period 2, MCQ 2; Book p.43"),
    q(2, "2-2", "Which concept describes the traditional boundary that assumes inside the organization's network is completely safe and outside is not — a boundary blurred by cloud services and remote work?",
      ["The perimeter", "The DMZ", "Edge computing", "Quantum superposition"],
      "Ministry assessments, lesson 2-2, period 2 home tasks, MCQ 1; Book p.46"),
    q(2, "2-2", "Which is NOT an appropriate use of a VPN?",
      ["Automatically deleting files infected with viruses", "Connecting safely from home to an organization's network",
       "Connecting offices in different locations safely", "Encrypting communication content on public Wi-Fi"],
      "Book p.45 — Try 2(1)"),
    q(2, "2-3", "In the risk evaluation matrix, how are risks with high impact and low likelihood usually classed?",
      ["Medium", "Very high", "Very low", "None"],
      "Ministry assessments, lesson 2-3, weekly model C, MCQ 3; Book p.50 matrix"),
    q(2, "2-3", "Which most appropriately describes the order of incident response?",
      ["Preparation → Detection → Containment → Eradication → Recovery → Prevention of recurrence",
       "Detection → Eradication → Containment → Recovery",
       "Detection → Recovery → Containment → Prevention of recurrence",
       "Containment → Detection → Eradication → Preparation"],
      "Book p.54 — Exercise 3(2)"),
]

# Six of each letter, never three of one in a row, and no pattern across
# lessons a guesser could ride.
POS = "BDACABDCADCBDACBACBDBADC"
assert len(POS) == len(MCQ)
for item, p in zip(MCQ, POS):
    item["pos"] = p

ESSAY = [
    {"marks": 2, "lesson": "2-3", "lines": 7,
     "q": "What is meant by a security incident? Give two typical examples.",
     "model": "A security incident is a situation in which actual damage occurs due to an information security problem. Examples: an information leak (personal or confidential information leaked to the outside), data tampering, or a service outage caused by attacks on the server.",
     "points": ["Correct definition: actual damage from an information security problem (1)",
                "Two of the three typical examples (1)"],
     "src": "Ministry assessments, lesson 2-3, period 1, essay 1; Book p.49"},
    {"marks": 3, "lesson": "2-2", "lines": 10,
     "q": "Why is placing a public web server in a DMZ safer than placing it directly inside the organization's internal network?",
     "model": "The public web server is the part most exposed to attack from the Internet. In a DMZ it is kept separate from the internal network, so if it is attacked the attacker still cannot reach the internal network and its confidential data. Inside the internal network, a hacked public server would give the attacker a way straight in.",
     "points": ["The public server is the most exposed to attack (1)",
                "The DMZ keeps it separate from the internal network (1)",
                "So an attack on it does not reach the internal network / its data (1)"],
     "src": "Ministry assessments, lesson 2-2, period 1 home tasks, essay 2; Book p.43 Pause & Think"},
    {"marks": 3, "lesson": "2-1", "lines": 10,
     "q": "Explain how using a second, independent factor (such as an authenticator app or an SMS code) prevents an account being broken into, even if the main password is leaked.",
     "model": "The password is one factor: knowledge. The second factor is from a different category: possession — a code sent to the owner's phone or shown in their app. An attacker who has the leaked password still does not have the owner's device, so cannot get the code, and the login is blocked.",
     "points": ["The password is only one factor, knowledge (1)",
                "The second factor is a different category, possession, which the attacker does not have (1)",
                "So knowing the password alone is not enough to log in (1)"],
     "src": "Ministry assessments, lesson 2-1, weekly model B, essay 4; Book p.36 Pause & Think"},
    {"marks": 4, "lesson": "2-2", "lines": 12,
     "q": "Compare traditional security with zero trust, and explain why traditional designs alone are no longer enough today.",
     "model": "Traditional security protects a perimeter, on the idea that inside the organization's network is safe and outside is dangerous, so users inside are trusted once they are in. Zero trust trusts no communication automatically, even from inside the network, and verifies every access — identity, permissions and context — every time. Traditional designs alone are no longer enough because cloud services and remote work have blurred the line between inside and outside, so protecting only the perimeter leaves gaps.",
     "points": ["Traditional: protects the perimeter; inside is assumed safe (1)",
                "Zero trust: no automatic trust, even inside (1)",
                "Zero trust verifies every access (identity, permissions, context) (1)",
                "Why traditional is not enough: cloud services and remote work blurred inside and outside (1)"],
     "src": "Ministry assessments, lesson 2-2, weekly model A, essay 4; Book p.43"},
    {"marks": 6, "lesson": "2-3", "lines": 16,
     "q": "Explain why the six stages of incident response must be carried out in order, using recovery and eradication as an example. Refer to what happens if the cause is not removed.",
     "model": "Each stage depends on the one before it. Containment comes first, to stop the damage spreading; eradication then removes the cause, such as the malware; only after that does recovery return the systems to normal. If recovery is done before eradication, the systems are restored while the cause is still there, so the same incident can happen again and the work has to be repeated. Following the order keeps the damage small and stops the incident returning; in practice, if recovery reveals traces of the threat, the team goes back to containment or eradication.",
     "points": ["Containment first stops the damage spreading (1)",
                "Eradication removes the cause, e.g. the malware (1)",
                "Recovery returns systems to normal only after that (1)",
                "If recovery comes before eradication, the cause is still there (1)",
                "So the same incident can happen again (1)",
                "Conclusion: order keeps damage small / the team may step back a stage (1)"],
     "src": "Book p.51 — Exam-style question [6]; Ministry assessments, lesson 2-3, weekly model A, essay 4"},
    {"marks": 6, "lesson": "2-1", "lines": 16,
     "q": "Explain why HTTPS uses public-key cryptography to share the key but common-key cryptography to exchange the data. Refer to security and speed.",
     "model": "HTTPS needs the same common key on both sides, but sending it openly would let an eavesdropper copy it. Public-key cryptography solves this: the browser locks the common key with the server's public key, and only the server's private key can unlock it, so the key is shared safely. But public-key cryptography is slow, so exchanging all the data with it would make the connection slow. Common-key cryptography is fast, so once the key is shared, the data is exchanged with it. This division of roles gives both security and speed.",
     "points": ["Both sides need the same common key, and sharing it openly is not safe (1)",
                "Public-key cryptography shares the key safely: public key locks, private key unlocks (1)",
                "Public-key cryptography is slow for large amounts of data (1)",
                "Common-key cryptography exchanges large amounts of data quickly (1)",
                "So public-key is used only to share the key, common-key for the data (1)",
                "Result: security and speed together (1)"],
     "src": "Book p.37 — Exam-style question [6]; Ministry assessments, lesson 2-1, weekly model B, essay 2"},
]

EXAM = {
    "title": "Chapter 2 Exam",
    "unit": "Cybersecurity",
    "lessons": "Lessons 2-1 to 2-3",
    "minutes": 70,
    "note": "Every item comes from the textbook's own questions (Try, Worked Example, Exercise, exam-style) or the ministry's assessment book for the first term, translated into the textbook's English, and says which in `src`. Options are written correct-first; `pos` is the printed letter.",
    "levels": LEVELS,
    "mcq": MCQ,
    "essay": ESSAY,
}
io.open("lecture7/_teacher/chapter2-exam.json", "w", encoding="utf-8", newline="\n").write(
    json.dumps(EXAM, ensure_ascii=False, indent=1) + "\n")
print("chapter 2 exam: %d MCQ, %d essays" % (len(MCQ), len(ESSAY)))
