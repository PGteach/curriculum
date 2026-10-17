# ------------------------------------------------------------------ booklet
def booklet(head, tail):
    """The booklet follows the deck slide by slide, in the same order, so what
    a student revises from is what they were taught from. The slide numbers
    in the comments are the deck's; keep them in step when either changes.
    Only the title, the video and the exam QR have no page of their own."""
    STAGES, MATRIX = slide_svg("STAGES"), slide_svg("MATRIX")
    p = []
    # slides 2-6: recap, the hook, the guiding question, the map, explore
    p.append(page(
        masthead('Student Booklet')
        + '<h2>Before we start &middot; lesson 2-2</h2>'
        '<table><tr><th>Layer</th><th>Measure</th></tr>'
        '<tr><td class="k">1 &middot; Network entry</td><td>Firewall</td></tr>'
        '<tr><td class="k">2 &middot; Communication path</td><td>VPN</td></tr>'
        '<tr><td class="k">3 &middot; Server placement</td><td>DMZ</td></tr>'
        '<tr><td class="k">4 &middot; Endpoints</td><td>Antivirus, an updated OS</td></tr></table>'
        '<p class="ar">حتى مع الدفاع في العمق ممكن يحصل حادث أمني؛ الدرس ده بينقلنا من الوقاية للاستجابة وإدارة المخاطر.</p>'
        '<h2>A rushed reaction makes it worse</h2>'
        '<p>Even a well-protected system can be attacked: data leaked, files tampered with, a service knocked offline. '
        'A rushed, unplanned reaction only makes the damage worse. Organizations follow a clear, ordered response so that '
        'damage is contained, the cause is removed, and the same problem does not return &mdash; and they decide in advance '
        'which risks to guard against first, because no team can fix everything at once.</p>'
        '<div class="summary"><p><b>Today&#8217;s question.</b> When a security incident happens, how should an organization '
        'respond in order &mdash; and how does it decide which risks to address first?</p>'
        '<p class="ar">السؤال الرئيسي: لما يحصل حادث أمني، المؤسسة تنظّم استجابتها إزاي بالترتيب، وتقرر أنهي مخاطر تعالجها الأول؟</p></div>'
        '<div class="summary hw"><p><b>Explore &middot; in pairs.</b> A school computer is infected with malware that is '
        'spreading. Put these in order: restore the files from a backup &middot; unplug it from the network &middot; find out '
        'how it got in &middot; remove the malware.</p>'
        '<p class="ar">رتّبوا الأربع خطوات دول قبل ما تكمّلوا.</p></div>'))
    # slides 7-9: security incidents, (video), not an incident
    p.append(page(
        '<h2>Part 1 &middot; What is a security incident?</h2>'
        + term('Security incident', 'A situation in which actual damage occurs due to an information security problem.',
               'الحادث الأمني: حدث بيأثر على سرية المعلومات أو سلامتها أو توافرها، أو بيهددها بجدية، أو بيخالف سياسة أمنية.')
        + '<table><tr><th>Type</th><th>Description</th></tr>'
        '<tr><td class="k">Information leak</td><td>Personal or confidential information is leaked to the outside</td></tr>'
        '<tr><td class="k">Data tampering</td><td>Data within a system is altered without authorization</td></tr>'
        '<tr><td class="k">Service outage</td><td>A service becomes unavailable due to attacks on the server, etc.</td></tr></table>'
        '<table><tr><th>Is it a security incident?</th><th style="width:30%">Answer</th></tr>'
        '<tr><td>Data was encrypted by a ransomware infection</td><td>Yes</td></tr>'
        '<tr><td>Customer information was leaked through unauthorized access</td><td>Yes &mdash; an information leak</td></tr>'
        '<tr><td>A software update was performed to add new features</td><td><b>No</b> &mdash; nothing was damaged</td></tr>'
        '<tr><td>A web service became unavailable due to an attack on the server</td><td>Yes &mdash; a service outage</td></tr></table>'
        '<h2>Part 2 &middot; Six stages, in order</h2>'
        + dg(STAGES)))
    # slides 10-13: what each stage does, two names, contain first
    p.append(page(
        '<table><tr><th style="width:26%">Stage</th><th>What happens</th></tr>'
        '<tr><td class="k">1 Preparation</td><td>Establish response procedures and structures in advance, in preparation for incidents</td></tr>'
        '<tr><td class="k">2 Detection</td><td>Discover and confirm that an incident has occurred</td></tr>'
        '<tr><td class="k">3 Containment</td><td>Limit the scope of impact so that damage does not spread further</td></tr>'
        '<tr><td class="k">4 Eradication</td><td>Remove the cause of the incident (e.g. remove malware)</td></tr>'
        '<tr><td class="k">5 Recovery</td><td>Return systems and services to their normal state (may restore from a clean backup)</td></tr>'
        '<tr><td class="k">6 Prevention of recurrence</td><td>Analyze the cause and take measures so that the same incident does not occur again</td></tr></table>'
        '<p class="ar">التحضير ← الاكتشاف ← الاحتواء ← إزالة التهديد (الاستئصال) ← الاستعادة ← الدروس المستفادة والتحسين.</p>'
        '<div class="summary"><p><b>Stage 6 has two names.</b> The English book says <b>prevention of recurrence</b>; the Arabic '
        'book and the ministry say <b>lessons learned and improvement</b> &mdash; analyze what happened, document the lessons, '
        'improve the controls. Learn both.</p>'
        '<p class="ar">المرحلة السادسة: \"منع التكرار\" = \"الدروس المستفادة والتحسين\".</p></div>'
        '<h2>Contain first, then remove the cause</h2>'
        + term('Containment &middot; eradication', 'Containment limits the spread of damage; eradication removes the cause. Containment comes first. '
               'If recovery is performed without removing the cause, the same incident may occur again.',
               'الاحتواء: الحد من انتشار الضرر. الاستئصال: إزالة السبب. الاحتواء الأول.')))
    # slides 14-17: pause & think, in practice, which stage, exam-style question
    p.append(page(
        '<div class="summary hw"><p><b>Pause and think.</b> Why must containment come before eradication in the six-stage response?</p>'
        '<p class="ar">ليه الاحتواء لازم ييجي قبل الاستئصال؟</p></div>'
        '<h2>The order is a guide, not a cage</h2>'
        '<p>The six stages give the general sequence, but in a real response some activities can <b>overlap</b> or <b>repeat</b>. '
        'For example, recovery can reveal traces of the threat that are still there &mdash; and the team goes back to containment or eradication.</p>'
        '<p class="ar">الاستجابة الفعلية ممكن يحصل فيها تداخل أو تكرار؛ الاسترداد ممكن يكشف بقايا للتهديد فنرجع للاحتواء أو إزالة التهديد.</p>'
        '<h2>Which stage is it?</h2>'
        '<table><tr><th>Action</th><th style="width:30%">Stage</th></tr>'
        '<tr><td>Establishing response procedures in advance</td><td>Preparation</td></tr>'
        '<tr><td>Discovering and confirming that an incident has occurred</td><td>Detection</td></tr>'
        '<tr><td>Disconnecting a malware-infected computer from the network</td><td>Containment</td></tr>'
        '<tr><td>Removing the malware infection</td><td>Eradication</td></tr>'
        '<tr><td>Restoring a clean system from a backup</td><td>Recovery</td></tr>'
        '<tr><td>Analyzing the cause so it does not occur again</td><td>Prevention of recurrence</td></tr></table>'
        '<div class="summary"><p><b>Why must the six stages go in order?</b> If recovery is done before eradication, the system '
        'is back but the cause is still there, so the same incident can happen again. Eradicate first, and recovery returns a clean system.</p>'
        '<p class="ar">لو رجّعنا النظام قبل ما نشيل السبب، الحادث ممكن يتكرر.</p></div>'))
    # slides 18-22: risk, the matrix, put the risks in order, the exam warning
    p.append(page(
        '<h2>Part 3 &middot; Risk = impact &times; likelihood</h2>'
        + term('Risk', 'The possibility of an information security problem occurring in the future, and its impact.',
               'الخطر: احتمال إن يحصل حدث بيسبب ضرر، مع مراعاة احتمال وقوعه وحجم أثره.')
        + '<table><tr><th>Factor</th><th>Meaning</th></tr>'
        '<tr><td class="k">Impact</td><td>How much damage occurs if the risk actually materializes</td></tr>'
        '<tr><td class="k">Likelihood</td><td>How high the probability is that the risk will actually materialize</td></tr></table>'
        + dg(MATRIX)
        + '<p>Risks with both <b>high impact and high likelihood</b> are addressed first; it is difficult to address every risk at '
        'the same time, so priorities are set. High impact with low likelihood (3 &times; 1 = 3) is usually classed as medium.</p>'
        '<p class="ar">التأثير العالي والاحتمالية العالية أعلى أولوية؛ ومش هنقدر نعالج كل المخاطر في نفس الوقت.</p>'
        '<table><tr><th>Looks right, but is false</th><th>Why</th></tr>'
        '<tr><td>The size of a risk can be determined by impact alone.</td><td>Impact and likelihood, multiplied.</td></tr>'
        '<tr><td>It is enough to address only high-impact, or only high-likelihood, risks.</td><td>Both factors count.</td></tr>'
        '<tr><td>All risks must be addressed simultaneously.</td><td>Set priorities.</td></tr>'
        '<tr><td>Detection &rarr; Eradication &rarr; Containment &rarr; Recovery.</td><td>Containment comes before eradication.</td></tr></table>'))
    # slides 23-27: think as an engineer, new context, key takeaway, unit 2
    p.append(page(
        '<h2>Think as an engineer</h2>'
        '<div class="summary hw"><p>Ransomware hits a school&#8217;s student records: files encrypted, staff locked out, the incident '
        'just detected. <b>Respond from here</b>: list the stages still to do. <b>Assess the risks</b>: another ransomware attack, '
        'or a brief power cut? <b>Decide</b>: the first three actions, and why order matters.</p>'
        '<p class="ar">تلميح: لو رجّعت قبل ما تشيل السبب، البرمجية الخبيثة لسه موجودة.</p></div>'
        '<h2>In a new context</h2>'
        '<div class="summary hw"><p>An online shop has just detected that customer data has been leaked. Name the next two '
        'stages it should carry out and why, and identify one risk it should prioritize afterward.</p>'
        '<p class="ar">حدد المرحلتين الجايين وليه، وخطر واحد ياخد الأولوية بعد كده.</p></div>'
        '<h2>Key takeaway &middot; respond in order, fix the worst first</h2><div class="summary">'
        '<p>Follow the six stages in order (prepare &rarr; detect &rarr; contain &rarr; eradicate &rarr; recover &rarr; prevent), '
        'and prioritize risks by impact &times; likelihood.</p>'
        '<p class="ar">اتبع المراحل الست بالترتيب مع إمكانية الرجوع لمرحلة سابقة، وحدد أولويات المخاطر بالتأثير × الاحتمالية.</p></div>'
        '<h2>Unit 2 &middot; complete</h2>'
        '<table><tr><th>Lesson</th><th>What to know</th></tr>'
        '<tr><td class="k">2-1</td><td>HTTPS, common-key and public-key, certificates, signatures, multi-factor login</td></tr>'
        '<tr><td class="k">2-2</td><td>Firewall, VPN, DMZ, defense in depth, zero trust</td></tr>'
        '<tr><td class="k">2-3</td><td>Security incidents, the six stages, risk = impact &times; likelihood</td></tr></table>'))
    p.append(page('<h2>Class work</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
                  + exercise(1, 1) + exercise(2, 2)))
    p.append(page('<h2>Class work</h2><p class="ar">كمّل مع زميلك.</p>'
                  + exercise(3, 3) + exercise(4, 4)))
    return head + ''.join(p) + lastpage('booklet') + tail
