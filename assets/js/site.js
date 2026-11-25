/* Ruben Svanerud: small, dependency-free behaviour */
(function () {
  'use strict';
  var doc = document;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* nav: transparent over the hero, solid after 80px */
  var nav = doc.querySelector('.nav');
  var hasHero = doc.body.classList.contains('has-hero');
  function navState() { if (nav && hasHero) nav.classList.toggle('is-solid', window.scrollY > 80); }
  navState();
  window.addEventListener('scroll', navState, { passive: true });

  /* full-screen menu */
  var toggle = doc.querySelector('.nav__toggle');
  var menu = doc.getElementById('menu');
  if (toggle && menu) {
    var setMenu = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.textContent = open ? 'Close' : 'Menu';
      menu.classList.toggle('is-open', open);
      menu.toggleAttribute('inert', !open);
      doc.body.classList.toggle('menu-open', open);
      if (!open) navState();
      if (open) { var first = menu.querySelector('a'); if (first) first.focus(); }
    };
    toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setMenu(false); toggle.focus(); }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1024 && toggle.getAttribute('aria-expanded') === 'true') setMenu(false);
    });
  }

  /* hero: place the frame symbol around the focal point of the photo (the cable cars) */
  var card = doc.querySelector('.hero__card[data-focus]');
  if (card) {
    var frame = card.querySelector('.hero__frame');
    var img = card.querySelector('.hero__media img');
    var placeFrame = function () {
      if (!img || !img.naturalWidth) return;
      var f = (card.getAttribute('data-focus') || '0.5,0.5').split(',').map(Number);
      var W = card.clientWidth, H = card.clientHeight;
      var iw = img.naturalWidth, ih = img.naturalHeight;
      var s = Math.max(W / iw, H / ih);
      var x = (W - iw * s) / 2 + f[0] * iw * s;
      var y = (H - ih * s) / 2 + f[1] * ih * s;
      frame.style.left = (x / W * 100) + '%';
      frame.style.top = (y / H * 100) + '%';
      frame.style.width = (W < 700 ? Math.min(W * 0.86, 340) : Math.min(H * 0.5, W * 0.4, iw * s * 0.3)) + 'px';
    };
    if (img.complete) placeFrame(); else img.addEventListener('load', placeFrame);
    window.addEventListener('resize', placeFrame);
  }

  /* stills masonry: put each picture in the shortest column (keeps columns even) */
  var mason = doc.querySelector('[data-masonry]');
  if (mason) {
    var figs = Array.prototype.slice.call(mason.children);
    var layout = function () {
      var n = window.innerWidth >= 1025 ? 3 : (window.innerWidth >= 640 ? 2 : 1);
      if (mason.getAttribute('data-cols') === String(n)) return;
      mason.setAttribute('data-cols', String(n));
      mason.classList.add('is-js');
      var cols = [], heights = [];
      mason.innerHTML = '';
      for (var c = 0; c < n; c++) { var col = doc.createElement('div'); col.className = 'm-col'; mason.appendChild(col); cols.push(col); heights.push(0); }
      figs.forEach(function (fig) {
        var k = heights.indexOf(Math.min.apply(null, heights));
        cols[k].appendChild(fig);
        heights[k] += 1 / Number(fig.getAttribute('data-ar') || 1.5) + 0.12;
      });
    };
    layout();
    window.addEventListener('resize', layout);
  }

  /* entrance: one pattern, once per element */
  var items = doc.querySelectorAll('[data-reveal]');
  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-in'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* scroll rows: arrow buttons */
  doc.querySelectorAll('[data-row-for]').forEach(function (ctl) {
    var row = doc.getElementById(ctl.getAttribute('data-row-for'));
    if (!row) return;
    ctl.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        var step = row.clientWidth * 0.8 * Number(b.getAttribute('data-dir'));
        row.scrollBy({ left: step, behavior: reduced ? 'auto' : 'smooth' });
      });
    });
  });

  /* project filters */
  var filters = doc.querySelectorAll('[data-filter]');
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filter');
      filters.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      doc.querySelectorAll('.pc[data-cats]').forEach(function (c) {
        c.hidden = !(f === 'all' || c.getAttribute('data-cats').split(' ').indexOf(f) !== -1);
      });
    });
  });

  /* YouTube: load the player only when asked */
  function makeFrame(id, title) {
    var f = doc.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
    f.title = title;
    f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    f.allowFullscreen = true;
    return f;
  }
  doc.querySelectorAll('[data-yt-inline]').forEach(function (box) {
    var btn = box.querySelector('button');
    if (!btn) return;
    btn.addEventListener('click', function () {
      box.classList.add('is-playing');
      box.appendChild(makeFrame(box.getAttribute('data-yt-inline'), box.getAttribute('data-title') || 'Video'));
    });
  });
  var player = doc.getElementById('player');
  if (player && typeof player.showModal === 'function') {
    var holder = player.querySelector('.player__frame');
    var label = player.querySelector('.player__title');
    var yt = player.querySelector('.player__yt');
    doc.querySelectorAll('[data-yt-dialog]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var id = btn.getAttribute('data-yt-dialog');
        var title = btn.getAttribute('data-title') || 'Video';
        holder.innerHTML = '';
        holder.appendChild(makeFrame(id, title));
        label.textContent = title;
        if (yt) yt.href = 'https://www.youtube.com/watch?v=' + id;
        player.showModal();
      });
    });
    player.querySelector('.player__close').addEventListener('click', function () { player.close(); });
    player.addEventListener('click', function (e) { if (e.target === player) player.close(); });
    player.addEventListener('close', function () { holder.innerHTML = ''; });
  } else {
    doc.querySelectorAll('[data-yt-dialog]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        window.location.href = 'https://www.youtube.com/watch?v=' + btn.getAttribute('data-yt-dialog');
      });
    });
  }

  /* lightbox for galleries and the stills page */
  var lb = doc.getElementById('lightbox');
  var shots = Array.prototype.slice.call(doc.querySelectorAll('[data-lightbox]'));
  if (lb && shots.length && typeof lb.showModal === 'function') {
    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('.lightbox__cap');
    var at = 0;
    var show = function (i) {
      at = (i + shots.length) % shots.length;
      var s = shots[at];
      lbImg.src = s.getAttribute('data-src');
      lbImg.alt = (s.querySelector('img') || {}).alt || '';
      lbCap.textContent = s.getAttribute('data-cap') || '';
    };
    shots.forEach(function (s, i) {
      s.addEventListener('click', function () { show(i); lb.showModal(); });
    });
    lb.querySelector('.lightbox__close').addEventListener('click', function () { lb.close(); });
    lb.querySelector('.lightbox__prev').addEventListener('click', function () { show(at - 1); });
    lb.querySelector('.lightbox__next').addEventListener('click', function () { show(at + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(at - 1);
      if (e.key === 'ArrowRight') show(at + 1);
    });
  }
})();
