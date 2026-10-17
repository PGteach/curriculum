import io, sys, os
N, T, ACC = int(sys.argv[1]), sys.argv[2], sys.argv[3]
for d in ("slides", "quiz", "handout", "homework", "_teacher"):
    os.makedirs("lecture%d/%s" % (N, d), exist_ok=True)
L5T = "Is this connection safe?"
b = io.open("scripts/lecture5_slides_base.html", encoding="utf-8").read()
for a, c in [("<title>Lecture 5 — %s · PGteach</title>" % L5T, "<title>Lecture %d — %s · PGteach</title>" % (N, T)),
             ("const LECTURE_NUM   = 5;", "const LECTURE_NUM   = %d;" % N),
             ('const LECTURE_TITLE = "%s";' % L5T, 'const LECTURE_TITLE = "%s";' % T),
             ('const LECTURE_ACCENT = "#2D7A4B";', 'const LECTURE_ACCENT = "%s";' % ACC)]:
    assert b.count(a) == 1, a; b = b.replace(a, c)
io.open("scripts/lecture%d_slides_base.html" % N, "w", encoding="utf-8", newline="\n").write(b)
q = io.open("lecture5/quiz/index.html", encoding="utf-8").read()
for a, c in [("<title>Lecture 5 Quiz — %s · PGteach</title>" % L5T, "<title>Lecture %d Quiz — %s · PGteach</title>" % (N, T)),
             ("const LECTURE_NUM   = 5;", "const LECTURE_NUM   = %d;" % N),
             ('const LECTURE_TITLE = "%s";' % L5T, 'const LECTURE_TITLE = "%s";' % T)]:
    assert q.count(a) == 1, a; q = q.replace(a, c)
io.open("lecture%d/quiz/index.html" % N, "w", encoding="utf-8", newline="\n").write(q)
print("shell for lecture", N)
