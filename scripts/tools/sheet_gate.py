# -*- coding: utf-8 -*-
"""Render every .sheet of a document ON ITS OWN and count its printed pages."""
import io, os, re, subprocess, sys
import pypdfium2 as pdfium
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SP = sys.argv[1]; bad = 0
for doc in sys.argv[2:]:
    html = io.open(doc, encoding="utf-8").read()
    starts = [m.start() for m in re.finditer(r'<section class="sheet', html)]
    first, last = starts[0], html.rindex("</section>") + len("</section>")
    res = []
    for s in starts:
        e = html.index("</section>", s) + len("</section>")
        f = os.path.join(SP, "gate.html"); pdf = os.path.join(SP, "gate.pdf")
        io.open(f, "w", encoding="utf-8", newline="\n").write(html[:first] + html[s:e] + html[last:])
        if os.path.exists(pdf): os.remove(pdf)
        subprocess.run([CH, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=3000", "--print-to-pdf=" + pdf, "file:///" + f], capture_output=True)
        d = pdfium.PdfDocument(pdf); res.append(len(d)); d.close()
    b = sum(1 for r in res if r != 1); bad += b
    print("%-4s%-40s %s" % ("OK" if not b else "BAD", doc, " ".join(map(str, res))))
print("\n%d sheet(s) not exactly one page" % bad)
