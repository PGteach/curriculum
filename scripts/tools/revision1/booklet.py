# ------------------------------------------------------------------ booklet
def booklet(head, tail):
    """A revision booklet: three pages a lesson, in the deck's order -- the
    book's key takeaway, the lesson's picture and the exam traps; every key
    term with its meaning; the exam question, room to plan it, and its
    marking points. All of it is read from the same
    tools/lectureN/data.py the deck uses, so the two cannot drift. Then the
    class work."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "revdata", str(ROOT / "scripts" / "tools" / T.parent.name.replace("chapter", "revision") / "data.py"))
    # T is revision/chapterK/_teacher; the sources are scripts/tools/revisionK
    D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)

    p = []
    p.append(page(
        masthead('Revision Booklet')
        + '<h2>How to use this booklet</h2>'
        '<p>Three pages for each lesson. Decide each trap true or false before you read the answer; cover the meaning '
        'of each key term and say it before you look; and plan the exam question before you read its points.</p>'
        '<p class="ar">تلات صفحات لكل درس. غطّي عمود المعاني وقول التعريف قبل ما تبص، وقرّر صح ولا غلط قبل ما تقرا الإجابة، '
        'وخطّط سؤال الامتحان قبل ما تقرا النقط.</p>'
        '<h2>The unit at a glance</h2>'
        '<table><tr><th style="width:12%">Lesson</th><th>Remember</th></tr>'
        + ''.join('<tr><td class="k">%s</td><td><b>%s.</b> %s</td></tr>' % (L["id"], L["title"], L["remember"]) for L in D.LESSONS)
        + '</table>'))
    for L in D.LESSONS:
        # 1 · the big idea: the takeaway, the picture, the exam traps
        p.append(page(
            '<h2>%s &middot; %s</h2>' % (L["id"], L["title"])
            + '<div class="summary"><p><b>Remember.</b> %s</p><p class="ar">%s</p></div>' % (L["remember"], L["remember_ar"])
            + dg(slide_svg(L["svg"]))
            + '<h2>Exam traps</h2>'
            + '<table><tr><th>Statement</th><th style="width:12%">T / F</th><th style="width:34%">Why</th></tr>'
            + ''.join('<tr><td>%s</td><td><b>%s</b></td><td>%s</td></tr>' % (st, "True" if ok else "False", why)
                      for st, ok, why in L["traps"])
            + '</table>'))
        # 2 · every key term, with its meaning in English and Arabic
        p.append(page(
            '<h2>%s &middot; Key terms</h2>' % L["id"]
            + '<p>Cover the right-hand column and say each meaning before you look.</p>'
            + '<table><tr><th style="width:27%">Key term</th><th>Meaning</th></tr>'
            + ''.join('<tr><td class="k">%s</td><td>%s<div class="ar tdar">%s</div></td></tr>' % (t, d, a)
                      for t, d, a in L["terms"])
            + '</table>'))
        # 3 · the lesson's exam question, a place to plan, then the points
        ex = L["exam"]
        p.append(page(
            '<h2>%s &middot; Exam-style question &middot; %d marks</h2>' % (L["id"], ex["marks"])
            + '<p><b>%s</b></p><p class="src">%s</p>' % (ex["q"], ex["src"])
            + '<div class="summary hw"><p><b>Plan first.</b> Write your points here, then check them against the '
              'marking points below. Each point is about one mark.</p></div>'
            + rules(7)
            + '<h2>The marking points</h2>'
            + '<ol class="qs">' + ''.join('<li>%s</li>' % x for x in D.POINTS[L["id"]]) + '</ol>'))
    p.append(page('<h2>Class work</h2><p class="ar">شغل الحصة — نحل دول سوا.</p>'
                  + exercise(1, 1) + exercise(2, 2)))
    p.append(page('<h2>Class work</h2><p class="ar">كمّل مع زميلك.</p>'
                  + exercise(3, 3) + exercise(4, 4)))
    return head + ''.join(p) + lastpage('booklet') + tail