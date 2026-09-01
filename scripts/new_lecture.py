#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scaffold a new lecture from templates/.

    python scripts/new_lecture.py 2 "Variables & Data Types"

Creates lectureN/slides/index.html and lectureN/quiz/index.html with the
lecture number, title, topic and quiz URL already filled in, then prints the
GitHub Pages URLs to check.

Nothing in the generated files hardcodes a slide count or a question count:
both are derived at runtime from the DOM and the QUESTIONS array, and the QR
code is built from the lecture number, so there is no third place to update.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
SITE_BASE = "https://pgteach.github.io/curriculum"

# (subfolder, template filename)
PAGES = (
    ("slides", "slides-template.html"),
    ("quiz", "quiz-template.html"),
    ("handout", "handout-template.html"),
)

TOKEN_RE = re.compile(r"__[A-Z_]+__")
HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

# A different accent per lecture, so the decks are not all the same colour.
# Cycled by lecture number when --accent is not given. All picked dark enough
# to hold white text in the slide chrome and the handout header.
ACCENTS = [
    "#0E7C7B",   # teal      (lecture 1)
    "#6A4C93",   # violet
    "#1D6FA5",   # blue
    "#A63D5B",   # rose
    "#3F7D3A",   # green
    "#B4622A",   # amber
]


def esc_html(text: str) -> str:
    """Escape for an HTML text node."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def esc_js(text: str) -> str:
    """Escape for a double-quoted JavaScript string literal."""
    return (text.replace("\\", "\\\\")
                .replace('"', '\\"')
                .replace("</", "<\\/"))


def render(template: str, num: int, title: str, topic: str, accent: str) -> str:
    out = (template
           .replace("__ACCENT__", accent)
           .replace("__LECTURE_NUM__", str(num))
           .replace("__TITLE_HTML__", esc_html(title))
           .replace("__TITLE_JS__", esc_js(title))
           .replace("__TOPIC_HTML__", esc_html(topic))
           .replace("__TOPIC_JS__", esc_js(topic)))
    leftover = sorted(set(TOKEN_RE.findall(out)))
    if leftover:
        sys.exit("error: template placeholder(s) left unfilled: %s\n"
                 "       Add a matching --option to scripts/new_lecture.py."
                 % ", ".join(leftover))
    return out


def verify(path: Path, num: int, title: str) -> None:
    """Cheap post-write sanity check on the file we just produced."""
    text = path.read_text(encoding="utf-8")
    problems = []

    if TOKEN_RE.search(text):
        problems.append("unfilled __TOKEN__ placeholders remain")
    if 'const LECTURE_NUM   = %d;' % num not in text:
        problems.append("LECTURE_NUM was not set to %d" % num)
    if esc_js(title) not in text:
        problems.append("lecture title missing from the config block")
    # The URL is assembled at runtime, so check the parts it is built from.
    if SITE_BASE not in text:
        problems.append("SITE_BASE missing (quiz URL would be wrong)")
    if path.parent.name == "slides":
        if 'id="qr"' not in text or "create-qr-code" not in text:
            problems.append("QR code element or generator missing")
        if 'href="../quiz/"' not in text:
            problems.append("relative link to ../quiz/ missing")
    if path.parent.name == "quiz":
        if "lecture: LECTURE.label" not in text:
            problems.append("submission payload is missing the lecture field")
        if 'href="../slides/"' not in text:
            problems.append("relative link to ../slides/ missing")
        if "image: image" not in text:
            problems.append("submission payload is missing the result screenshot")
    if "--teal" not in text and path.parent.name in ("slides", "handout"):
        problems.append("accent colour is never applied")
    if path.parent.name == "handout":
        # A printed sheet cannot be corrected later, so check it hard.
        if 'id="qr"' not in text or "create-qr-code" not in text:
            problems.append("QR code element or generator missing")
        if "encodeURIComponent(LECTURE.quizUrl)" not in text:
            problems.append("QR is not built from the lecture's quiz URL")
        if text.count('class="sheet"') < 2:
            problems.append("handout has fewer than two printable pages")
        if 'class="pageno"' not in text:
            problems.append("page-number slots missing from the footers")

    if problems:
        sys.exit("error: %s failed verification:\n  - %s"
                 % (path.relative_to(ROOT), "\n  - ".join(problems)))


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Scaffold lectureN/{slides,quiz} from templates/.",
        epilog='example: python scripts/new_lecture.py 2 "Variables & Data Types"')
    ap.add_argument("number", type=int, help="lecture number, e.g. 2")
    ap.add_argument("title", help='lecture title, e.g. "Variables & Data Types"')
    ap.add_argument("-t", "--topic", default="Programming & Artificial Intelligence",
                    help="course line shown on slide 1 (default: %(default)s)")
    ap.add_argument("-a", "--accent", default=None,
                    help="hex accent colour for the slides and handout, "
                         "e.g. \"#6A4C93\" (default: cycles by lecture number)")
    ap.add_argument("-f", "--force", action="store_true",
                    help="overwrite lectureN if it already exists")
    ap.add_argument("-n", "--dry-run", action="store_true",
                    help="report what would be written, write nothing")
    args = ap.parse_args()

    if args.number < 1:
        sys.exit("error: lecture number must be 1 or greater.")
    title = args.title.strip()
    if not title:
        sys.exit("error: lecture title must not be empty.")

    accent = args.accent or ACCENTS[(args.number - 1) % len(ACCENTS)]
    if not HEX_RE.match(accent):
        sys.exit("error: --accent must be a hex colour like #6A4C93, got %r" % accent)

    dest = ROOT / ("lecture%d" % args.number)
    if dest.exists() and not (args.force or args.dry_run):
        sys.exit("error: %s already exists. Re-run with --force to overwrite it."
                 % dest.relative_to(ROOT))

    missing = [t for _, t in PAGES if not (TEMPLATES / t).is_file()]
    if missing:
        sys.exit("error: missing template(s) in templates/: %s" % ", ".join(missing))

    written = []
    for folder, tpl_name in PAGES:
        template = (TEMPLATES / tpl_name).read_text(encoding="utf-8")
        page = render(template, args.number, title, args.topic.strip(), accent)
        out = dest / folder / "index.html"

        if args.dry_run:
            print("would write %s (%d bytes)" % (out.relative_to(ROOT), len(page)))
            continue

        out.parent.mkdir(parents=True, exist_ok=True)
        # newline="\n" keeps GitHub Pages output byte-identical across machines.
        with out.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(page)
        verify(out, args.number, title)
        written.append(out)

    if args.dry_run:
        print("\nDry run — nothing written.")
        return

    rel = dest.relative_to(ROOT).as_posix()
    print("Created Lecture %d — %s\n" % (args.number, title))
    for out in written:
        print("  %s" % out.relative_to(ROOT).as_posix())
    print("\nLive once pushed to the main branch:")
    print("  slides  %s/lecture%d/slides" % (SITE_BASE, args.number))
    print("  quiz    %s/lecture%d/quiz" % (SITE_BASE, args.number))
    print("  handout %s/lecture%d/handout" % (SITE_BASE, args.number))
    print("\nAccent colour: %s  (change LECTURE_ACCENT in either file, "
          "or re-run with --accent)" % accent)
    print("\nNext:")
    print("  1. Write the slides    -> %s/slides/index.html" % rel)
    print("     (add/remove <section class=\"slide\"> blocks; counts update themselves)")
    print("  2. Write the questions -> %s/quiz/index.html" % rel)
    print("     (edit SECTIONS and QUESTIONS near the top of the <script>)")
    print("  3. Write the handout   -> %s/handout/index.html" % rel)
    print("     (one <section class=\"sheet\"> per printed A4 page; the QR and the")
    print("      page numbers fill themselves in)")
    print("  4. Open all three in a browser to check them, then commit.")


if __name__ == "__main__":
    main()
