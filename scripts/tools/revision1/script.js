/* ---- flashcards (revision lectures 12 and 13) --------------------------------
   .fcards: the term on the front; Flip (or tap the card) shows the definition,
   in English and Arabic. "I knew it" takes the card out of the pile; "Not
   yet" sends it to the back, so it comes round again. Space and Enter on the
   card or a button stay here, so they do not also turn the slide. */
(function(){
  if(!document.querySelectorAll) return;
  document.querySelectorAll('.fcards').forEach(function(box){
    var all = JSON.parse(box.getAttribute('data-cards'));
    var card = box.querySelector('.fcard'), front = box.querySelector('.ff');
    var en = box.querySelector('.fb .en'), ar = box.querySelector('.fb .ar'), prog = box.querySelector('.fprog');
    var fl = box.querySelector('.fl'), kn = box.querySelector('.kn'), ny = box.querySelector('.ny'), rs = box.querySelector('.rs');
    var pile = [], known = 0;

    function show(){
      card.classList.remove('flipped');
      if(!pile.length){
        front.textContent = 'All ' + all.length + ' known!';
        en.textContent = ''; ar.textContent = '';
        prog.textContent = 'Well done — press Start again to go through them once more.';
        fl.disabled = kn.disabled = ny.disabled = true;
        card.classList.add('done');
        return;
      }
      card.classList.remove('done');
      var c = all[pile[0]];
      front.textContent = c[0];
      en.textContent = c[1]; ar.textContent = c[2] || '';
      prog.textContent = 'Known ' + known + ' of ' + all.length + ' · ' + pile.length + ' left · say the meaning, then flip';
      fl.disabled = kn.disabled = ny.disabled = false;
    }
    function flip(){ if(pile.length) card.classList.toggle('flipped'); }
    function start(){
      pile = all.map(function(_, k){ return k; });
      known = 0;
      show();
    }
    fl.addEventListener('click', flip);
    card.addEventListener('click', flip);
    kn.addEventListener('click', function(){ if(!pile.length) return; pile.shift(); known++; show(); });
    ny.addEventListener('click', function(){ if(!pile.length) return; pile.push(pile.shift()); show(); });
    rs.addEventListener('click', start);
    box.addEventListener('keydown', function(e){
      if(e.key !== ' ' && e.key !== 'Enter') return;
      var t = e.target;
      if(t === card){ e.preventDefault(); e.stopPropagation(); flip(); }
      else if(t.tagName === 'BUTTON') e.stopPropagation();
    });
    start();
  });
})();
