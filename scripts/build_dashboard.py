#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the teacher dashboard at dashboard/index.html.

    python scripts/build_dashboard.py

Everything on the page is read out of the lecture folders themselves --
titles, accent colours, slide counts, question counts, exercise counts,
which materials exist -- so the dashboard cannot drift from what is
actually published. Re-run it after adding or changing a lecture.

The first control on the page is the exam-code switch. The dashboard and the
decks are served from the same origin, so a flag written to localStorage
here is read by the deck; the teacher flips it in their own browser and the
code appears on their slides. Every other browser, including every
every student's, keeps the default and the code stays covered.

THE PASSWORD
The published file is the page encrypted (AES-GCM, key from PBKDF2-SHA256)
inside a small lock screen, so neither the site nor the public repo shows
what is on it without the password. The password is read from the
DASHBOARD_PASSWORD environment variable, or else from
scripts/.dashboard-password, which .gitignore keeps out of the repo. To
change it, change that file and rebuild.

WHAT STUDENTS SEE
Once open, the page reads scripts/answers-released.json from GitHub and
shows a switch for each lecture's model answers and each chapter exam. A
switch commits the change straight to GitHub -- the public copy added or
removed, and the list updated -- using a GitHub key the teacher pastes in
once per device, kept in that browser only. That is what lets it work from
a phone. The site updates about a minute later. The same page opens the
answer keys, model answers and exams from _teacher/ for printing.
The lecture pages themselves are not locked: anyone with a page's address
can still open it.
"""

from __future__ import annotations

import base64
import io
import json
import os
import re
import sys
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://pgteach.github.io/curriculum"
OUT = ROOT / "dashboard" / "index.html"
FLAG = "pgteach.examCode"          # shared with the decks
sys.path.insert(0, str(Path(__file__).resolve().parent))
from release_answers import EXAMS, model_paths  # noqa: E402

SECRET = ROOT / "scripts" / ".dashboard-password"
ROUNDS = 310000                    # PBKDF2 iterations; the lock page uses the same


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
    # the students' model answers: published only once released (see
    # scripts/release_answers.py), otherwise held back in _teacher/
    info["model"] = (folder / "_teacher" / "model-answers.html").is_file()
    pub = folder / "answers" / "index.html"
    if pub.is_file():
        info["pages"]["answers"] = {
            "url": "%s/lecture%d/answers/" % (SITE, num),
            "sheets": len(re.findall(r'<section class="sheet', read(pub))),
            "exercises": 0,
        }
    return info


def card(L: dict) -> str:
    rows = []
    labels = {"slides": "Slides", "quiz": "Exam",
              "handout": "Booklet", "homework": "Homework", "answers": "Model answers"}
    for name in ("slides", "quiz", "handout", "homework", "answers"):
        if name == "answers" and L.get("model"):
            rows.append('<div class="mat none" data-ans="%d"><span>Model answers</span>'
                        '<em>checking&hellip;</em></div>' % L["num"])
            continue
        p = L["pages"].get(name)
        if not p:
            why = ("not released yet &mdash; held back until the homework is in"
                   if name == "answers" and L.get("model") else "not made")
            rows.append('<div class="mat none"><span>%s</span><em>%s</em></div>'
                        % (labels[name], why))
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
        opens = [("Answer key", "lecture%d/_teacher/answer-key.html" % L["num"])]
        if L.get("model"):
            opens.append(("Model answers", model_paths(L["num"])[0]))
        teacher = ('<p class="teacher">For you only, %d exercises: %s</p>'
                   % (L.get("exercises", 0), " ".join(
                       '<button class="open" type="button" data-open="%s">%s</button>' % (path, t)
                       for t, path in opens)))

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

.rel{display:grid;gap:8px;margin-top:14px}
.relrow{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;
  border:1px solid var(--line);border-radius:8px;padding:9px 12px;background:var(--paper)}
.relrow b{font-size:14px}
.relrow .state{font-size:12.5px}
.relrow .busy{font-size:12.5px;color:var(--soft)}
.gh{margin-top:16px;font-size:13.5px}
.gh summary{cursor:pointer;font-weight:600}
.gh p{margin-top:8px}
.gh input{font:inherit;flex:1 1 220px;padding:9px 12px;border:1px solid var(--line);border-radius:8px}
button.open{font:inherit;font-size:12.5px;font-weight:600;cursor:pointer;border:1px solid var(--line);
  border-radius:6px;padding:4px 10px;background:var(--paper);color:var(--ink);margin:2px 4px 0 0}
button.open:hover{border-color:var(--ink-2)}
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

<section class="panel" id="release">
  <h3>What students can see</h3>
  <p>Turn each one on once the homework is in, or the exam has been sat.
  The change goes straight to the site and shows there about a minute later.</p>
  <p class="ar">شغّل كل واحدة لما الواجب يتسلّم أو الامتحان يخلص. التغيير بيتنشر على الموقع وبيبان بعد دقيقة تقريبًا.</p>
  <div class="rel" id="rel"><p class="note">Loading&hellip;</p></div>
  <details class="gh" id="gh">
    <summary id="ghsum">Sign in to GitHub to change these</summary>
    <p>Once per device: make a key on GitHub and paste it here. It stays in
    this browser only. On GitHub: <a href="https://github.com/settings/personal-access-tokens/new"
    target="_blank" rel="noopener">new fine-grained token</a> &rarr; Repository access:
    <b>Only select repositories &rarr; curriculum</b> &rarr; Permissions:
    <b>Contents &rarr; Read and write</b> &rarr; Generate, and copy it.</p>
    <p class="ar">مرة واحدة على كل جهاز: اعمل مفتاح من GitHub بالخطوات دي والصقه هنا. بيتحفظ في المتصفح ده بس.</p>
    <div class="switchrow">
      <input type="password" id="tok" placeholder="github_pat_…" autocomplete="off" aria-label="GitHub key">
      <button class="toggle" id="tokSave" type="button">Save</button>
      <button class="toggle" id="tokForget" type="button">Sign out</button>
    </div>
    <p class="note" id="tokMsg"></p>
  </details>
</section>

<section class="panel">
  <h3>Chapter exams</h3>
  <p>For you only &mdash; open and print. Releasing a paper to students is above.</p>
  <div class="switchrow">__EXAMBTNS__</div>
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

/* ---- what students can see ----
   The list and the public copies live in the repo. Reading works without
   signing in (the repo is public); changing needs the teacher's GitHub key,
   kept in this browser's storage only. */
const API = "https://api.github.com/repos/__REPO__/";
const LIST = "scripts/answers-released.json";
const ITEMS = __ITEMS__;
const TOK = "pgteach.ghToken";
let pub = null, listSha = null;

function token(){ try { return localStorage.getItem(TOK) || ""; } catch(e){ return ""; } }
function gh(path, opt){
  opt = opt || {};
  const h = Object.assign({"Accept": "application/vnd.github+json"}, opt.headers || {});
  if (token()) h["Authorization"] = "Bearer " + token();
  return fetch(API + path, Object.assign({}, opt, {headers: h, cache: "no-store"}));
}
async function getFile(path){
  const r = await gh("contents/" + path + "?ref=main");
  if (r.status === 404) return null;
  if (!r.ok) throw new Error("GitHub said " + r.status);
  return r.json();
}
const b64 = s => btoa(String.fromCharCode(...new TextEncoder().encode(s)));
const unb64 = s => new TextDecoder().decode(Uint8Array.from(atob(s.replace(/\\n/g, "")), c => c.charCodeAt(0)));

async function put(path, content, sha, message){
  const r = await gh("contents/" + path, {method: "PUT", body: JSON.stringify(
    Object.assign({message: message, content: content, branch: "main"}, sha ? {sha: sha} : {}))});
  if (!r.ok) throw new Error(r.status === 403 || r.status === 401 ? "your GitHub key cannot write here" : "GitHub said " + r.status);
  return r.json();
}
async function remove(path, sha, message){
  const r = await gh("contents/" + path, {method: "DELETE", body: JSON.stringify({message: message, sha: sha, branch: "main"})});
  if (!r.ok) throw new Error(r.status === 403 || r.status === 401 ? "your GitHub key cannot write here" : "GitHub said " + r.status);
}

function isOn(it){ return (pub[it.kind] || []).indexOf(it.n) >= 0; }

function render(){
  const box = document.getElementById("rel");
  const can = !!token();
  box.innerHTML = "";
  ITEMS.forEach(function(it){
    const on = isOn(it);
    const row = document.createElement("div");
    row.className = "relrow";
    row.innerHTML = '<b></b><span class="state' + (on ? ' on' : '') + '"><span class="dot"></span>'
      + (on ? 'Students can see it' : 'Hidden from students') + '</span>';
    row.querySelector("b").textContent = it.label;
    if (can) {
      const b = document.createElement("button");
      b.className = "toggle"; b.type = "button";
      b.textContent = on ? "Hide" : "Show to students";
      b.onclick = function(){ flip(it, row, b); };
      row.appendChild(b);
    }
    box.appendChild(row);
  });
  if (!can) {
    const p = document.createElement("p");
    p.className = "note";
    p.textContent = "Sign in below to change these.";
    box.appendChild(p);
  }
  document.querySelectorAll("[data-ans]").forEach(function(el){
    const n = +el.dataset.ans, on = (pub.released || []).indexOf(n) >= 0;
    if (on) {
      const a = document.createElement("a");
      a.className = "mat"; a.target = "_blank"; a.rel = "noopener";
      a.href = "__SITE__/lecture" + n + "/answers/";
      a.innerHTML = "<span>Model answers</span><em>public</em>";
      el.replaceWith(a);
      a.dataset.ans = n;
    } else {
      el.className = "mat none";
      el.innerHTML = "<span>Model answers</span><em>hidden from students</em>";
    }
  });
}

async function load(){
  try {
    const f = await getFile(LIST);
    listSha = f.sha;
    pub = JSON.parse(unb64(f.content));
    render();
  } catch(e) {
    document.getElementById("rel").innerHTML = '<p class="note">Could not read the list from GitHub (' + e.message + '). Check the connection and reload.</p>';
  }
}

async function flip(it, row, btn){
  const on = !isOn(it);
  btn.disabled = true;
  const busy = document.createElement("span");
  busy.className = "busy"; busy.textContent = on ? "Publishing…" : "Taking it down…";
  row.appendChild(busy);
  try {
    const msg = (on ? "Release " : "Withdraw ") + it.label + " (from the dashboard)";
    const dst = await getFile(it.dst);
    if (on) {
      const src = await getFile(it.src);
      if (!src) throw new Error(it.src + " is not in the repo");
      await put(it.dst, src.content.replace(/\\n/g, ""), dst && dst.sha, msg);
    } else if (dst) {
      await remove(it.dst, dst.sha, msg);
    }
    const f = await getFile(LIST);           // fresh, in case another device changed it
    const s = JSON.parse(unb64(f.content));
    const list = (s[it.kind] || []).filter(x => x !== it.n);
    if (on) list.push(it.n);
    s[it.kind] = list.sort((a, b) => a - b);
    const r = await put(LIST, b64(JSON.stringify(s, null, 2) + "\\n"), f.sha, msg);
    listSha = r.content.sha; pub = s;
    render();
    const rows = document.querySelectorAll(".relrow");
    const done = document.createElement("span");
    done.className = "busy"; done.textContent = "Done — on the site in about a minute.";
    rows[ITEMS.indexOf(it)].appendChild(done);
  } catch(e) {
    busy.textContent = "Not changed: " + e.message;
    btn.disabled = false;
  }
}

const tokMsg = document.getElementById("tokMsg");
function signedIn(){
  document.getElementById("ghsum").textContent = token() ? "Signed in to GitHub on this device" : "Sign in to GitHub to change these";
}
document.getElementById("tokSave").onclick = async function(){
  const t = document.getElementById("tok").value.trim();
  if (!t) return;
  tokMsg.textContent = "Checking…";
  try {
    const r = await fetch(API.slice(0, -1), {headers: {"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}, cache: "no-store"});
    const j = await r.json();
    if (!r.ok || !j.permissions || !j.permissions.push) throw new Error("this key cannot change the curriculum repo — check Contents is Read and write");
    try { localStorage.setItem(TOK, t); } catch(e){ throw new Error("this browser will not store it"); }
    document.getElementById("tok").value = "";
    tokMsg.textContent = "Saved. You can change what students see now.";
    signedIn(); load();
  } catch(e) { tokMsg.textContent = "Not saved: " + e.message; }
};
document.getElementById("tokForget").onclick = function(){
  try { localStorage.removeItem(TOK); } catch(e){}
  tokMsg.textContent = "Signed out on this device.";
  signedIn(); if (pub) render();
};
signedIn();
load();

/* teacher files: read from the repo and opened in a new tab, to print.
   The tab is opened first, inside the tap, or phones block it. */
document.addEventListener("click", async function(ev){
  const b = ev.target.closest("button.open");
  if (!b) return;
  const w = window.open("", "_blank");
  if (!w) { alert("Allow pop-ups for this page to open teacher files."); return; }
  w.document.write("<p style='font-family:sans-serif;padding:20px'>Opening…</p>");
  try {
    const r = await gh("contents/" + b.dataset.open + "?ref=main", {headers: {"Accept": "application/vnd.github.raw+json"}});
    if (!r.ok) throw new Error("GitHub said " + r.status);
    const html = await r.text();
    w.document.open(); w.document.write(html); w.document.close();
  } catch(e) {
    w.document.body.textContent = "Could not open it: " + e.message;
  }
});
</script>
</body>
</html>
"""


LOCK = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Curriculum dashboard &middot; PGteach</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:#FBFAF7;color:#16233F;min-height:100vh;
  display:flex;align-items:center;justify-content:center;padding:16px}
form{background:#fff;border:1px solid #DFE3E8;border-radius:12px;padding:24px;width:100%;max-width:360px}
h1{font-size:20px;margin-bottom:4px}
p{font-size:13.5px;color:#6B7688;margin-bottom:14px}
input[type=password]{font:inherit;width:100%;padding:10px 12px;border:1px solid #DFE3E8;border-radius:8px}
label{display:flex;gap:8px;align-items:center;font-size:13px;color:#31405F;margin:12px 0}
button{font:inherit;font-weight:600;width:100%;padding:10px;border:0;border-radius:8px;background:#16233F;color:#fff;cursor:pointer}
#err{color:#9C3B2E;font-size:13px;min-height:18px;margin-top:10px}
</style>
</head>
<body>
<form id="f">
  <h1>Curriculum dashboard</h1>
  <p>For the teacher only. Enter the password.</p>
  <input type="password" id="pw" autocomplete="current-password" aria-label="Password" autofocus>
  <label><input type="checkbox" id="keep"> Remember on this device</label>
  <button type="submit">Open</button>
  <div id="err" role="alert"></div>
</form>
<script>
/* The dashboard is encrypted below; only the right password opens it. The
   remembered key is stored in this browser only, so tick it on your own
   devices and never on a school computer. */
const DATA = "__DATA__", SALT = "__SALT__", IV = "__IV__", ROUNDS = __ROUNDS__, KEEP = "pgteach.dashKey";
const bytes = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
async function derive(pw){
  const base = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveBits"]);
  return new Uint8Array(await crypto.subtle.deriveBits({name:"PBKDF2", hash:"SHA-256", salt:bytes(SALT), iterations:ROUNDS}, base, 256));
}
async function unlock(raw){
  const key = await crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["decrypt"]);
  const plain = await crypto.subtle.decrypt({name:"AES-GCM", iv:bytes(IV)}, key, bytes(DATA));
  const html = new TextDecoder().decode(plain);
  document.open(); document.write(html); document.close();
}
(async function(){
  let saved = null;
  try { saved = localStorage.getItem(KEEP); } catch(e){}
  if (saved) { try { await unlock(bytes(saved)); return; } catch(e){ try { localStorage.removeItem(KEEP); } catch(_){} } }
})();
document.getElementById("f").onsubmit = async function(ev){
  ev.preventDefault();
  const err = document.getElementById("err");
  err.textContent = "Checking…";
  try {
    const raw = await derive(document.getElementById("pw").value);
    if (document.getElementById("keep").checked) {
      try { localStorage.setItem(KEEP, btoa(String.fromCharCode(...raw))); } catch(e){}
    }
    await unlock(raw);
  } catch(e) { err.textContent = "Wrong password."; }
};
</script>
</body>
</html>
"""


def password() -> str:
    pw = os.environ.get("DASHBOARD_PASSWORD") or (SECRET.read_text(encoding="utf-8").strip()
                                                 if SECRET.is_file() else "")
    if len(pw) < 8:
        raise SystemExit("set a password of 8+ characters in %s (kept out of git) "
                         "or in DASHBOARD_PASSWORD" % SECRET.relative_to(ROOT).as_posix())
    return pw


def lock(html: str) -> str:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    import hashlib
    salt, iv = os.urandom(16), os.urandom(12)
    key = hashlib.pbkdf2_hmac("sha256", password().encode("utf-8"), salt, ROUNDS, 32)
    data = AESGCM(key).encrypt(iv, html.encode("utf-8"), None)
    b64 = lambda b: base64.b64encode(b).decode("ascii")
    return (LOCK.replace("__DATA__", b64(data)).replace("__SALT__", b64(salt))
                .replace("__IV__", b64(iv)).replace("__ROUNDS__", str(ROUNDS)))


def main() -> None:
    lectures = [L for L in (scan(n) for n in range(1, 30)) if L]
    if not lectures:
        raise SystemExit("no lectures found")
    items = [{"kind": "released", "n": L["num"], "label": "Lecture %d model answers" % L["num"],
              "src": model_paths(L["num"])[0], "dst": model_paths(L["num"])[1]}
             for L in lectures if L.get("model")]
    items += [{"kind": "exams", "n": ch, "label": "Chapter %d exam paper" % ch, "src": src, "dst": dst}
              for ch, (src, dst) in sorted(EXAMS.items()) if (ROOT / src).is_file()]
    exams = " ".join(
        '<button class="open" type="button" data-open="%s">Chapter %d %s</button>' % (path, ch, what)
        for ch, (src, _) in sorted(EXAMS.items()) if (ROOT / src).is_file()
        for what, path in (("exam", src), ("marking scheme", src.replace("-exam.html", "-exam-key.html"))))
    html = (PAGE.replace("__CARDS__", "\n".join(card(L) for L in lectures))
                .replace("__EXAMBTNS__", exams)
                .replace("__ITEMS__", json.dumps(items))
                .replace("__REPO__", "PGteach/curriculum")
                .replace("__SITE__", SITE)
                .replace("__FLAG__", FLAG))
    html = lock(html)
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
