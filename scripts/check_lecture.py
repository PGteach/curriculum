#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check a lecture before you publish it.

    python scripts/check_lecture.py          # every lecture
    python scripts/check_lecture.py 2        # just lecture 2

Catches the mistakes that are easy to make and hard to see: template text left
in place, a QR pointing at the wrong lecture, an answer index off the end of
its options, a section with no questions, a page that will not build on GitHub
Pages. Exits non-zero if anything is wrong, so it can gate a commit.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from protect_answers import fingerprint          # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE_BASE = "https://pgteach.github.io/curriculum"
PAGES = ("slides", "quiz", "handout")
OPTIONAL_PAGES = ("homework",)

TOKEN_RE = re.compile(r"__[A-Z][A-Z_]*__")
LIQUID_RE = re.compile(r"\{[%{]")
HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

# Text that ships in the templates and must be replaced before publishing.
PLACEHOLDERS = [
    "Section name", "The question this slide answers", "First idea",
    "Second idea", "Point one", "Point two", "Row label",
    "A second slide", "Replace this line with", "First section",
    "Second section", "First question for this lecture",
    "Second question?", "Third question", "Fourth question",
    "A wrong answer", "The right answer", "Another wrong answer",
    "Explain in one sentence why that is the answer",
    "First Section", "Second Section", "Third Section",
    "Explain the first idea here", "Its definition", "First term",
    "Second term", "A term worth its own block", "My answer",
    "First question?", "Second question?", "Three or four one-line takeaways",
    "الشرح بالعربي", "سطر المقدمة بالعربي",
]


class Report:
    def __init__(self) -> None:
        self.problems: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0

    def ok(self) -> None:
        self.checks += 1

    def fail(self, msg: str) -> None:
        self.checks += 1
        self.problems.append(msg)

    def warn(self, msg: str) -> None:
        self.checks += 1
        self.warnings.append(msg)

    def want(self, cond: bool, msg: str) -> None:
        self.ok() if cond else self.fail(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def js_of(html: str) -> str:
    blocks = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)
    return blocks[0] if len(blocks) == 1 else ""


def const_of(js: str, name: str) -> str | None:
    m = re.search(r'const\s+%s\s*=\s*"([^"]*)"\s*;' % name, js)
    if m:
        return m.group(1)
    m = re.search(r"const\s+%s\s*=\s*(\d+)\s*;" % name, js)
    return m.group(1) if m else None


def node_available() -> bool:
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def node_check(js: str, label: str, rep: Report) -> None:
    """Parse the page's script the way a browser would."""
    if not node_available():
        rep.warn("%s: node not installed, JavaScript not syntax-checked" % label)
        return
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(js)
        tmp = fh.name
    try:
        out = subprocess.run(["node", "--check", tmp], capture_output=True, text=True,
                         encoding="utf-8")
        if out.returncode != 0:
            first = (out.stderr or "").strip().split("\n")
            detail = next((l for l in first if "Error" in l), first[0] if first else "")
            rep.fail("%s: JavaScript does not parse — %s" % (label, detail.strip()))
        else:
            rep.ok()
    finally:
        Path(tmp).unlink(missing_ok=True)


def quiz_data(js: str, rep: Report) -> dict | None:
    """Pull SECTIONS and QUESTIONS out by evaluating just those two literals."""
    secs = re.search(r"const SECTIONS = (\[.*?\n\];)", js, re.DOTALL)
    ques = re.search(r"const QUESTIONS = (\[.*?\n\];)", js, re.DOTALL)
    if not secs or not ques:
        rep.fail("quiz: could not find the SECTIONS / QUESTIONS arrays")
        return None
    if not node_available():
        rep.warn("quiz: node not installed, questions not validated")
        return None

    prog = ("const SECTIONS = %s\nconst QUESTIONS = %s\n"
            "console.log(JSON.stringify({SECTIONS, QUESTIONS}));"
            % (secs.group(1), ques.group(1)))
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(prog)
        tmp = fh.name
    try:
        out = subprocess.run(["node", tmp], capture_output=True, text=True,
                         encoding="utf-8")
        if out.returncode != 0:
            rep.fail("quiz: SECTIONS/QUESTIONS do not evaluate — %s"
                     % (out.stderr or "").strip().split("\n")[0])
            return None
        return json.loads(out.stdout)
    finally:
        Path(tmp).unlink(missing_ok=True)


def check_common(name: str, html: str, num: int, rep: Report,
                 titles: dict, accents: dict) -> None:
    label = name

    left = sorted(set(TOKEN_RE.findall(html)))
    rep.want(not left, "%s: template placeholder(s) never filled in: %s"
                       % (label, ", ".join(left)))

    liquid = LIQUID_RE.search(html)
    rep.want(not liquid,
             "%s: contains a Liquid delimiter — this fails the GitHub Pages "
             "build and takes the whole site down with it" % label)

    js = js_of(html)
    rep.want(bool(js), "%s: expected exactly one <script> block" % label)
    if not js:
        return
    node_check(js, label, rep)

    got_num = const_of(js, "LECTURE_NUM")
    rep.want(got_num == str(num),
             "%s: LECTURE_NUM is %s but the folder is lecture%d"
             % (label, got_num, num))

    title = const_of(js, "LECTURE_TITLE")
    rep.want(bool(title and title.strip()), "%s: LECTURE_TITLE is empty" % label)
    if title:
        titles[label] = title

    rep.want("SITE_BASE" in js and SITE_BASE in js,
             "%s: SITE_BASE is missing or not %s" % (label, SITE_BASE))

    if name in ("slides", "handout"):
        accent = const_of(js, "LECTURE_ACCENT")
        rep.want(bool(accent and HEX_RE.match(accent)),
                 "%s: LECTURE_ACCENT is not a hex colour (got %r)" % (label, accent))
        if accent:
            accents[label] = accent
        rep.want("encodeURIComponent(LECTURE.quizUrl)" in js,
                 "%s: the QR is not built from this lecture's quiz URL" % label)

    visible = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    visible = re.sub(r"/\*.*?\*/", "", visible, flags=re.DOTALL)
    hits = [p for p in PLACEHOLDERS if p in visible]
    if hits:
        rep.fail("%s: template text still in the page: %s"
                 % (label, ", ".join(sorted(set(hits))[:6])))
    else:
        rep.ok()


def check_slides(html: str, rep: Report) -> None:
    body = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    n = len(re.findall(r'<section class="slide', body))
    rep.want(n >= 2, "slides: only %d slide(s) — did you add any content?" % n)
    rep.want('id="qr"' in html, "slides: the QR slide is missing")
    rep.want('href="../quiz/"' in html, "slides: no relative link to the quiz")

    last = body.rfind('<section class="slide')
    rep.want(last != -1 and 'id="qr"' in body[last:],
             "slides: the QR slide is not the last slide")

    rep.want(len(re.findall(r'class="[^"]*\bar\b', body)) >= 1,
             "slides: no Arabic lines at all — is that intended?")


def check_quiz(html: str, rep: Report) -> None:
    js = js_of(html)
    rep.want("lecture: LECTURE.label" in js,
             "quiz: the submission payload is missing the lecture field")
    rep.want("image: image" in js,
             "quiz: the submission payload is missing the result screenshot")
    rep.want('id="sClass"' in html,
             "quiz: the intake form is missing the class field")
    rep.want("class:  state.klass" in js,
             "quiz: the submission payload is missing the class")
    rep.want('href="../slides/"' in html, "quiz: no relative link back to the slides")

    url = re.search(r'const RESULTS_URL = "([^"]*)"', js)
    if url and not url.group(1):
        rep.warn("quiz: RESULTS_URL is empty — results will not be recorded")
    else:
        rep.want(bool(url and url.group(1).startswith("https://script.google.com/")),
                 "quiz: RESULTS_URL is not an Apps Script /exec URL")

    data = quiz_data(js, rep)
    if not data:
        return
    secs, qs = data["SECTIONS"], data["QUESTIONS"]

    m = re.search(r"const ANSWER_SALT\s*=\s*(\d+)\s*;", js)
    salt = int(m.group(1)) if m else None
    if any("k" in q for q in qs):
        rep.want(salt is not None,
                 "quiz: answers are fingerprinted but ANSWER_SALT is missing")
    salt = salt if salt is not None else 0

    rep.want(len(secs) >= 1, "quiz: SECTIONS is empty")
    rep.want(len(qs) >= 1, "quiz: QUESTIONS is empty")
    rep.want(len(secs) == len(set(secs)), "quiz: two sections share a name")

    used = set()
    for i, q in enumerate(qs, 1):
        where = "quiz: question %d" % i
        opts = q.get("o") or []
        rep.want(bool(str(q.get("q", "")).strip()), "%s has no text" % where)
        rep.want(len(opts) >= 2, "%s has %d option(s), needs at least 2"
                                 % (where, len(opts)))
        rep.want(len(opts) == len(set(opts)), "%s repeats an option" % where)
        rep.want(all(str(o).strip() for o in opts), "%s has a blank option" % where)

        if "k" in q:
            # fingerprinted by protect_answers.py: exactly one option must match
            hits = [o for o in opts if fingerprint(str(o), salt) == q["k"]]
            rep.want(len(hits) == 1,
                     "%s: %d option(s) match the stored answer fingerprint. An "
                     "option's text was almost certainly edited without "
                     "re-running scripts/protect_answers.py, which would make "
                     "every answer count as wrong." % (where, len(hits)))
        else:
            a = q.get("a")
            rep.want(isinstance(a, int) and 0 <= a < len(opts),
                     "%s: answer index %r is outside its %d options"
                     % (where, a, len(opts)))

        s = q.get("s")
        rep.want(isinstance(s, int) and 0 <= s < len(secs),
                 "%s: section index %r has no matching entry in SECTIONS"
                 % (where, s))
        if isinstance(s, int):
            used.add(s)

        rep.want(bool(str(q.get("why", "")).strip()),
                 "%s has no explanation, so the review list will be blank" % where)

    empty = [secs[k] for k in range(len(secs)) if k not in used]
    rep.want(not empty,
             "quiz: section(s) with no questions, so the results bar divides by "
             "zero: %s" % ", ".join(empty))


def check_handout(html: str, rep: Report) -> None:
    n = len(re.findall(r'<section class="sheet"', re.sub(r"<!--.*?-->", "", html,
                                                         flags=re.DOTALL)))
    rep.want(n >= 2, "handout: only %d printed page(s)" % n)
    rep.want('class="pageno"' in html, "handout: page-number slots are missing")
    rep.want("@page{size:A4; margin:0}" in html.replace(" ", " "),
             "handout: @page margin is not 0, so the browser will print its own "
             "header and footer over your sheet")
    rep.want('id="qr"' in html, "handout: the QR panel is missing")


def check_lecture(num: int) -> Report:
    rep = Report()
    folder = ROOT / ("lecture%d" % num)
    titles: dict = {}
    accents: dict = {}

    for name in PAGES + OPTIONAL_PAGES:
        path = folder / name / "index.html"
        if not path.is_file():
            if name not in OPTIONAL_PAGES:
                rep.fail("%s: missing (%s)" % (name, path.relative_to(ROOT)))
            continue
        html = read(path)
        check_common(name, html, num, rep, titles, accents)
        if name == "slides":
            check_slides(html, rep)
        elif name == "quiz":
            check_quiz(html, rep)
        else:
            check_handout(html, rep)
            if name == "homework":
                rep.want("class=\"ex\"" in html,
                         "homework: no exercises on the page")

    if len(set(accents.values())) > 1:
        rep.fail("the slides and the handout use different accent colours: %s"
                 % ", ".join("%s=%s" % kv for kv in sorted(accents.items())))
    else:
        rep.ok()

    # A deck may reasonably carry a shortened form of the booklet's title;
    # only flag titles that are genuinely about different things.
    def norm(t):
        return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()

    vals = [norm(t) for t in titles.values()]
    unrelated = any(a not in b and b not in a
                    for a in vals for b in vals)
    if unrelated:
        rep.warn("the pages carry unrelated titles: %s"
                 % "; ".join("%s=%r" % kv for kv in sorted(titles.items())))
    else:
        rep.ok()

    return rep


def main() -> None:
    args = sys.argv[1:]
    if args and not args[0].isdigit():
        sys.exit(__doc__)

    if args:
        nums = [int(args[0])]
    else:
        nums = sorted(int(p.name[7:]) for p in ROOT.glob("lecture*")
                      if p.is_dir() and p.name[7:].isdigit())
    if not nums:
        sys.exit("No lecture folders found in %s" % ROOT)

    bad = 0
    for num in nums:
        rep = check_lecture(num)
        head = "Lecture %d" % num
        if rep.problems:
            bad += 1
            print("%s — %d problem(s), %d check(s) run"
                  % (head, len(rep.problems), rep.checks))
            for p in rep.problems:
                print("  FAIL  %s" % p)
        else:
            print("%s — all %d checks passed" % (head, rep.checks))
        for w in rep.warnings:
            print("  warn  %s" % w)
        print()

    if bad:
        sys.exit("%d lecture(s) need fixing before publishing." % bad)
    print("Ready to publish.")


if __name__ == "__main__":
    main()
