# -*- coding: utf-8 -*-
"""Make build_lectureN.py from build_lecture5.py: same helpers, homework,
key and model-answer code; lecture N's constants, booklet and page plans.
    python derive_print.py spec.py"""
import io, sys, importlib.util
spec = importlib.util.spec_from_file_location("spec", sys.argv[1]); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
N = S.N
L5 = io.open("scripts/build_lecture5.py", encoding="utf-8").read()

def swap(s, a, b, label):
    i = s.index(a); j = s.index(b, i)
    return s[:i] + "@@" + label + "@@" + s[j:], s[i:j]

out = L5
d0 = out.index('"""'); d1 = out.index('"""', d0 + 3) + 3
out = out[:d0] + '"""' + S.DOC + '\n"""' + out[d1:]
out, _ = swap(out, "HW_SECTIONS = [", "HOMEWORK = [n for", "HW")
out, _ = swap(out, "# ------------------------------------------------------------------ booklet", "# ----------------------------------------------------------------- homework", "BOOK")
out, _ = swap(out, "KEY_PAGES = [", "def check_key_order():", "KEY")
out, _ = swap(out, "MODEL_PAGES = [", "def model_answers(head, tail):", "MODEL")
i = out.index("        head = ('<h2>What to revise</h2>"); j = out.index("    else:", i)
out = out[:i] + "@@REVISE@@" + out[j:]
out = (out.replace("@@HW@@", S.HW.strip() + "\n")
          .replace("@@BOOK@@", S.BOOK.strip() + "\n\n\n")
          .replace("@@KEY@@", S.KEY.strip() + "\n\n\n")
          .replace("@@MODEL@@", S.MODEL.strip() + "\n\n\n")
          .replace("@@REVISE@@", S.REVISE.rstrip() + "\n"))
for a, b in [('T = ROOT / "lecture5" / "_teacher"', 'T = ROOT / "lecture%d" / "_teacher"' % N),
             ('TITLE = "Is this connection safe?"', 'TITLE = "%s"' % S.TITLE),
             ('ACCENT = "#2D7A4B"', 'ACCENT = "%s"' % S.ACCENT),
             ("build_lecture5_slides.py", "build_lecture%d_slides.py" % N),
             ('.replace("__LECTURE_NUM__", "5")', '.replace("__LECTURE_NUM__", "%d")' % N),
             ("' &middot; Lecture 5</div>", "' &middot; Lecture %d</div>" % N),
             ('L5 = "Lecture 5 %s — " + TITLE', 'L%d = "Lecture %d %%s — " + TITLE' % (N, N)),
             ("L5 %", "L%d %%" % N), ("lecture5/", "lecture%d/" % N)]:
    assert a in out, a
    out = out.replace(a, b)
bad = [l for l in out.split("\n") if ("lecture5" in l or "Lecture 5" in l) and "Derived from" not in l]
assert not bad, bad
io.open("scripts/build_lecture%d.py" % N, "w", encoding="utf-8", newline="\n").write(out)
print("written build_lecture%d.py" % N, len(out))
