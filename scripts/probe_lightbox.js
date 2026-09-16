/* Photo-lightbox behaviour check, run in a real browser.
 *
 * check_lecture.py verifies the guards are present in the source; this
 * verifies they work. The difference matters here, because the thing worth
 * proving -- that the arrow keys move the photo and NOT the slide behind it
 * -- depends on two real window listeners running in order against a real
 * classList, which a stubbed DOM cannot reproduce.
 *
 * Not in CI: it needs a browser, and the GitHub runner has no reason to
 * carry one for this. Run it by hand after touching the deck's navigation
 * or the lightbox:
 *
 *   1. copy lectureN/slides/ somewhere writable, with its media/ folder
 *   2. paste this file into index.html inside a <script> before </body>
 *   3. open it in Chrome and read document.title, or headless:
 *
 *      chrome --headless=new --virtual-time-budget=6000  *             --window-size=1280,720 --dump-dom file:///.../index.html  *        | grep -o "<title>R:[^<]*"
 *
 * Every line must read PASS. 21 of them.
 */
window.addEventListener('load', function () {
  var out = [], slideAtOpen;

  function ok(name, cond, detail) {
    out.push((cond ? 'PASS  ' : 'FAIL  ') + name + (detail ? '  [' + detail + ']' : ''));
  }
  function key(k) {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
  }
  function slideNow() {
    return document.getElementById('counter').textContent.trim();
  }

  setTimeout(function () {
    /* go to the first slide that has a photo grid */
    var grid = document.querySelector('.shots');
    var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
    go(slides.indexOf(grid.closest('.slide')));

    var shots = grid.querySelectorAll('figure.shot');
    var zoom = document.getElementById('zoom');
    var zimg = document.getElementById('zimg');

    ok('starts closed', !zoom.classList.contains('on'));
    ok('photos are focusable', shots[0].querySelector('img').tabIndex === 0);

    /* --- click the SECOND photo ------------------------------------- */
    slideAtOpen = slideNow();
    shots[1].querySelector('img').click();
    ok('click opens it', zoom.classList.contains('on'));
    ok('opens the photo that was clicked',
       zimg.src.indexOf(shots[1].querySelector('img').getAttribute('src').split('/').pop()) > -1,
       zimg.src.split('/').pop());
    ok('overlay is actually visible',
       getComputedStyle(zoom).display === 'flex', getComputedStyle(zoom).display);
    ok('caption came across',
       document.getElementById('zcap').textContent.length > 10);
    ok('counter reads 2 / ' + shots.length,
       document.getElementById('znum').textContent === '2 / ' + shots.length,
       document.getElementById('znum').textContent);

    /* the overlay must not be scaled by the slide's auto-fit transform */
    var r = zoom.getBoundingClientRect();
    ok('overlay fills the viewport (not inside the fitbox transform)',
       Math.abs(r.width - window.innerWidth) < 2 && Math.abs(r.height - window.innerHeight) < 2,
       Math.round(r.width) + 'x' + Math.round(r.height) +
       ' vs ' + window.innerWidth + 'x' + window.innerHeight);
    ok('rendered bigger than the thumbnail',
       zimg.getBoundingClientRect().height >
       shots[1].querySelector('img').getBoundingClientRect().height * 1.5,
       Math.round(zimg.getBoundingClientRect().height) + 'px vs ' +
       Math.round(shots[1].querySelector('img').getBoundingClientRect().height) + 'px');

    /* --- THE POINT: arrows move the photo, not the slide ------------- */
    key('ArrowRight');
    ok('right arrow advances the photo',
       document.getElementById('znum').textContent === '3 / ' + shots.length,
       document.getElementById('znum').textContent);
    ok('right arrow did NOT change the slide', slideNow() === slideAtOpen,
       slideNow() + ' vs ' + slideAtOpen);

    key('ArrowLeft'); key('ArrowLeft');
    ok('left arrow goes back', document.getElementById('znum').textContent === '1 / ' + shots.length,
       document.getElementById('znum').textContent);
    ok('still on the same slide', slideNow() === slideAtOpen);

    key('ArrowLeft');
    ok('wraps round to the last photo',
       document.getElementById('znum').textContent === shots.length + ' / ' + shots.length,
       document.getElementById('znum').textContent);

    /* --- closing ---------------------------------------------------- */
    key('Escape');
    ok('escape closes it', !zoom.classList.contains('on'));
    ok('escape did not change the slide', slideNow() === slideAtOpen);
    ok('src released on close', !zimg.getAttribute('src'));

    /* arrows work on the deck again once it is shut */
    key('ArrowRight');
    ok('arrows drive the deck again after closing', slideNow() !== slideAtOpen,
       slideNow() + ' vs ' + slideAtOpen);

    /* --- backdrop click --------------------------------------------- */
    go(slides.indexOf(grid.closest('.slide')));
    shots[0].querySelector('img').click();
    zoom.click();
    ok('clicking the backdrop closes it', !zoom.classList.contains('on'));

    shots[0].querySelector('img').click();
    document.getElementById('zimg').click();
    ok('clicking the photo itself does NOT close it', zoom.classList.contains('on'));

    /* --- the QR image must not be wired up -------------------------- */
    var qr = document.getElementById('qr');
    ok('the QR code is not a lightbox trigger', !qr || qr.tabIndex !== 0,
       qr ? 'tabIndex=' + qr.tabIndex : 'no qr on this deck');

    document.title = 'R:' + out.join(' | ');
  }, 900);
});
