#!/usr/bin/env node
/**
 * Behavioural tests for every lecture.
 *
 *     node scripts/test_pages.js        # all lectures
 *     node scripts/test_pages.js 2      # just lecture 2
 *
 * check_lecture.py reads the pages. This one RUNS them: it stubs enough of a
 * browser to execute each page's real <script>, drives a whole quiz attempt,
 * and asserts what the student sees and what gets submitted.
 *
 * That distinction matters. The bug that made the quiz completely dead — a
 * stray "[cite: 3]" inside a string literal — and the one where the correct
 * answer sat in slot 2 of nine questions were both invisible to a reader and
 * obvious to a runner.
 *
 * No dependencies. Exits non-zero if anything fails.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SITE_BASE = "https://pgteach.github.io/curriculum";

/* ------------------------------------------------------------------ */
/* a very small DOM                                                    */
/* ------------------------------------------------------------------ */

class El {
  constructor(tag) {
    this.tag = tag;
    this.children = [];
    this._text = "";
    this._html = "";
    this.value = "";
    this.className = "";
    this.style = {};
    this.disabled = false;
    this.onclick = null;
    this.type = "";
    this.src = "";
    this.alt = "";
    const set = new Set();
    this.classList = {
      add: (c) => set.add(c),
      remove: (c) => set.delete(c),
      contains: (c) => set.has(c),
      toggle: (c, on) => (on ? set.add(c) : set.delete(c)),
    };
  }
  set textContent(v) { this._text = String(v); this.children = []; }
  get textContent() {
    return this._text || this.children.map((c) => c.textContent).join("");
  }
  set innerHTML(v) { this._html = v; this.children = []; this._text = ""; }
  get innerHTML() { return this._html; }
  setAttribute(k, v) { this[k] = v; }
  appendChild(c) { this.children.push(c); return c; }
  querySelector() { return new El("stub"); }
  focus() {}
}

function makeCanvas(calls) {
  const cv = { width: 0, height: 0 };
  cv.getContext = () => ({
    scale() {}, fillRect() {}, drawImage() {}, beginPath() {}, fill() {},
    fillText(t) { calls.push(String(t)); },
    measureText: (t) => ({ width: String(t).length * 7.5 }),
    set font(v) {}, set fillStyle(v) {}, set textBaseline(v) {},
  });
  cv.toDataURL = () => "data:image/png;base64,VEVTVA==";
  return cv;
}

/** Builds a fresh fake browser and runs `js` inside it. */
function runPage(js, opts) {
  const nodes = new Map();
  const byId = (id) => {
    if (!nodes.has(id)) nodes.set(id, new El("div"));
    return nodes.get(id);
  };
  const slides = [];
  for (let k = 0; k < (opts.slideCount || 0); k++) slides.push(new El("section"));

  const cssVars = {};
  const canvasText = [];
  let sent = null;

  const document = {
    getElementById: byId,
    createElement: (t) => (t === "canvas" ? makeCanvas(canvasText) : new El(t)),
    createTextNode: (t) => { const e = new El("#text"); e.textContent = t; return e; },
    querySelectorAll: (sel) => {
      if (sel === ".slide") return slides;
      if (sel === ".opt") return byId("options").children;
      return [];
    },
    body: { style: {} },
    documentElement: { style: { setProperty: (k, v) => { cssVars[k] = v; } } },
    fonts: { ready: Promise.resolve() },
  };

  const sandbox = {
    document,
    addEventListener: () => {},
    location: { hash: "" },
    fetch: (url, o) => {
      sent = { url, opts: o, payload: JSON.parse(o.body) };
      return Promise.resolve({ ok: true });
    },
    setTimeout, clearTimeout, console, Math, Date, JSON, Promise, Image: function () {},
  };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;

  const names = Object.keys(sandbox);
  const expose = ";return {" + (opts.expose || []).map((n) => n + ":typeof " + n +
                 '!=="undefined"?' + n + ":undefined").join(",") + "};";
  const fn = new Function(...names, js + expose);
  const exported = fn(...names.map((n) => sandbox[n]));

  return { byId, slides, cssVars, canvasText, get sent() { return sent; }, exported };
}

/* ------------------------------------------------------------------ */
/* helpers                                                             */
/* ------------------------------------------------------------------ */

const fails = [];
let checks = 0;
function check(cond, msg) {
  checks++;
  if (!cond) fails.push(msg);
}

function scriptOf(file) {
  const html = fs.readFileSync(file, "utf8");
  const m = html.match(/<script>([\s\S]*?)<\/script>/);
  if (!m) throw new Error("no <script> in " + file);
  return { html, js: m[1] };
}

function countSlides(html) {
  return (html.replace(/<!--[\s\S]*?-->/g, "").match(/<section class="slide/g) || []).length;
}

/* ------------------------------------------------------------------ */
/* slides                                                              */
/* ------------------------------------------------------------------ */

function testSlides(num, file) {
  const tag = "L" + num + " slides";
  const { html, js } = scriptOf(file);
  const total = countSlides(html);
  check(total >= 2, tag + ": only " + total + " slide(s)");

  const p = runPage(js, { slideCount: total });

  const want = SITE_BASE + "/lecture" + num + "/quiz";
  const qr = p.byId("qr");
  check(qr.src.includes("create-qr-code"), tag + ": no QR generated");
  const data = decodeURIComponent((qr.src.split("data=")[1] || ""));
  check(data === want, tag + ": QR points at " + JSON.stringify(data) +
                       ", expected " + want);

  check(/^#[0-9a-fA-F]{3,6}$/.test(p.cssVars["--teal"] || ""),
        tag + ": accent not applied (--teal = " + p.cssVars["--teal"] + ")");
  check(/^rgb\(/.test(p.cssVars["--teal-pale"] || ""),
        tag + ": accent tint not applied");

  check(p.byId("dots").children.length === total,
        tag + ": " + p.byId("dots").children.length + " dots for " + total + " slides");
  check(p.byId("counter").textContent === " · 1 / " + total,
        tag + ": counter starts at " + JSON.stringify(p.byId("counter").textContent));

  p.byId("dots").children[total - 1].onclick();
  check(p.byId("counter").textContent === " · " + total + " / " + total,
        tag + ": jumping to the last slide did not update the counter");
  check(p.byId("bar").style.width === "100%",
        tag + ": progress bar at the end is " + p.byId("bar").style.width);
  p.byId("next").onclick();
  check(p.byId("counter").textContent === " · " + total + " / " + total,
        tag + ": did not clamp at the last slide");
}

/* ------------------------------------------------------------------ */
/* quiz                                                                */
/* ------------------------------------------------------------------ */

function testQuiz(num, file) {
  const tag = "L" + num + " quiz";
  const { html, js } = scriptOf(file);
  const p = runPage(js, {
    expose: ["QUESTIONS", "SECTIONS", "state", "LECTURE", "RESULTS_URL",
             "currentQ", "render"],
  });
  const Q = p.exported.QUESTIONS, S = p.exported.SECTIONS, st = p.exported.state;
  check(Array.isArray(Q) && Q.length > 0, tag + ": no questions");
  if (!Q || !Q.length) return;

  // intake
  const start = (name, phone, date) => {
    p.byId("sName").value = name;
    p.byId("sPhone").value = phone;
    p.byId("sDate").value = date;
    p.byId("intakeErr")._text = "";
    p.byId("quiz").className = "hide";
    p.byId("start").onclick();
    return { err: p.byId("intakeErr").textContent,
             started: p.byId("quiz").className === "" };
  };
  check(p.byId("sDate").value === new Date().toISOString().slice(0, 10),
        tag + ": date not prefilled with today");
  check(!start("Ali", "01001234567", "2026-09-02").started,
        tag + ": a one-word name was accepted as a full name");
  check(!start("Ali Hassan", "123", "2026-09-02").started,
        tag + ": a 3-digit phone was accepted");
  check(!start("Ali Hassan", "01001234567", "").started,
        tag + ": a missing date was accepted");
  check(start("Ali Hassan Mohamed", "01001234567", "2026-09-02").started,
        tag + ": a valid intake did not start the quiz");

  // one full attempt, deliberately wrong on the 1st and the 6th (or last)
  const wrongAt = new Set([0, Math.min(5, Q.length - 1)]);
  const shown = [], picked = {};

  for (let n = 0; n < Q.length; n++) {
    const q = p.exported.currentQ();
    shown.push(q);
    const right = q.o[q.a];
    const opts = p.byId("options").children;

    check(opts.length === q.o.length,
          tag + " q" + (n + 1) + ": " + opts.length + " options, expected " + q.o.length);
    check(JSON.stringify(opts.map((o) => o.textContent).sort()) ===
          JSON.stringify(q.o.slice().sort()),
          tag + " q" + (n + 1) + ": shuffled options do not match the source");
    check(p.byId("count").textContent === "Question " + (n + 1) + " of " + Q.length,
          tag + " q" + (n + 1) + ": counter reads " + p.byId("count").textContent);
    check(p.byId("tag").textContent === S[q.s],
          tag + " q" + (n + 1) + ": wrong section label");

    // find the button by text, never by position — the options are shuffled
    const target = wrongAt.has(n)
      ? opts.find((o) => o.textContent !== right)
      : opts.find((o) => o.textContent === right);
    picked[n] = target.textContent;
    target.onclick();

    check(opts.find((o) => o.textContent === right).classList.contains("correct"),
          tag + " q" + (n + 1) + ": correct option not highlighted");
    if (wrongAt.has(n)) {
      check(target.classList.contains("chosen-wrong"),
            tag + " q" + (n + 1) + ": wrong pick not marked");
    }
    check(opts.every((o) => o.disabled),
          tag + " q" + (n + 1) + ": options not locked after answering");
    check(p.byId("verdict").textContent.includes(q.why),
          tag + " q" + (n + 1) + ": explanation not shown");

    p.byId("next").onclick();
  }

  check(new Set(shown.map((q) => q.q)).size === Q.length,
        tag + ": a question was asked twice or skipped");

  const expScore = Q.length - wrongAt.size;
  check(p.byId("finalScore").textContent === expScore + "/" + Q.length,
        tag + ": score shows " + p.byId("finalScore").textContent);
  check(p.byId("breakdown").children.length === S.length,
        tag + ": " + p.byId("breakdown").children.length + " breakdown rows for " +
        S.length + " sections");
  check(p.byId("wrongList").children.length === wrongAt.size,
        tag + ": " + p.byId("wrongList").children.length + " review cards, expected " +
        wrongAt.size);

  return { tag, p, Q, S, st, shown, picked, expScore, wrongAt };
}

async function checkSubmission(ctx, num) {
  if (!ctx) return;
  const { tag, p, Q, S, shown, picked, expScore, wrongAt } = ctx;
  await new Promise((r) => setImmediate(r));   // sendResult awaits the card

  const sent = p.sent;
  check(sent !== null, tag + ": nothing was submitted");
  if (!sent) return;

  const d = sent.payload;
  check(sent.opts.method === "POST", tag + ": method is " + sent.opts.method);
  check(/^https:\/\/script\.google\.com\/macros\/s\//.test(sent.url),
        tag + ": endpoint is " + sent.url);

  const want = ["lecture", "name", "phone", "date", "score", "total",
                "weak", "sections", "wrongQuestions", "image"];
  want.forEach((k) => check(k in d, tag + ": payload is missing " + k));
  Object.keys(d).forEach((k) =>
    check(want.includes(k), tag + ": payload has an unexpected key " + k));

  check(d.lecture === "Lecture " + num, tag + ": payload.lecture is " + d.lecture);
  check(d.name === "Ali Hassan Mohamed", tag + ": payload.name is " + d.name);
  check(d.phone === "01001234567", tag + ": payload.phone is " + d.phone);
  check(d.score === expScore, tag + ": payload.score is " + d.score);
  check(d.total === Q.length, tag + ": payload.total is " + d.total);
  check(Array.isArray(d.wrongQuestions) && d.wrongQuestions.length === wrongAt.size,
        tag + ": wrongQuestions has " + (d.wrongQuestions || []).length + " entries");
  check((d.wrongQuestions || []).every((w) => w.selected !== w.correct),
        tag + ": a mistake was recorded with selected === correct");
  check(d.wrongQuestions[0] && d.wrongQuestions[0].question === shown[0].q &&
        d.wrongQuestions[0].selected === picked[0],
        tag + ": the first mistake does not match what was clicked");
  check(d.sections.split(" | ").length === S.length,
        tag + ": sections summary is " + d.sections);
  check(typeof d.image === "string" && d.image.length > 0,
        tag + ": no result screenshot in the payload");

  // the card must actually have been drawn
  check(p.canvasText.includes("PGteach"), tag + ": result card has no header");
  check(p.canvasText.includes("Ali Hassan Mohamed"), tag + ": result card has no name");
  check(p.canvasText.some((t) => t === expScore + " / " + Q.length),
        tag + ": result card has no score");

}

function testShuffle(num, file) {
  const tag = "L" + num + " quiz";
  const { js } = scriptOf(file);
  const p = runPage(js, { expose: ["QUESTIONS", "currentQ", "render", "state"] });
  const Q = p.exported.QUESTIONS;
  p.byId("sName").value = "Ali Hassan Mohamed";
  p.byId("sPhone").value = "01001234567";
  p.byId("sDate").value = "2026-09-02";
  p.byId("start").onclick();

  const q = p.exported.currentQ();
  if (q.o.length > 1) {
    const slots = new Set();
    for (let t = 0; t < 400; t++) {
      p.exported.render();
      slots.add(p.byId("options").children.findIndex(
        (o) => o.textContent === q.o[q.a]));
    }
    check(slots.size === q.o.length,
          tag + ": the correct answer only ever appeared in slot(s) [" +
          [...slots].sort().join(",") + "] of " + q.o.length);
  }

  const firsts = new Set();
  for (let t = 0; t < 200; t++) {
    p.byId("restart").onclick();
    firsts.add(p.exported.currentQ().q);
  }
  check(firsts.size > 1,
        tag + ": every attempt opened with the same question, so two students " +
        "side by side would see the same screen");
}

/* ------------------------------------------------------------------ */

async function main() {
  const only = process.argv[2];
  const lectures = fs.readdirSync(ROOT)
    .filter((d) => /^lecture\d+$/.test(d) &&
                   fs.statSync(path.join(ROOT, d)).isDirectory())
    .map((d) => parseInt(d.replace("lecture", ""), 10))
    .filter((n) => !only || String(n) === only)
    .sort((a, b) => a - b);

  if (!lectures.length) {
    console.error("No lecture folders found" + (only ? " for " + only : ""));
    process.exit(1);
  }

  for (const num of lectures) {
    const dir = path.join(ROOT, "lecture" + num);
    const slides = path.join(dir, "slides", "index.html");
    const quiz = path.join(dir, "quiz", "index.html");
    if (fs.existsSync(slides)) testSlides(num, slides);
    if (fs.existsSync(quiz)) {
      const ctx = testQuiz(num, quiz);
      await checkSubmission(ctx, num);
      testShuffle(num, quiz);
    }
    console.log("  lecture" + num + " exercised");
  }

  console.log("");
  if (fails.length) {
    console.log("FAILED — " + fails.length + " of " + checks + " checks");
    fails.forEach((f) => console.log("  x " + f));
    process.exit(1);
  }
  console.log("All " + checks + " behavioural checks passed across " +
              lectures.length + " lecture(s).");
}

main().catch((e) => {
  console.error("harness error: " + (e && e.stack || e));
  process.exit(1);
});
