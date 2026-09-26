# Handoff — state of this repo

Last updated: 2026-09-26. Written so a new session (or another machine) can pick
this up with no prior context. Read this first, then [README.md](README.md) for
how the pages actually work.

## What this repo is

Interactive lecture slides + self-check quizzes for PGteach, served from GitHub
Pages at `https://pgteach.github.io/curriculum/lectureN/{slides,quiz}`.
No build step — every page is one self-contained `index.html`.

Repo: `https://github.com/PGteach/curriculum` · Pages: `main` branch, `/` root.

## Current structure

```
lecture1/slides/index.html    12 slides
lecture1/quiz/index.html      10 questions, 4 sections
lecture1/handout/index.html   7-page A4 booklet, printed from the browser

lecture2/slides/index.html    34 slides, 14 photos in slides/media/
lecture2/quiz/index.html      20 questions, 5 sections, cumulative over L1+L2
lecture2/handout/index.html   10-page booklet: the lesson + 4 class exercises
lecture2/homework/index.html  6-page take-home sheet, 9 exercises
lecture2/_teacher/            answer key + exercise source (Jekyll ignores _*)
scripts/build_lecture2.py     builds those three from _teacher/exercises.json

lecture3/slides/index.html    46 slides, 9 diagrams, photos; exam code covered
lecture3/quiz/index.html      36 questions, 4 options each, cumulative L1-L3
lecture3/handout/index.html   12-page booklet: lessons 1-2 AND 1-3 + 4 class exercises
lecture3/homework/index.html  take-home sheet, 20 exercises in 3 labelled parts
lecture3/_teacher/            15-page answer key + exercises.json (unpublished)
scripts/build_lecture3.py         booklet, homework, answer key
scripts/build_lecture3_slides.py  the deck, from scripts/lecture3_slides_base.html
scripts/build_lecture3_quiz.py    the quiz (then run protect_answers.py 3)

lecture4/slides/index.html    30 slides, lesson 1-4 Ethical Issues with AI; exam code covered
lecture4/quiz/index.html      24 questions, 4 options each: 18 on lesson 1-4, 6 Unit 1 review
lecture4/handout/index.html   10-page booklet, same sections in the same order as the deck
lecture4/homework/index.html  9-page take-home sheet, 14 exercises in 4 parts
lecture4/_teacher/            answer key + UNIT 1 EXAM paper + its marking scheme (unpublished)
scripts/build_lecture4.py         booklet, homework, answer key, unit exam, exam key
scripts/build_lecture4_slides.py  the deck, from scripts/lecture4_slides_base.html
scripts/build_lecture4_quiz.py    the quiz (then run protect_answers.py 4)
_config.yml                   excludes scripts/ from the published site -- see below

dashboard/index.html          teacher dashboard (generated) with exam-code switch
scripts/build_dashboard.py    regenerates it from the lecture folders

templates/slides-template.html
templates/quiz-template.html
templates/handout-template.html
scripts/new_lecture.py        scaffolds slides/quiz/handout from templates/
scripts/check_lecture.py      pre-publish gate; run it before every commit
scripts/test_pages.js         behavioural harness over every lecture, runs in CI
scripts/protect_answers.py    turns quiz a: indices into fingerprints
scripts/apps-script.gs        the Google Apps Script that records results
README.md · HANDOFF.md · .gitignore
```

`homework/` is an **optional** fourth page. `check_lecture.py` validates it
with the handout's rules when the folder exists and says nothing when it does
not, so lecture 1 is unaffected. `new_lecture.py` does not scaffold one yet.

## What was done, in order

1. **Restructured** from a flat `slides/` + `quiz/` at the repo root into
   `lecture1/slides` + `lecture1/quiz`. Deleted `web-files.zip`, the two
   one-line `README.md` stubs, and the unused `slides/quiz_qr.png`.
2. **Fixed a quiz that could not run at all.** The file carried 11
   `[cite: 3]` paste artifacts, 9 of them inside JavaScript string literals
   (`why:"…"[cite: 3]`), which is a `SyntaxError` — the whole `<script>`
   failed to parse. Verified broken with `node --check` before, and clean
   after.
3. **Added a single `LECTURE CONFIG` block** to the top of each page's
   `<script>` (number, title, topic). The QR code, both Pages URLs, the page
   titles and the payload's `lecture` field all derive from it. Slide count,
   nav dots, progress bar, `n / total` and question totals are computed at
   runtime, so no counts are ever edited by hand.
4. **Templates + `scripts/new_lecture.py`** so a new lecture is one command.
5. **Fixed the mobile nav bar.** `.dot` set `width:7px` but `#nav button` set
   `padding:.45em .9em` and won on specificity, so the dots rendered as wide
   pills; 12 of them did not fit a phone, the teacher name wrapped onto four
   lines, and the `← → or swipe` hint sat on top of the Arabic line. Dots are
   now real circles, and below 620px the dots and hint are hidden (the
   `n / total` counter does the same job) with extra bottom padding so text
   clears the bar.
6. **Made the quiz un-copyable.** Both the options and the question order are
   shuffled — see below.
7. **Rewrote the Apps Script** to record `lecture` and `wrongQuestions`, use
   one tab per lecture, and stop Sheets from eating phone numbers.
8. **Automatic result screenshots.** The result screen is redrawn onto a
   `<canvas>` when the student finishes and sent as base64 PNG in the payload;
   the Apps Script files it in Drive and links it from the sheet. The student
   does nothing. Plain 2D canvas calls only — no library, nothing newer than
   `fillRect`, so old phone browsers cope. Measured at 1800x1972 px / 253 KB
   for a typical 8/10 attempt with two mistakes.

9. **Printable handout** (`lectureN/handout/index.html`). The student booklet
   used to be a Word-made PDF whose QR pointed at
   `eissa2002.github.io/quiz` — a different account entirely, and a **404**.
   The booklet is now an HTML page laid out in A4, printed from the browser,
   with the QR generated from the lecture number and the footer page numbers
   counted at runtime. Nothing on paper can go stale again.

10. **Accent colour per lecture.** `LECTURE_ACCENT` in the deck and the
    handout overrides `--teal` and a tinted `--teal-pale` at runtime, so each
    lecture reads as its own without touching structure or typography.
    `new_lecture.py` cycles a six-colour palette by lecture number, or takes
    `--accent`. The quiz is deliberately excluded — its green and red carry
    meaning.
11. **The browser stopped printing its own header and footer** on the handout.
    Chrome was stamping the date, the page title and the `file:///…` path onto
    every page. Those are only ever drawn inside the `@page` margin, so the
    margin is now `0` and each sheet pads itself instead — same layout, no
    furniture, and no reliance on the user unticking anything.

## Lecture 2 — what is different about it

Written outside the repo and wired in afterwards, so it needed the things the
templates give you for free. Worth knowing before touching it:

- **The deck is not scaffolded from the template.** It was merged: the deck's
  own CSS and 31 slides were kept, and the template's `LECTURE CONFIG`,
  fixed nav chrome and phone media query were merged in. A change meant for
  every lecture still has to be applied here by hand.
- **It arrived with two regressions that this repo had already fixed** — a
  checked-in `quiz_qr.png` (the stale-QR problem that 404'd the old booklet)
  and the `.dot` vs `#nav button` specificity bug from item 5, which with 31
  dots is worse than the 12 that prompted the fix. Both are corrected; do not
  reintroduce them by copying the original file back.
- **Photos are local.** `slides/media/` holds all 14, because hot-linking
  meant no photos on a slow school connection. `media/SOURCES.md` records
  where each came from. The `localise-photos.sh` that shipped with the deck
  calls `python3`, which is not installed on the teaching machine.
- **The printed material is generated, not hand-written.**
  `scripts/build_lecture2.py` holds the lesson prose and reads the exercises
  from `lecture2/_teacher/exercises.json`. Edit those and re-run it; do not
  edit the three HTML files directly, they are overwritten.
- **The class/homework split is one line** in that script: `IN_CLASS` and
  `HOMEWORK`. Class work is deliberately short — the session is 90-120
  minutes and most of it is teaching.
- **Page breaks are verified, not guessed.** One `section.sheet` must print
  as exactly one A4 page. Render each sheet on its own and count the PDF's
  pages after changing any exercise; several tighter packings were tried and
  overflowed.
- **Answers are in `_teacher/`,** which Jekyll does not serve, so the key is
  versioned without being published next to the homework it answers. Adding
  `.nojekyll` — discussed under Open decisions — would publish it. Move it
  out of the repo first if that ever happens.

## Photos open full size (the lightbox)

Any `figure.shot` inside a `.shots` grid is clickable; the overlay is `#zoom`,
fixed to `<body>` so the slide's auto-fit transform does not scale it.

The one thing to know before touching the deck's navigation: **the arrow-key
and swipe handlers must keep their `zoomOpen()` guard.** Both they and the
lightbox listen on `window`, where `stopPropagation` does not stop a sibling
listener — so without the guard, Right with a photo open moves the photo and
the slide underneath it. That reads as the deck randomly skipping, and nobody
reports it, they just stop clicking photos.

`check_lecture.py` fails if a guard goes missing. Getting that check right
took two tries: the first version searched the raw script from
`addEventListener('keydown'` to the next `go(i+1)`, which ran straight past
the end of the lightbox's own keydown handler and found *its* `zoomOpen()` —
so it passed with the guard deleted. It now splits the script into whole
handler bodies first. Deleting each of the three guards on purpose is what
found that, and all three are now caught by name.

`scripts/probe_lightbox.js` is the behavioural half, run by hand in a browser
(its header says how). It is not in CI because it needs a real one.

## The print button that silently did nothing

Reported from the answer key specifically: clicking "Print this sheet" did
nothing, no error visible anywhere. Root cause was one line -- the button
bound its click handler on the LAST line of its setup IIFE, after five other
`getElementById()` calls nothing checked the result of. The answer key has
no QR panel (a teacher does not need one to scan), so
`getElementById('quizUrl').textContent = ...` threw on null three lines
before the print binding, and the whole script just stopped there.

Same shared script, so the same bug was latent on every page built from
`templates/handout-template.html` -- it only ever surfaced on the one page
missing an element the others all have. Fixed structurally, not just for
this page: the print button now binds first, unconditionally
(`if(printBtn) printBtn.onclick = ...`), and every other lookup that is not
guaranteed present -- `quizUrl`, `qr` -- is wrapped in its own `if(...)` and
skips its block rather than assuming the element exists. Patched in five
files: the template and the four pages already built from it.

Fixing this exposed a second, unrelated bug while verifying the first: the
"about 5 minutes" -> "about 10 minutes" change in `templates/handout-template.html`
was never followed by an update to the six literal `.replace()` calls in
`scripts/build_lecture2.py`'s `qr_panel()` that patch that template into the
exam-specific panel. One of those six calls -- the heading -- had gone
stale, and `str.replace()` on a miss just returns the input unchanged: no
error, so the built handout and homework silently kept a leftover comment
and the wrong heading text. Only found because regenerating them to verify
the print-button fix produced output that no longer matched what was
already committed. `qr_panel()` now runs its replacements through `lit()`,
which raises if a target does not match exactly once -- sabotage-tested by
drifting the template text on purpose; the build now fails loudly instead
of shipping quietly wrong output.

`check_lecture.py` gained `check_print_button()`: the print binding must be
`if(printBtn)`-guarded, and must sit before any `quizUrl`/`qr` lookup, each
itself behind its own named guard. It runs on handout, homework, and now
every `_teacher/*.html` page too (added to the checker's own loop), so a
future teacher-only page gets this for free. Proved by reproducing the
original bug byte-for-byte and confirming it is caught by name, then two
more sabotages -- the binding moved after the lookups, and a lookup left
unguarded -- each caught individually. One early version of this check used
a general "is this getElementById call guarded" heuristic; it failed
against its own intended target the first time it ran, which is why the
final version checks the two specific optional lookups by name instead of
trying to infer guardedness generally.

## The anti-cheating change (item 6)

The original questions had the correct answer at index `1` in **9 of 10
questions** — a student could score 9/10 by always tapping the second option.

Both are now shuffled with Fisher-Yates:

- **options** — reshuffled on every render, so the answer moves slot every time
- **question order** — reshuffled once per attempt (`newAttempt()`), so two
  students sitting together are not on the same question at the same moment

`q.a` stays the source of truth. `state.order` maps a displayed button position
back to its index in `q.o`, and `state.qOrder` maps a step number to an index in
`QUESTIONS`; `currentQ()` resolves the latter. Anything that compares positions
must go through those maps — that was the one trap when writing this.

## Google Sheet / Apps Script — ACTION STILL NEEDED

The live endpoint is `AKfycbxfgPaAaOTuOhyyaRI4fWLclsYF1VsDXpkDQoURb_yUIsG35Lmf2wgg0IJ7Zff_BnHn`
and it works, but when last checked **it was still running the old 8-column
script**. The repo's script is now at `DESIGN_VERSION = 6` and its last column
is **How it was taken** (the quiz's new `integrity` field — see *Attempt
integrity* below). Nobody in these sessions can deploy it; that needs the
teacher's Google account. If the sheet's header row does not end with *How it
was taken*, the live copy is behind. Nothing breaks meanwhile — the script
reads fields by name, so scores still land; only the newer columns are lost.

To finish: paste [scripts/apps-script.gs](scripts/apps-script.gs) into the Sheet's
Apps Script editor, then **Deploy > Manage deployments > edit > Version: New
version**. Saving alone does not update the live URL. Then run
`reformatAllTabs()` once and `testSubmission()` to confirm the whole path.

What that script changes:

- adds a **Lecture** column and a **Mistakes** column (`wrongQuestions`
  flattened into readable text) — both were being silently discarded
- **one tab per lecture**, created on demand and kept in numeric order. Set
  `ONE_TAB_PER_LECTURE = false` for a single "All results" tab instead —
  **do this if AppSheet is in the picture.** AppSheet binds one table to one
  worksheet and does not discover new tabs by itself, so a tab per lecture
  means adding a new AppSheet table every lecture. `mergeTabsIntoOne()` moves
  existing per-lecture rows into the single tab
- `formatTab_()` sets every column's width, alignment and wrapping from the
  `COLUMNS` table, plus a dark header row, frozen panes, borders and zebra
  striping. `reformatAllTabs()` applies it to tabs that already exist — run it
  once after pasting a new version
- forces the Phone column to text format. Sheets was reading `01129907116` as
  a number and dropping the leading zero (visible in the old `Sheet1`:
  `12436494`). Already-stored numbers cannot be recovered
- `migrateOldRows()` copies the 4 existing `Sheet1` rows into the Lecture 1 tab,
  marking Mistakes as `(not recorded)`. Run it once by hand, check, then delete
  `Sheet1` yourself
- **a `DESIGN_VERSION` stamp.** Every tab records the version it was last
  formatted at, and the next submission reformats any tab that is behind. So
  the look is a rule the script enforces, not something anyone styles by hand,
  and existing tabs catch up on their own — bump `DESIGN_VERSION` after
  changing `COLUMNS` or `formatTab_()` and that is the whole job. The check is
  one property read per submission, wrapped in try/catch: formatting is
  cosmetic and must never cost a submission
- **an optional hand-styled `Template` tab**, off unless you create it. If it exists, every new lecture
  tab is a copy of it, so colours, widths, conditional formatting and notes set
  by hand in Sheets carry over without touching code. `createTemplateTab()`
  makes one; delete it and the script falls back to `formatTab_()`.
  `reformatAllTabs()` pushes the Template's look onto tabs that already exist
  (formats yes; banding and conditional-format rules only travel with a fresh
  copy). Two sources of truth is the trade — `getSheet_` re-stamps the header
  row if the Template has drifted from `COLUMNS`
- saves the result screenshot to Drive and links it from the Screenshot column.
  **This adds a Drive scope, so the first run will ask for authorisation again**
  — approve it, or every row lands with `(image failed: …)` while the rest of
  the row still saves correctly. Run `testSubmission()` from the editor once to
  confirm the whole path, including Drive; it sends a real 2x2 PNG

Because the quiz posts with `mode:"no-cors"`, **the browser cannot read the
response** — if the script throws, the student still sees "sent to your
teacher". Verify in the sheet, or in the Apps Script editor's Executions tab.

## Open decisions

- **Old QR codes are dead, on two different domains.** `/curriculum/slides`
  and `/curriculum/quiz` return 404 after the restructure. Separately, the
  printed booklet's QR pointed at `https://eissa2002.github.io/quiz`, which
  also returns 404 (that account's root still answers 200, so a redirect stub
  could be added *there* — it is a different repo, not this one). Redirect
  stubs were offered for both and are not done; the new handout avoids the
  problem for anything printed from now on.
- ~~The handout's Arabic needs a read-through.~~ **Resolved.** The first
  PDF's Arabic could not be extracted (no usable ToUnicode map — it came out
  as detached, reordered glyphs). A second PDF was supplied whose fonts embed
  correctly, and its Arabic is now in the handout verbatim, including the
  per-stage, per-term and per-habit lines. Also restored: the "quickest way to
  keep them apart" paragraph, which the first HTML pass had dropped.
- **No landing page.** `/curriculum/` currently renders `README.md` via Jekyll.
  `/curriculum/dashboard/` now does what a landing page would; making it the
  root was offered and not yet decided.
- Slide 12 says "10 questions" as static text; it is not derived from the
  quiz's `QUESTIONS.length` (different page). Templates say just
  "Test yourself".
- **Jekyll is a liability here.** Any Markdown file containing Liquid
  delimiters fails the build, and a failed build blocks the deploy of the
  slides and quiz too — a docs typo can take the teaching pages offline.
  Adding `.nojekyll` makes the build serve files verbatim and immune to
  this, but it also removes the auto-generated landing page at
  `/curriculum/`, so it needs a real root `index.html` alongside it.
  Offered, not yet decided. **Warning:** `.nojekyll` would also start serving
  `lecture2/_teacher/` and `lecture3/_teacher/` — the answer keys — publicly.
  Move those out of the repo (or to a private one) before ever adding it.

## Adding a lecture

```bash
python scripts/new_lecture.py 2 "Variables & Data Types"
```

Then write the slides (`<section class="slide">` blocks, QR slide stays last)
and the questions (`SECTIONS` / `QUESTIONS` at the top of the quiz `<script>`).
Answer positions do not matter any more — they get shuffled.

For anything bigger than lecture 1, copy lecture 3's generators instead and
keep content in them and in `_teacher/exercises.json`. Before publishing, all
of these, not only the first:

1. `python scripts/check_lecture.py` and `node scripts/test_pages.js`
2. `python scripts/protect_answers.py N` after any question edit
3. render every printed `.sheet` on its own; each must be exactly one A4 page
4. look at the rendered pages — the gates measure structure, not teaching;
   lecture 3's first build passed them all while it was thin and picture-less
5. read every exercise against its answer; check questions for duplicate
   *facts*, not duplicate wording
6. `python scripts/build_dashboard.py`

## Lecture 3 — what to know before touching it

Covers **two** textbook lessons, 1-2 How AI Works (pp. 13-19) and 1-3 AI in
Daily Life and Industry (pp. 20-25): one alone was about 70% of lecture 2's
material. Title "How does it learn?", accent `#1D6FA5`.

**Every lecture 3 file is generated — edit the generator, never the HTML.**

| Output | Generator |
|---|---|
| slides | `build_lecture3_slides.py` (slide list inside; shell in `lecture3_slides_base.html`) |
| quiz | `build_lecture3_quiz.py`, then `protect_answers.py 3` |
| handout, homework, answer key | `build_lecture3.py` + `lecture3/_teacher/exercises.json` |

All three rebuild byte-identical from the repo. The slide builder must start
from the base file, never from the published deck — its injections (lightbox,
exam-code gate) are guarded by their CSS, so rebuilding on a built deck skips
markup it needs.

**The Arabic is written, not sourced.** The Arabic textbook yields no
extractable Arabic (the ToUnicode problem lecture 1 had) and no OCR is
installed, so all lecture 3 Arabic is written in the Egyptian teaching
register. It needs a teacher's read-through.

**The quiz**: 36 questions, weighted to the exam — 3 from lecture 1, 9 from
lecture 2, 24 from lecture 3. Four options each, every wrong option from the
same material (the first draft had absurd distractors that made it easy
whatever the labels said). Four **minimal pairs** differ by one word that
flips the answer. Questions carry `d:` 1-3; `bandedOrder()` goes easy → hard,
shuffling inside each band.

**The exam code is covered on the deck** until the teacher presses **E**,
clicks the panel, or turns it on from the dashboard. A speed bump only — the
quiz address is guessable. The QR is still built from `LECTURE.quizUrl` on
load (the harness checks it); only the view is gated. The printed booklet and
homework carry **no QR or quiz address**: the exam is taken in the lesson.
`check_lecture.py` now treats a QR on the handout as optional.

**Class work 1-4, homework 1-20 in three parts** (lesson 1-2, lesson 1-3,
optional thinking/research), numbered by printed position; the answer key
uses the same numbers. A **four-tasks interlude** (classification, detection,
recognition, generation — not in the book, labelled as such) sits in both the
deck and the booklet.

**Printed documents are one `.sheet` per A4 page, always.** The answer key was
one long `.sheet`; Chrome paginated it, other PDF paths did not, and it would
not print. `KEY_PAGES` in `build_lecture3.py` now lists what goes on each of
its 15 pages. Add an exercise → add it to a page there and re-run the page gate.

Bugs caught here, all fixed: `short` exercises printed no question (no branch
in `exercise()`); five answers attached to the wrong question; two exercises
that were the same task; the template's demo pages leaking in (QR sheet found
from the wrong `<section>`). None of those are visible to the checker.

## Lecture 4, and the Unit 1 exam

Lecture 4 is lesson 1-4, Ethical Issues with AI (pp. 26-32), accent `#A63D5B`,
and it closes Unit 1. **Curriculum only** -- the teacher's instruction: no
foundations or extras. Two ideas the English book gives one line each get a
slide, because the ministry's assessment book asks about them directly:
responsibility against accountability, and the proxy variable.

**The booklet follows the deck section by section, in the same order** --
also the teacher's instruction. `booklet()` in `build_lecture4.py` carries the
slide numbers each page covers in its comments; keep them in step. Only the
title, the part dividers and the exam QR have no page.

**The Unit 1 exam is printed, not online** -- the teacher's choice, because
essay answers cannot be marked automatically. `lecture4/_teacher/unit1-exam.html`
is the paper (6 pages) and `unit1-exam-key.html` the marking scheme (5 pages);
content in `unit1-exam.json`. Shape copied from the ministry's weekly
assessments: four-option MCQ plus essay. 20 MCQ in three labelled levels
(Remember 7, Understand 7, Apply and analyse 6), then 6 essays rising 2-3-3-3-3-6
marks; 40 marks, 60 minutes, every lesson 1-1 to 1-4 at every level. The last
essay is the book's own [6] exam-style question from lesson 1-3.

**Every item is sourced -- the teacher's rule.** Each question is either one of
the textbook's own (Try, Worked Example, Exercise, exam-style) or an item from
the ministry's assessment book in `data sources/`, translated into the book's
English, and its `src` names which, down to the model and question number.
`check_exam()` refuses any item whose `src` does not begin `Book p.` or
`Ministry assessments`, and requires exactly five MCQ per lesson. The first
draft had five scenarios written for it; all five were replaced. A paper
cannot shuffle, so each MCQ's correct letter is set by hand in `pos`;
`check_exam()` fails the build unless the letters are exactly five each, no
letter runs three times in a row, both sections go easy to hard, and every
essay has one marking point per mark. Writing space is roughly three to four
lines per mark -- the first render gave a 3-mark answer four lines and left
the pages half blank, which no gate caught.

## scripts/ is not published -- it was serving the quiz answers

Until 2026-09-26 `/curriculum/scripts/build_lecture3_quiz.py` returned 200,
and that file holds every lecture 3 question with its answer and explanation
in plain text (it must: fingerprinting happens after). The page's answer
fingerprinting protected nothing. `_config.yml` now excludes `scripts/`;
verified 404 live, with the site otherwise unchanged. Anything secret must
live in a `_teacher/` folder or in `scripts/`, never anywhere else, and never
add `.nojekyll`.

## The dashboard

`/curriculum/dashboard/` lists every lecture and its parts, generated by
`build_dashboard.py` from the lecture folders — re-run it after any lecture
change. Its one control is the exam-code switch: it writes
`localStorage["pgteach.examCode"]`, which the decks read because they share
the origin. It affects the teacher's browser only.

## Attempt integrity

No web page can block screenshots, screen recording, or leaving the tab —
those are operating-system actions, and nothing here claims otherwise. The
quiz instead **records** the shape of each attempt (time taken, times the page
lost focus, seconds away) and sends it as `integrity`, the sheet's **How it
was taken** column. A veil covers the questions while the page is away, and
students are told before starting. In the template and all three lectures.

The harness runs page scripts against a minimal DOM: calls such as
`getAttribute` or `document.addEventListener` must be feature-checked
(`typeof ... === "function"`) or CI fails.

## Why "trying again" appeared on a submission that had landed

A row was in the sheet, complete with its screenshot, while the student's
page still read "the connection is slow — trying again". Nothing was broken:
the page had simply stopped waiting before the server stopped working.

Measured against the live endpoint, using an id already in the sheet so no
row is written and no image uploaded — the cheapest path there is:

```
{"ok":true,"duplicate":true,"tab":"Lecture 2","row":2}   2.0-2.7s
```

A real submission adds a ~340KB base64 screenshot decoded and written to
Drive, and the first one after a deploy also runs the whole sheet reformat
inside `doPost` because `DESIGN_VERSION` changed. The client gave up at 12s
while the server carried on and finished the write.

Two changes. `TRY_LIMIT` is 30s, chosen from that measurement rather than
guessed. And `formatTab_` now styles the rows in use plus a 200-row margin
instead of all 1000 — about 2.6k cells instead of 13k — with each new row
inheriting the formatting of the row above, so the margin never runs out.

The dedupe is what made this safe to leave alone in the meantime: every
retry carried the same id, so the worst case was a student reading a
pessimistic message, never a duplicate row.

## Explanatory text does not belong inside an SVG

Measured at 1280x720: the smallest text inside lecture 2's diagrams rendered
at **8.7px** while ordinary HTML on the same slide was 25px. Two shrinks
stack — the figure is capped at `max-height:34vh`, and auto-fit then scales
the slide to about 0.78 — so a sentence set at 12.5 SVG units ends up
unreadable from the back of a room.

The rule now: **a diagram may carry labels, never the sentence that explains
it.** Sentences live in HTML where `clamp()` keeps them readable; labels left
inside an SVG get a floor of 15 units. On the Moore's Law slide that took the
explanation from 8.7px to 15.5px and the diagram's own numbers to 12.5px.

That is also why `.fig figcaption` is the wrong home for anything load-bearing:
its own `clamp()` tops out at 15px, which auto-fit then shrinks again.

## A slide at the 0.72 floor wants splitting

Improving slides 20 and 21 pushed both to the auto-fit floor, and 21 still
overflowed by 62px. That is the floor doing its job: it is a signal, not a
budget. Slide 21 was split into "So what do we do instead?" (the two answers)
and "Quantum computing" (the definition and the qubit diagram), and the
redundant caption came off slide 20. Lecture 2 is 32 slides now, nothing
overflows, and nothing sits at the floor.

## Slides fit themselves

`fit()` in each deck measures the active slide and scales its content to the
space available, with `FIT_FLOOR = 0.72` as the limit. The script wraps a
slide's children in a `.fitbox` at runtime, so no slide markup changed and
every future lecture gets it from the template. `transform` does not affect
layout, so the box's height is pinned to the scaled height — that is what
stops the slide scrolling, and it is easy to leave out.

Measured, not guessed: seven slides in lecture 2 overflowed by 32–90px at
1280x720; after this they overflow by 0, at scales between 0.761 and 0.898.
Lecture 1 is byte- and pixel-identical, because nothing in it needed scaling.

Shrinking the figures was tried first and rejected on the numbers: at
`max-height:24vh` the slides still overflowed by 27–59px, and one of the seven
has no figure at all. The content volume was the problem.

Two traps found while building it. `.rise` entrance delays use
`:nth-child(n)`, which still works after wrapping because the children keep
their order inside the fitbox. And in the harness, a stubbed `appendChild`
that does not detach the node from its old parent turns
`while (s.firstChild)` into an infinite loop.

A slide that hits the floor is a slide to split. There is no check for that
yet — the overflow sweep was run by hand with headless Chrome.

## Delivery is confirmed, and retries are deduplicated

The old `mode:"no-cors"` made the reply unreadable, so "sent" was a guess.
Apps Script does send `Access-Control-Allow-Origin: *` — tested, on both the
302 and the redirected response — so the reply can be read, and that is what
makes a retry a decision rather than a hope.

Page side: `deliver()` tries at 0s / 5s / 15s, tells the student the truth
between attempts, keeps unsent payloads in `localStorage` (stripped of the
~340KB screenshot), retries them on the next page load, and fires a
`sendBeacon` on `pagehide` if one is still in flight. The beacon and the queue
both drop the image because a beacon is capped near 64KB and the payload is
340KB.

Script side: a `Submission id` column, and `findById_()` refuses to append a
row for an id already present. A duplicate that carries the screenshot when
the stored row has none fills it in instead of being discarded.

Two traps worth remembering. `formatTab_` now has to *grow* a tab, not only
trim it — adding a column would otherwise make `setValues()` write past the
end of an existing sheet and throw. And `isResultsTab_` compares only the
columns that exist, so a tab written before a column was added still counts as
ours; the legacy `Sheet1` still fails it, because its second column is Name
where ours is Lecture.

The test that matters most here is the one that was missing at first: an
endpoint that *answers* with `ok:false`. A dropped connection is obvious, but
a script that ran and failed looks exactly like success unless the reply is
actually read — which is precisely the bug this replaced.

## The quiz English was simplified, and it was wrong

Lecture 2's quiz reads hard — *chronological*, *empirical observation*,
*approximately*, *escapes unintentionally*, *overlays*, *appropriate
description*, *dramatically*, *computations*. I rewrote all of it into easier
English, then checked the Ministry textbook on Drive
(`Programming-ArtificialIntelligence-En-EB-part1_copy.pdf`, Lesson 1-1) and
found every one of those words in it — several inside the book's own Worked
Examples, with the option strings matching the quiz **verbatim**. The quiz
even records `src: "p.9 — Worked Example (1), answer B"` on each question.

So the simplification was reverted. A student who only ever meets "order,
earliest first" is ambushed by "chronological order" in the exam. The quiz's
job is to rehearse the exam's language, not to be comfortable.

What replaced it, in two steps. The first was an `ar:` field glossing the
hard words in Arabic under the explanation, after the student answers. That
was still wrong, and the teacher said so immediately: *"م4 مفروض يترجم قبل ما
يجاوب"* — shouldn't it translate before he answers? He was right. A word the
student cannot read stops them answering at all, so a translation that waits
for the explanation arrives after the mark is already lost. He also pointed
out that a word like `emerging` had no gloss at all.

So the help split in two, by timing:

| field | carries | renders |
| --- | --- | --- |
| `v:` | the hard **words**, as `[["english","العربي"], ...]` | above the options, **before** answering |
| `ar:` | the **reasoning** in Arabic | with the explanation, after answering |

Ten of lecture 2's twenty questions carry a `v:`, and three of lecture 1's
ten — most of them a single term. The first pass glossed far more (19 and 9)
and the teacher cut it back: *"مترجمش كلمات سهلة أو اللي ممكن تتجاب بالsense
لكن الكلمات التقيلة ترجمها"*. He is right, and not only about noise. It took three passes to land, because
"is this word hard" keeps answering yes — `staff`, `vehicle`, `goods and
services` all survived a cut on that question and had to be removed after he
pointed at `staff` on a live question. The test that actually works is
different: **cover the word with your thumb — can you still answer? Then cut
it.** Ask what the rest of the sentence already gives you, not how hard the
word looks on its own — a list
that is mostly easy words pushes the options down a phone screen and teaches
the eye to skip the block, so it costs you the words that mattered. What
survives is formal English carrying no marks (*chronological*,
*Commercialization*, *purchasing*, *appropriate*, *dramatically*, *roughly*,
*onward*, *computations*), false friends (*notes and coins* is not ملاحظات,
*works out* is not يتمرن), and technical phrases the sentence does not
explain (*integrated circuit*, *emerging technology*). What went: everyday
words, Arabic loanwords they already say, and their own syllabus terms in
English — glossing *Input*, *Compiling* or *debug* undoes the lesson.

The reasoning was stripped back out of the five `ar:` fields, because
`v:` renders while the options are still live — leaving "the right order is
computer, then internet" in there would have printed an answer key above the
answers.

`check_lecture.py` enforces the three rules that keep the two apart: every
glossed term must appear in the question or an option; translating the correct
option in full obliges you to translate every option (or the right answer is
the only readable one); and at most six terms, or the block pushes the options
off a phone screen. `test_pages.js` drives a full attempt and asserts the
gloss is on screen *before* the pick, that it clears between questions, and
that `ar:` never leaks into it.

The general rule this settles: **check the source material before deciding
the wording is too hard.** Lecture 1, which is not textbook-derived, was
already at a plain level — but it still got glosses, because plain English is
not the same as English an Arabic-speaking student reads without friction.

## Editing a question after it is fingerprinted

`protect_answers.py --unlock` turns each `k: "..."` back into `a: N` by
finding which option still matches, so questions can be edited and then
re-fingerprinted. It has to run **before** the edit: once an option's text has
changed, nothing matches and the index is unrecoverable. In that case it names
the question and refuses rather than guessing.

This gap was found the hard way. Simplifying lecture 2's English changed the
text of three correct options, and the tool could not re-derive their indices
— they had to be recovered by resolving the fingerprints in the committed
version from git. `--unlock` exists so that is never necessary again.

## Answers are fingerprinted, not hidden

`QUESTIONS` used to carry `a: 1`, so View Source handed a student every
answer — an easier route than the `_teacher/` folder ever was.
`scripts/protect_answers.py` rewrites each `a: N` as `k: "<cyrb53>"`, and
`ansOf(q)` in the page finds which option matches. It still accepts a plain
`a:` so an unconverted lecture keeps working.

Be clear about the ceiling: the fingerprint function ships in the page, so
`QUESTIONS.map(q => q.o[ansOf(q)])` in the console returns everything. This
moves the answers from *readable* to *computable*, which for a foundations
class that has not learned programming is a real barrier and for anyone else
is none. There is no way to hide them properly in a client-side quiz — that
needs server-side grading, which would cost the instant per-question
feedback, and that feedback is the most valuable thing the quiz does.

The dangerous failure mode is an option's text being edited without
re-running the script: nothing matches, `ansOf` returns -1, and every answer
counts as wrong, silently. Both checks fail on it and both run in CI. Tested
by adding a single trailing space to a correct option — invisible to the eye,
caught by both.

## Two tests, and the difference between them

```bash
python scripts/check_lecture.py     # reads the pages
node    scripts/test_pages.js       # runs them
```

Both run in CI on every push (`.github/workflows/check-lectures.yml`).

The second one matters more than it looks. It stubs enough of a browser to
execute each page's real `<script>`, drives a whole quiz attempt, and asserts
what the student sees and what gets submitted — the shuffled options located
by text rather than position, the payload key by key, the result card's
contents, and that the correct answer reaches every slot over 400 renders.
The two worst bugs in this repo's history — a stray `[cite: 3]` inside a
string literal that made the quiz completely dead, and the correct answer
sitting in slot 2 of nine questions — were both invisible to a reader and
obvious to a runner. 330 checks across two lectures at the time of writing.

An earlier version of this harness lived in a scratch directory and was lost
when it was cleaned up. That is why it is in the repo now.

## How this was verified

There is no test framework in the repo; verification was done by extracting
each page's `<script>` and running it against a stubbed DOM under Node. If you
change page logic, do the same rather than trusting a visual check — the
`[cite:]` bug and the always-slot-2 bug were both invisible on screen.

What was asserted: intake rejections (one-word name, short/long phone, missing
date), date autofill, every question rendered with its options intact, section
tags, counters, answer highlighting, locked options after answering, score,
section breakdown rows, review cards, retake reset, and the exact POST payload
key-by-key. The canvas is stubbed so the card code really runs, and every text
run it draws is asserted (header, name, score, each section, the mistakes, the
footer).

The card was also rendered for real, by extracting its code into a standalone
page with fake state and screenshotting it with headless Chrome:

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu   --window-size=920,1500 --virtual-time-budget=12000   --screenshot=card.png "file:///path/to/card-test.html"
```

Worth repeating after any change to the drawing code — the stub proves the calls
happen, not that the layout looks right. Plus: the correct answer reaches every slot over 400 renders, every
question is asked exactly once per attempt, and 200 attempts open with all
questions represented.

Quick sanity check without the harness:

```bash
python - <<'PY'
import io, re
for p in ["lecture1/quiz/index.html", "lecture1/slides/index.html"]:
    s = io.open(p, encoding="utf-8").read()
    print(p, "| [cite:", s.count("[cite:"), "| sections", s.count('<section class="slide'))
PY
node --check <(sed -n '/<script>/,/<\/script>/p' lecture1/quiz/index.html | sed '1d;$d')
```

## Gotchas

- Keep files LF. Both `new_lecture.py` and the page writers use `newline="\n"`.
- `templates/` holds its own copy of the shared CSS and quiz engine. A change
  meant for *every* lecture must go into the template **and** the existing
  `lectureN/` files — templates are only read when scaffolding.
- Placeholders are split by escaping context: `__TITLE_HTML__` is
  HTML-escaped, `__TITLE_JS__` is escaped for a JS string. Do not merge them,
  or a title containing `&` or `"` breaks one of the two.
- **Pages builds with Jekyll**, which runs Liquid over every `.md` and
  `.html` file *before* Markdown. Liquid's two delimiters — a doubled
  curly brace, and a curly brace followed by a percent sign — therefore
  break the build even inside backticks or a fenced code block. There is
  no way to show them literally in this file, which is exactly what broke
  commits `a63ed4e` and `2209593`: first by writing the warning, then by
  trying to escape it with a raw block whose closing tag ended the block
  early. Describe them in words instead.
- **A failed Jekyll build skips the deploy entirely**, so the whole site
  keeps serving the previous commit — the slides and quiz included. The
  Pages API reports this as `building`, never as an error, so check the
  workflow instead. Before every push:

  ```bash
  grep -rnE '\{[%{]' --include='*.md' --include='*.html' .   # must print nothing
  ```

  ```bash
  gh run list --repo PGteach/curriculum --limit 1   # must say success
  ```
- Do not add paths starting with `_`; Jekyll ignores them.
- The git identity on the original machine was `eissa2002`, but the repo
  belongs to `PGteach`; pushing needs `gh auth login` as PGteach. Commits here
  are authored as `PGteach <323123806+PGteach@users.noreply.github.com>`.
