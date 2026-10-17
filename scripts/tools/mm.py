import io,sys,subprocess,re
doc=sys.argv[1]; SP=sys.argv[2]
s=io.open(doc,encoding="utf-8").read()
probe='''<script>addEventListener("load",function(){setTimeout(function(){var px=96/25.4,o=[];document.querySelectorAll("section.sheet").forEach(function(sh,i){var f=sh.querySelector(".foot"),top=sh.getBoundingClientRect().top,last=0;Array.prototype.forEach.call(sh.children,function(c){if(c!==f){var r=c.getBoundingClientRect();if(r.bottom>last)last=r.bottom;}});o.push((i+1)+":"+Math.round((last-top)/px));});document.title="R:"+o.join(" ");},800);});</script>'''
f=SP+"/mm.html"; io.open(f,"w",encoding="utf-8").write(s.replace("</body>",probe+"</body>",1))
d=subprocess.run([r"C:\Program Files\Google\Chrome\Application\chrome.exe","--headless=new","--disable-gpu","--virtual-time-budget=4000","--dump-dom","file:///"+f],capture_output=True).stdout.decode("utf-8","replace")
print(re.search(r"<title>R:([^<]*)",d).group(1))
