# -*- coding: utf-8 -*-
"""Make build_lectureN_slides.py from lecture 5's builder: keep its proven
helpers and build block, swap in lecture N's diagrams, drawings and slides.
    python derive_slides.py N content.py slides.py css.txt doc.txt"""
import io, sys
N = int(sys.argv[1])
content = io.open(sys.argv[2], encoding="utf-8").read().strip()
slides = io.open(sys.argv[3], encoding="utf-8").read().strip()
css = io.open(sys.argv[4], encoding="utf-8").read().strip()
doc = io.open(sys.argv[5], encoding="utf-8").read().strip()
L5 = io.open("scripts/build_lecture5_slides.py", encoding="utf-8").read()

def at(s, a, start=0):
    i = s.index(a, start); return i
c0 = at(L5, "# --------------------------------------------------------------------------\n# diagrams")
c1 = at(L5, 'PHOTO_CSS = """')
s0 = at(L5, "SLIDES = []")
s1 = at(L5, "def port_lightbox(out):")
head = L5[:c0]
head = head[head.index("import io, re"):]
out = ('# -*- coding: utf-8 -*-\n"""' + doc + '\n"""\n' + head.replace('lecture5/slides', 'lecture%d/slides' % N)
       + content + "\n\n\n" + L5[c1:s0] + slides + "\n\n\n" + L5[s1:])
out = out.replace("scripts/lecture5_slides_base.html", "scripts/lecture%d_slides_base.html" % N)
out = out.replace("/* the video: bigger", "/* lecture %d's drawings */\n%s\n\n/* the video: bigger" % (N, css), 1)
assert "lecture5" not in out, [l for l in out.split("\n") if "lecture5" in l]
assert 'DST = "lecture%d/slides/index.html"' % N in out
io.open("scripts/build_lecture%d_slides.py" % N, "w", encoding="utf-8", newline="\n").write(out)
print("written build_lecture%d_slides.py" % N, len(out))
