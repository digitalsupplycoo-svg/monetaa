/* Moneta — shared behaviour. No dependencies. */
(function () {
  'use strict';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- scroll reveal ---------------------------------------------------- */
  var revealEls = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -40px 0px', threshold: 0 });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---- magnetic hover --------------------------------------------------- */
  var magnets = document.querySelectorAll('[data-magnet]');
  if (!reduced && matchMedia('(hover:hover)').matches) {
    magnets.forEach(function (el) {
      var pad = parseInt(el.dataset.magnetPad || '150', 10);
      var strength = parseFloat(el.dataset.magnetStrength || '3');
      var active = false;
      window.addEventListener('mousemove', function (ev) {
        var r = el.getBoundingClientRect();
        var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
        var dx = ev.clientX - cx, dy = ev.clientY - cy;
        var inside = Math.abs(dx) < r.width / 2 + pad && Math.abs(dy) < r.height / 2 + pad;
        if (inside) {
          if (!active) { el.style.transition = 'transform .3s ease-out'; active = true; }
          el.style.transform = 'translate3d(' + dx / strength + 'px,' + dy / strength + 'px,0)';
        } else if (active) {
          el.style.transition = 'transform .6s ease-in-out';
          el.style.transform = 'translate3d(0,0,0)';
          active = false;
        }
      }, { passive: true });
    });
  }

  /* ---- scroll-driven marquee ------------------------------------------- */
  var marquee = document.querySelector('[data-marquee]');
  var rows = marquee ? marquee.querySelectorAll('.marquee-row') : [];
  function moveMarquee() {
    if (!marquee) return;
    var top = marquee.getBoundingClientRect().top + window.scrollY;
    var offset = (window.scrollY - top + window.innerHeight) * 0.3;
    var x = offset - 200;
    if (rows[0]) rows[0].style.transform = 'translateX(' + x + 'px)';
    if (rows[1]) rows[1].style.transform = 'translateX(' + (-x) + 'px)';
  }

  /* ---- sticky card stacking -------------------------------------------- */
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-stack] .card'));
  function scaleCards() {
    var total = cards.length;
    cards.forEach(function (card, i) {
      if (i === total - 1) return;
      var item = card.parentElement;
      var r = item.getBoundingClientRect();
      var stickTop = parseFloat(getComputedStyle(item).top) || 0;
      var travel = r.height;
      var p = Math.min(1, Math.max(0, (stickTop - r.top) / travel));
      var target = 1 - (total - 1 - i) * 0.03;
      card.style.transform = 'scale(' + (1 - (1 - target) * p).toFixed(4) + ')';
    });
  }

  /* ---- character reveal paragraph -------------------------------------- */
  var charPara = document.querySelector('[data-chars]');
  var chars = [];
  if (charPara) {
    var text = charPara.textContent;
    charPara.textContent = '';
    for (var i = 0; i < text.length; i++) {
      var s = document.createElement('span');
      s.textContent = text[i];
      if (reduced) s.className = 'on';
      charPara.appendChild(s);
      chars.push(s);
    }
  }
  function revealChars() {
    if (!charPara || reduced) return;
    var r = charPara.getBoundingClientRect();
    var vh = window.innerHeight;
    var p = (vh * 0.8 - r.top) / (vh * 0.6 + r.height);
    p = Math.min(1, Math.max(0, p));
    var n = Math.round(p * chars.length);
    for (var i = 0; i < chars.length; i++) chars[i].classList.toggle('on', i < n);
  }

  /* ---- rAF scroll loop -------------------------------------------------- */
  var queued = false;
  function onScroll() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () {
      queued = false;
      if (!reduced) moveMarquee();
      scaleCards();
      revealChars();
    });
  }
  if (marquee || cards.length || charPara) {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    onScroll();
    window.addEventListener('load', onScroll);
  }

  /* ---- footer year ------------------------------------------------------ */
  var y = document.querySelectorAll('[data-year]');
  y.forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
