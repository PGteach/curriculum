# -*- coding: utf-8 -*-
"""Write Lecture 6's quiz questions into lecture6/quiz/index.html.

    python scripts/build_lecture6_quiz.py && python scripts/protect_answers.py 6

The second command is required: this writes plaintext a: indices, and
protect_answers turns them into fingerprints before publishing.

Lecture 6's paper: 20 questions, all on lesson 2-2, Network Security Design
(English textbook pp. 41-47; Arabic textbook pp. 38-43). Curriculum only:
the book's own Worked Example, Try and Exercise items, and the ministry's
assessment book for the lesson (the perimeter, zero trust's checks, the
layer each measure belongs to).

Every question has four options, every wrong option taken from the same
lesson. d: 1 easy, 2 medium, 3 hard -- the page runs easy to hard.
"""
import io, re

SECTIONS = [
    "Firewalls",
    "VPN",
    "DMZ",
    "Defense in depth",
    "Zero trust and the perimeter",
]

# (section, difficulty, question, options, answer index, why, src, glosses)
Q = [
    # ================= band 1 =================
    (0, 1, "What is a firewall?",
     ["A system at a network's entry/exit point that allows or denies communication based on rules set in advance",
      "An encrypted virtual private line over the Internet",
      "An area where public-facing servers are kept apart from the internal network",
      "Software that removes viruses from each device"], 0,
     "Allows or denies by rules. The other three are a VPN, a DMZ and endpoint protection.",
     "p.42 — Point 1(1)", []),
    (1, 1, "What is the three-letter abbreviation for the technology that creates an encrypted virtual private line over the Internet?",
     ["VPN", "DMZ", "MFA", "TLS"], 0,
     "VPN — virtual private network.",
     "p.45 — Try 1 (2)", []),
    (2, 1, "What is a DMZ?",
     ["An area where servers exposed to the external network are placed separately from the internal network",
      "A system that exposes all servers to the outside",
      "A line that connects offices in different locations",
      "A rule that blocks all communication from outside"], 0,
     "Web and mail servers go in the DMZ, apart from the internal network.",
     "p.42 — Point 3(1); p.44 Worked Example (1) C", []),
    (3, 1, "What is the concept of layering multiple security measures called?",
     ["Defense in depth", "Zero trust", "The perimeter", "Multi-factor authentication"], 0,
     "Layering measures so that if one is breached the next still protects the system.",
     "p.45 — Try 1 (4)", []),
    (4, 1, "Which describes zero trust?",
     ["No communication is trusted, and it is always verified",
      "Access from inside the organization's network is safe, so verification is unnecessary",
      "A firewall alone is sufficient to protect the network",
      "Only access from outside needs to be monitored"], 0,
     "Zero trust verifies every access — inside or outside.",
     "p.47 — Exercise 3(2)", []),
    (1, 1, "Which is a main use of a VPN?",
     ["Connecting safely to the organization's network from home or while away",
      "Removing viruses from the hard disk automatically",
      "Making the public Internet faster without passwords",
      "Managing large databases through a graphical interface"], 0,
     "Remote work, and connecting branches.",
     "p.42 — Point 2(2); Ministry assessments, form A", []),

    # ================= band 2 =================
    (1, 2, "Which is NOT an appropriate use of a VPN?",
     ["Automatically deleting files infected with viruses",
      "Connecting safely from home to an organization's network",
      "Connecting offices in different locations safely",
      "Encrypting communication content on public Wi-Fi"], 0,
     "Deleting infected files is antivirus software on the endpoints.",
     "p.45 — Try 2(1)", []),
    (1, 2, "Why does a VPN reduce the risk of eavesdropping on public Wi-Fi?",
     ["The communication content is encrypted",
      "It blocks every other user from the Wi-Fi",
      "It moves the user's device into a DMZ",
      "It checks the user's fingerprint"], 0,
     "Inside the tunnel the content is encrypted, so someone listening sees only scrambled data.",
     "p.42 — Point 2(3)", [["eavesdropping", "التنصت — حد بيسمع أو بيقرا من غير إذن"]]),
    (2, 2, "What is the most appropriate reason for providing a DMZ?",
     ["To prevent damage to the internal network even if a public-facing server is attacked",
      "To improve communication speed",
      "To expose all servers to the outside",
      "To automatically detect and remove viruses"], 0,
     "The DMZ is about containing an attack on a public server, not about speed.",
     "p.47 — Exercise 3(1)", []),
    (3, 2, "Which layer of defense in depth does installing antivirus software and keeping the OS updated belong to?",
     ["Endpoints", "Network entry", "Communication path", "Server placement"], 0,
     "Layer 4 — the devices themselves.",
     "p.43 — Point 4(2); Ministry assessments, period 2", []),
    (3, 2, "Which layer does encrypting communication with a VPN belong to?",
     ["Communication path", "Network entry", "Server placement", "Endpoints"], 0,
     "Layer 2: the VPN protects the path the data travels.",
     "p.45 — Try 2(2) b", []),
    (0, 2, "A firewall allows outside users to reach the web server. What should it do with direct external access to the database server?",
     ["Deny it", "Allow it, because the web server is allowed",
      "Encrypt it with a VPN", "Move it to the DMZ"], 0,
     "The book's example: allow the web server, deny direct external access to the database.",
     "p.42 — Point 1(1) e.g.", []),
    (4, 2, "What is the perimeter?",
     ["The traditional boundary that assumes inside the network is safe and outside is dangerous",
      "The area where public-facing servers are placed",
      "The encrypted tunnel of a VPN",
      "The last layer of defense in depth"], 0,
     "Cloud services and remote work have blurred it.",
     "p.46 — key terms; Ministry assessments, period 2 home tasks", []),
    (4, 2, "Under zero trust, what happens when a user inside the organization's network asks for a resource?",
     ["Identity and access permissions are checked, every time",
      "Access is given automatically, because the user is inside",
      "Only the firewall decides, once a day",
      "The user is moved to the DMZ"], 0,
     "Even inside access is verified every time.",
     "p.43 — Point 5(1) e.g.", []),

    # ================= band 3 =================
    (3, 3, "Why does defense in depth protect an organization better than a firewall alone?",
     ["If one measure is breached, the next can still protect the system",
      "A firewall is slower than several measures together",
      "Defense in depth removes the need for any firewall",
      "It trusts everything inside the network"], 0,
     "That is the whole point: one breach does not expose everything.",
     "p.45 — exam-style question", []),
    (4, 3, "Why have designs that protect only the perimeter become insufficient?",
     ["Cloud services and remote work have blurred the line between inside and outside",
      "Firewalls have stopped working",
      "VPNs made the Internet safe",
      "Attackers now attack only from inside"], 0,
     "Data sits in the cloud and staff work from home, so the 'inside' is no longer one place.",
     "p.43 — Point 5(2)", []),
    (4, 3, "Zero trust checks three things when access is requested. Which three?",
     ["Identity, permissions and context",
      "Speed, efficiency and cost",
      "Public key, private key and password",
      "Firewall, VPN and DMZ"], 0,
     "Who is asking, whether they may, and whether the request fits.",
     "Arabic book p.40 — Point 5(1); Ministry assessments, form B", []),
    (2, 3, "A public web server in the DMZ is attacked. What is the most likely result?",
     ["The internal network is still protected",
      "The attacker reaches the internal database at once",
      "Every server is exposed to the Internet",
      "The VPN stops working"], 0,
     "That is what separating it achieves: an attack there does not reach the internal network.",
     "p.43 — DMZ figure; p.42 Point 3(2)", []),
    (3, 3, "Which matches each measure to its layer correctly?",
     ["Firewall — network entry; VPN — communication path; DMZ — server placement; antivirus — endpoints",
      "Firewall — endpoints; VPN — server placement; DMZ — network entry; antivirus — communication path",
      "Firewall — communication path; VPN — network entry; DMZ — endpoints; antivirus — server placement",
      "Firewall — server placement; VPN — endpoints; DMZ — communication path; antivirus — network entry"], 0,
     "Entry, path, placement, endpoints — in that order.",
     "p.43 — Point 4(2)", []),
    (0, 3, "Which statement about a firewall is correct?",
     ["It can sit at the network boundary, between parts of a network, or on a host",
      "It encrypts all communication on public Wi-Fi",
      "It is enough on its own to protect a network",
      "It places public servers in a separate zone"], 0,
     "The Arabic book adds where a firewall can sit. Encrypting is a VPN; the separate zone is a DMZ.",
     "Arabic book p.39 — Point 1(1)", []),
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

    p = "lecture6/quiz/index.html"
    page = io.open(p, encoding="utf-8").read()
    page = re.sub(r"const SECTIONS = \[.*?\n\];", lambda m: "const SECTIONS = " + secs,
                  page, count=1, flags=re.DOTALL)
    page = re.sub(r"const QUESTIONS = \[.*?\n\];", lambda m: "const QUESTIONS = " + qs,
                  page, count=1, flags=re.DOTALL)
    io.open(p, "w", encoding="utf-8", newline="\n").write(page)
    print("written: %d questions" % len(Q))
