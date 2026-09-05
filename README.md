# PGteach — Curriculum

Interactive lecture slides and self-check quizzes, served straight from GitHub
Pages. One folder per lecture, two pages per lecture.

## Live URLs

| Lecture | Slides | Quiz | Printable handout |
| --- | --- | --- | --- |
| 1 — How does a computer think? | [/lecture1/slides](https://pgteach.github.io/curriculum/lecture1/slides) | [/lecture1/quiz](https://pgteach.github.io/curriculum/lecture1/quiz) | [/lecture1/handout](https://pgteach.github.io/curriculum/lecture1/handout) |

Every lecture follows the same pattern:

```
https://pgteach.github.io/curriculum/lectureN/slides
https://pgteach.github.io/curriculum/lectureN/quiz
https://pgteach.github.io/curriculum/lectureN/handout
```

## Structure

```
curriculum/
├── lecture1/
│   ├── slides/index.html      12 slides, keyboard + swipe navigation
│   ├── quiz/index.html        10 questions, 4 sections, results recorded to a Sheet
│   └── handout/index.html     7-page A4 student booklet, print from the browser
├── templates/
│   ├── slides-template.html   skeleton deck with the shared chrome
│   ├── quiz-template.html     skeleton quiz with the shared engine
│   └── handout-template.html  skeleton booklet with the print stylesheet
├── templates/blocks.html      gallery: every slide layout, one per slide
├── scripts/
│   ├── new_lecture.py         scaffolds lectureN/ from the templates
│   ├── check_lecture.py       validates a lecture before you publish it
│   ├── test_pages.js          runs every page in a fake browser
│   ├── protect_answers.py     turns `a: 1` into an answer fingerprint
│   └── apps-script.gs         the Apps Script that records quiz results
├── HANDOFF.md                 current state, open items, gotchas
└── README.md
```

Each `index.html` is fully self-contained — no build step, no bundler, no
shared asset folder. The only external requests are Google Fonts and the QR
image service, so a page dropped anywhere still works.

## Adding a lecture

```bash
python scripts/new_lecture.py 2 "Variables & Data Types"
```

That creates `lecture2/slides/index.html` and `lecture2/quiz/index.html` with
the lecture number, title, page titles, QR code target and quiz payload label
all filled in, then verifies the result and prints the two live URLs.

Useful flags:

| Flag | Effect |
| --- | --- |
| `-t, --topic "…"` | course line on slide 1 (default: *Programming & Artificial Intelligence*) |
| `-a, --accent "#6A4C93"` | accent colour for the deck and handout (default: cycles by lecture number) |
| `-n, --dry-run` | report what would be written, write nothing |
| `-f, --force` | overwrite an existing `lectureN/` |

Then fill in the content:

1. **Slides** — add or remove `<section class="slide">` blocks in
   `lectureN/slides/index.html`. Keep the QR slide last.
2. **Questions** — edit `SECTIONS` and `QUESTIONS` at the top of the
   `<script>` in `lectureN/quiz/index.html`.
3. **Handout** — one `<section class="sheet">` per printed A4 page in
   `lectureN/handout/index.html`.
4. Check it before publishing:

   ```bash
   python scripts/check_lecture.py 2
   ```

   It fails on template text left in place, a QR pointing at the wrong
   lecture, an answer index off the end of its options, a section with no
   questions, JavaScript that will not parse, and a Liquid delimiter that
   would take the whole site down. Exit code is non-zero when anything is
   wrong, so it can gate a commit.
5. Hide the answers from the page source:

   ```bash
   python scripts/protect_answers.py 2
   ```

   Each `a: 1` becomes `k: "<fingerprint>"`. **Re-run it after editing any
   option's text** — if an option changes and its fingerprint does not, no
   option matches and every answer counts as wrong. Both checks fail on
   exactly that, and both run in CI, so it cannot reach students.

   This stops the answers being *read*. It does not stop them being
   *computed*: the fingerprint function is in the page, so one line in the
   console still returns them. For a class that has not learned programming
   it is a real barrier; treat it as nothing more than that.

6. Open all three in a browser, then commit and push to `main`.

### Answer positions do not matter

Both the options and the question order are shuffled at runtime, so you can
write the correct answer in whatever slot reads most naturally. Options are
reshuffled on every render; question order is reshuffled once per attempt, so
two students sitting together are not on the same question at the same time.

### Every lecture is the same shape, not the same colour

Structure, typography and behaviour are shared on purpose — students should
not have to relearn where things are each week. What changes per lecture is
the **accent colour**, set once in `LECTURE_ACCENT` and picked up by the deck
and the handout: the progress bar, the eyebrow labels, the numbered steps, the
nav dots, the compare panels, the table headers and the handout's header rule.

`new_lecture.py` cycles a palette by lecture number (teal, violet, blue, rose,
green, amber) or takes `--accent "#RRGGBB"`. **The quiz keeps the standard
palette** — green and red mean right and wrong there, and that must not drift
lecture to lecture.

For more variety than colour, vary the *layout blocks* rather than the design.
Open **[templates/blocks.html](templates/blocks.html)** in a browser: it is a
real deck with one slide per available layout, so you can see them all and copy
the markup straight out of its source.

| Block | Use it when |
| --- | --- |
| `.pipe` + `.step` | a flow, read across |
| `.timeline` + `.tl` | a sequence, read down — better for four or more steps |
| `.vs` + `.pane` | two things, side by side |
| `.scale` | a spectrum, when the answer is "somewhere between" |
| `.statement` | one line, nothing else — the point you want to land |
| `.stats` + `.stat` | the figure is the point |
| `.check` | do this, not that |
| `.quote` | someone else's words |
| `.kit` + `.card` | a small set of things, with icons |
| `table` | many rows, same shape |
| `.fields` + `.chip` | a list with no order |

`class="slide dark"` inverts any slide to navy — worth doing on the one or two
slides you most want remembered.

### Nothing needs counting by hand

The slide total, the nav dots, the progress bar, the `n / total` counter, the
question total, the per-section tracks and the QR code are all derived at
runtime from the DOM and the `QUESTIONS` array. Adding a slide or a question is
a one-place edit.

Each page carries a single `LECTURE CONFIG` block near the top of its
`<script>` — the lecture number, title and topic. Everything else on the page,
including both `pgteach.github.io` URLs, is built from it. That block is the
only thing `new_lecture.py` rewrites.

## Writing slides

Slides are plain HTML using the classes already in the deck:

| Class | Use |
| --- | --- |
| `class="slide dark"` | inverted (navy) slide |
| `class="rise"` | reveal this child in sequence when the slide opens |
| `.eyebrow` / `h2` / `.sub` | section label, headline, supporting line |
| `.arline .ar` | the Arabic explanation line (RTL, IBM Plex Sans Arabic) |
| `.pipe` + `.step` | numbered pipeline diagram |
| `.vs` + `.pane a` / `.pane b` | two-column compare |
| `.kit` + `.card` | icon row |
| `.fields` + `.chip` | tag cloud |
| `table` | comparison table |
| `.codeline .mono` | inline code chip |

Navigation: arrow keys, space, PageUp/PageDown, Home/End, the dots, or swipe.
The current slide is mirrored in the URL hash, so `#7` deep-links to slide 7.

## Printing the handout

Open `lectureN/handout` in a browser and press **Print this sheet**, or
Ctrl/Cmd-P. The page is laid out in A4 with margins already set, one
`<section class="sheet">` per sheet of paper, so what you see is what prints —
there is no separate PDF to keep in sync.

The page margin is deliberately `0`, with the margins supplied by each sheet's
own padding. Browsers can only draw their date / title / file-path / page-number
furniture inside the page margin, so with none there they print nothing of their
own. If a browser still adds them, switch off **Headers and footers** in the
print dialog.

The QR code on the last page is generated from the lecture number, and the page
numbers in the footers are counted at runtime, so copying a sheet block or
adding a page needs no renumbering and can never leave a stale link on paper.
If the QR image fails to load, a red warning appears next to it — never print a
sheet that shows it.

Reusable blocks: `.stages` (numbered row), `table` with `td.k` for the label
column, `.term` (gold rule), `.fields`/`.chip` (tag row), `.write` + `.rule`
(write-in line), `ol.qs` (numbered questions), `.summary` (highlighted box),
`p.ar` (Arabic line, RTL).

## Quiz results

On submission the quiz POSTs JSON to the Apps Script endpoint set as
`RESULTS_URL`:

```json
{
  "lecture": "Lecture 1",
  "name": "Ali Hassan Mohamed",
  "phone": "01001234567",
  "date": "2026-08-31",
  "score": 8,
  "total": 10,
  "weak": "How computers work, Tools & mindset",
  "sections": "How computers work: 1/2 | Programming & AI terms: 3/3 | Tools & mindset: 2/3 | Career fields: 2/2",
  "wrongQuestions": [
    {
      "question": "What is the first stage in how a computer handles any task?",
      "selected": "Processing",
      "correct": "Input",
      "why": "Everything starts with input — the computer receives data before it can do anything with it."
    }
  ],
  "image": "iVBORw0KGgoAAAANSUhEUgAA…"
}
```

`wrongQuestions` is an array — one entry per mistake, in the order they were
made. The same list is what the student sees under **Questions to review** on
the results screen.

`image` is a base64 PNG of the result card, drawn on a `<canvas>` from the same
data at the moment the student finishes — the student does not screenshot
anything. It is roughly 250 KB for a typical attempt. If the drawing fails for
any reason the field is `""` and the submission still goes through; it is also
dropped if it somehow exceeds 4 MB.

The Apps Script decodes it into Drive under
`PGteach quiz results / Lecture N /` and writes the file link in the sheet's
Screenshot column. **Those files are deliberately left private** to the account
that owns the script — they carry student names and phone numbers, so nothing in
the script shares them.

The request is sent with `mode: "no-cors"` (a browser cannot read a response
from Apps Script without CORS headers, and none are needed here) and
`Content-Type: text/plain;charset=utf-8`, which is the only JSON-carrying
content type a no-cors request is allowed to set. Apps Script reads the body
from `e.postData.contents` either way.

The receiving script lives in [scripts/apps-script.gs](scripts/apps-script.gs).
It writes one tab per lecture (created on demand), flattens `wrongQuestions`
into a readable Mistakes column, and forces the Phone column to text so Sheets
does not read `01129907116` as a number and drop the leading zero.

To install it: open the Sheet, Extensions > Apps Script, paste the file in, then
Deploy > New deployment > Web app, **Execute as: me**, **Who has access:
anyone**, and paste the `/exec` URL into `RESULTS_URL`. After any later edit you
must deploy a **new version** — saving alone does not change the live URL.

Set `RESULTS_URL = ""` to turn sending off; the quiz still runs and still
shows the student their review list.

Intake requires a full name (two words or more), a phone number of 8–15
digits, and a date, which is pre-filled with today.

### The submission is confirmed, not assumed

It used to be fire-and-forget: `mode:"no-cors"` meant the browser could not
read the reply, so the page said "sent" the moment the request left — true or
not. Thirty phones on one classroom network is exactly when that lies.

Apps Script does return CORS headers, so the reply is readable. Now:

1. it POSTs with the screenshot and **reads the reply**
2. on failure it retries — at 0s, 5s and 15s — and the student is told
   "the connection is slow, trying again", never "sent"
3. anything still unsent is kept in `localStorage` and retried on the next
   visit, without the screenshot so it stays small
4. if the page is closing mid-flight, `navigator.sendBeacon` carries a slim
   copy; a row with no picture beats no row

Every attempt sends the same `id`, and the script ignores an id it has already
stored, so retrying cannot produce two rows for one student. If a later copy
carries the screenshot and the stored row does not, it fills it in.

The student only ever sees **Saved** when the script has said so.

## GitHub Pages

Settings → Pages → Deploy from a branch → `main` / `/ (root)`. Folder names
map straight to URL paths, and every in-repo link is relative
(`../quiz/`, `../slides/`), so the pages work opened from disk as well as on
Pages.

## Keeping the templates current

`templates/` holds its own copy of the shared chrome (the CSS, the deck
navigation, the quiz engine). A change to how *every* lecture looks or behaves
belongs in both the template and the existing `lectureN/` files — the
templates are only read when a new lecture is scaffolded.
