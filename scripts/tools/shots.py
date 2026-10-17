import sys, subprocess, os
from PIL import Image
N, SP = int(sys.argv[1]), sys.argv[2]
d = os.path.join(SP, "l%d" % N); os.makedirs(d, exist_ok=True)
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
import re, io
n = io.open("lecture%d/slides/index.html" % N, encoding="utf-8").read().count('<section class="slide')
for k in range(1, n + 1):
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=5000",
                    "--window-size=1600,900", "--screenshot=" + os.path.join(d, "s%d.png" % k),
                    "file:///C:/web-files/lecture%d/slides/index.html#%d" % (N, k)], capture_output=True)
for part in range(0, n, 6):
    W = Image.new("RGB", (1600, 1350), "white")
    for i in range(6):
        k = part + i + 1
        if k > n: break
        W.paste(Image.open(os.path.join(d, "s%d.png" % k)).resize((800, 450)), ((i % 2) * 800, (i // 2) * 450))
    W.save(os.path.join(d, "sheet%d.png" % (part // 6)))
print(n, "slides")
