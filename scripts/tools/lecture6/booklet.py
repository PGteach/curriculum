# ------------------------------------------------------------------ booklet
def booklet(head, tail):
    """The booklet follows the deck slide by slide, in the same order, so what
    a student revises from is what they were taught from. The slide numbers
    in the comments are the deck's; keep them in step when either changes.
    Only the title and the exam QR have no page of their own."""
    DMZ, LAYERS, TRUST = slide_svg("DMZ"), slide_svg("LAYERS"), slide_svg("TRUST")
    p = []
    # slides 2-6: recap, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Before we start &middot; lesson 2-1</h2>'
        '<table><tr><th>Technology</th><th>What it protects</th></tr>'
        '<tr><td class="k">Encryption</td><td>The content, from being read</td></tr>'
        '<tr><td class="k">Digital certificate</td><td>That the other side is genuine</td></tr>'
        '<tr><td class="k">Digital signature</td><td>The data, from being altered</td></tr>'
        '<tr><td class="k">Multi-factor authentication</td><td>The account, from unauthorized login</td></tr></table>'
        '<p class="ar">في الدرس 2-1 اتعلمت إزاي تقنيات التشفير والمصادقة بتحمي الاتصال والحسابات. النهارده هنوسّع الحماية لتصميم الشبكة نفسها.</p>'
        '<h2>One lock on the front door is not enough</h2>'
        '<p>An organization&#8217;s network holds confidential data &mdash; customer records, financial files and '
        'private messages &mdash; and attackers constantly look for a way in. If a single lock is picked, '
        'everything inside is exposed. So modern network security uses several layers: even when one defense '
        'is breached, the next one still protects the system.</p>'
        '<p class="ar">وسيلة حماية واحدة مش كفاية؛ لو فشلت، موارد تانية ممكن تبقى في خطر. عشان كده بنستخدم الدفاع في العمق.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> How can an organization design its network so that, '
        'even if one defense is breached, the system stays protected?</p>'
        '<p class="ar">السؤال الرئيسي: إزاي مؤسسة تقدر تصمم شبكتها بحيث، حتى لو دفاع واحد اتخرق، النظام يفضل محمي؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> A company has a public website, staff who work '
        'from home, and a customer database. Predict where an attacker would try to get in &mdash; and if you could '
        'build only one wall, where you would put it.</p>'
        '<p class="ar">توقّعوا: المهاجم هيحاول يدخل منين؟ ولو هتبني حيطة واحدة بس، هتحطها فين؟</p></div>'))
    # slides 7-9: the firewall, the VPN, not a use of a VPN
    p.append(page(
        '<h2>Part 1 &middot; The firewall</h2>'
        + term('Firewall', 'A system installed at the entry/exit point of a network that allows or denies communication based on '
               'rules set in advance. <i>e.g.</i> Allow access to the web server, but deny direct external access to the database server.',
               'جدار الحماية: بيراقب حركة الشبكة وبيسمح بيها أو يمنعها حسب قواعد. ممكن يكون عند حدود الشبكة، أو بين أجزائها، أو على جهاز مضيف.')
        + '<h2>Part 2 &middot; VPN (Virtual Private Network)</h2>'
        + term('VPN', 'A technology that creates an encrypted virtual private line (a tunnel) over the Internet, allowing safe '
               'connection to a network from a remote location. Because the content is encrypted, the risk of eavesdropping is reduced '
               'even on public Wi-Fi.',
               'الـ VPN: اتصال منطقي خاص عبر شبكة عامة، بيستخدم التشفير وتقنيات النفق.')
        + '<table><tr><th>Main use</th><th>What it means</th></tr>'
        '<tr><td class="k">Remote work</td><td>Connecting safely to the organization&#8217;s network from home or while away</td></tr>'
        '<tr><td class="k">Connecting branches</td><td>Connecting offices in different locations safely</td></tr>'
        '<tr><td class="k">NOT a use</td><td>Automatically deleting files infected with viruses &mdash; that is antivirus software</td></tr></table>'))
    # slides 10-11: the DMZ, pause & think
    p.append(page(
        '<h2>Part 3 &middot; DMZ (Demilitarized Zone)</h2>'
        + term('DMZ', 'An area where servers exposed to the external network (web servers, mail servers, etc.) are placed separately '
               'from the internal network. If a public-facing server is attacked, damage to the internal network can be prevented.',
               'المنطقة المعزولة: الخوادم العامة منفصلة عن الشبكة الداخلية، فلو واحد اتخرق، الهجوم ميوصلش للداخل.')
        + dg(DMZ)
        + '<div class="summary hw"><p><b>Pause and think.</b> Why is it safer to place a public web server in a DMZ rather '
        'than inside the internal network?</p>'
        '<p class="ar">ليه حط خادم ويب عام في المنطقة المعزولة أأمن من حطه جوه الشبكة الداخلية؟</p></div>'))
    # slides 12-14: defense in depth, which layer, the exam-style question
    p.append(page(
        '<h2>Part 4 &middot; Defense in depth</h2>'
        + term('Defense in depth', 'Layering multiple security measures so that, even if one is breached, the next can still protect the system.',
               'الدفاع في العمق: طبقات كتير من الضوابط الأمنية، لو طبقة فشلت، الباقي يقلل الخطر ويحد من أثر الاختراق.')
        + dg(LAYERS)
        + '<table><tr><th>Security measure</th><th style="width:32%">Layer</th></tr>'
        '<tr><td>Blocking unauthorized communication with a firewall</td><td>1 &middot; Network entry</td></tr>'
        '<tr><td>Encrypting communication with a VPN</td><td>2 &middot; Communication path</td></tr>'
        '<tr><td>Separating public-facing servers using a DMZ</td><td>3 &middot; Server placement</td></tr>'
        '<tr><td>Installing antivirus software; keeping the OS updated</td><td>4 &middot; Endpoints</td></tr></table>'
        '<div class="summary"><p><b>Why is layering better than a firewall alone?</b> A firewall alone is one barrier: if it '
        'is breached, everything inside is exposed. With several layers, if one is breached, the next still protects the '
        'system &mdash; so one breach is far less likely to expose the whole network.</p>'
        '<p class="ar">حاجز واحد لو اتخرق كل حاجة بتتكشف؛ الطبقات: لو واحدة وقعت، اللي بعدها لسه بتحمي.</p></div>'))
    # slides 15-19: the perimeter, zero trust, true or false, which term, exam warning
    p.append(page(
        '<h2>Part 5 &middot; The perimeter has blurred</h2>'
        + term('Perimeter', 'The old boundary built on the idea that &#8220;inside the organization&#8217;s network is safe, and outside '
               'is dangerous&#8221;. With cloud services and remote work, the line between inside and outside has blurred, and designs '
               'that protect only the perimeter are no longer enough.',
               'المحيط الأمني: الحدود التقليدية اللي بتفترض إن الداخل آمن، واللي طمستها الخدمات السحابية والشغل عن بُعد.')
        + term('Zero trust', 'The system does not trust any communication, including from within the organization&#8217;s network, and '
               'always verifies it. <i>e.g.</i> Even for access from inside, identity verification and access-permission checks are '
               'performed every time.',
               'نهج انعدام الثقة: مفيش ثقة تلقائية لمجرد إنك جوه الشبكة؛ الهوية والصلاحيات والسياق بيتفحصوا عند كل وصول.')
        + dg(TRUST)
        + '<table><tr><th>Looks right, but is false</th><th>Why</th></tr>'
        '<tr><td>Access from inside the network is safe, so verification is unnecessary.</td><td>Zero trust verifies inside access too.</td></tr>'
        '<tr><td>A firewall alone is sufficient.</td><td>If it is breached, nothing else stands.</td></tr>'
        '<tr><td>A DMZ exposes all servers to the outside, or improves speed.</td><td>It keeps public servers apart, to protect the inside.</td></tr></table>'))
    # slides 20-22: think as an engineer, new context, key takeaway
    p.append(page(
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>A company has a public website, staff who work from home, and confidential customer data. '
        '<b>Collect data</b>: its three assets and the main threat to each. <b>Rank the layers</b> for this company and justify '
        'your top choice. <b>Decide</b>: recommend a design with two reasons why layering is safer than a single firewall.</p>'
        '<p class="ar">تلميح: حط الخادم العام في المنطقة المعزولة، ومتعتمدش على العزل لوحده.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>A hospital moves its patient records to a cloud service and lets doctors access them from home. '
        'Using zero trust and defense in depth, suggest two measures and say where each one helps, then identify one risk that could still remain.</p>'
        '<p class="ar">اقترح إجراءين وبيّن كل واحد بيساعد فين، وحدد خطر واحد ممكن يفضل موجود.</p></div>'
        '<h2>Key takeaway &middot; layer your defenses</h2><div class="summary">'
        '<p>Layer your defenses &mdash; firewall, VPN, DMZ, endpoints &mdash; and verify every access (zero trust). One breach is '
        'then far less likely to expose the whole network.</p>'
        '<p class="ar">كدّس دفاعاتك، واتأكد من كل عملية وصول — ساعتها خرق واحد مش هيكشف الشبكة كلها.</p></div>'
        '<h2>Lesson question &mdash; answered</h2>'
        '<p>Layering: a firewall controls what enters and leaves, a VPN encrypts remote communication, a DMZ keeps public '
        'servers apart, and endpoint measures protect each device &mdash; and zero trust verifies every request.</p>'))
    p.append(page('<h2>Class work</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
                  + exercise(1, 1) + exercise(2, 2)))
    # exercise 4's options run long: with an Arabic line under the heading
    # this page is a few millimetres past one sheet, so the heading carries it
    p.append(page('<h2>Class work &middot; كمّل مع زميلك</h2>'
                  + exercise(3, 3) + exercise(4, 4)))
    return head + ''.join(p) + lastpage('booklet') + tail
