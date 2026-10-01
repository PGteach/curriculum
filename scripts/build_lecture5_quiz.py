# -*- coding: utf-8 -*-
"""Write Lecture 5's quiz questions into lecture5/quiz/index.html.

    python scripts/build_lecture5_quiz.py && python scripts/protect_answers.py 5

The second command is required: this writes plaintext a: indices, and
protect_answers turns them into fingerprints before publishing.

Lecture 5's paper: 20 questions, all on lesson 2-1, Cryptographic
Technologies and Authentication (English textbook pp. 33-40; Arabic
textbook pp. 31-37). Curriculum only. Most are the book's own Worked
Example, Try and Exercise items; the rest are the ministry's assessment
book for the lesson (the TLS handshake, session keys, 2FA, non-repudiation),
which is where the term exam's wording comes from.

Every question has four options, and every wrong option is something from
the same lesson a student who half-knows could genuinely pick: the other
key, the other factor, the other technology.

d: 1 easy, 2 medium, 3 hard -- bandedOrder() on the page runs easy to hard,
shuffling inside each band. v: word glosses, heavy words only, by the thumb
test in README. Syllabus terms (encryption, certificate, possession ...) are
never glossed; they are what is being learned.
"""
import io, re

SECTIONS = [
    "Common-key and public-key cryptography",
    "HTTPS and the TLS handshake",
    "Certificates and signatures",
    "Authentication",
    "Combining security technologies",
]

# (section, difficulty, question, options, answer index, why, src, glosses)
Q = [
    # ================= band 1 =================
    (1, 1, "What is HTTPS?",
     ["A communication protocol that adds TLS encryption to HTTP",
      "A system that allows or denies communication based on rules",
      "A method that combines two or more authentication factors",
      "A certificate that proves a website is genuine"], 0,
     "HTTPS is HTTP with TLS encryption added. The second option is a firewall, from lesson 2-2.",
     "p.34 — Point 1(1)", []),
    (1, 1, "What is the procedure for establishing a secure HTTPS connection called?",
     ["The TLS handshake", "A digital signature", "Multi-factor authentication",
      "Common-key cryptography"], 0,
     "Setting up the secure connection is the TLS handshake. The ministry asks this one directly.",
     "p.34 — Point 1(1); Ministry assessments, period 1", []),
    (0, 1, "In HTTPS, which cryptographic method is used for the data communication after the common key has been shared?",
     ["Common-key cryptography", "Public-key cryptography",
      "A digital signature", "Multi-factor authentication"], 0,
     "Stage 3: data is encrypted with the shared common key, because common-key is fast.",
     "p.37 — Try 1(2)", []),
    (3, 1, "What is multi-factor authentication?",
     ["Combining two or more of the three factors of authentication",
      "Setting one very strong and complex password",
      "Using a fingerprint only to log in",
      "Using an email address with a normal password"], 0,
     "Two or more of knowledge, possession and biometric. Option two is still one factor.",
     "p.35 — Point 2(1); Ministry assessments, period 1", []),
    (3, 1, "Which list gives the three factors of authentication?",
     ["Knowledge, possession, biometric",
      "Speed, efficiency, cost",
      "Public key, private key, password",
      "Wireless, local network, cloud"], 0,
     "Knowledge (what you know), possession (what you have), biometric (your body).",
     "p.35 — Point 2(1); Ministry assessments, form A", []),
    (2, 1, "Which technology verifies that the communication partner is authentic?",
     ["Digital certificate", "Digital signature", "Common-key cryptography",
      "Multi-factor authentication"], 0,
     "The certificate proves the other side is genuine. The signature is about the data: was it altered, and who sent it.",
     "p.36 — technology table; Worked Example (2) c", []),

    # ================= band 2 =================
    (1, 2, "In HTTPS, what cryptographic method is used so that the browser and the server can safely share a common key?",
     ["Public-key cryptography", "Common-key cryptography",
      "A digital signature", "Two-factor authentication"], 0,
     "Stage 2: the common key is locked with the server's public key, so only the server's private key can open it.",
     "p.37 — Try 1(1)", []),
    (1, 2, "Which statement about HTTPS is NOT correct?",
     ["HTTPS exchanges all of its data using public-key cryptography",
      "HTTPS uses both public-key and common-key cryptography",
      "HTTPS protects users from eavesdropping, tampering and impersonation",
      "In HTTPS, the browser checks the server's certificate"], 0,
     "Exchanging all data with public-key would be slow, so the data itself goes by common-key.",
     "p.36 — Worked Example (1) B", []),
    (0, 2, "What does public-key cryptography use?",
     ["A pair of linked keys: a public key and a private key",
      "One key that both locks and unlocks",
      "A password and a one-time password",
      "A quantum bit and a classical bit"], 0,
     "A public key locks; a different private key unlocks. One shared key is common-key cryptography.",
     "p.34 margin; Ministry assessments, form B", []),
    (2, 2, "Which technology detects tampering and impersonation, and provides non-repudiation?",
     ["Digital signature", "Digital certificate", "Common-key cryptography",
      "The TLS handshake"], 0,
     "Non-repudiation — the sender cannot deny having sent it — is the digital signature's.",
     "p.36 — key terms; Ministry assessments, period 2", [["non-repudiation", "عدم التنصل — ميقدرش ينكر إنه بعتها"]]),
    (3, 2, "Which is an example of a possession factor?",
     ["A one-time password sent to a phone, or a smart card",
      "Knowing the answer to a secret question",
      "The user's fingerprint",
      "Recognising the user's face"], 0,
     "Possession is something the user has. A secret question is knowledge; fingerprint and face are biometric.",
     "Ministry assessments, form B", []),
    (3, 2, "A service uses a password plus fingerprint authentication. Which combination of factors is this?",
     ["Knowledge + biometric", "Knowledge + possession",
      "Biometric + possession", "Knowledge + knowledge"], 0,
     "Password is knowledge; fingerprint is biometric.",
     "p.37 — Try 2(1) b", []),
    (3, 2, "Which is NOT an example of multi-factor authentication?",
     ["Password + secret question",
      "Password + smartphone notification",
      "Fingerprint authentication + smart card",
      "Password + SMS authentication"], 0,
     "A password and a secret question are both knowledge — the same factor twice.",
     "p.40 — Exercise 3(2)", []),
    (4, 2, "Which technology prevents communication content from being read by third parties?",
     ["Encryption", "Digital signature", "Digital certificate",
      "Multi-factor authentication"], 0,
     "Encryption keeps the content private. The others prove the data, the site, or the user.",
     "p.36 — Worked Example (2) a; Ministry assessments, period 3", []),

    # ================= band 3 =================
    (1, 3, "Why does HTTPS use public-key cryptography to share the key but common-key cryptography to exchange the data?",
     ["Public-key shares a key safely; common-key exchanges large amounts of data quickly — together, security and speed",
      "Public-key is faster for data; common-key is safer for sharing keys",
      "Common-key is only used when public-key fails",
      "Both are used so that no certificate is needed"], 0,
     "The division of roles: public-key to share keys safely, common-key to move data quickly. Option two swaps the strengths.",
     "p.35 — Point 1(3); p.37 exam-style question", []),
    (2, 3, "During the TLS handshake, what does the browser check about the server's certificate?",
     ["That it is valid, leads back to a trusted authority, and matches the site's name",
      "That the server's password is strong",
      "That the user has a second factor ready",
      "That the data is encrypted with the private key"], 0,
     "Validity, the chain of trust, and a match with the site's name — the Arabic book's wording, and the ministry's.",
     "Arabic book p.32 — table stage 1; Ministry assessments, form C", []),
    (3, 3, "Which is a WRONG example of two-factor authentication, because it uses the same category of factor twice?",
     ["Password + a second secret password",
      "Password + a one-time password sent to the phone",
      "Password + fingerprint",
      "Password + a code from an authenticator app"], 0,
     "Two passwords are both knowledge. This is two-step authentication, not two-factor.",
     "Ministry assessments, period 3; p.37 Worked Example (1) D", []),
    (3, 3, "A password is leaked. Why can a code sent to the owner's phone still keep the account safe?",
     ["The attacker knows the password but does not have the phone — a different factor",
      "The code makes the password stronger and longer",
      "The phone encrypts the password so it cannot be read",
      "The code proves the website is genuine"], 0,
     "One factor is broken; the possession factor still stands. The last option describes a certificate.",
     "p.36 — Pause & Think; p.35 Point 2(2)", []),
    (4, 3, "A user is led to a fake website that looks like their bank. Which technology mainly addresses this?",
     ["Digital certificate", "Encryption", "Digital signature",
      "Common-key cryptography"], 0,
     "A fake site is impersonation of the server, and the certificate is what proves the real one.",
     "p.40 — Exercise 3(1) c", []),
    (4, 3, "Which describes how security is achieved for online shopping and banking?",
     ["By combining encryption, certificates, signatures and multi-factor authentication to reduce many risks",
      "By relying on one technology only, so that it runs quickly",
      "By removing passwords completely",
      "By using common-key encryption alone, without any authentication"], 0,
     "Security comes from layers, each covering a different threat — and none is absolute.",
     "p.35 Point 3(1); Ministry assessments, form B", []),
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

    p = "lecture5/quiz/index.html"
    page = io.open(p, encoding="utf-8").read()
    page = re.sub(r"const SECTIONS = \[.*?\n\];", lambda m: "const SECTIONS = " + secs,
                  page, count=1, flags=re.DOTALL)
    page = re.sub(r"const QUESTIONS = \[.*?\n\];", lambda m: "const QUESTIONS = " + qs,
                  page, count=1, flags=re.DOTALL)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    print("written: %d questions" % len(Q))
