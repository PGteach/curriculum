# Handoff — state of this repo

Last updated: 2026-08-31. Written so a new session (or another machine) can pick
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
templates/slides-template.html
templates/quiz-template.html
scripts/new_lecture.py        scaffolds lectureN from templates/
scripts/apps-script.gs        the Google Apps Script that records results
README.md · HANDOFF.md · .gitignore
```

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
and it works, but **it is still running the old 8-column script**, which drops
two fields the quiz now sends.

To finish: paste [scripts/apps-script.gs](scripts/apps-script.gs) into the Sheet's
Apps Script editor, then **Deploy > Manage deployments > edit > Version: New
version**. Saving alone does not update the live URL.

What that script changes:

- adds a **Lecture** column and a **Mistakes** column (`wrongQuestions`
  flattened into readable text) — both were being silently discarded
- **one tab per lecture**, created on demand and kept in numeric order. Set
  `ONE_TAB_PER_LECTURE = false` for a single "All results" tab instead
- forces the Phone column to text format. Sheets was reading `01129907116` as
  a number and dropping the leading zero (visible in the old `Sheet1`:
  `12436494`). Already-stored numbers cannot be recovered
- `migrateOldRows()` copies the 4 existing `Sheet1` rows into the Lecture 1 tab,
  marking Mistakes as `(not recorded)`. Run it once by hand, check, then delete
  `Sheet1` yourself

Because the quiz posts with `mode:"no-cors"`, **the browser cannot read the
response** — if the script throws, the student still sees "sent to your
teacher". Verify in the sheet, or in the Apps Script editor's Executions tab.

## Open decisions

- **Old QR codes are dead.** `/curriculum/slides` and `/curriculum/quiz` now
  return 404. If printed QR codes are in circulation, add redirect stubs at
  those two paths. Not done — waiting on whether any are out there.
- **No landing page.** `/curriculum/` currently renders `README.md` via Jekyll.
  A real root `index.html` listing lectures was offered and not yet requested.
- Slide 12 says "10 questions" as static text; it is not derived from the
  quiz's `QUESTIONS.length` (different page). Templates say just
  "Test yourself".
- **Jekyll is a liability here.** Any Markdown file containing Liquid
  delimiters fails the build, and a failed build blocks the deploy of the
  slides and quiz too — a docs typo can take the teaching pages offline.
  Adding `.nojekyll` makes the build serve files verbatim and immune to
  this, but it also removes the auto-generated landing page at
  `/curriculum/`, so it needs a real root `index.html` alongside it.
  Offered, not yet decided.

## Adding a lecture

```bash
python scripts/new_lecture.py 2 "Variables & Data Types"
```

Then write the slides (`<section class="slide">` blocks, QR slide stays last)
and the questions (`SECTIONS` / `QUESTIONS` at the top of the quiz `<script>`).
Answer positions do not matter any more — they get shuffled.

## How this was verified

There is no test framework in the repo; verification was done by extracting
each page's `<script>` and running it against a stubbed DOM under Node. If you
change page logic, do the same rather than trusting a visual check — the
`[cite:]` bug and the always-slot-2 bug were both invisible on screen.

What was asserted: intake rejections (one-word name, short/long phone, missing
date), date autofill, every question rendered with its options intact, section
tags, counters, answer highlighting, locked options after answering, score,
section breakdown rows, review cards, retake reset, and the exact POST payload
key-by-key. Plus: the correct answer reaches every slot over 400 renders, every
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
- Pages builds with Jekyll (`build_type: legacy`), which runs Liquid over
  every `.md` and `.html` file **before** Markdown, so its delimiters break
  the build even inside backticks or a fenced code block. Writing that
  warning literally is what broke the deploy in commit `a63ed4e`; the fix
  is a raw block:
  {% raw %}
  ```
  {% raw %} ... {% endraw %}   <- wrap any literal {{ or {% you need
  ```
  {% endraw %}
  A failed Jekyll build skips the deploy entirely, so the whole site keeps
  serving the previous commit — check
  `gh run list --repo PGteach/curriculum` after pushing, not just the
  Pages API, which reports `building` rather than `errored`.
  Also do not add paths starting with `_`.
- The git identity on the original machine was `eissa2002`, but the repo
  belongs to `PGteach`; pushing needs `gh auth login` as PGteach. Commits here
  are authored as `PGteach <323123806+PGteach@users.noreply.github.com>`.
