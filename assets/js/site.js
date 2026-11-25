/* Ruben Svanerud — small, dependency-free behaviour */
(function () {
  'use strict';
  var doc = document;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* nav: transparent over the hero, solid after 80px */
  var nav = doc.querySelector('.nav');
  if (nav && doc.body.classList.contains('has-hero')) {
    var onScroll = function () { nav.classList.toggle('is-solid', window.scrollY > 80); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

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
      if (nav && open) nav.classList.add('is-solid');
      if (nav && !open && doc.body.classList.contains('has-hero')) nav.classList.toggle('is-solid', window.scrollY > 80);
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

  /* entrance: one pattern, once per element */
  var items = doc.querySelectorAll('[data-reveal]');
  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-in'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* YouTube: load the player only when asked */
  function ytSrc(id) {
    return 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
  }
  function makeFrame(id, title) {
    var f = doc.createElement('iframe');
    f.src = ytSrc(id);
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

  var dialog = doc.getElementById('player');
  if (dialog && typeof dialog.showModal === 'function') {
    var holder = dialog.querySelector('.player__frame');
    var label = dialog.querySelector('.player__title');
    doc.querySelectorAll('[data-yt-dialog]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var title = btn.getAttribute('data-title') || 'Video';
        holder.innerHTML = '';
        holder.appendChild(makeFrame(btn.getAttribute('data-yt-dialog'), title));
        label.textContent = title;
        var yt = dialog.querySelector('.player__yt');
        if (yt) yt.href = 'https://www.youtube.com/watch?v=' + btn.getAttribute('data-yt-dialog');
        dialog.showModal();
      });
    });
    var close = function () { dialog.close(); };
    dialog.querySelector('.player__close').addEventListener('click', close);
    dialog.addEventListener('click', function (e) { if (e.target === dialog) close(); });
    dialog.addEventListener('close', function () { holder.innerHTML = ''; });
  } else {
    /* no <dialog> support: open YouTube directly */
    doc.querySelectorAll('[data-yt-dialog]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        window.location.href = 'https://www.youtube.com/watch?v=' + btn.getAttribute('data-yt-dialog');
      });
    });
  }
})();
