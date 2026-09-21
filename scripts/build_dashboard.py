#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the teacher dashboard at dashboard/index.html.

    python scripts/build_dashboard.py

Everything on the page is read out of the lecture folders themselves --
titles, accent colours, slide counts, question counts, exercise counts,
which materials exist -- so the dashboard cannot drift from what is
actually published. Re-run it after adding or changing a lecture.

The one control on the page is the exam-code switch. The dashboard and the
decks are served from the same origin, so a flag written to localStorage
here is read by the deck; the teacher flips it in their own browser and the
code appears on their slides. Every other browser, including every
student's, keeps the default and the code stays covered.
"""

from __future__ import annotations

import io
import json
import re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://pgteach.github.io/curriculum"
OUT = ROOT / "dashboard" / "index.html"
FLAG = "pgteach.examCode"          # shared with the decks


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def const(js: str, name: str):
    m = re.search(r'const\s+%s\s*=\s*"([^"]*)"\s*;' % name, js)
    if m:
        return m.group(1)
    m = re.search(r"const\s+%s\s*=\s*(\d+)\s*;" % name, js)
    return m.group(1) if m else None


def scan(num: int) -> dict | None:
    folder = ROOT / ("lecture%d" % num)
    if not folder.is_dir():
        return None
    slides = read(folder / "slides" / "index.html")
    quiz = read(folder / "quiz" / "index.html")
    if not slides:
        return None

    info = {
        "num": num,
        "title": const(slides, "LECTURE_TITLE") or "Lecture %d" % num,
        "topic": const(slides, "LECTURE_TOPIC") or "",
        "accent": const(slides, "LECTURE_ACCENT") or "#0E7C7B",
        "slides": len(re.findall(r'<section class="slide', slides)),
        "diagrams": len(re.findall(r"<svg", slides)),
        "photos": len(list((folder / "slides" / "media").glob("*.jpg")))
                  + len(list((folder / "slides" / "media").glob("*.png")))
                  + len(list((folder / "slides" / "media").glob("*.jpeg")))
                  + len(list((folder / "slides" / "media").glob("*.JPG"))),
        "pages": {},
    }

    m = re.search(r"const QUESTIONS = (\[.*?\n\];)", quiz, re.DOTALL)
    info["questions"] = len(re.findall(r"\{\s*s:", m.group(1))) if m else 0
    bands = re.findall(r"d:(\d)", m.group(1)) if m else []
    info["bands"] = {b: bands.count(b) for b in sorted(set(bands))} if bands else {}

    for name in ("slides", "quiz", "handout", "homework"):
        p = folder / name / "index.html"
        if p.is_file():
            html = read(p)
            info["pages"][name] = {
                "url": "%s/lecture%d/%s/" % (SITE, num, name),
                "sheets": len(re.findall(r'<section class="sheet', html)),
                "exercises": len(re.findall(r'class="ex"', html)),
            }

    ex = folder / "_teacher" / "exercises.json"
    if ex.is_file():
        data = json.loads(read(ex))
        items = [e for part in data["SHEET"]["parts"] for e in part["exercises"]]
        info["exercises"] = len(items)
        info["answers"] = len(data.get("ANSWERS", {}))
        info["teacher_key"] = (folder / "_teacher" / "answer-key.html").is_file()
    return info


def card(L: dict) -> str:
    rows = []
    labels = {"slides": "Slides", "quiz": "Exam",
              "handout": "Booklet", "homework": "Homework"}
    for name in ("slides", "quiz", "handout", "homework"):
        p = L["pages"].get(name)
        if not p:
            rows.append('<div class="mat none"><span>%s</span><em>not made</em></div>'
                        % labels[name])
            continue
        if name == "slides":
            detail = "%d slides &middot; %d diagrams &middot; %d photos" % (
                L["slides"], L["diagrams"], L["photos"])
        elif name == "quiz":
            b = L.get("bands") or {}
            detail = "%d questions" % L["questions"]
            if b:
                detail += " &middot; %s easy / %s medium / %s hard" % (
                    b.get("1", 0), b.get("2", 0), b.get("3", 0))
        else:
            detail = "%d printed pages" % p["sheets"]
            if p["exercises"]:
                detail += " &middot; %d exercises" % p["exercises"]
        rows.append(
            '<a class="mat" href="%s" target="_blank" rel="noopener">'
            '<span>%s</span><em>%s</em></a>' % (p["url"], labels[name], detail))

    teacher = ""
    if L.get("teacher_key"):
        teacher = ('<p class="teacher">Answer key and exercise source are in '
                   '<code>lecture%d/_teacher/</code> &mdash; not published, open them '
                   'from the repo on this machine. %d exercises, %d answers.</p>'
                   % (L["num"], L.get("exercises", 0), L.get("answers", 0)))

    return ('<article class="card" style="--accent:%s">'
            '<header><span class="num">Lecture %d</span>'
            '<h2>%s</h2><p class="topic">%s</p></header>'
            '<div class="mats">%s</div>%s</article>'
            % (L["accent"], L["num"], esc(L["title"]), esc(L["topic"]),
               "".join(rows), teacher))


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Curriculum dashboard &middot; PGteach</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Sans+Arabic:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#16233F; --ink-2:#31405F; --soft:#6B7688;
  --paper:#FBFAF7; --line:#DFE3E8; --white:#fff;
  --ok:#2F7D5B; --off:#9C3B2E;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Inter",system-ui,sans-serif;background:var(--paper);color:var(--ink);line-height:1.55}
.ar{font-family:"IBM Plex Sans Arabic","Inter",sans-serif;direction:rtl;unicode-bidi:isolate}
.wrap{max-width:1040px;margin:0 auto;padding:clamp(22px,4vw,54px) clamp(16px,4vw,36px) 72px}

header.top{border-bottom:2px solid var(--ink);padding-bottom:14px;margin-bottom:26px}
header.top .brand{font-size:11.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--soft)}
header.top h1{font-family:"Fraunces",Georgia,serif;font-size:clamp(26px,4vw,40px);font-weight:600;margin-top:4px}
header.top p{color:var(--ink-2);margin-top:6px;max-width:62ch}

.panel{background:var(--white);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin-bottom:28px}
.panel h3{font-size:15px;font-weight:600;margin-bottom:4px}
.panel p{font-size:13.5px;color:var(--soft);max-width:66ch}
.switchrow{display:flex;align-items:center;gap:14px;margin-top:14px;flex-wrap:wrap}
button.toggle{
  font:inherit;font-weight:600;font-size:14px;cursor:pointer;
  border:1px solid var(--line);border-radius:8px;padding:9px 16px;background:var(--paper);color:var(--ink);
}
button.toggle:hover{border-color:var(--ink-2)}
button.toggle:focus-visible{outline:3px solid var(--ink);outline-offset:2px}
.state{font-size:13.5px;font-weight:600;display:flex;align-items:center;gap:7px}
.state .dot{width:9px;height:9px;border-radius:50%;background:var(--off)}
.state.on .dot{background:var(--ok)}
.note{font-size:12.5px;color:var(--soft);margin-top:10px;max-width:72ch}

.cards{display:grid;gap:18px}
@media(min-width:760px){.cards{grid-template-columns:1fr 1fr}}
.card{background:var(--white);border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:12px;padding:18px 20px 16px}
.card .num{font-size:11.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--accent)}
.card h2{font-family:"Fraunces",Georgia,serif;font-size:21px;font-weight:600;margin:2px 0 1px}
.card .topic{font-size:12.5px;color:var(--soft);margin-bottom:12px}
.mats{display:grid;gap:7px}
.mat{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
  text-decoration:none;color:inherit;border:1px solid var(--line);border-radius:8px;padding:9px 12px;background:var(--paper)}
.mat:hover{border-color:var(--accent);background:var(--white)}
.mat span{font-weight:600;font-size:14px}
.mat em{font-style:normal;font-size:12.5px;color:var(--soft);text-align:right}
.mat.none{opacity:.55}
.teacher{font-size:12.5px;color:var(--soft);margin-top:11px}
.teacher code{font-family:ui-monospace,monospace;font-size:12px;background:var(--paper);padding:1px 5px;border-radius:4px}

footer{margin-top:34px;padding-top:16px;border-top:1px solid var(--line);font-size:12.5px;color:var(--soft)}
footer a{color:var(--ink-2)}
</style>
</head>
<body>
<div class="wrap">

<header class="top">
  <div class="brand">PGteach &middot; Programming &amp; Artificial Intelligence</div>
  <h1>Curriculum dashboard</h1>
  <p>Every published page, and what is in it. Generated from the lecture
  folders, so the numbers here are what is actually on the site.</p>
</header>

<section class="panel">
  <h3>Exam code on the slides</h3>
  <p>The code is covered by default so a class cannot sit the exam at home the
  night before. Turn it on here and it appears on your decks, in this browser
  only &mdash; students' browsers keep the default. On the slide itself you can
  also just press <b>E</b>.</p>
  <p class="ar">الكود مغطى افتراضيًا عشان الطلبة ميحلوش الامتحان في البيت قبل الحصة.
  شغّله من هنا يظهر في الديك بتاعك، في المتصفح ده بس. أو اضغط E وانت على السلايدة.</p>
  <div class="switchrow">
    <button class="toggle" id="toggle" type="button">Show the code on my slides</button>
    <span class="state" id="state"><span class="dot"></span><span id="stateText">Covered</span></span>
  </div>
  <p class="note">Being straight about this: the exam address can be worked out
  from the address of the slides, so it stops the code being handed to a class
  in advance rather than stopping a student who goes looking.</p>
</section>

<div class="cards">
__CARDS__
</div>

<footer>
  <p>Results arrive in the Google Sheet the quiz posts to. Rebuild this page with
  <code>python scripts/build_dashboard.py</code> after adding a lecture.</p>
</footer>

</div>

<script>
/* The decks read this same key, and they are served from this origin, so the
   switch here reaches them. Wrapped because storage throws in a private
   window and the page must still work. */
const FLAG = "__FLAG__";
const btn = document.getElementById('toggle');
const state = document.getElementById('state');
const stateText = document.getElementById('stateText');

function shown(){
  try { return localStorage.getItem(FLAG) === 'shown'; } catch(e){ return false; }
}
function paint(){
  const on = shown();
  state.classList.toggle('on', on);
  stateText.textContent = on ? 'Showing on your slides' : 'Covered';
  btn.textContent = on ? 'Cover it again' : 'Show the code on my slides';
}
btn.onclick = function(){
  try { localStorage.setItem(FLAG, shown() ? 'hidden' : 'shown'); }
  catch(e){ stateText.textContent = 'This browser will not store the setting'; return; }
  paint();
};
paint();
</script>
</body>
</html>
"""


def main() -> None:
    lectures = [L for L in (scan(n) for n in range(1, 30)) if L]
    if not lectures:
        raise SystemExit("no lectures found")
    html = (PAGE.replace("__CARDS__", "\n".join(card(L) for L in lectures))
                .replace("__FLAG__", FLAG))
    if re.search(r"\{[%{]", html):
        raise SystemExit("a Liquid delimiter would break the Pages build")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print("%s  (%d lecture(s))" % (OUT.relative_to(ROOT).as_posix(), len(lectures)))
    for L in lectures:
        print("  Lecture %d  %-28s %2d slides  %2d questions  %s"
              % (L["num"], L["title"][:28], L["slides"], L["questions"],
                 ", ".join(sorted(L["pages"]))))


if __name__ == "__main__":
    main()
