# PGteach — Curriculum

Interactive lecture slides and self-check quizzes, served straight from GitHub
Pages. One folder per lecture, two pages per lecture.

## Live URLs

| Lecture | Slides | Quiz |
| --- | --- | --- |
| 1 — How does a computer think? | [/lecture1/slides](https://pgteach.github.io/curriculum/lecture1/slides) | [/lecture1/quiz](https://pgteach.github.io/curriculum/lecture1/quiz) |

Every lecture follows the same pattern:

```
https://pgteach.github.io/curriculum/lectureN/slides
https://pgteach.github.io/curriculum/lectureN/quiz
```

## Structure

```
curriculum/
├── lecture1/
│   ├── slides/index.html      12 slides, keyboard + swipe navigation
│   └── quiz/index.html        10 questions, 4 sections, results recorded to a Sheet
├── templates/
│   ├── slides-template.html   skeleton deck with the shared chrome
│   └── quiz-template.html     skeleton quiz with the shared engine
├── scripts/
│   ├── new_lecture.py         scaffolds lectureN/ from the templates
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
| `-n, --dry-run` | report what would be written, write nothing |
| `-f, --force` | overwrite an existing `lectureN/` |

Then fill in the content:

1. **Slides** — add or remove `<section class="slide">` blocks in
   `lectureN/slides/index.html`. Keep the QR slide last.
2. **Questions** — edit `SECTIONS` and `QUESTIONS` at the top of the
   `<script>` in `lectureN/quiz/index.html`.
3. Open both files in a browser, then commit and push to `main`.

### Answer positions do not matter

Both the options and the question order are shuffled at runtime, so you can
write the correct answer in whatever slot reads most naturally. Options are
reshuffled on every render; question order is reshuffled once per attempt, so
two students sitting together are not on the same question at the same time.

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
  ]
}
```

`wrongQuestions` is an array — one entry per mistake, in the order they were
made. The same list is what the student sees under **Questions to review** on
the results screen.

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

Because the request is fire-and-forget, a student always sees "sent to your
teacher" even if the script errors. Confirm in the Sheet, or in the Apps Script
editor's Executions tab.

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
