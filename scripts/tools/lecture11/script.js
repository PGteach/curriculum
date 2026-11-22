/* ---- the live demos (lecture 11) -------------------------------------------
   .layers: the same small page as HTML only, then with CSS, then with
   JavaScript (only then does its button count). .resp: one layout at phone,
   tablet and PC width. .live: an editor whose preview is a sandboxed frame
   (sandbox="" -- nothing typed there can run a script), redrawn as you type.
   Keys and swipes inside a demo stay there, so typing a space or an arrow
   does not also turn the slide. */
(function(){
  if(!document.querySelectorAll) return;
  function keep(el){
    ['keydown', 'touchstart', 'touchend'].forEach(function(ev){
      el.addEventListener(ev, function(e){
        var t = e.target && e.target.tagName;
        if(ev !== 'keydown' || t === 'TEXTAREA' || (t === 'BUTTON' && (e.key === ' ' || e.key === 'Enter'))) e.stopPropagation();
      }, {passive: true});
    });
  }
  function note(box, en, ar){
    var n = box.querySelector('.lnote');
    if(!n) return;
    n.querySelector('.en').textContent = en;
    n.querySelector('.ar').textContent = ar;
  }

  var STAGES = {
    html: ['HTML only: the content and its structure — a heading, a paragraph, a button. No colours, and the button does nothing.',
           'HTML بس: المحتوى وبنيته — عنوان وفقرة وزرار. مفيش ألوان، والزرار مش بيعمل حاجة.'],
    css:  ['+ CSS: the same content, now with colours, spacing and a styled button. The button still does nothing.',
           '+ CSS: نفس المحتوى، بس بقى فيه ألوان ومسافات وزرار متنسّق. والزرار لسه مش بيعمل حاجة.'],
    js:   ['+ JavaScript: now the button responds. Press it, and the number goes up.',
           '+ JavaScript: دلوقتي الزرار بيستجيب. دوس عليه والرقم هيزيد.']
  };
  document.querySelectorAll('.layers').forEach(function(box){
    var count = 0, btn = box.querySelector('.dp-btn'), out = box.querySelector('.dp-count');
    function set(s){
      box.setAttribute('data-stage', s);
      /* without JavaScript the button does nothing, so the count starts over */
      if(s !== 'js'){ count = 0; out.textContent = '0 signed up'; }
      box.querySelectorAll('.lbtns button').forEach(function(b){ b.classList.toggle('on', b.getAttribute('data-s') === s); });
      note(box, STAGES[s][0], STAGES[s][1]);
    }
    box.querySelectorAll('.lbtns button').forEach(function(b){
      b.addEventListener('click', function(){ set(b.getAttribute('data-s')); });
    });
    btn.addEventListener('click', function(){
      if(box.getAttribute('data-stage') !== 'js') return;
      count++;
      out.textContent = count + ' signed up';
    });
    keep(box);
    set('html');
  });

  var WIDTHS = {
    phone:  ['Phone: the three boxes stack in one column, so nothing is too small to read.',
             'موبايل: الصناديق التلاتة بتترص تحت بعض في عمود واحد، فمفيش حاجة صغيرة أوي.'],
    tablet: ['Tablet: two boxes side by side, the third below.',
             'تابلت: صندوقين جنب بعض، والتالت تحتهم.'],
    pc:     ['PC: there is room for all three boxes in one row.',
             'كمبيوتر: فيه مكان للتلات صناديق في صف واحد.']
  };
  document.querySelectorAll('.resp').forEach(function(box){
    function set(w){
      box.setAttribute('data-w', w);
      box.querySelectorAll('.lbtns button').forEach(function(b){ b.classList.toggle('on', b.getAttribute('data-w') === w); });
      note(box, WIDTHS[w][0], WIDTHS[w][1]);
    }
    box.querySelectorAll('.lbtns button').forEach(function(b){
      b.addEventListener('click', function(){ set(b.getAttribute('data-w')); });
    });
    keep(box);
    set('pc');
  });

  var BASE = '<style>body{font:16px/1.5 Inter,Arial,sans-serif;margin:12px;color:#16233F}</style>';
  document.querySelectorAll('.live').forEach(function(box){
    var ta = box.querySelector('textarea'), fr = box.querySelector('iframe'), timer = null;
    function draw(){ fr.srcdoc = BASE + ta.value; }
    ta.addEventListener('input', function(){
      if(timer) clearTimeout(timer);
      timer = setTimeout(draw, 250);
    });
    box.querySelector('.lreset').addEventListener('click', function(){ ta.value = ta.defaultValue; draw(); });
    keep(box);
    draw();
  });
})();
