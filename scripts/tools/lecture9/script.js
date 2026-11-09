/* ---- the step-by-step players (lecture 9) ---------------------------------
   .stepper[data-kind=flow]: lights one tier per step and shows what is
   passed on. .stepper[data-kind=code]: lights a code line, fills the value
   boxes and prints to the console. Next step, Play all, Again. Space and
   Enter on the buttons must not also turn the slide, so they stop here. */
(function(){
  if(!document.querySelectorAll) return;
  document.querySelectorAll('.stepper').forEach(function(box){
    var steps = JSON.parse(box.getAttribute('data-steps'));
    var kind = box.getAttribute('data-kind');
    var en = box.querySelector('.tstat .en'), ar = box.querySelector('.tstat .ar');
    var nx = box.querySelector('.nx'), pl = box.querySelector('.pl'), rs = box.querySelector('.rs');
    var lines = box.querySelectorAll('.ln'), cons = box.querySelector('.tcons');
    var tiers = box.querySelectorAll('.tier'), packet = box.querySelector('.packet');
    var i = 0, timer = null;

    function stop(){ if(timer){ clearInterval(timer); timer = null; } }
    function say(e, a){ en.textContent = e || ''; ar.textContent = a || ''; }
    function reset(){
      stop(); i = 0;
      for(var j = 0; j < lines.length; j++) lines[j].classList.remove('hot');
      for(var t = 0; t < tiers.length; t++) tiers[t].classList.remove('on');
      if(packet) packet.textContent = '';
      if(cons) cons.querySelectorAll('.line').forEach(function(l){ l.remove(); });
      box.querySelectorAll('.box b').forEach(function(b){ b.textContent = '?'; b.classList.remove('pop'); });
      nx.disabled = false; pl.disabled = false;
      say('Press Next step to start.', 'اضغط Next step عشان تبدأ.');
    }
    function next(){
      if(i >= steps.length) return;
      var s = steps[i++];
      if(kind === 'flow'){
        for(var t = 0; t < tiers.length; t++) tiers[t].classList.toggle('on', tiers[t].getAttribute('data-t') === s.t);
        packet.textContent = '';
        if(s.msg){ var p = document.createElement('span'); p.textContent = s.msg; packet.appendChild(p); }
      } else {
        for(var j = 0; j < lines.length; j++) lines[j].classList.toggle('hot', j === s.ln);
        if(s.set) Object.keys(s.set).forEach(function(k){
          var b = box.querySelector('.box[data-k="' + k + '"] b');
          if(!b) return;
          b.textContent = s.set[k];
          b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop');
        });
        if(s.out !== undefined){
          var l = document.createElement('span'); l.className = 'line'; l.textContent = s.out; cons.appendChild(l);
        }
      }
      say(s.en, s.ar);
      if(i >= steps.length){ stop(); nx.disabled = true; pl.disabled = true; }
    }
    nx.addEventListener('click', function(){ stop(); next(); });
    pl.addEventListener('click', function(){
      if(timer) return;
      if(i >= steps.length) reset();
      pl.disabled = true; next(); timer = setInterval(next, 1500);
    });
    rs.addEventListener('click', reset);
    box.addEventListener('keydown', function(e){
      if(e.target.tagName === 'BUTTON' && (e.key === ' ' || e.key === 'Enter')) e.stopPropagation();
    });
    reset();
  });
})();
