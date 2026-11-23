# -*- coding: utf-8 -*-
"""Make a chapter revision's shell and builders, from lecture 5's like every
lecture's -- but writing to revision/chapterK/, not to a lecture folder.

    python scripts/tools/derive_revision.py K "Title" "#accent"   # once: the shell
    python scripts/tools/derive_revision.py K                     # the builders

The sources are scripts/tools/revisionK/ (content.py, slides.py, css.txt,
doc.txt, script.js, spec.py, booklet.py). The builders are derived with the
ordinary derive_slides.py and derive_print.py under a stand-in lecture number
(900 + K), then every path and label is moved to the revision:

    scripts/build_revisionK_slides.py   -> revision/chapterK/slides/
    scripts/build_revisionK.py          -> revision/chapterK/handout/, homework/, _teacher/
    scripts/revisionK_slides_base.html     the deck's shell

Each page's LECTURE CONFIG gets PAGE_PATH and PAGE_LABEL (revisionize()),
from which its quiz link, QR code and recorded results are built; see
scripts/units.py. Run from the repo root.
"""
import io, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)

REVISIONIZE = r'''
def revisionize(html, k):
    """A revision page builds its links and label from PAGE_PATH and
    PAGE_LABEL, not from a lecture number (see scripts/units.py)."""
    num = re.search(r"const LECTURE_NUM\s*=\s*%d;" % k, html)
    assert num, "no LECTURE_NUM = %d in the page" % k
    if "const PAGE_PATH" not in html:
        html = (html[:num.end()]
                + '\nconst PAGE_PATH     = "revision/chapter%d";   /* a revision, not a lecture */' % k
                + '\nconst PAGE_LABEL    = "Chapter %d Revision";' % k
                + html[num.end():])
    html = html.replace('"Lecture " + LECTURE_NUM', "PAGE_LABEL")
    html = html.replace('"/lecture" + LECTURE_NUM + "/', '"/" + PAGE_PATH + "/')
    assert '"Lecture " + LECTURE_NUM' not in html and '"/lecture" + LECTURE_NUM' not in html
    return html
'''
exec(REVISIONIZE)


def shell(k, title, accent):
    """The deck's shell and the quiz page, as new_shell.py makes them for a
    lecture, then revisionized."""
    for d in ("slides", "quiz", "handout", "homework", "_teacher"):
        os.makedirs("revision/chapter%d/%s" % (k, d), exist_ok=True)
    L5T = "Is this connection safe?"
    b = io.open("scripts/lecture5_slides_base.html", encoding="utf-8").read()
    for a, c in [("<title>Lecture 5 — %s · PGteach</title>" % L5T, "<title>Chapter %d Revision — %s · PGteach</title>" % (k, title)),
                 ("const LECTURE_NUM   = 5;", "const LECTURE_NUM   = %d;" % k),
                 ('const LECTURE_TITLE = "%s";' % L5T, 'const LECTURE_TITLE = "%s";' % title),
                 ('const LECTURE_ACCENT = "#2D7A4B";', 'const LECTURE_ACCENT = "%s";' % accent)]:
        assert b.count(a) == 1, a; b = b.replace(a, c)
    io.open("scripts/revision%d_slides_base.html" % k, "w", encoding="utf-8", newline="\n").write(revisionize(b, k))
    q = io.open("lecture5/quiz/index.html", encoding="utf-8").read()
    for a, c in [("<title>Lecture 5 Quiz — %s · PGteach</title>" % L5T, "<title>Chapter %d Revision Quiz — %s · PGteach</title>" % (k, title)),
                 ("const LECTURE_NUM   = 5;", "const LECTURE_NUM   = %d;" % k),
                 ('const LECTURE_TITLE = "%s";' % L5T, 'const LECTURE_TITLE = "%s";' % title)]:
        assert q.count(a) == 1, a; q = q.replace(a, c)
    io.open("revision/chapter%d/quiz/index.html" % k, "w", encoding="utf-8", newline="\n").write(revisionize(q, k))
    print("shell for Chapter %d Revision" % k)


def builders(k):
    t = 900 + k                                     # the stand-in lecture number
    src = "scripts/tools/revision%d" % k
    # the deck
    subprocess.run([sys.executable, "scripts/tools/derive_slides.py", str(t)]
                   + ["%s/%s" % (src, f) for f in ("content.py", "slides.py", "css.txt", "doc.txt", "script.js")], check=True)
    s = io.open("scripts/build_lecture%d_slides.py" % t, encoding="utf-8").read()
    os.remove("scripts/build_lecture%d_slides.py" % t)
    s = (s.replace('DST = "lecture%d/slides/index.html"' % t, 'DST = "revision/chapter%d/slides/index.html"' % k)
          .replace("scripts/lecture%d_slides_base.html" % t, "scripts/revision%d_slides_base.html" % k)
          .replace("/* lecture %d's drawings */" % t, "/* the Chapter %d Revision's drawings */" % k))
    assert str(t) not in s, [l for l in s.split("\n") if str(t) in l]
    io.open("scripts/build_revision%d_slides.py" % k, "w", encoding="utf-8", newline="\n").write(s)
    # the printed pages: the spec says N = 900 + K only while deriving
    spec = io.open("%s/spec.py" % src, encoding="utf-8").read()
    tmp = "%s/_spec_tmp.py" % src
    io.open(tmp, "w", encoding="utf-8", newline="\n").write(re.sub(r"(?m)^N = \d+$", "N = %d" % t, spec))
    try:
        subprocess.run([sys.executable, "scripts/tools/derive_print.py", tmp], check=True)
    finally:
        os.remove(tmp)
    s = io.open("scripts/build_lecture%d.py" % t, encoding="utf-8").read()
    os.remove("scripts/build_lecture%d.py" % t)
    for a, b in [('T = ROOT / "lecture%d" / "_teacher"' % t, 'T = ROOT / "revision" / "chapter%d" / "_teacher"' % k),
                 ("build_lecture%d_slides.py" % t, "build_revision%d_slides.py" % k),
                 ('.replace("__LECTURE_NUM__", "%d")' % t, '.replace("__LECTURE_NUM__", "%d")' % k),
                 ("' &middot; Lecture %d</div>" % t, "' &middot; Chapter %d Revision</div>" % k),
                 ('L%d = "Lecture %d %%s — " + TITLE' % (t, t), 'LREV = "Chapter %d Revision %%s — " + TITLE' % k),
                 ("L%d %%" % t, "LREV %"),
                 ("lecture%d/" % t, "revision/chapter%d/" % k)]:
        assert a in s, a
        s = s.replace(a, b)
    # every printed page is revisionized as it comes out of the shell
    hook = '          .replace("__ACCENT__", ACCENT))\n'       # the end of the placeholder fill-in
    assert s.count(hook) == 1
    s = s.replace(hook, hook + "    t = revisionize(t, %d)\n" % k, 1)
    s = s.replace("\n\ndef shell():", "\n" + REVISIONIZE + "\n\ndef shell():", 1)
    assert str(t) not in s, [l for l in s.split("\n") if str(t) in l]
    io.open("scripts/build_revision%d.py" % k, "w", encoding="utf-8", newline="\n").write(s)
    print("written build_revision%d_slides.py and build_revision%d.py" % (k, k))


if __name__ == "__main__":
    k = int(sys.argv[1])
    if len(sys.argv) > 2:
        shell(k, sys.argv[2], sys.argv[3])
    else:
        builders(k)
